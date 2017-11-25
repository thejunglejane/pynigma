from setuptools import setup

import versioneer

_version = versioneer.get_version()


setup(
    name='pynigma',
    description='A Python client for the Enigma API.',
    version=_version,
    cmdclass=versioneer.get_cmdclass(),
    packages=[
        'pynigma'
    ],
    test_suite='tests',
    setup_requires=[
        'coverage',
        'Sphinx',
        'sphinx_rtd_theme'
    ],
    install_requires=[
        'requests'
    ],
    author='Jane Stewart Adams',
    author_email='jane@thejunglejane.com',
    license='MIT',
    url='https://github.com/thejunglejane/pynigma',
    download_url = 'https://github.com/thejunglejane/pynigma/archive/{}.tar.gz'.format(_version)
)
