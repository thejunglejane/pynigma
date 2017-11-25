from setuptools import setup

import versioneer


setup(
    name='pynigma',
    description='A Python client for the Enigma API.',
    version=versioneer.get_version(),
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
    url='https://github.com/thejunglejane/pynigma'
)
