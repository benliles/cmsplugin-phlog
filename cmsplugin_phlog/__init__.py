from django.conf import settings



if 'cmsplugin_phlog' in settings.INSTALLED_APPS:
    if not hasattr(settings,'CMS_PLUGIN_PHLOG_MEDIA_URL'):
        settings.CMS_PLUGIN_PHLOG_MEDIA_URL = settings.MEDIA_URL + 'cmsplugin_phlog/'