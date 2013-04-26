import os.path

from django.conf import settings
from django.forms.widgets import Widget
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


_base_js = list(os.path.join(settings.CMS_MEDIA_URL, path) for path in (
                'js/libs/jquery.ui.core.js',
                'js/libs/jquery.ui.dialog.js',
                'js/libs/jquery.ui.sortable.js'))
_base_css = list(os.path.join(settings.CMS_MEDIA_URL, path) for path in (
                'css/jquery/cupertino/jquery-ui.css',))

class PluginsWidget(Widget):
    
    class Media:
        css = {
            'all': _base_css + [settings.CMS_PLUGIN_PHLOG_MEDIA_URL + 'css/plugins_widget.css']
        }
        
        js = _base_js + [settings.CMS_PLUGIN_PHLOG_MEDIA_URL + 'js/plugins_widget.js']
    
    def __init__(self, request=None, **kwargs):
        super(PluginsWidget, self).__init__(**kwargs)
        if request is None:
            self.request = request
        else:
            self.request = ''
    
    def render(self, name, value, attrs=None):
        if value:
            context = {
                'plugin_list': value.cmsplugin_set.filter(parent=value).order_by('position'),
                'installed_plugins': plugin_pool.get_all_plugins(value.placeholder.slot),
                'placeholder': value.placeholder,
                'plugin': value}
        else:
            context = {'add': True}
        
        return mark_safe(render_to_string(
                         'admin/phlog/widgets/plugins.html', context, RequestContext(self.request)))

