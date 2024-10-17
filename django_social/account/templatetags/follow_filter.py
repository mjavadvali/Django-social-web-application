from django import template
from ..models import UserFollowing

register = template.Library()

@register.filter
def is_following(following_user, followed_user):
    return UserFollowing.objects.filter(following_user=following_user, followed_user=followed_user, value='Follow').exists()