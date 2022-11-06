from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(year):
    if year > datetime.now().year:
        raise ValidationError(
            _('Year must be smaller than current one.')
        )
