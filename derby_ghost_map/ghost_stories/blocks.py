from wagtail.blocks import (
    StructBlock, CharBlock, TextBlock, RichTextBlock, 
    ListBlock, BooleanBlock, ChoiceBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


class AudioBlock(StructBlock):
    """
    A block for adding audio content with optional caption
    """
    title = CharBlock(required=True)
    audio = DocumentChooserBlock(required=True)
    caption = CharBlock(required=False)
    autoplay = BooleanBlock(required=False, default=False)
    loop = BooleanBlock(required=False, default=False)
    
    class Meta:
        template = 'ghost_stories/blocks/audio_block.html'
        icon = 'media'
        label = 'Audio Track'


class QuoteBlock(StructBlock):
    """
    A block for quotes with attribution
    """
    quote = TextBlock(required=True)
    attribution = CharBlock(required=False)
    
    class Meta:
        template = 'ghost_stories/blocks/quote_block.html'
        icon = 'openquote'
        label = 'Quote'


class GalleryImageBlock(StructBlock):
    """
    A block for images in a gallery with captions
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    
    class Meta:
        template = 'ghost_stories/blocks/gallery_image_block.html'
        icon = 'image'
        label = 'Gallery Image'


class GalleryBlock(StructBlock):
    """
    A gallery of images
    """
    title = CharBlock(required=False)
    images = ListBlock(GalleryImageBlock())
    
    class Meta:
        template = 'ghost_stories/blocks/gallery_block.html'
        icon = 'image'
        label = 'Image Gallery'