from pathlib import Path

import setuptools

readme = Path("README.md")
long_description = readme.read_text()

setuptools.setup(
    name="manga-dlp",
    version="2.0.3",
    author="Ivan Schaller",
    author_email="ivan@schaller.sh",
    description="A cli manga downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olofvndrhr/manga-dlp",
    project_urls={
        "Bug Tracker": "https://github.com/olofvndrhr/manga-dlp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "mangadlp"},
    packages=setuptools.find_packages(where="mangadlp"),
    py_modules=["manga-dlp"],
    python_requires=">=3.6",
)
