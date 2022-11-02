from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(year):
    if datetime.now().year < year:
        raise ValidationError(
            _('Year of film must be correct.')
        )
