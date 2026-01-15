from django import template
from django.core.exceptions import BadRequest
from ..constants import forbidden_words
from django.utils.translation import gettext as _


register = template.Library()


@register.filter()
def censor(value):
   if not isinstance(value, str):
      raise TypeError('Value must be a string')

   censored_text = value
   for word in forbidden_words:
      words = censored_text.split()
      censored_words = []
      for w in words:
         if word in w.lower():
            censored_words.append(w[0] + '*' * (len(w) - 2) + w[-1])
         else:
            censored_words.append(w)
      censored_text = ' '.join(censored_words)

   return censored_text


@register.filter
def join_categories(value):
    return ", ".join([category.name for category in value])


@register.filter()
def beautiful_post_type(value):
   if value == 'news':
      return _('News')
   elif value == 'article':
      return _('Articles')
   else:
      return value


@register.filter()
def author(user):
    if user.groups.filter(name='authors').exists():
        return True
    else:
        return False


@register.filter()
def admin(user):
    if user.groups.filter(name='admin').exists():
        return True
    else:
        return False