from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.blocks import RichTextBlock
from wagtail.api import APIField

from .blocks import AudioBlock, QuoteBlock, GalleryBlock


class GhostMapPage(Page):
    """
    The main map page showing all ghost story locations
    """
    introduction = RichTextField(blank=True)
    map_zoom_level = models.IntegerField(default=14)
    map_center_latitude = models.FloatField(default=52.9225)
    map_center_longitude = models.FloatField(default=-1.4746)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        MultiFieldPanel([
            FieldPanel('map_center_latitude'),
            FieldPanel('map_center_longitude'),
            FieldPanel('map_zoom_level'),
        ], heading="Map Settings"),
    ]
    
    # Control what can be created beneath this page
    subpage_types = ['ghost_stories.LocationPage']
    
    # Create a template context for the map page
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all published location pages
        context['locations'] = LocationPage.objects.live().child_of(self)
        
        return context


class LocationPage(Page):
    """
    A page representing a location in Derby with ghost stories
    """
    description = models.CharField(max_length=255)
    coordinates = models.CharField(
        max_length=255,
        help_text="Latitude and longitude as 'lat,lng', e.g. '52.9225,-1.4746'"
    )
    address = models.CharField(max_length=255, blank=True)
    
    # Featured image for the location marker/page
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Historical information about this location
    history = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('coordinates'),
        FieldPanel('address'),
        FieldPanel('featured_image'),
        FieldPanel('history'),
    ]
    
    # Parent and child page types
    parent_page_types = ['ghost_stories.GhostMapPage']
    subpage_types = ['ghost_stories.StoryPage']
    
    # API fields for map integration
    api_fields = [
        APIField('description'),
        APIField('coordinates'),
        APIField('address'),
        APIField('featured_image'),
        APIField('story_count'),
    ]
    
    @property
    def latitude(self):
        if self.coordinates:
            return float(self.coordinates.split(',')[0].strip())
        return None
    
    @property
    def longitude(self):
        if self.coordinates:
            return float(self.coordinates.split(',')[1].strip())
        return None
    
    @property
    def story_count(self):
        return self.get_children().live().count()
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['stories'] = StoryPage.objects.live().child_of(self)
        return context


class StoryPage(Page):
    """
    A page representing a specific ghost story at a location
    """
    summary = models.CharField(max_length=255)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # The story content using StreamField for flexible content
    story_content = StreamField([
        ('paragraph', RichTextBlock()),
        ('quote', QuoteBlock()),
        ('image', ImageChooserBlock()),
        ('gallery', GalleryBlock()),
        ('audio', AudioBlock()),
    ], use_json_field=True)
    
    # Audio narration
    narration = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Story metadata
    year = models.IntegerField(null=True, blank=True)
    author = models.CharField(max_length=255, blank=True)
    sources = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('main_image'),
        FieldPanel('story_content'),
        FieldPanel('narration'),
        MultiFieldPanel([
            FieldPanel('year'),
            FieldPanel('author'),
            FieldPanel('sources'),
        ], heading="Story Metadata"),
    ]
    
    # Parent page types
    parent_page_types = ['ghost_stories.LocationPage']
    subpage_types = []
    
    # API fields
    api_fields = [
        APIField('summary'),
        APIField('main_image'),
        APIField('narration'),
        APIField('year'),
    ]
    
    def get_location(self):
        return self.get_parent().specific