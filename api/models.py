from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserWatchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    tmdb_id = models.PositiveIntegerField()
    media_type = models.CharField(max_length=10)  # 'movie' or 'tv'
    title = models.CharField(max_length=255, null=True, blank=True)  # Title of the movie or TV show
    poster_url = models.URLField(max_length=500, null=True, blank=True)  # URL to the poster image
    backdrop_url = models.URLField(max_length=500, null=True, blank=True)  # URL to the backdrop image
    overview = models.TextField(null=True, blank=True)  # Description/overview of the content
    release_date = models.DateField(null=True, blank=True)  # Release date for movies or first air date for TV shows
    vote_average = models.FloatField(null=True, blank=True)  # Rating from TMDB
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tmdb_id', 'media_type')

    def __str__(self):
        return f"{self.user.username}'s watchlist item: {self.title or self.tmdb_id}"

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    tmdb_id = models.PositiveIntegerField()
    media_type = models.CharField(max_length=10)  # 'movie' or 'tv'
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(null=True, blank=True)
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tmdb_id', 'media_type')

    def __str__(self):
        return f"{self.user.username}'s rating for {self.tmdb_id}"