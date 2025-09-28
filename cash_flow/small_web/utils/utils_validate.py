from datetime import datetime
from typing import Union

from small_web.models import CustomUsers


def username_validation_on_creating(username: str) -> bool:
    existed_username = CustomUsers.objects.filter(username=username).first()
    return False if not existed_username else True


def email_validation_on_creating(email: str) -> bool:
    existed_email = CustomUsers.objects.filter(email=email).first()
    return False if not existed_email else True


CHOSEN_FIELD = [
    "status", "type", "category",
    "subcategory", "created_at_start", "created_at_end"
]
