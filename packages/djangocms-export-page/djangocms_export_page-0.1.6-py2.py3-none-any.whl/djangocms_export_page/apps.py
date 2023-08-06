from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoCmsExportPageConfig(AppConfig):
    name = "djangocms_export_page"
    verbose_name = _("Django CMS Export Page")
