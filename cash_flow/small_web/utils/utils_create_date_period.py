from django.db.models import Q


def create_date_period(start_date: str = None, end_date: str = None):
    if start_date and end_date:
        result = Q(created_at__gt=start_date) & Q(created_at__lt=end_date)
        return result
    if start_date:
        result = Q(created_at__gt=start_date)
        return result
    if end_date:
        result = Q(created_at__lt=end_date)
        return result
    return Q(created_at=None)
