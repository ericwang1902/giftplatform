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



@register.filter
def to_price_output(productItems):
    product_items = productItems.order_by("price").all()
    start_price = product_items.first().price
    end_price = product_items.last().price
    if start_price == end_price:
        return start_price
    else:
        return '{} - {}'.format(start_price,end_price)

@register.filter
def to_sell_price_output(productItems):
    product_items = productItems.order_by("price").all()
    start_price = product_items.first().favouredprice
    end_price = product_items.last().favouredprice
    if start_price == end_price:
        return start_price
    else:
        return '{} - {}'.format(start_price,end_price)
