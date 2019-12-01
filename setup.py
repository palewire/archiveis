import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='archiveis',
    version='0.0.9',
    description='A simple Python wrapper for the archive.is capturing service',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Ben Welsh',
    author_email='ben.welsh@gmail.com',
    url='https://www.github.com/pastpages/archiveis/',
    packages=('archiveis',),
    include_package_data=True,
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'requests>=2.22.0',
        'click'
    ],
entry_points='''
        [console_scripts]
        archiveis=archiveis.api:cli
    ''',
)
