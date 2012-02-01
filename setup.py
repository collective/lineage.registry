from setuptools import setup, find_packages
import sys, os

version = '1.0.1'
shortdesc ="Lineage AddOn: plone.app.registry for subsites"
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

setup(name='lineage.registry',
      version=version,
      description=shortdesc,
      long_description=longdesc,
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
      package_dir = {'': 'src'},
      namespace_packages=['lineage',],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.lineage',
      ],
      extras_require={
          'test': [
              'collective.lineage[test]',
          ],
      },      
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
