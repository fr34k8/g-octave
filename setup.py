#!/usr/bin/env python

import warnings
warnings.filterwarnings('ignore')

from distutils.core import setup
from distutils.command.sdist import sdist as _sdist
from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean

import os

import g_octave

current_dir = os.path.dirname(os.path.realpath(__file__))

def bdoc():
    
    from codecs import open
    from StringIO import StringIO
    from datetime import date
    
    try:
        from docutils import core
    except ImportError:
        pass
    
    # creating the man-page
    print 'building the manpage'
    
    path_rst = os.path.join(current_dir, 'g-octave.1.rst')
    path = os.path.join(current_dir, 'g-octave.1')
    
    man_rst = open(path_rst, 'r', encoding='utf-8')
    manpage = man_rst.read()
    man_rst.close()
    
    man_tmp = StringIO(manpage % {
        'author_email': g_octave.__email__,
        'date': date(2009, 12, 28).strftime('%Y-%m-%d'),
        'copyright': g_octave.__author__,
        'version': g_octave.__version__,
    })
    
    man = open(path, 'w', encoding='utf-8')
    
    try:
        core.publish_file(
            source = man_tmp,
            source_path = path_rst,
            destination = man,
            destination_path = path,
            writer_name='manpage',
        )
        man_tmp.close()
        man.close()
    except:
        raise RuntimeError('Failed to build the manpage')
    
    # creating the README.html
    print 'building the html doc'
    
    path_rst = os.path.join(current_dir, 'README.rst')
    path = os.path.join(current_dir, 'g-octave.html')
    
    readme_rst =  open(path_rst, 'r', encoding='utf-8')
    readme = open(path, 'w', encoding='utf-8')
    
    try:
        core.publish_file(
            source = readme_rst,
            source_path = path_rst,
            destination = readme,
            destination_path = path,
            writer_name='html',
        )
        readme_rst.close()
        readme.close()
    except:
        raise RuntimeError('Failed to build the html doc')


class sdist(_sdist):
    
    def run(self):
        bdoc()
        _sdist.run(self)


class build(_build):
    
    def run(self):
        _build.run(self)
        for i in ['g-octave.1', 'g-octave.html']:
            if os.path.exists(os.path.join(current_dir, i)):
                return
        bdoc()


class clean(_clean):
    
    def run(self):
        _clean.run(self)
        if self.all:
            for i in ['g-octave.1', 'g-octave.html']:
                my_path = os.path.join(current_dir, i)
                if os.path.exists(my_path):
                    print 'removing %s' % my_path
                    os.remove(my_path)


setup(
    name='g-octave',
    version = g_octave.__version__,
    license = g_octave.__license__,
    description = g_octave.__description__,
    long_description = open('README.rst').read(),
    author = g_octave.__author__,
    author_email = g_octave.__email__,
    url = g_octave.__url__,
    packages = ['g_octave'],
    scripts = ['scripts/g-octave'],
    data_files = [('/etc', ['etc/g-octave.cfg'])],
    requires = ['portage'],
    cmdclass = {
        'sdist': sdist,
        'build': build,
        'clean': clean,
    }
)
