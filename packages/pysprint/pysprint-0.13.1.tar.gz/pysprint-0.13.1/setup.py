import sys

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

import versioneer

setup(
    name="pysprint",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Péter Leéh",
    author_email="leeh123peter@gmail.com",
    description="Spectrally refined interferometry for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ptrskay3/PySprint",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=["numpy>=1.16.6", "scipy", "matplotlib", "pandas", "Jinja2"],
    extras_require={"optional": ["numba", "lmfit", "pytest", "dask"]},
    entry_points={
        'console_scripts': [
            'pysprint = pysprint.templates.build:main',
        ],
    }
)
