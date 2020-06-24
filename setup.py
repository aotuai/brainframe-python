from setuptools import setup, find_namespace_packages

setup(
    name="brainframe-api",
    description="Provides a Python wrapper around the BrainFrame REST API.",
    long_description=open("README.rst").read(),
    author="Aotu",
    url="https://github.com/aotuai/brainframe_python",
    license="BSD-3-Clause",

    setup_requires=[
        "setuptools_scm",
    ],
    use_scm_version={
        # We want to be able to push these releases to PyPI, which doesn't
        # support local versions. Local versions are anything after the "+" in
        # a version string like "0.26.0.dev16+cooltext".
        "local_scheme": "no-local-version",
    },

    packages=find_namespace_packages(
        include=["brainframe.api*"]
    ),

    install_requires=[
        "requests==2.*",
        "pillow==6.*",
        "numpy==1.*",
        "dataclasses==0.*",
    ],
)
