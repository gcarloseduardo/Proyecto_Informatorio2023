from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Replaces or adds GET parameters in the current URL.
    Usage: {% url_replace param1="value1" param2="value2" %}
    Set a parameter's value to None to remove it.
    """
    query = context['request'].GET.copy()

    # Update or remove parameters
    for key, value in kwargs.items():
        if value is None:
            if key in query:
                del query[key]
        else:
            query[key] = value

    # Ensure 'id', 'buscar', 'fecha', 'orden' are handled correctly.
    # This part ensures that if you provide a new 'id' for instance,
    # it replaces the old one cleanly.
    # This is more important if we're not removing existing params in kwargs.
    # The kwargs dict already handles setting the new value.

    # Convert to URL-encoded string
    return query.urlencode()

@register.simple_tag(takes_context=True)
def url_with_new_params(context, **kwargs):
    """
    Creates a new query string from current GET params,
    overriding or adding parameters specified in kwargs.
    Usage: <a href="?{% url_with_new_params param1='value1' param2='value2' %}">

    This is a simpler version where provided kwargs override existing,
    and other existing params are kept.
    """
    query_params = context['request'].GET.copy()
    for key, value in kwargs.items():
        query_params[key] = value

    # We need to make sure 'fecha' and 'orden' are mutually exclusive,
    # and 'id' overrides cleanly. This is best handled by explicit kwargs.
    # For example, if setting 'fecha', remove 'orden'.
    if 'fecha' in kwargs and 'orden' in query_params:
        del query_params['orden']
    if 'orden' in kwargs and 'fecha' in query_params:
        del query_params['fecha']

    return query_params.urlencode()