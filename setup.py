import pathlib

import pkg_resources
from setuptools import find_packages, setup


PWD = pathlib.Path(__file__).parent.absolute()


with open(PWD / "requirements.txt") as fp:
    install_requires = [
        req.name for req in pkg_resources.parse_requirements(fp)  # type: ignore
    ]


setup(
    name="vitiplace-client",
    version="0.1",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "vitiplace-client = vitiplace_client.cli:main",
        ],
    },
)
