
from django import template
register = template.Library()

@register.filter
def userColorClass(user):
    if user is None:
        return ""
    if user.rating <= 0:
        return "UserBlack"
    elif user.rating < 1200:
        return "UserGray"
    elif user.rating < 1400:
        return "UserGreen"
    elif user.rating < 1600:
        return "UserCyan"
    elif user.rating < 1900:
        return "UserBlue"
    elif user.rating < 2100:
        return "UserPurple"
    elif user.rating < 2300:
        return "UserOrange"
    elif user.rating < 2400:
        return "UserOrangeRed"
    elif user.rating < 2600:
        return "UserLightRed"
    elif user.rating < 3000:
        return "UserRed"
    else:
        return "UserDarkRed"

