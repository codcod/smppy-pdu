from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    name='smpppdu',
    version=version,
    author='Roger Hoover',
    author_email='roger.hoover@gmail.com',
    description='Library for parsing Protocol Data Units (PDUs) in SMPP protocol',
    license='Apache License 2.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='smpp pdu',
    url='https://github.com/devtud/smpppdu',
    python_requires='>=3.7, <4',
    include_package_data=True,
    package_data={'smpppdu': ['README.markdown']},
    zip_safe=False,
    test_suite='smpppdu.tests',
    project_urls={
        'Source': 'https://github.com/devtud/smpppdu',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: System :: Networking',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
