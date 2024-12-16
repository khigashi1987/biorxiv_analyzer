from setuptools import setup, find_packages

setup(
    name="biorxiv-analyzer",
    version="0.1.0",
    description="A tool for analyzing bioRxiv preprints using their API",
    author="Koichi Higashi",
    author_email="khigashi@nig.ac.jp",
    url="https://github.com/khigashi1987/biorxiv_analyzer",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
