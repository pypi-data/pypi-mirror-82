#!/usr/bin/python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
deps = ['matplotlib', 'multiprocess', 'scipy', 'numpy', 'matplotlib', 'pandas', 'pathos', 'PyYAML', 'Shapely']

setuptools.setup(
    name="neutpy",
    version="0.0.3",
    author="Maxwell D. Hill, Jonathan J. Roveto",
    install_requires=deps,
    author_email="max.hill@pm.me, veto1024@gmail.com",
    description="NeutPy - A neutrals code for tokamak fusion reactors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gt-frc/neutpy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires='>=2.7',
)

if __name__ == '__main__':
    print "Test"
    pass
