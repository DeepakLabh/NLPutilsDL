from distutils.core import setup

setup(
    # Application name:
    name="utils",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Deepak Labh",
    author_email="labh111349@gmail.com",

    # Packages
    packages=["utils"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="not yet available",

    #
    # license="LICENSE.txt",
    description="basic utility tools for NLP",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "numpy",
        "json",
    ],
)
