from django.forms import ModelForm, IntegerField, HiddenInput

from cmsplugin_phlog.forms.fields import ChildPluginsField
from cmsplugin_phlog.models import GalleryPlugin



class GalleryPluginForm(ModelForm):
    plugins = ChildPluginsField()
    
    def __init__(self, data=None, files=None, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.setdefault('initial', {})
            kwargs['initial']['plugins'] = instance
        
        super(GalleryPluginForm, self).__init__(data=data, files=files, **kwargs)
    
    class Meta:
        model = GalleryPlugin
