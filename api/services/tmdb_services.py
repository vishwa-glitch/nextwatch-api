import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TMDBService:
    """Service class to handle TMDB API requests"""

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.read_access_token = settings.TMDB_READ_ACCESS_TOKEN
        self.base_url = settings.TMDB_API_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL

    def _make_request(self, endpoint, params=None, cache_key=None, cache_timeout=3600):
        """Make a request to the TMDB API with optional caching"""
        if not params:
            params = {}

        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.read_access_token}',
            'Content-Type': 'application/json;charset=utf-8'
        }

        # Log the actual request being made to TMDB
        print(f"Making TMDB API request to: {url}")
        print(f"With params: {params}")
        print(f"Cache key: {cache_key}, Cache timeout: {cache_timeout}")

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB API error: {str(e)}")
            return {'error': str(e)}

    def discover(self, media_type, params=None):
        """Discover movies or TV shows based on filters"""
        if not params:
            params = {}

        # Default to 'movie' if media_type is not specified or invalid
        if not media_type or media_type not in ['movie', 'tv']:
            media_type = 'movie'

        # Ensure watch_region is set when with_watch_providers is present
        if 'with_watch_providers' in params and 'watch_region' not in params:
            params['watch_region'] = 'US'  # Default to US region

        # Log the parameters for debugging
        logger.info(f"TMDB discover params: {params}")
        print(f"TMDB discover media_type: {media_type}")
        print(f"TMDB discover params: {params}")

        endpoint = f"discover/{media_type}"

        # Make the request directly without caching
        return self._make_request(endpoint, params)

    def search(self, query, media_type=None, params=None):
        """Search for content by query"""
        if not params:
            params = {}

        params['query'] = query

        if not media_type or media_type == 'all':
            endpoint = "search/multi"
        else:
            endpoint = f"search/{media_type}"

        # No caching for search results
        return self._make_request(endpoint, params)

    def trending(self, media_type, time_window='day'):
        """Get trending content"""
        # Log the parameters for debugging
        print(f"TMDB trending media_type: {media_type}")
        print(f"TMDB trending time_window: {time_window}")

        # Ensure valid media_type and time_window
        if media_type not in ['all', 'movie', 'tv']:
            media_type = 'all'
        if time_window not in ['day', 'week']:
            time_window = 'day'

        endpoint = f"trending/{media_type}/{time_window}"
        return self._make_request(endpoint)

    def get_details(self, media_type, item_id, append_to_response=None):
        """Get detailed information for a specific item"""
        endpoint = f"{media_type}/{item_id}"
        params = {}

        if append_to_response:
            params['append_to_response'] = append_to_response

        return self._make_request(endpoint, params)

    def format_image_url(self, path, size='w500'):
        """Format image URL with base URL and size"""
        if not path:
            return None
        return f"{self.image_base_url}/{size}{path}"

    def prepare_content_item(self, item, media_type=None):
        """Prepare content item with formatted image URLs and additional information"""
        if not item:
            return None

        if not media_type:
            media_type = item.get('media_type')
            if not media_type:
                if 'title' in item:
                    media_type = 'movie'
                elif 'name' in item:
                    media_type = 'tv'

        if 'poster_path' in item and item['poster_path']:
            item['poster_url'] = self.format_image_url(item['poster_path'])

        if 'backdrop_path' in item and item['backdrop_path']:
            item['backdrop_url'] = self.format_image_url(item['backdrop_path'], 'original')

        if media_type and 'media_type' not in item:
            item['media_type'] = media_type

        if 'name' in item and 'title' not in item:
            item['title'] = item['name']

        return item