from django.urls import path
from .views import *


urlpatterns = [
    path('', PosterList.as_view(), name="poster_list"),
    path('<int:pk>/', PosterDetail.as_view(), name="poster_detail"),
    path('create/', PosterCreate.as_view(), name="create_poster"),
    path('<int:pk>/edit/', PosterEdit.as_view(), name="edit_poster"),
    path('<int:pk>/delete/', PosterDelete.as_view(), name='poster_delete'),
    path('search/', PosterSearch.as_view(), name="poster_search"),
    path('<int:pk>/respond/', ResponseCreate.as_view(), name="respond"),
    path('responses/', ResponseList.as_view(), name="response_list"),
    path('responses/<int:pk>/', ResponseDetail.as_view(), name="response_detail"),
    path('responses/<int:pk>/approve/', approve_response, name="approve"),
    path('responses/<int:pk>/reject/', reject_response, name="reject"),
    path('success/', SuccessView.as_view(), name="success"),
]