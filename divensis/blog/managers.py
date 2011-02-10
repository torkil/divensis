import datetime

from django.db.models import Manager


class PublicManager(Manager):
    """ Returns public posts less than or equal current time """
    
    def published(self):
        return self.get_query_set().filter(
            status__exact=2,
            published_date__lte=datetime.datetime.now()
        )