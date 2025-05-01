from rest_framework import views, status
from rest_framework.response import Response
from ..services.tmdb_services import TMDBService
from ..serializers import SearchParamsSerializer

class SearchView(views.APIView):
    """
    API view for searching content
    """
    
    def get(self, request):
        # Validate and parse parameters
        serializer = SearchParamsSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract validated parameters
        params = serializer.validated_data.copy()
        query = params.pop('query')
        media_type = params.pop('type')
        
        # Make request to TMDB API
        tmdb_service = TMDBService()
        response = tmdb_service.search(query, media_type, params)
        
        if 'error' in response:
            return Response({'error': response['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Format results
        results = response.get('results', [])
        formatted_results = [tmdb_service.prepare_content_item(item) for item in results]
        
        # Return response with pagination info
        return Response({
            'results': formatted_results,
            'page': response.get('page', 1),
            'total_pages': response.get('total_pages', 1),
            'total_results': response.get('total_results', 0)
        })