import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="manga-dlp-olofvndrhr",
    version="0.0.1",
    author="Ivan Schaller",
    author_email="ivan@schaller.sh",
    description="A manga downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olofvndrhr/manga-dlp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)