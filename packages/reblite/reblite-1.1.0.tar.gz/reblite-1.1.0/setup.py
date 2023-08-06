import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reblite",
    version="1.1.0",
    author="Harsh Vardhan",
    author_email="vardhan.harsh4041@gmail.com",
    description="A simple SQLite wrapper built for personal use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4041RebL/sqlite-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)