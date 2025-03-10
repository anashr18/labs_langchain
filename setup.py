"""Set up the package."""

from pathlib import Path

from setuptools import find_packages, setup

with open(Path(__file__).absolute().parents[0] / "labs_langchain" / "VERSION") as _f:
    __version__ = _f.read().strip()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="labs-langchain",  # Change this to avoid conflicts
    version=__version__,
    packages=find_packages(),  # Automatically finds the renamed folder
    description="Custom experimental version of Langchain for LLM applications",
    install_requires=["pydantic"],
    long_description=long_description,
    license="MIT",
    url="https://github.com/anashr18/labs_langchain",
    include_package_data=True,
    long_description_content_type="text/markdown",
)
