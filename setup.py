# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.3.1'
short_description = u"Lineage Add-On: Child Site Local Registry"
long_description = u'\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
    open('LICENSE.rst').read(),
])


setup(
    name='lineage.registry',
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url=u'https://github.com/collective/lineage.registry',
    license='GNU General Public Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['lineage'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.lineage',
    ],
    extras_require={
        'test': [
            'collective.lineage [test]',
            'interlude',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
