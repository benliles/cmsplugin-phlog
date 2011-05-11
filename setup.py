from os.path import dirname, join

from setuptools import setup, find_packages



version = '0.1'

setup(
    name = 'cmsplugin-phlog',
    version = version,
    description = "Django CMS Plugin for Photologue galleries",
    long_description = open(join(dirname(__file__), 'README')).read() + "\n" + 
                       open(join(dirname(__file__), 'HISTORY')).read(),
    classifiers = [
        "Framework :: Django",
        "Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules"],
    keywords = 'django cms plugin photologue',
    author = 'Benjamin Liles',
    author_email = 'ben@ltwebdev.com',
    url = 'https://github.com/benliles/cmsplugin-phlog',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'django-photologue>=2.3',
        'django-cms>=2.1.0',],
)