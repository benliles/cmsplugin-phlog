Introduction
------------

This is a `Django CMS` plugin for incorporating `photologue` galleries.

Installation
------------

First, you must install `Django CMS` and `photologue` which require `Django` 
and a few other libraries such as `PIL`. For full details, see the installation 
instructions for those packages.

Install ``cmsplugin-phlog`` to your environment with a tool such as `PIP`, 
`setuptools`, or `buildout`.

Add ``cmsplugin_phlog`` to the ``INSTALLED_APPS`` list in your project's 
``settings.py`` and run the ``syncdb`` command on your ``manage.py``.

.. _Django: http://www.djangoproject.com/
.. _Django CMS: https://www.django-cms.org/
.. _photologue: http://code.google.com/p/django-photologue/
.. _PIL: http://www.pythonware.com/products/pil/
.. _PIP: http://www.pip-installer.org/
.. _setuptools: http://pypi.python.org/pypi/setuptools/
.. _buildout: http://pypi.python.org/pypi/zc.buildout/

What's Inside
-------------

In order to facilitate ordering of the galleries on display, there is a new 
`photologue` gallery with ordering support called ``OrderedGallery``. This model 
can be linked using a CMS plugin to display photos on your page.

The default rendering of the gallery plugin is an unordered list of images. This
can be overridden by placing a template in your project's template folder at 
``cms/plugins/phlog/gallery.html`` to override all rendering or at 
``cms/plugins/phloge/{{ placeholder }}-gallery.html`` to override the template 
for a single placeholder (by name).
