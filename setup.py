from setuptools import setup, find_namespace_packages

setup(
    name="brainframe-api",
    version="0.26.0",
    description="Provides a Python wrapper around the BrainFrame REST API.",
    long_description=open("README.rst").read(),
    author="Aotu",
    packages=find_namespace_packages(
        include=["brainframe.api*"]
    ),
    install_requires=[
        "requests==2.*",
        "pillow==6.*",
        "numpy==1.*",
    ],
)
