from rest_framework import views, status
from rest_framework.response import Response
from ..services.tmdb_services import TMDBService

from rest_framework.permissions import AllowAny

class ContentDetailView(views.APIView):
    """
    API view for detailed content information
    """
    permission_classes = [AllowAny]

    def get(self, request, media_type, item_id):
        if media_type not in ['movie', 'tv', 'person']:
            return Response(
                {'error': 'Invalid media type. Use "movie", "tv", or "person".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get additional data to include in response
        append_to_response = None
        if media_type in ['movie', 'tv']:
            append_to_response = 'credits,videos,watch/providers,recommendations,similar'
        elif media_type == 'person':
            append_to_response = 'movie_credits,tv_credits,images'

        # Make request to TMDB API
        tmdb_service = TMDBService()
        response = tmdb_service.get_details(media_type, item_id, append_to_response)

        if 'error' in response:
            return Response({'error': response['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Format result
        formatted_result = tmdb_service.prepare_content_item(response, media_type)

        # Format image URLs in nested objects
        if 'credits' in formatted_result:
            for person in formatted_result['credits'].get('cast', []):
                if 'profile_path' in person and person['profile_path']:
                    person['profile_url'] = tmdb_service.format_image_url(person['profile_path'])

            for person in formatted_result['credits'].get('crew', []):
                if 'profile_path' in person and person['profile_path']:
                    person['profile_url'] = tmdb_service.format_image_url(person['profile_path'])

        # Process streaming providers data
        if 'watch/providers' in formatted_result:
            providers_data = formatted_result['watch/providers']
            # Extract US providers or use an empty dict if not available
            us_providers = providers_data.get('results', {}).get('US', {})

            # Create a simplified providers structure
            formatted_result['streaming_providers'] = {
                'flatrate': us_providers.get('flatrate', []),
                'rent': us_providers.get('rent', []),
                'buy': us_providers.get('buy', [])
            }

        if 'recommendations' in formatted_result:
            for item in formatted_result['recommendations'].get('results', []):
                tmdb_service.prepare_content_item(item, media_type)

        if 'similar' in formatted_result:
            for item in formatted_result['similar'].get('results', []):
                tmdb_service.prepare_content_item(item, media_type)

        # Return response
        return Response(formatted_result)

class CategoryListView(views.APIView):
    """
    API view for content category listings
    """
    permission_classes = [AllowAny]

    def get(self, request, media_type, category):
        if media_type not in ['movie', 'tv']:
            return Response(
                {'error': 'Invalid media type. Use "movie" or "tv".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_categories = {
            'movie': ['popular', 'top_rated', 'upcoming', 'now_playing'],
            'tv': ['popular', 'top_rated', 'on_the_air', 'airing_today']
        }

        if category not in valid_categories[media_type]:
            return Response(
                {'error': f'Invalid category for {media_type}. Valid categories: {valid_categories[media_type]}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get page parameter
        page = request.query_params.get('page', '1')
        try:
            page = int(page)
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        # Make request to TMDB API
        tmdb_service = TMDBService()
        endpoint = f"{media_type}/{category}"
        params = {'page': page}

        cache_key = f"{media_type}_{category}_{page}"
        response = tmdb_service._make_request(endpoint, params, cache_key, 3600)

        if 'error' in response:
            return Response({'error': response['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Format results
        results = response.get('results', [])
        formatted_results = [tmdb_service.prepare_content_item(item, media_type) for item in results]

        # Return response
        return Response({
            'results': formatted_results,
            'page': response.get('page', 1),
            'total_pages': response.get('total_pages', 1),
            'total_results': response.get('total_results', 0)
        })

