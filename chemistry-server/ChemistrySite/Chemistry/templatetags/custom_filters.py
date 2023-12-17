from django import template

from Chemistry.models import Answers

register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name


@register.filter
def create_range(value, start_index=0):
    return range(start_index, value + start_index)


@register.filter
def get_answer_for_question(name):
    return Answers.objects.filter(question__name_text=name)

