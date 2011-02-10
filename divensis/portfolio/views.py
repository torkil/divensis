from django.db.models import F
from django.shortcuts import get_object_or_404
from django.views.generic import date_based, list_detail
from django.conf import settings

from divensis.portfolio.models import Project, Category


def project_list(request, **kwargs):
    """
    Project list

    Template: ``portfolio/project_list.html``
    Context:
        object_list
            List of all projects
    """
    return list_detail.object_list(
        request,
        queryset = Project.objects.all(),
        **kwargs
    )

def project_detail(request, slug, **kwargs):
    """
    Project detail

    Template: ``portfolio/project_detail.html``
    Context:
        object
            Project details
    """
    project = get_object_or_404(
        Project,
        slug=slug
    )

    if not request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
        project.visits = F('visits') + 1
        project.save()

    return list_detail.object_detail(
        request,
        slug = slug,
        slug_field = 'slug',
        queryset = Project.objects.all()
    )

def category_detail(request, slug, template_name = 'portfolio/category_detail.html', **kwargs):
    """
    Category detail

    Template: ``portfolio/category_detail.html``
    Context:
        object_list
            List of projects specific to the given category.
        category
            Given category.
    """
    category = get_object_or_404(Category, slug__iexact=slug)

    return list_detail.object_list(
        request,
        queryset = category.project_set.all(),
        extra_context = {'category': category},
        template = template_name
    )
