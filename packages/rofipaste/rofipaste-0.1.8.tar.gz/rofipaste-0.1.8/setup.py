#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'click_config_file>=0.6.0', 'pyxdg>=0.26']

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest>=3',
]

setup(
    author="Tom GOUVILLE",
    author_email='tom.gouville@telecomnancy.net',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A tool to paste some useful things",
    entry_points={
        'console_scripts': [
            'rofipaste=rofipaste.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='rofipaste',
    name='rofipaste',
    packages=find_packages(include=['rofipaste', 'rofipaste.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Any0ne22/rofipaste',
    version='0.1.8',
    zip_safe=False,
)
