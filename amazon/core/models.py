from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_merchant = models.BooleanField(_('merchant status'), default=False,
                                      help_text=_('If user register in mercahnt this\
                                                  field return True automatically.'))
