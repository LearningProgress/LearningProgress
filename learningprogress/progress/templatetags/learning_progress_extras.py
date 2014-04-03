from django import template
from django.db.models import Avg

from ..views import get_progress_info

register = template.Library()


def section_progress_icon(context, section):
    """
    Template tag which returns a string for the icon css class
    (glyphicon-xxx) depending on the context dictionary 'section_progresses'
    and the given section.
    """
    try:
        value = get_progress_info(context['section_progresses'][section.pk], 'css_glyphicon')
    except KeyError:
        value = ''
    return value


def branch_average(context, mockexambranch):
    """
    Template tag to return the average of all user's marks for the given mock
    exam branch.
    """
    value = mockexambranch.mockexam_set.filter(user=context['user']).aggregate(Avg('mark'))['mark__avg']
    return '{:.2f}'.format(value)


register.simple_tag(takes_context=True)(section_progress_icon)
register.simple_tag(takes_context=True)(branch_average)
