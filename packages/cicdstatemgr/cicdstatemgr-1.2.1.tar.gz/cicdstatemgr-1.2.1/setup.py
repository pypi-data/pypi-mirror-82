import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cicdstatemgr",
    version="1.2.1",
    author="bitsofinfo",
    author_email="bitsofinfo.g@gmail.com",
    description="State management utility for CICD systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bitsofinfo/cicdstatemgr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'jinja2',
        'pyyaml',
        'redis ',
        'jsonpath-ng', 
        'requests'
    ],
    entry_points = {
        "console_scripts": ['cicdstatemgr = cicdstatemgr.cli:main']
    },
    python_requires='>=3.8',
)