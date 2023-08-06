import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="music_metadata_edi",
    version="20.9b4",
    author="Matija Kolarić",
    author_email="matijakolaric@users.noreply.github.com",
    description="Music Metedata - EDI-based formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/musicmetadata/territories",
    packages=setuptools.find_namespace_packages(include=['music_metadata.*']),
    namespace_packages=['music_metadata'],
    package_data={
        '': ['CW19000*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
