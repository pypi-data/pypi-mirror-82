import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='StreamV',
    version="0.0.3",
    author="YanggeLiu",
    author_email="liu1251658965@outlook.com",
    description="Stream Capture with UDP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)