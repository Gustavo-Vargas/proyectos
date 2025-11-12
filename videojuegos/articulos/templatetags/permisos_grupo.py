from django import template

register = template.Library()

@register.filter(name='pertenece_grupo')
def pertenece_grupo(usuario, grupo):
    for gpo in usuario.groups.all():
        if gpo.name == grupo:
            return True
    return False


@register.simple_tag(takes_context=True)
def cart_count(context):
    request = context.get('request')
    if not request:
        return 0
    cart = request.session.get('cart', {})
    return sum(item.get('cantidad', 0) for item in cart.values())