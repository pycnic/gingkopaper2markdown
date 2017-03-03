# coding: utf-8

from setuptools import setup

setup(
    name='gingkopaper2markdown',
    version='0.1',
    py_modules=['gingkopaper2markdown'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        gingkopaper2markdown=gingkopaper2markdown:gingkopaper2markdown_cli
    ''',
)
