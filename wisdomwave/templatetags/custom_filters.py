from django import template
from django import templatetags

register = template.Library()

@register.filter
def cls(value):
    if ',' in value:
        return value.rsplit(',', 1)[0]
    else:
        return value 
    
     
@register.filter
def sec(value):
    if ',' in value:
        return value.rsplit(',', 1)[1]
    else:
        return value  
    
@register.filter
def grade(value):
    if value >= 80:
        return 'A+'
    elif value >=70:
        return 'A'
    elif value >=60:
        return 'A-'
    elif value >=50:
        return 'B'
    elif value >=40:
        return 'C'
    elif value >=33:
        return 'D'
    else:
        return 'F'
 

@register.filter
def gpa(value):
    if value >= 80:
        return 5.00
    elif value >=70:
        return 4.00
    elif value >=60:
        return 3.50
    elif value >=50:
        return 3.00
    elif value >=40:
        return 2.00
    elif value >=33:
        return 1.00
    else:
        return 0.00

@register.filter
def total_gpa(marks):
    total = sum(gpa(float(mark.marks_obtained)) for mark in marks)
    total = total/len(marks)
    return f'{total:.2f}' if marks else '0.00'

