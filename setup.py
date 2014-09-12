import os
from setuptools import (
    find_packages,
    setup,
)

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-financial-transactions',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A Django app to import and categorise financial '
                'transactions.',
    long_description=README,
    url='http://github.com/absoludity/django-financial-transactions',
    author='Michael Nelson',
    author_email='absoludity@gmail.com',
    install_requires=[
        'django-categories >= 1.1.4',
        'south >= 0.7.6',
        'ofxparse >= 0.14',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
