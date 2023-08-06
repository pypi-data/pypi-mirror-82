from setuptools import setup
import os

VERSION = "1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="healthkit-to-sqlite",
    description="Convert an Apple Healthkit export zip to a SQLite database",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/dogsheep/healthkit-to-sqlite",
    project_urls={
        "Issues": "https://github.com/dogsheep/healthkit-to-sqlite/issues",
        "CI": "https://github.com/dogsheep/healthkit-to-sqlite/actions",
        "Changelog": "https://github.com/dogsheep/healthkit-to-sqlite/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["healthkit_to_sqlite"],
    entry_points="""
        [console_scripts]
        healthkit-to-sqlite=healthkit_to_sqlite.cli:cli
    """,
    install_requires=["sqlite-utils>=2.4.4"],
    extras_require={"test": ["pytest"]},
    tests_require=["healthkit-to-sqlite[test]"],
)
