# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='kgschart',
    version='0.1',
    description='KGS rank graph parser',
    author='Kota Mori', 
    author_email='kmori05@gmail.com',
    
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'scikit-learn>=0.18.0', 'matplotlib', 'pillows'],
    package_data={'kgschart': ['models/*.pkl']}
)




