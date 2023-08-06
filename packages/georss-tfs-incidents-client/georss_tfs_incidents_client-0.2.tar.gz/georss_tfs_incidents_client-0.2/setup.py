from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = [
    'georss_client>=0.8',
]

setup(
    name="georss_tfs_incidents_client",
    version="0.2",
    author="Malte Franken",
    author_email="coding@subspace.de",
    description="A GeoRSS client library for the Tasmania Fire Service Incidents feed.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exxamalte/python-georss-tfs-incidents-client",
    packages=find_packages(exclude=("tests*",)),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRES
)
