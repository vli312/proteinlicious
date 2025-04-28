from django.urls import path
from . import views
app_name = 'recipe'
urlpatterns = [
    # recipe views
    path('', views.homeview, name='homeview'),
    path('list/', views.listview, name='listview'),
    path('upload/', views.uploadview, name='uploadview'),
    path('edit/<int:recipe_id>/', views.editview, name='editview'),
    path('chickencurry/', views.chickencurryview, name='chickencurryview'),
    path('altchickencurry/', views.altchickencurryview, name='altchickencurryview'),
    path('recipe/<int:recipe_id>/', views.recipe_detail_view, name='recipe_detail_view'),
    path('recipe/<int:recipe_id>/loggedout/', views.alt_recipe_detail_view, name='alt_recipe_detail_view'),
    path('adminpage/', views.adminview, name='adminview'),
    path('adminusers/', views.adminusersview, name='adminusersview'),
    path('search/', views.searchview, name='searchview'),
]