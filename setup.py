# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='kgschart',
    version='0.3',
    description='KGS rank graph parser',
    author='Kota Mori', 
    author_email='kmori05@gmail.com',
    url='https://github.com/kota7/kgschart',
    
    packages=['kgschart'],
    install_requires=['pillow', 'numpy', 'scipy', 'pandas',  
                      'scikit-learn', 'matplotlib'],
    package_data={'kgschart': ['pretrained/prot2/*.pkl', 'pretrained/prot3/*.pkl', 
                               'pretrained/model-info.json',
                               'example/*.png']},
    entry_points={'console_scripts': 'kgschart=kgschart.commandline:main'},
    
    test_suite='tests'
)




