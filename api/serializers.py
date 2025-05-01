from rest_framework import serializers
from .models import UserWatchlist, UserRating

class UserWatchlistSerializer(serializers.ModelSerializer):
    """Serializer for user watchlist items"""
    # Add item_id as an alias for tmdb_id for frontend compatibility
    item_id = serializers.IntegerField(source='tmdb_id', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserWatchlist
        fields = (
            'id', 'user_id', 'username', 'tmdb_id', 'item_id', 'media_type', 'title', 'poster_url',
            'backdrop_url', 'overview', 'release_date', 'vote_average', 'added_at'
        )
        read_only_fields = ('id', 'user_id', 'username', 'added_at', 'item_id')

    def validate(self, attrs):
        # Make sure we have a tmdb_id
        if 'tmdb_id' not in attrs and 'item_id' in self.initial_data:
            attrs['tmdb_id'] = self.initial_data['item_id']

        # Make sure we have a media_type
        if 'media_type' not in attrs:
            raise serializers.ValidationError({'media_type': 'This field is required.'})

        # Make sure the media_type is valid
        if attrs['media_type'] not in ['movie', 'tv']:
            raise serializers.ValidationError({'media_type': 'Must be either "movie" or "tv"'})

        return attrs

    def create(self, validated_data):
        # Support both tmdb_id and item_id in request data
        if 'item_id' in self.initial_data and 'tmdb_id' not in validated_data:
            validated_data['tmdb_id'] = self.initial_data['item_id']

        # Copy additional fields from initial_data if they exist
        for field in ['title', 'poster_url', 'backdrop_url', 'overview', 'vote_average']:
            if field in self.initial_data and field not in validated_data:
                validated_data[field] = self.initial_data[field]

        # Handle release_date field specially
        if 'release_date' in self.initial_data and 'release_date' not in validated_data:
            try:
                # If it's already a valid date string in YYYY-MM-DD format, keep it
                from datetime import datetime
                date_str = self.initial_data['release_date']
                if date_str:
                    datetime.strptime(date_str, '%Y-%m-%d')
                    validated_data['release_date'] = date_str
            except (ValueError, TypeError):
                # If it's not a valid date, don't include it
                print(f"Invalid release_date format: {self.initial_data['release_date']}, not including it")
                pass

        # Get the user from the context or from the validated_data
        if 'user' not in validated_data:
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                validated_data['user'] = request.user
            else:
                raise serializers.ValidationError({'user': 'User is required'})

        print(f"Creating watchlist item with data: {validated_data}")
        return super().create(validated_data)

class UserRatingSerializer(serializers.ModelSerializer):
    """Serializer for user ratings"""
    class Meta:
        model = UserRating
        fields = ('id', 'tmdb_id', 'media_type', 'rating', 'review', 'rated_at')
        read_only_fields = ('id', 'rated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TMDBParamsSerializer(serializers.Serializer):
    """Serializer for validating TMDB API parameters"""
    page = serializers.IntegerField(min_value=1, required=False, default=1)
    language = serializers.CharField(required=False, default='en-US')

class DiscoverParamsSerializer(TMDBParamsSerializer):
    """Serializer for validating discover endpoint parameters"""
    type = serializers.ChoiceField(choices=['movie', 'tv'], required=False, default='movie')
    year = serializers.CharField(required=False)
    release_date_gte = serializers.DateField(required=False)
    release_date_lte = serializers.DateField(required=False)
    sort_by = serializers.CharField(required=False, default='popularity.desc')
    with_runtime_gte = serializers.IntegerField(required=False)
    with_runtime_lte = serializers.IntegerField(required=False)
    with_genres = serializers.CharField(required=False)
    with_watch_providers = serializers.CharField(required=False)
    watch_region = serializers.CharField(required=False, default='US')
    vote_average_gte = serializers.FloatField(required=False, min_value=0, max_value=10)

    def validate(self, data):
        # Handle year range
        if 'year' in data and data['year']:
            try:
                year_range = data.pop('year').split(',')
                if len(year_range) == 2:
                    start_year, end_year = year_range
                    data['primary_release_date.gte' if data['type'] == 'movie' else 'first_air_date.gte'] = f"{start_year}-01-01"
                    data['primary_release_date.lte' if data['type'] == 'movie' else 'first_air_date.lte'] = f"{end_year}-12-31"
                else:
                    year = year_range[0]
                    data['primary_release_year' if data['type'] == 'movie' else 'first_air_date_year'] = year
            except (ValueError, IndexError):
                pass

        # Print all parameters for debugging
        print(f"Serializer validated data: {data}")

        return data

class SearchParamsSerializer(TMDBParamsSerializer):
    """Serializer for validating search endpoint parameters"""
    query = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=['multi', 'movie', 'tv'], required=False, default='multi')

class TrendingParamsSerializer(TMDBParamsSerializer):
    """Serializer for validating trending endpoint parameters"""
    media_type = serializers.ChoiceField(choices=['all', 'movie', 'tv'], required=False, default='all')
    time_window = serializers.ChoiceField(choices=['day', 'week'], required=False, default='day')