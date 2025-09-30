from rest_framework.throttling import UserRateThrottle

class MenuItemListThrottle(UserRateThrottle):
    """
    Custom throttle class to limit public access to menu item list endpoint.
    Default rate: 10 requests per minute per user.
    """
    rate = '10/min' 