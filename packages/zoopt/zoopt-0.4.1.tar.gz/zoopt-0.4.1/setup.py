#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zoopt',
    version='0.4.1',
    description=(
        'A Python Package for Zeroth-Order Optimization'
    ),
    author='Yang Yu',
    author_email='yuy@nju.edu.cn',
    maintainer='Yu-Ren Liu, Xiong-Hui Chen, Yi-Qi Hu, Chao Feng, Yang Yu',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/polixir/ZOOpt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'numpy',
        'matplotlib',
    ]
)
