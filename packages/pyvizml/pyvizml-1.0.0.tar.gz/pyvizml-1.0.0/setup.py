import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvizml", # Replace with your own username
    version="1.0.0",
    author="Kuo, Yao-Jen",
    author_email="tonykuoyj@gmail.com",
    description="A package for my book: Machine Learning for Newbies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://yaojenkuo.io/ml-newbies/index.html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)