from django.apps import AppConfig


class IngredientRequestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ingredient_requests"

    def ready(self):
        import ingredient_requests.signals