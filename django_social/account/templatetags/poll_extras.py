from django import template 
from ..models import User 
    
  
register = template.Library() 
@register.simple_tag 
def any_function(): 
      return User.objects.count()