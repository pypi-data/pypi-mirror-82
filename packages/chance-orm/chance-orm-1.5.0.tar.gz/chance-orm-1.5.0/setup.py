#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: setup.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.10.2017
from setuptools import find_packages, setup


setup(
    name='chance-orm',
    version='1.5.0',
    description='The orm for chancefocus',
    url='https://gitee.com/QianFuFinancial/orm_sqlalchemy.git',
    author='Jimin Huang',
    author_email='huangjimin@whu.edu.cn',
    license='MIT',
    packages=find_packages(exclude='tests'),
    install_requires=[
        'nose>=1.3.7',
        'coverage>=4.1',
        'SQLAlchemy>=1.0.13',
        'chance-mock-logger>=0.0.2',
        'flake8>=3.3.0',
        'arrow>=0.12.0',
        'mock>=2.0.0',
        'rethinkdb>=2.3.0.post6',
        'inflection>=0.3.1',
        'influxdb>=5.2.0'
    ],
    zip_safe=False,
)
