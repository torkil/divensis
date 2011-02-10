from imagekit.specs import ImageSpec
from imagekit import processors
from divensis.util import custprocessor


# Resize processors
class ResizeThumb(custprocessor.ResizeBugFix):
    width = 75
    height = 50
    crop = True

class ResizeDisplay(custprocessor.ResizeBugFix):
    width = 600

# Images in RSS feed
class ResizeFeedImage(custprocessor.ResizeBugFix):
    width = 720
    height = 415
    crop = True

# Featured images
class ResizeFeatured(custprocessor.ResizeBugFix):
    width = 720
    height = 415
    crop = True

# Large blog image
class ResizeBlogLarge(custprocessor.ResizeBugFix):
    width = 720

# Images in blog list
class ResizeBlogList(custprocessor.ResizeBugFix):
    width = 350
    height = 195
    crop = True

# Images in portfolio
class ResizePortfolioFilter(custprocessor.ResizeBugFix):
    width = 230
    height = 115
    crop = True

# Adjustment processors
class EnhanceThumb(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1

# Set filetype PNG
class JPEGFile(processors.Format):
    format = 'JPEG'
    extension = 'jpg'

# Set filetype PNG
class PNGFile(processors.Format):
    format = 'PNG'
    extension = 'png'

# Specs
class Featured(ImageSpec):
    access_as = 'featured'
    quality = 95
    pre_cache = True
    processors = [ResizeFeatured]

class BlogList(ImageSpec):
    access_as = 'blog_list'
    quality = 95
    pre_cache = True
    processors = [ResizeBlogList]

class BlogLarge(ImageSpec):
    access_as = 'blog_large'
    quality = 95
    pre_cache = True
    processors = [ResizeBlogLarge]

class PortfolioFilter(ImageSpec):
    access_as = 'portfolio_filter'
    quality = 95
    pre_cache = True
    processors = [ResizePortfolioFilter]

class PortfolioLarge(ImageSpec):
    access_as = 'portfolio_large'
    quality = 95
    pre_cache = True
    processors = [ResizeFeatured]
    
class FeedImage(ImageSpec):
    access_as = 'feed_image'
    quality = 95
    pre_cache = True
    processors = [ResizeFeedImage]

class AdminThumbnail(ImageSpec):
    access_as = 'admin_thumbnail'
    quality = 95
    pre_cache = True
    processors = [ResizeThumb]

class Display(ImageSpec):
    access_as = 'display'
    quality = 95
    increment_count = True
    processors = [ResizeDisplay]
