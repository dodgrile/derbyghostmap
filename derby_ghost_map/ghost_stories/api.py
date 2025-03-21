from django.http import JsonResponse
from django.urls import path

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from .models import LocationPage, StoryPage


# Create custom API endpoints
api_router = WagtailAPIRouter('wagtailapi')

# Register standard Wagtail endpoints
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)


# Custom API view for map locations
def locations_api(request):
    """
    Return all ghost story locations as GeoJSON for the map
    """
    # Get all published location pages
    locations = LocationPage.objects.live()
    
    # Create GeoJSON feature collection
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for location in locations:
        if location.latitude and location.longitude:
            # Add a GeoJSON feature for this location
            feature = {
                "type": "Feature",
                "properties": {
                    "id": location.id,
                    "title": location.title,
                    "description": location.description,
                    "story_count": location.story_count,
                    "url": location.url,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [location.longitude, location.latitude]
                }
            }
            
            # Add featured image if available
            if location.featured_image:
                feature["properties"]["image_url"] = location.featured_image.get_rendition('fill-200x200').url
            
            geojson["features"].append(feature)
    
    return JsonResponse(geojson)


# Custom API view for location stories
def location_stories_api(request, location_id):
    """
    Return all stories for a specific location
    """
    try:
        location = LocationPage.objects.get(id=location_id)
        stories = StoryPage.objects.live().child_of(location)
        
        stories_data = []
        for story in stories:
            story_data = {
                "id": story.id,
                "title": story.title,
                "summary": story.summary,
                "url": story.url,
            }
            
            # Add main image if available
            if story.main_image:
                story_data["image_url"] = story.main_image.get_rendition('fill-400x300').url
            
            # Add narration if available
            if story.narration:
                story_data["narration_url"] = story.narration.url
            
            stories_data.append(story_data)
        
        return JsonResponse(stories_data, safe=False)
    
    except LocationPage.DoesNotExist:
        return JsonResponse({"error": "Location not found"}, status=404)