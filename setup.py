import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SciDataTool",
    version="1.3.6",
    author="Helene Toubin",
    author_email="helene.toubin@eomys.com",
    description="Scientific Data Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eomys/SciDataTool",
    download_url="https://github.com/Eomys/SciDataTool/archive/1.3.6.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
    install_requires=["numpy", "scipy", "matplotlib"],
)
