import datetime

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from haystack.query import SearchQuerySet


# Latest items, returns all items
class RssTumbleweedFeed(Feed):
    title = "Divensis.no: Latest content"
    link = "/"
    description = "Latest blog posts and projects"
    
    def items(self):
        return SearchQuerySet().filter(is_public=True, pub_date__lte=datetime.datetime.now()).order_by('-pub_date')[:10]
    
    def item_title(self, item):
        return item.title
    
    description_template = "tumbleweed/feed_item_description.html"
    
    #def item_description(self, item):
    #    return item.body_html
    
    def item_link(self, item):
        return item.url
    
    def item_title(self, item):
        return item.title
    
    def item_author_name(self, item):
        return item.author
    
    def item_pubdate(self, item):
        return item.pub_date
    

class AtomTumbleweedFeed(RssTumbleweedFeed):
    feed_type = Atom1Feed
    subtitle = RssTumbleweedFeed.description