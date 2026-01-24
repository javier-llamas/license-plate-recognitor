import os

from dbos import DBOS, DBOSConfig
from django.apps import AppConfig


class WebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.web"

    def ready(self):
        dbos_config: DBOSConfig = {
            "name": "django-app",
            "system_database_url": os.environ.get("DBOS_DATABASE_URL"),
        }
        DBOS(config=dbos_config)
        DBOS.launch()
        return super().ready()
