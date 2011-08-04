from django.forms import Field

try:
    from cmsplugin_phlog.forms.widgets import PluginsWidget
except Exception, e:
    print str(e)
    raise e



class ChildPluginsField(Field):
    widget = PluginsWidget
    
    def __init__(self, **kwargs):
        kwargs['required'] = False
        super(ChildPluginsField, self).__init__(**kwargs)
    