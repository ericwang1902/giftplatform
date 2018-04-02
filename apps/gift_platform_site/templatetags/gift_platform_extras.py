from django import template

register = template.Library()

@register.filter
def take(values, arg):
    """
    根据步进和步数来取出相关数据
    :param values:
    :param args:
    :return:
    """
    print(arg)
    if arg is None:
        return values
    else:
        return values[(int(arg)) * 8: (int(arg) + 1) * 8]

@register.filter
def to_range(value):
    return range(1, int(value / 8) + 1)
