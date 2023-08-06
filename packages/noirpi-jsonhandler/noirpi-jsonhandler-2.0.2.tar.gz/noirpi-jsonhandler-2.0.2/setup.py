import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noirpi-jsonhandler",  # Replace with your own username
    version="2.0.2",
    author="NoirPi",
    author_email="noirpi@noircoding.de",
    description="A small json Filehandler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noirpi/json-filehandler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
    ],
    python_requires='>=3.6',
)
