from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import UserWatchlist, UserRating
from ..serializers import UserWatchlistSerializer, UserRatingSerializer
from ..services.tmdb_services import TMDBService

class UserWatchlistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user watchlist items
    """
    serializer_class = UserWatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to only user's watchlist items"""
        return UserWatchlist.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new watchlist item"""
        print(f"Received watchlist create request: {request.data}")
        print(f"Request headers: {request.headers}")
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        print(f"Auth header: {request.headers.get('Authorization')}")

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            print("User is not authenticated")
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Create a mutable copy of the request data
        data = dict(request.data)
        print(f"Request data type: {type(request.data)}")

        # Create a mutable copy of the data for processing
        data_dict = dict(request.data)

        # If we have content details in the request, use them directly
        # Otherwise, fetch from TMDB API
        if 'tmdb_id' in data_dict and 'media_type' in data_dict and not data_dict.get('title'):
            try:
                tmdb_service = TMDBService()
                tmdb_id = data_dict['tmdb_id']
                media_type = data_dict['media_type']

                print(f"Fetching details for {media_type} {tmdb_id} from TMDB API")
                # Fetch details from TMDB API
                details = tmdb_service.get_details(media_type, tmdb_id)
                print(f"TMDB API response: {details}")

                if 'error' not in details:
                    # Map TMDB fields to our model fields
                    if media_type == 'movie':
                        data_dict['title'] = details.get('title')
                        data_dict['release_date'] = details.get('release_date')
                    else:  # TV show
                        data_dict['title'] = details.get('name')
                        data_dict['release_date'] = details.get('first_air_date')

                    data_dict['poster_url'] = f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}" if details.get('poster_path') else None
                    data_dict['backdrop_url'] = f"https://image.tmdb.org/t/p/original{details.get('backdrop_path')}" if details.get('backdrop_path') else None
                    data_dict['overview'] = details.get('overview')
                    data_dict['vote_average'] = details.get('vote_average')

                    print(f"Enhanced request data with TMDB details: {data_dict}")
                else:
                    print(f"Error in TMDB API response: {details['error']}")
            except Exception as e:
                print(f"Error fetching TMDB details: {e}")
                # Continue with the request even if we couldn't fetch details
                pass

        try:
            print("Creating watchlist item...")

            # Handle release_date field - it might be in the wrong format
            if 'release_date' in data_dict and data_dict['release_date']:
                try:
                    # If it's already a valid date string in YYYY-MM-DD format, keep it
                    # Otherwise, set it to None to avoid validation errors
                    from datetime import datetime
                    datetime.strptime(data_dict['release_date'], '%Y-%m-%d')
                except (ValueError, TypeError):
                    print(f"Invalid release_date format: {data_dict['release_date']}, setting to None")
                    data_dict['release_date'] = None

            # Create a serializer with our data
            serializer = self.get_serializer(data=data_dict)

            # Check if the data is valid
            if not serializer.is_valid():
                print(f"Serializer validation errors: {serializer.errors}")
                return Response(
                    {"error": "Invalid data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Add the user to the validated data
            serializer.validated_data['user'] = request.user

            # Save the instance
            instance = serializer.save()
            print(f"Watchlist item created successfully: {instance}")

            # Return the serialized data
            return Response(
                self.get_serializer(instance).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            import traceback
            print(f"Error creating watchlist item: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        """Support removal by TMDB ID and media type"""
        pk = kwargs.get('pk')

        # Check if we're using TMDB ID and media type to delete
        tmdb_id = request.query_params.get('tmdb_id')
        media_type = request.query_params.get('media_type')

        if tmdb_id and media_type:
            try:
                instance = self.get_queryset().get(
                    tmdb_id=tmdb_id,
                    media_type=media_type
                )
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except UserWatchlist.DoesNotExist:
                return Response(
                    {'error': 'Item not found in watchlist'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Fall back to default destroy implementation
        return super().destroy(request, *args, **kwargs)

class UserRatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user ratings
    """
    serializer_class = UserRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to only user's ratings"""
        return UserRating.objects.filter(user=self.request.user)

class WatchlistStatusView(APIView):
    """
    API view for checking if item is in user's watchlist or returning the entire watchlist
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Log authentication information
        print(f"WatchlistStatusView - User authenticated: {request.user.is_authenticated}")
        print(f"WatchlistStatusView - User: {request.user}")
        print(f"WatchlistStatusView - Auth header: {request.headers.get('Authorization')}")
        print(f"WatchlistStatusView - Request headers: {request.headers}")

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            print("WatchlistStatusView - User is not authenticated")
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Support both tmdb_id and item_id for backward compatibility
        tmdb_id = request.query_params.get('tmdb_id') or request.query_params.get('item_id')
        media_type = request.query_params.get('media_type')
        print(f"WatchlistStatusView - Query params: tmdb_id={tmdb_id}, media_type={media_type}")

        if not tmdb_id or not media_type:
            # If no parameters, return the entire watchlist with full details
            print("WatchlistStatusView - Returning entire watchlist")
            watchlist_items = UserWatchlist.objects.filter(user=request.user)
            print(f"WatchlistStatusView - Found {watchlist_items.count()} items")
            serializer = UserWatchlistSerializer(watchlist_items, many=True)

            # Return a structured response with all the watchlist items
            return Response({
                'count': watchlist_items.count(),
                'results': serializer.data
            })

        try:
            # Check if item exists in watchlist
            print(f"WatchlistStatusView - Checking if {media_type} {tmdb_id} is in watchlist")
            item = UserWatchlist.objects.get(
                user=request.user,
                tmdb_id=tmdb_id,
                media_type=media_type
            )
            print(f"WatchlistStatusView - Item found in watchlist with ID: {item.id}")

            # Return the full item details along with the status
            serializer = UserWatchlistSerializer(item)
            return Response({
                'in_watchlist': True,
                'id': item.id,
                'item': serializer.data
            })
        except UserWatchlist.DoesNotExist:
            print(f"WatchlistStatusView - Item not found in watchlist")
            return Response({'in_watchlist': False})

class UserRatingStatusView(APIView):
    """
    API view for checking user rating for an item
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tmdb_id = request.query_params.get('tmdb_id')
        media_type = request.query_params.get('media_type')

        if not tmdb_id or not media_type:
            return Response(
                {'error': 'tmdb_id and media_type parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Check if item has been rated
            rating = UserRating.objects.get(
                user=request.user,
                tmdb_id=tmdb_id,
                media_type=media_type
            )
            return Response({'has_rating': True, 'id': rating.id, 'rating': rating.rating})
        except UserRating.DoesNotExist:
            return Response({'has_rating': False})