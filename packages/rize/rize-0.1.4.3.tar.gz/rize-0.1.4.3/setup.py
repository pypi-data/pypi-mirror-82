#from distutils.core import setup
from setuptools import setup

setup(
    name='rize',
    version='0.1.4.3',
    author='Enrique Coronado',
    author_email='enriquecoronadozu@gmail.mx',
    url='http://enriquecoronadozu.github.io',
    description='Robot Interface from Zero Experience Python Code',
    packages=["rize"],
    install_requires=['nep', 'sharo'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development"
    ]
)

