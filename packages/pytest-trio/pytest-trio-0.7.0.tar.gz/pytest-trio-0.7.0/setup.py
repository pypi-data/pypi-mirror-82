from setuptools import setup, find_packages

exec(open("pytest_trio/_version.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="pytest-trio",
    version=__version__,
    description="Pytest plugin for trio",
    url="https://github.com/python-trio/pytest-trio",
    long_description=open("README.rst").read(),
    author="Emmanuel Leblond",
    author_email="emmanuel.leblond@gmail.com",
    license="MIT -or- Apache License 2.0",
    packages=find_packages(),
    entry_points={'pytest11': ['trio = pytest_trio.plugin']},
    install_requires=[
        "trio >= 0.15.0",
        "async_generator >= 1.9",
        "outcome",
        # For node.get_closest_marker
        "pytest >= 3.6"
    ],
    keywords=[
        'async',
        'pytest',
        'testing',
        'trio',
    ],
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Testing",
        "Framework :: Hypothesis",
        "Framework :: Pytest",
        "Framework :: Trio",
    ],
)
