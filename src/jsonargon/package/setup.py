from setuptools import setup, find_packages
import os


# Function to retrieve resources files
def _get_resources(package_name):
    # Get all the resources (also on nested levels)
    res_paths = os.path.join(package_name, "resources")
    all_resources = [os.path.join(folder, file) for folder, _, files in os.walk(res_paths) for file in files]
    # Remove the prefix: start just from "resources"
    return [resource[resource.index("resources"):] for resource in all_resources]


# Read requirements
requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = f.read().splitlines()


# Package configuration
name = "jsonargon"
setup(
    name=name,
    version="0.0.0",
    packages=find_packages(),
    package_data={name: _get_resources(name), "tests": ["stubs/*"]},
    install_requires=requirements,

    description="Serialization and deserialization of JSON objects from/into Python objects (with validation and remapping capabilities)",
    url="https://gitlab.com/federico_pugliese/jsonargon",
    author="Federico Pugliese",
    license="Apache Software License, Version 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha"
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ]
)
