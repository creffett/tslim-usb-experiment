"""Setup."""


try:
    from setuptools import setup
except:  # pylint: disable=bare-except # noqa: E722 # NOLINT
    from distutils.core import setup  # pylint: disable=wrong-import-order

VERSION = 0.1.0

setup(
    author='Chris Reffett',
    name='tslim_usb',
    description='Experimental tool/library to get data from a Tandem t:slim X2 insulin pump.',
    version=VERSION,
    packages=['tslim_usb'],
    install_requires=['pyserial'],
    url='https://github.com/creffett/tslim-usb-experiment',
    classifiers=[
        "License :: OSI Approved :: MIT License ",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
)
