from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.discover_views import DiscoverView
from .views.search_views import SearchView
from .views.trending_views import TrendingView
from .views.detail_views import ContentDetailView, CategoryListView
from .views.user_views import (
    UserWatchlistViewSet,
    WatchlistStatusView
)

# Set up routers
router = DefaultRouter()
router.register(r'watchlist', UserWatchlistViewSet, basename='watchlist')

urlpatterns = [
    # Content discovery endpoints
    path('discover/', DiscoverView.as_view(), name='discover'),
    path('search/', SearchView.as_view(), name='search'),
    path('trending/', TrendingView.as_view(), name='trending'),

    # Detailed content information
    path('movies/<int:item_id>/', ContentDetailView.as_view(), kwargs={'media_type': 'movie'}, name='movie-detail'),
    path('tv/<int:item_id>/', ContentDetailView.as_view(), kwargs={'media_type': 'tv'}, name='tv-detail'),
    path('person/<int:item_id>/', ContentDetailView.as_view(), kwargs={'media_type': 'person'}, name='person-detail'),

    # Category listings
    path('movies/<str:category>/', CategoryListView.as_view(), kwargs={'media_type': 'movie'}, name='movie-category'),
    path('tv/<str:category>/', CategoryListView.as_view(), kwargs={'media_type': 'tv'}, name='tv-category'),

    # User feature endpoints
    path('', include(router.urls)),
    path('watchlist-status/', WatchlistStatusView.as_view(), name='watchlist-status'),
]