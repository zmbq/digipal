#
# PLEASE IGNORED THIS FILE
# TODO: bring it up to date and test
#
from setuptools import setup, find_packages
import os
import digipal

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Researchers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    "Programming Language :: Python :: 2.7",
]

SCRIPTS = [
    'start-archetype-personal=personal.scripts:run_server',
    'print-archetype-directories=personal.scripts:print_directories'
]

REQUIREMENTS = [
    'Django==1.8.18',
    'django-contrib-comments<1.9.0',  # Fix derived Mezzanine requirement
    'Mezzanine==4.2.3',
    'grappelli-safe==0.4.6',  # Replace buggy template on Mezzanine
    'Pillow==6.0.0',
    'Digital-Lightbox@https://github.com/geoffroy-noel-ddh/Digital-Lightbox/archive/6775f5d6b329b4b903c20040b8b433fc905585d2.zip',
    'django-iipimage@https://github.com/geoffroy-noel-ddh/django-iipimage/archive/d927997207402abc5525add1c5c907819229c0bb.zip',
    'django-pagination@https://github.com/geoffroy-noel-ddh/django-pagination/archive/bd35668b35168eaaec9fbc374b69044404bea298.zip',
    'django-reversion==1.8.7',
    'django-tinymce==2.6.0',
    'django-compressor==1.5',
    'django-sendfile==0.3.11',
    'lxml==3.4.0',
    'Whoosh==2.7.3',
    'regex==2019.5.25',
    'gunicorn==19.9.0',
    'waitress==1.3.0',
]

setup(
    author="Peter Stokes",
    name='archetype-personal',
    version=digipal.__version__,
    description='Digital Resource and Database of Palaeography, Manuscript Studies and Diplomatic',
    long_description=open(os.path.join(
        os.path.dirname(__file__), 'README.md')).read(),
    url='https://archetype.ink',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    tests_require=[
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={ 'console_scripts': SCRIPTS },
)
