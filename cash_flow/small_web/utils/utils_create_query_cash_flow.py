from django.db.models import Q


def create_date_period(start_date: str = None, end_date: str = None) -> Q:
    if start_date and end_date:
        result = Q(created_at__gt=start_date) & Q(created_at__lt=end_date)
        return result
    if start_date:
        result = Q(created_at__gt=start_date)
        return result
    if end_date:
        result = Q(created_at__lt=end_date)
        return result
    return ~Q(created_at=None)


def create_status_filter(status: str) -> Q:
    if int(status) != 0:
        return Q(status=status)
    return ~Q(status=0)


def create_type_filter(type: str) -> Q:
    if int(type) != 0:
        return Q(type=type)
    return ~Q(type=0)


def create_category_filter(category: str) -> Q:
    if int(category) != 0:
        return Q(category=category)
    return ~Q(category=0)


def create_subcategory_filter(subcategory: str) -> Q:
    if int(subcategory) != 0:
        return Q(subcategory=subcategory)
    return ~Q(subcategory=0)
