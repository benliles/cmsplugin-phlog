from os.path import join

from django.conf import settings
from django.contrib.admin import StackedInline
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.plugin_rendering import render_plugins

from photologue.models import Photo

from cmsplugin_phlog.forms import GalleryPluginForm
from cmsplugin_phlog.models import PhlogGalleryPlugin, PhlogPhotoPlugin, PhlogPhoto, GalleryPlugin



class CMSPhlogPlugin(CMSPluginBase):
    model = PhlogGalleryPlugin
    name = _('Photologue Gallery (Deprecated)')
    render_template = 'cms/plugins/phlog/gallery.html'
    
    def render(self, context, instance, placeholder):
        if instance.order == 'random':
            images = instance.gallery.sample(limit=instance.limit,
                                             public=instance.public)
        elif instance.order == 'date':
            images = instance.gallery.latest(limit=instance.limit,
                                             public=instance.public)
        else:
            images = instance.gallery.in_order(public=instance.public,
                                               limit=instance.limit)
        
        context.update({
            'gallery': instance.gallery,
            'image_list': images,
            'gallery_plugin': instance,
            'placeholder': placeholder})
        
        return context

class PhotoAdminInline(StackedInline):
    model = PhlogPhoto

class SinglePhotoAdminInline(PhotoAdminInline):
    max_num=1
    extra=1
    can_delete=False

class PhlogPhotoPlugin(CMSPluginBase):
    model = PhlogPhotoPlugin
    name = _('Photologue Photo')
    render_template = 'cms/plugins/phlog/photo.html'
    inlines=[SinglePhotoAdminInline]
    text_enabled = True
    
    def render(self, context, instance, placeholder):
        context.update({
            'photo': instance.photos.all()[0],
            'instance': instance})
        return context
    
    def icon_src(self, instance):
        try:
            instance.photos.all()[0].get_admin_thumbnail_url()
        except:
            return settings.CMS_MEDIA_URL + u"images/plugins/image.png"

class PhlogGalleryPlugin(CMSPluginBase):
    model = GalleryPlugin
    form = GalleryPluginForm
    name = _('Phlog Gallery')
    render_template = 'cms/plugins/phlog/gallery.html'
    change_form_template = 'cms/plugins/phlog/gallery_change_form.html'
    # Need to create a form for the plugin to add a widget for child plugins
    
    def render(self, context, instance, placeholder):
        context.update({
            'placeholder': placeholder,
            'gallery': instance})
        
        context.update({
            'plugins': render_plugins(instance.cmsplugin_set.filter(parent=instance).order_by('position'),
                                      context, placeholder)
        })
        
        return context
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        plugin = getattr(self, 'cms_plugin_instance', None)
        
        if plugin:
            context.update({
                'base_plugin': plugin,
                'installed_plugins': plugin_pool.get_all_plugins(plugin.placeholder.slot)
            })
            context['adminform'].form.initial.setdefault('plugins', plugin)
        
        return super(PhlogGalleryPlugin, self).render_change_form(request, context, add, change, form_url, obj)
    

plugin_pool.register_plugin(CMSPhlogPlugin)
plugin_pool.register_plugin(PhlogPhotoPlugin)
plugin_pool.register_plugin(PhlogGalleryPlugin)
