import time

from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import date_based, list_detail
from django.conf import settings

from tagging.models import Tag, TaggedItem

from divensis.blog.models import Post, Category


def post_list(request, page=0, paginate_by=20, **kwargs):
    # TODO: Make setting
    page_size = 2

    return list_detail.object_list(
        request,
        queryset = Post.objects.published(),
        paginate_by = page_size,
        page = page,
        **kwargs
    )


def post_archive_year(request, year, **kwargs):
    return date_based.archive_year(
        request,
        year = year,
        date_field = 'published_date',
        queryset = Post.objects.published(),
        make_object_list = True,
        **kwargs
    )


def post_archive_month(request, year, month, **kwargs):
    return date_based.archive_month(
        request,
        year = year,
        month = month,
        month_format='%m',
        date_field = 'published_date',
        queryset = Post.objects.published(),
        **kwargs
    )


def post_archive_day(request, year, month, day, **kwargs):
    return date_based.archive_day(
        request,
        year = year,
        month = month,
        day = day,
        month_format = '%m',
        date_field = 'published_date',
        queryset = Post.objects.published(),
        **kwargs
    )


def post_detail(request, slug, year, month, day, **kwargs):
    '''
    Displays post detail. If user is superuser, view will display
    unpublished post detail for previewing purposes.
    '''
    
    month_format = '%m'
    
    # This logic completely duplicates date_based.object_detail but allows us
    # to increment the view count for each post at the cost of a duplicate
    # query and some extra parsing:
    try:
        tt = time.strptime('%s-%s-%s' % (year, month, day), '%%Y-%s-%%d' % month_format)
    except ValueError:
        raise Http404
    
    post = get_object_or_404(
        Post,
        slug=slug,
        published_date__year=tt.tm_year,
        published_date__month=tt.tm_mon,
        published_date__day=tt.tm_mday
    )
 
    #if user is not superuser then don't allow viewing of non-public posts
    if not request.user.is_superuser and post.status != Post.STATUS_PUBLIC:
        raise Http404
 
    if not request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
        post.visits = F('visits') + 1
        post.save()
        
    return date_based.object_detail(
        request,
        year = year,
        month = month,
        month_format = month_format,
        day = day,
        date_field = 'published_date',
        slug = slug,
        queryset = Post.objects.all(),
        **kwargs
    )


def category_list(request, template_name='blog/category_list.html', **kwargs):
    """
    Category list

    Template: ``blog/category_list.html``
    Context:
        object_list
            List of categories.
    """
    return list_detail.object_list(
        request,
        queryset = Category.objects.all(),
        template_name = template_name,
        **kwargs
    )


def category_detail(request, slug, template_name='blog/category_detail.html', **kwargs):
    """
    Category detail

    Template: ``blog/category_detail.html``
    Context:
        object_list
            List of posts specific to the given category.
        category
            Given category.
    """
    category = get_object_or_404(Category, slug__iexact=slug)

    return list_detail.object_list(
        request,
        queryset = category.post_set.published(),
        extra_context = {'category': category},
        template_name = template_name,
        **kwargs
    )


def tag_detail(request, slug, template_name='blog/tag_detail.html', **kwargs):
    """
    Tag detail

    Template: ``blog/tag_detail.html``
    Context:
        object_list
            List of posts specific to the given tag.
        tag
            Given tag.
    """
    tag = get_object_or_404(Tag, name__iexact=slug)

    return list_detail.object_list(
        request,
        queryset = TaggedItem.objects.get_by_model(Post,tag).filter(status=2),
        extra_context = {'tag': tag},
        template_name = template_name,
        **kwargs
    )