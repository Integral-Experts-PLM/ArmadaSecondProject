from django import template
from datetime import datetime
import re

register = template.Library()

# @register.filter
# def format_datetime(value):
#     try:
#         date_part = value.split('T')[0]
#         return date_part
#     except (ValueError, AttributeError):
#         return ''

@register.filter
def format_datetime(value): 
     # Si 'value' es una instancia de datetime (proviene de la BBDD), formatea como DD/MM/YYYY
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    # Si 'value' es una cadena (proviene de webservices), asume que está en formato ISO y extrae la fecha
    elif isinstance(value, str):
        try:
            fecha_parte = value.split('T')[0]  # Cogemos solo la parte de la fecha
            # Parseamos y formateamos la fecha
            date_object = datetime.strptime(fecha_parte, "%Y-%m-%d")
            return date_object.strftime("%d/%m/%Y")
        except (ValueError, AttributeError):
            pass
    # En cualquier otro caso, o si hay un error, retorna una cadena vacía
    return ''

@register.filter
def extract_after_colon(value):
    try:
        if value is not None:
            if ":" in value:
                return value.split(":")[1].strip()
        return value
    except (ValueError, AttributeError):
        return ''
    
