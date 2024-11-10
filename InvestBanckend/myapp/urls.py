from django.urls import path
from .views import hotels_in_region, predict_building_growth, identify_suitable_areas, PredictBuildingGrowthView, get_buildings_in_region,get_futur_buildings_in_region,suitable_area,hotels_data_chart
from .views import RegisterView, LoginView, CheckSessionView, LogoutView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('check-session/', CheckSessionView.as_view(), name='check-session'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('hotels-in-region/', hotels_in_region, name='hotels_in_region'),
    path('predict_building_growth/', predict_building_growth, name='predict_building_growth'),
    path('identify_suitable_areas/', identify_suitable_areas, name='identify_suitable_areas'),
    path('get_buildings_in_region/', get_buildings_in_region, name='predict-building-growth'),
    path('get_futur_buildings_in_region/', get_futur_buildings_in_region, name='get_futur_buildings_in_region'),
    path('suitable_area/', suitable_area, name='suitable_area'),
    path('hotels_data_chart/', hotels_data_chart, name='hotels_data_chart')
]  

