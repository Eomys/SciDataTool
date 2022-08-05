import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as file:
    requirements = file.readlines()
    install_requires = "".join(
        requirements
    ).splitlines()  # remove endline in each element

setuptools.setup(
    name="SciDataTool",
    version="2.5.0",
    author="Helene Toubin",
    author_email="helene.toubin@eomys.com",
    description="Scientific Data Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eomys/SciDataTool",
    download_url="https://github.com/Eomys/SciDataTool/archive/2.5.0.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
)
