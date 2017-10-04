from setuptools import setup

from pynigma import __version__


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pynigma',
    packages=['pynigma', 'tests'],
    version=__version__,
    install_requires=['requests', 'mock'],
    description='A Python client for the Enigma API.',
    author='Jane Stewart Adams',
    author_email='jane@thejunglejane.com',
    license='MIT',
    url='https://github.com/thejunglejane/pynigma',
    download_url='https://github.com/thejunglejane/pynigma/tarball/{v}'.format(
        v=__version__)
)
