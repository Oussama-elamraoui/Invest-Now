import logging
from django.shortcuts import render

# Create your views here.
# from django.contrib.gis.geos import Polygon
from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import json
import ee
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from .models import InfoHotelsDetails, Parkdata, Clinics, Clubs, Banks, Restaut, HotelInfo,Users
from .serializers import InfoHotelsDetailsSerializer
from datetime import datetime
from shapely.geometry import Polygon, MultiPolygon,Point,shape
from shapely.ops import unary_union
from pyproj import Proj
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
import os
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
# Initialize the Earth Engine library.
ee.Authenticate()
ee.Initialize(project='ee-oussa')

wgs84 = Proj(init='epsg:4326')
utm = Proj(init='epsg:32633') 
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
class CheckSessionView(APIView):
    
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            raise AuthenticationFailed('Authorization header missing')

        token = auth_header.split(' ')[1]

        try:
            # Validate the token manually
            AccessToken(token)
            return Response({"status": "Active"}, status=status.HTTP_200_OK)
        except Exception as e:
            raise AuthenticationFailed('Invalid or expired token')
        
# Authentification logic
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

# class CheckSessionView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     # permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         print(f"User: {request.user}")  # Ensure the user is correctly authenticated
#         return Response({"status": "Active"}, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def hotels_in_region(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        region = data.get('region')
        print(region)
        if not region:
            return JsonResponse({'error': 'No region provided'}, status=400)

        # Define the region as a GeoJSON
        region_geojson = ee.Geometry.Polygon(region['coordinates'])

        # Query the database for all hotel details
        hotels = InfoHotelsDetails.objects.all()

        # Filter points within the region
        points_within = []
        for hotel in hotels:
            point = ee.Geometry.Point([hotel.longitude, hotel.latitude])
            if region_geojson.contains(point).getInfo():
                points_within.append(InfoHotelsDetailsSerializer(hotel).data)

        return JsonResponse({'points_within': points_within})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def predict_building_growth(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        region = data.get('region')  # GeoJSON or coordinates
        prediction = make_prediction(region)
        return JsonResponse({'prediction': prediction})

def make_prediction(region):
    # Convert region to an ee.Geometry object
    geometry = ee.Geometry.Polygon(region['coordinates'])
    
    # Define the time range for historical analysis
    start_date = '2017-01-01'
    end_date = '2023-12-31'
    
    # Fetch building data from the ESA WorldCover dataset
    worldcover = ee.ImageCollection('ESA/WorldCover/v100') \
        .filterBounds(geometry) \
        .filterDate(start_date, end_date)
    
    # Function to mask built-up areas
    def get_built_up(image):
        built_up = image.select('Map').eq(50)  # 50 represents built-up area in WorldCover
        return built_up.updateMask(built_up).set('system:time_start', image.get('system:time_start'))
    
    built_up_collection = worldcover.map(get_built_up)
    
    # Calculate the mean built-up area for each year
    def calculate_yearly_mean(image):
        year = ee.Date(image.get('system:time_start')).get('year')
        mean_built_up = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=10
        ).get('Map')
        return ee.Feature(None, {'year': year, 'mean_built_up': mean_built_up})
    
    yearly_built_up_fc = built_up_collection.map(calculate_yearly_mean)
    
    # Extract features and check for data
    features = yearly_built_up_fc.getInfo().get('features', [])
    if len(features) == 0:
        # Use GHSL image if the WorldCover dataset is insufficient
        ghsl_image = ee.Image('JRC/GHSL/P2016/BUILT_LDSMT_GLOBE_V1')
        
        def calculate_built_up_mean(image):
            mean_built_up = image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=30
            ).get('built')
            return ee.Feature(None, {'mean_built_up': mean_built_up})
        
        built_up_fc = calculate_built_up_mean(ghsl_image)
        features = [built_up_fc.getInfo()]
        if len(features) == 0:
            return {'error': 'Insufficient data for prediction. Please collect more data or use different datasets.'}
    print(features)
    # Prepare data for linear regression
    if len(features) < 2:
        return {'error': 'Insufficient historical data to perform prediction.'}
    
    years = [f['properties']['year'] for f in features]
    built_up_values = [f['properties']['mean_built_up'] for f in features]
    
    # Debugging step: Print the extracted years and values
    print("Extracted years:", years)
    print("Built-up values:", built_up_values)
    
    # Check if we have enough data points
    if len(years) < 2:
        return {'error': 'Insufficient historical data to perform prediction.'}
   
    X = np.array(years).reshape(-1, 1)
    y = np.array(built_up_values)
    
    # Fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future growth until 2028
    future_years = np.arange(2024, 2029).reshape(-1, 1)
    predictions = model.predict(future_years)
    
    # Format the predictions
    projected_growth = [{'year': int(year), 'projected_built_up': pred} for year, pred in zip(future_years.flatten(), predictions)]
    
    # Return the prediction result
    prediction_result = {
        'historical_data': [{'year': year, 'mean_built_up': value} for year, value in zip(years, built_up_values)],
        'projected_growth': projected_growth
    }
    return prediction_result
@csrf_exempt
def identify_suitable_areas(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        region = data.get('region')  # GeoJSON or coordinates
        suitable_areas = get_suitable_areas(region)
        return JsonResponse({'suitable_areas': suitable_areas})

def find_suitable_areas(region):
    geometry = ee.Geometry.Polygon(region['coordinates'])

    # Updated Sentinel-2 dataset
    image_collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(geometry) \
        .filterDate('2022-01-01', '2023-01-01')

    # Cloud masking function
    def mask_clouds(image):
        qa = image.select('QA60')
        cloud_mask = qa.bitwiseAnd(1 << 10).eq(0).And(qa.bitwiseAnd(1 << 11).eq(0))
        return image.updateMask(cloud_mask)

    # Calculate NDVI and mask clouds
    def preprocess_image(image):
        image = mask_clouds(image)
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi)
    
    processed_collection = image_collection.map(preprocess_image).median()
    
    # Use the GHSL dataset to mask built-up areas
    ghsl = ee.Image('JRC/GHSL/P2016/BUILT_LDSMT_GLOBE_V1')
    built_up_mask = ghsl.select('built').gt(0)
    
    # Combine with NDVI threshold to find suitable areas
    ndvi_threshold = 0.3
    suitable_areas_mask = processed_collection.select('NDVI').gt(ndvi_threshold).And(built_up_mask.Not())
    
    # Convert suitable areas mask to GeoJSON
    suitable_areas = suitable_areas_mask.reduceToVectors(
        geometryType='polygon',
        geometry=geometry,
        eightConnected=True,
        labelProperty='class'
    ).getInfo()
    
    return suitable_areas




def get_suitable_areas(region):
    try:
        # Convert the region to an ee.Geometry.Polygon
        polygon = ee.Geometry.Polygon(region['coordinates'])
        print(f"Polygon: {polygon.getInfo()}")

        # Load the ESA WorldCover dataset
        world_cover = ee.ImageCollection("ESA/WorldCover/v100").first()
        print(f"WorldCover image: {world_cover.getInfo()}")

        # Get the land cover band
        land_cover = world_cover.select('Map')
        print(f"Land cover band: {land_cover.getInfo()}")

        # Define non-built areas (assuming built-up areas are classified as 50 in this dataset)
        non_built_areas = land_cover.neq(50)
        print(f"Non-built mask: {non_built_areas.getInfo()}")

        # Mask the built-up areas within the polygon
        suitable_area = non_built_areas.selfMask().clip(polygon)
        print(f"Suitable area info: {suitable_area.getInfo()}")

        # Reduce to vectors
        vectors = suitable_area.reduceToVectors(
            geometryType='polygon',
            reducer=ee.Reducer.countEvery(),
            scale=30,
            maxPixels=1e9
        )
        print(f"Vectors: {vectors.getInfo()}")

        # Get the coordinates of the suitable areas
        features = vectors.getInfo().get('features', [])
        print(f"Features: {features}")

        # Extract coordinates from features
        suitable_points = []
        for feature in features:
            coordinates = feature['geometry']['coordinates']
            suitable_points.append(coordinates)
        geojon_suitable_areas=convert_to_geojson({"type": "MultiPoint", "coordinates": suitable_points})
        return geojon_suitable_areas

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"type": "MultiPoint", "coordinates": []}
# Update the Django view to use this function
def convert_to_geojson(suitable_areas):
    features = []
    for polygon in suitable_areas['coordinates']:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": polygon
            },
            "properties": {
                "class": 0,
                "count": len(polygon[0])  # Example property, you can modify as needed
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson_data


@method_decorator(csrf_exempt, name='dispatch')
class PredictBuildingGrowthView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            if 'region' not in data or 'coordinates' not in data['region']:
                return JsonResponse({'error': 'Invalid input format. Missing "region" or "coordinates".'}, status=400)

            region = data['region']
            coordinates = region['coordinates']
            if not isinstance(coordinates, list) or not all(isinstance(coord, list) for coord in coordinates):
                return JsonResponse({'error': 'Invalid coordinates format. Coordinates should be a list of lists.'}, status=400)

            # Define the region as an ee.Geometry
            polygon = ee.Geometry.Polygon(region['coordinates'])

            # Define the date range and bands for Landsat 5 Collection 2
            start_date = '1995-01-01'
            end_date = '2012-12-31'
            bands = ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7']

            # Endmembers for the unmixing process
            urban = [88, 42, 48, 38, 86, 115]
            veg = [50, 21, 20, 35, 50, 110]
            water = [51, 20, 14, 9, 7, 116]

            # Load the Landsat 5 Collection 2 Tier 1 image collection and filter by date and region
            all_Landsat5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
            filtered_Landsat5 = all_Landsat5.filterDate(start_date, end_date).filterBounds(polygon)

            def process_image(image):
                available_bands = image.bandNames().getInfo()
                if len(available_bands) != len(bands):
                    raise ValueError(f"Image does not have the expected number of bands. Found: {len(available_bands)}")

                image = image.select(bands)
                unmixed_image = image.unmix([urban, veg, water], True, True).rename(['urban', 'veg', 'water'])
                return unmixed_image.addBands(image.metadata('system:time_start').divide(1e13))

            def get_building_polygons(year):
                yearly_images = filtered_Landsat5.filter(ee.Filter.calendarRange(year, year, 'year'))

                processed_images = yearly_images.map(process_image)
                composite_image = processed_images.median().select('urban')

                binary_image = composite_image.gt(0.1).selfMask().rename('binary')

                building_polygons = binary_image.reduceToVectors(
                    geometry=polygon,
                    reducer=ee.Reducer.countEvery(),
                    scale=30,
                    maxPixels=1e9
                )

                building_polygons = building_polygons.getInfo()
                features = building_polygons.get('features', [])
                geojson_features = []

                for feature in features:
                    geom = feature.get('geometry', {})
                    geojson_features.append({
                        'type': 'Feature',
                        'geometry': geom,
                        'properties': {'year': year}
                    })
                return geojson_features

            years = list(range(2000, 2013))
            historical_polygons_counts = []

            for year in years:
                polys = get_building_polygons(year)
                if polys:
                    historical_polygons_counts.append(len(polys))
                else:
                    historical_polygons_counts.append(0)

            if not historical_polygons_counts:
                return JsonResponse({'error': 'No building data found for the specified years.'}, status=400)

            X = np.array(years).reshape(-1, 1)
            y = np.array(historical_polygons_counts)

            rf_model = RandomForestRegressor(n_estimators=100)
            rf_model.fit(X, y)

            future_years = np.array(list(range(2024, 2029))).reshape(-1, 1)
            rf_predictions = rf_model.predict(future_years)

            predicted_features = []
            for year, pred_count in zip(range(2024, 2029), rf_predictions):
                for _ in range(int(pred_count)):
                    predicted_features.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': [[
                                [-8.07356, 31.700101],
                                [-8.014329, 31.684631],
                                [-8.037253, 31.669983],
                                [-8.08182, 31.641013],
                                [-8.07356, 31.700101]
                            ]]
                        },
                        'properties': {'year': year}
                    })

            response = {
                'type': 'FeatureCollection',
                'features': predicted_features
            }
            return JsonResponse(response, status=200)

        except Exception as e:
            print(f"Error occurred: {e}")  # Debug: Print the error message
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt  # If you're testing locally or don't have CSRF protection enabled
def get_buildings_in_region(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            region = request_data.get('region')
            if not region:
                return JsonResponse({'error': 'No region provided in the request'}, status=400)
            geometry = ee.Geometry.Polygon(region['coordinates'])
            dataset = ee.ImageCollection('ESA/WorldCover/v100') \
                .filterBounds(geometry) \
                .first()
            built_up = dataset.select('Map').eq(50)
            built_up_masked = built_up.updateMask(built_up).clip(geometry)

            built_up_features = built_up_masked.reduceToVectors(
                geometry=geometry,
                geometryType='polygon',
                reducer=ee.Reducer.countEvery(),
                scale=10,
                maxPixels=1e8
            )

            total_features = built_up_features.size().getInfo()
            logging.info(f'Total built-up features: {total_features}')

            # Check if there are any features
            if total_features == 0:
                logging.warning('No built-up features found in the specified region.')
                return JsonResponse({'error': 'No built-up features found in the specified region.'}, status=404)
            # Convert to GeoJSON
            geojson_features = built_up_features.getInfo()
 
            return JsonResponse(geojson_features, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logging.error(f'Error occurred: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt 
def get_futur_buildings_in_region(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            region = request_data.get('region')
            if not region:
                return JsonResponse({'error': 'No region provided in the request'}, status=400)
            geometry = ee.Geometry.Polygon(region['coordinates'])

            # Collect historical data
            intervals = [[2016, 2020], [2020, 2024]]
            built_up_areas = []
            geojson_results = []
            for interval in intervals:
                start_date = f'{interval[0]}-01-01'
                end_date = f'{interval[1]}-12-31'
                path = 'ESA/WorldCover/v200' if interval[0] != 2016 else 'ESA/WorldCover/v100'
                dataset = ee.ImageCollection(path) \
                    .filterBounds(geometry) \
                    .filterDate(start_date, end_date) \
                    .first()
                if dataset:
                    try:
                        built_up = dataset.select('Map').eq(50)
                        built_up_masked = built_up.updateMask(built_up).clip(geometry)
                        built_up_features = built_up_masked.reduceToVectors(
                            geometry=geometry,
                            geometryType='polygon',
                            reducer=ee.Reducer.countEvery(),
                            scale=10,
                            maxPixels=1e8
                        )

                        # Get GeoJSON result
                        geojson = built_up_features.getInfo()
                        geojson_results.append({
                            'interval': f'{interval[0]}-{interval[1]}',
                            'geojson': geojson
                        })

                        # Count the number of features
                        total_features = len(geojson['features'])
                        built_up_areas.append(total_features)
                    except Exception as e:
                        return JsonResponse({'error': str(e)}, status=500)

            if len(built_up_areas) != len(intervals):
                return JsonResponse({'error': 'Failed to retrieve built-up data for all intervals'}, status=500)

            # Prepare data for linear regression
            X = np.array([interval[1] for interval in intervals]).reshape(-1, 1)
            y = np.array(built_up_areas)

            # Train the model
            model = LinearRegression()
            model.fit(X, y)

            # Predict future built-up areas
            future_intervals = [2028, 2032]
            predictions = model.predict(np.array(future_intervals).reshape(-1, 1))

            # Simulate future built-up areas based on predictions
            future_geojson_results = []
            for future_interval, prediction in zip(future_intervals, predictions):
                # Calculate the growth rate
                growth_rate = (built_up_areas[-1] - built_up_areas[0]) / built_up_areas[0]
                future_built_up_count = int(built_up_areas[-1] * (1 + growth_rate))

                # Generate random polygons to simulate future built-up areas
                polygons = []
                for _ in range(future_built_up_count):
                    # Randomly select a built-up feature from the latest interval
                    random_feature = np.random.choice(geojson_results[-1]['geojson']['features'])
                    random_polygon = random_feature['geometry']['coordinates']

                    # Slightly modify the polygon to simulate growth (e.g., scaling)
                    scale_factor = np.random.uniform(1.01, 1.1)  # Scale the polygon by 1% to 10%
                    scaled_polygon = [[
                        [point[0] * scale_factor, point[1] * scale_factor] for point in part
                    ] for part in random_polygon]

                    polygons.append(scaled_polygon)

                future_geojson = {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": polygon
                            },
                            "properties": {}
                        } for polygon in polygons
                    ]
                }
                future_geojson_results.append({
                    'interval': f'{future_interval-4}-{future_interval}',
                    'geojson': future_geojson
                })

            response_data = {
                # 'built_up_areas': built_up_areas,
                # 'geojson_results': geojson_results,
                # 'predictions': predictions.tolist(),
                'future_geojson_results': future_geojson_results[1]['geojson']
            }

            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import folium
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
from django.contrib.auth.decorators import login_required
from pyproj import Proj, Transformer
from shapely.ops import transform, unary_union
@csrf_exempt
# @login_required
@permission_classes([IsAuthenticated])
def suitable_area(request):
    if request.method == 'POST':
        # if request.user.is_authenticated:
        # else:
        #     return Response({"error": "You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        data = json.loads(request.body)
        region = data['region']
        buffer_clinics = float(data['bufferClinics'])
        buffer_restaut = float(data['bufferRestaut'])
        buffer_banks = float(data['bufferBanks'])
        buffer_clubs = float(data['bufferClubs'])
        buffer_parkdata = float(data.get('bufferParkdata', 0.01))
        buffer_hotels = float(data.get('bufferHotels', 0))
        hotel_types = data.get('hotelType', [])
        stars = data.get('stars', [])
        polygon = Polygon(region['coordinates'][0])

        # Initialize the transformer to convert WGS84 to UTM (meters)
        transformer_to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32630", always_xy=True)  # UTM zone 30N
        transformer_to_wgs84 = Transformer.from_crs("EPSG:32630", "EPSG:4326", always_xy=True)

       
        def point_to_utm(point):
            return transform(transformer_to_utm.transform, point)

       
        def geometry_to_wgs84(geometry):
            return transform(transformer_to_wgs84.transform, geometry)

        def get_buffered_points(model, buffer_size_meters):
            points = model.objects.values_list('latitude', 'longitude')
            original_points = []
            buffered_points = []
            for lat, lon in points:
                p = Point(lon, lat)
                if polygon.contains(p):
                    original_points.append(p)
                    # Transform the point to UTM, buffer in meters, and transform back
                    p_utm = point_to_utm(p)
                    buffered_point = p_utm.buffer(buffer_size_meters)
                    buffered_point_wgs84 = geometry_to_wgs84(buffered_point)
                    buffered_points.append(buffered_point_wgs84)
            return original_points, buffered_points

   
        def get_buffered_hotels(buffer_size_meters, types, stars):
            filters = {}
            if types:
                filters['type__in'] = types
            if stars:
                filters['stars__in'] = stars
            points = HotelInfo.objects.filter(**filters).values_list('latitude', 'longitude')
            original_points = []
            buffered_points = []
            for lat, lon in points:
                p = Point(lon, lat)
                if polygon.contains(p):
                    original_points.append(p)
                   
                    p_utm = point_to_utm(p)
                    buffered_point = p_utm.buffer(buffer_size_meters)
                    buffered_point_wgs84 = geometry_to_wgs84(buffered_point)
                    buffered_points.append(buffered_point_wgs84)
            return original_points, buffered_points

        clinics_points, clinics_buffers = get_buffered_points(Clinics, buffer_clinics)
        restaut_points, restaut_buffers = get_buffered_points(Restaut, buffer_restaut)
        banks_points, banks_buffers = get_buffered_points(Banks, buffer_banks)
        clubs_points, clubs_buffers = get_buffered_points(Clubs, buffer_clubs)
        parkdata_points, parkdata_buffers = get_buffered_points(Parkdata, buffer_parkdata)
        hotels_points, hotels_buffers = get_buffered_hotels(buffer_hotels, hotel_types, stars)




        def intersect_buffers(buffers_list):
            if not buffers_list:
                return None
            result = unary_union(buffers_list[0])
            for buffers in buffers_list[1:]:
                result = result.intersection(unary_union(buffers))
            return result

        def union_buffers(buffers_list):
            if not buffers_list:
                return None
            return unary_union(buffers_list)

        suitable_area = intersect_buffers([clinics_buffers, restaut_buffers, banks_buffers, clubs_buffers, parkdata_buffers])
        
        geometry = ee.Geometry.Polygon(region['coordinates'])
        dataset = ee.ImageCollection('ESA/WorldCover/v100').filterBounds(geometry).first()
        built_up = dataset.select('Map').eq(50)
        built_up_masked = built_up.updateMask(built_up).clip(geometry)
        built_up_features = built_up_masked.reduceToVectors(
            geometry=geometry,
            geometryType='polygon',
            reducer=ee.Reducer.countEvery(),
            scale=10,
            maxPixels=1e8
        )
        buildings_geojson = built_up_features.getInfo()

       
        building_polygons = [Polygon(feature['geometry']['coordinates'][0]) for feature in buildings_geojson['features']]
        buildings_union = unary_union(building_polygons)

        if suitable_area and hotels_buffers:
            hotels_union = union_buffers(hotels_buffers)
            suitable_area = suitable_area.difference(hotels_union)
        
        if suitable_area and not suitable_area.is_empty:
            suitable_area_no_buildings = suitable_area.difference(buildings_union)
        else:
            suitable_area_no_buildings = suitable_area

        suitable_area = suitable_area.intersection(polygon)
        suitable_area_no_buildings = suitable_area_no_buildings.intersection(polygon)
        
        # Calculate the center of the polygon
        center = polygon.centroid

        response_data = {
            'clinics': {
                'count': len(clinics_points),
                'buffer': buffer_clinics,
                'geojson': [polygon.__geo_interface__ for polygon in clinics_buffers],
                'original_points': [{'lat': point.y, 'lon': point.x} for point in clinics_points]
            },
            'restaurants': {
                'count': len(restaut_points),
                'buffer': buffer_restaut,
                'geojson': [polygon.__geo_interface__ for polygon in restaut_buffers],
                'original_points': [{'lat': point.y, 'lon': point.x} for point in restaut_points]
            },
            'banks': {
                'count': len(banks_points),
                'buffer': buffer_banks,
                'geojson': [polygon.__geo_interface__ for polygon in banks_buffers],
                'original_points': [{'lat': point.y, 'lon': point.x} for point in banks_points]
            },
            'clubs': {
                'count': len(clubs_points),
                'buffer': buffer_clubs,
                'geojson': [polygon.__geo_interface__ for polygon in clubs_buffers],
                'original_points': [{'lat': point.y, 'lon': point.x} for point in clubs_points]
            },
            'parks': {
                'count': len(parkdata_points),
                'buffer': buffer_parkdata,
                'geojson': [polygon.__geo_interface__ for polygon in parkdata_buffers],
                'original_points': [{'lat': point.y, 'lon': point.x} for point in parkdata_points]
            },
            'hotels': {
                'count': len(hotels_points),
                'buffer': buffer_hotels,
                'geojson': [polygon.__geo_interface__ for polygon in hotels_buffers],
                'original_points': [{'lat': point.y, 'lon': point.x} for point in hotels_points]
            },
            'suitable_area': {
                'geojson': suitable_area.__geo_interface__ if suitable_area and not suitable_area.is_empty else None,
            },
            'suitable_area_no_buildings': {
                'geojson': suitable_area_no_buildings.__geo_interface__ if suitable_area_no_buildings and not suitable_area_no_buildings.is_empty else None,
            },
            'buildings': {
                'geojson': buildings_geojson,
            },
            'center': {
                'lat': center.y,
                'lon': center.x
            },
        }

        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def hotels_data_chart(request):
    # Assume the region is sent as GeoJSON in the request body
    data = json.loads(request.body)
    
    # data=data['params']
    # Polygon(region['coordinates'][0])
    region = shape(data)

    # Filter hotels within the region using Shapely
    hotels_in_region = HotelInfo.objects.all()
    hotels_in_polygon = []
    
    for hotel in hotels_in_region:
        point = Point(hotel.longitude, hotel.latitude)
        if region.contains(point):
            hotels_in_polygon.append(hotel)

    # Calculate counts of types and stars
    types_count = {}
    stars_count = {}

    for hotel in hotels_in_polygon:
        # Count hotel types
        if hotel.type in types_count:
            types_count[hotel.type] += 1
        else:
            types_count[hotel.type] = 1
        
        # Count hotel stars
        if hotel.stars in stars_count:
            stars_count[hotel.stars] += 1
        else:
            stars_count[hotel.stars] = 1

    return JsonResponse({
        'types_count': types_count,
        'stars_count': stars_count,
    })