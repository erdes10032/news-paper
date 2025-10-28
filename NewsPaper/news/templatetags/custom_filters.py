from django import template
from django.core.exceptions import BadRequest
from ..constants import BAD_WORDS
register = template.Library()

@register.filter()
def censor(value):
   if not isinstance(value, str):
      raise TypeError('Value must be a string')

   censored_text = value
   for word in BAD_WORDS:
      words = censored_text.split()
      censored_words = []
      for w in words:
         if word in w.lower():
            censored_words.append(w[0] + '*' * (len(w) - 1))
         else:
            censored_words.append(w)
      censored_text = ' '.join(censored_words)

   return censored_text

@register.filter
def join_categories(value):
    return ", ".join([category.name for category in value])