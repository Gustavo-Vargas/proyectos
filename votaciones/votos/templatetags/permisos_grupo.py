from django import template

register = template.Library()

@register.filter(name='pertenece_grupo')
def pertenece_grupo(usuario, grupo):
    for gpo in usuario.groups.all():
        if gpo.name.lower() == grupo.lower():
            return True
    return False

