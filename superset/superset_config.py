import os
os.environ['LC_ALL'] = 'en_US.UTF-8'
os.environ['LANG'] = 'en_US.UTF-8'
import warnings
from flask_appbuilder.security.manager import AUTH_DB, BaseSecurityManager
from superset.security import SupersetSecurityManager
from superset.tasks.types import ExecutorType

THUMBNAIL_SELENIUM_USER = 'admin'
ALERT_REPORTS_EXECUTE_AS = [ExecutorType.SELENIUM]
# Custom Security Manager
class CustomSecurityManager(SupersetSecurityManager):
    def add_permissions(self):
        super().add_permissions()
        self.add_custom_permissions()

    def add_custom_permissions(self):
        from flask_appbuilder.models.sqla.interface import SQLAInterface
        from flask_appbuilder import Model
        from superset import db

        class Alert(Model):
            pass

        class Report(Model):
            pass

        self.add_permission_view_menu("can_read", "Alert Model")
        self.add_permission_view_menu("can_write", "Alert Model")
        self.add_permission_view_menu("can_read", "Report Model")
        self.add_permission_view_menu("can_write", "Report Model")

        db.session.commit()

CUSTOM_SECURITY_MANAGER = CustomSecurityManager

# Database configuration
#SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:aqeH#$9030@database-1.cr648soospc5.us-west-2.rds.amazonaws.com:5432/supersetdb'
SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://superset:supersetpassword@postgres:5432/superset_db'
# CSRF configuration
WTF_CSRF_ENABLED = True

# Feature flags configuration
FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    "ALERT_REPORTS": True,  # Enable ALERT_REPORTS feature flag
}

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_URL': 'redis://redis:6379/0',
}

# Celery configuration
from celery.schedules import crontab

REDIS_HOST = "redis"
REDIS_PORT = "6379"

class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    worker_prefetch_multiplier = 10
    task_acks_late = True
    task_annotations = {
        "sql_lab.get_sql_results": {
            "rate_limit": "100/s",
        },
    }
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=0, hour=0),
        },
    }
CELERY_CONFIG = CeleryConfig

SCREENSHOT_LOCATE_WAIT = 100
SCREENSHOT_LOAD_WAIT = 600

# Slack configuration
#SLACK_API_TOKEN = "xoxb-"

# Email configuration
SMTP_HOST = "email-smtp.us-west-2.amazonaws.com"  # change to your host
SMTP_PORT = 587 # your port, e.g. 587
SMTP_STARTTLS = True
SMTP_SSL_SERVER_AUTH = True  # If you're using an SMTP server with a valid certificate
SMTP_SSL = False
SMTP_USER = "AKIAXDRHV5ZLA5BTZW6T"  # use the empty string "" if using an unauthenticated SMTP server
SMTP_PASSWORD = "BKMS8bybTogsduzAlIMituI03RaFsOmiIE9I71TdkYC0"  # use the empty string "" if using an unauthenticated SMTP server
SMTP_MAIL_FROM = "artemis-alerts@omnissa.com"
EMAIL_REPORTS_SUBJECT_PREFIX = "[Superset] "  # optional - overwrites default value in config.py of "[Report] "

# WebDriver configuration
# If you use Firefox, you can stick with default values
# If you use Chrome, then add the following WEBDRIVER_TYPE and WEBDRIVER_OPTION_ARGS
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_OPTION_ARGS = [
    "--force-device-scale-factor=2.0",
    "--high-dpi-support=2.0",
    "--headless",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-extensions",
]

# This is for internal use, you can keep http
WEBDRIVER_BASEURL = "http://superset:8088"
# This is the link sent to the recipient. Change to your domain, e.g. https://superset.mydomain.com
WEBDRIVER_BASEURL_USER_FRIENDLY = "http://superset:8088"

# Disable dry-run mode
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False
RATELIMIT_STORAGE_URL = 'redis://redis:6379/3'
ENABLE_PROXY_FIX = True
# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module='flask_limiter.extension') 
warnings.filterwarnings("ignore", category=UserWarning, module='werkzeug.local')

