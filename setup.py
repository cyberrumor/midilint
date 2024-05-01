from setuptools import setup

setup(
    name="midilint",
    version="0.1",
    description="A midi normalizer, transposer, and note aligner.",
    author="cyberrumor",
    url="https://github.com/cyberrumor/midilint",
    packages=["midilint"],
    scripts=["bin/midilint"],
)
