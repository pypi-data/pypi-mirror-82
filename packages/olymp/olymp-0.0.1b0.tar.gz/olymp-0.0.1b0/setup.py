"""Olympus
"""

from setuptools import setup
from setuptools import find_packages

import versioneer


def readme():
    with open("README.md") as f:
        return f.read()


# taken from https://hanxiao.io/2019/11/07/A-Better-Practice-for-Managing-extras-require-Dependencies-in-Python/
def get_extra_requires(path, add_all=True):
    import re
    from collections import defaultdict

    with open(path) as content:
        extra_deps = defaultdict(set)
        for entry in content:
            if entry.strip() and not entry.startswith("#"):
                tags = set()
                if ":" in entry:
                    package, tag_list = entry.split(":")
                    tags.update(tag_entry.strip() for tag_entry in tag_list.split(","))
                tags.add(re.split("[<=>]", package)[0])
                for tag in tags:
                    extra_deps[tag].add(package)

        if add_all:
            extra_deps["all"] = set(vv for v in extra_deps.values() for vv in v)
    return extra_deps


# -----
# Setup
# -----
setup(
    name="olymp",
    version="0.0.1b0",  #versioneer.get_version(),
#    cmdclass=versioneer.get_cmdclass(),
    description="Benchmarking framework for noisy optimization and experiment planning",
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    url="https://github.com/aspuru-guzik-group/olympus",
    author="Florian Hase, Matteo Aldeghi, Riley Hickman",
    packages=find_packages('./src'),
    package_dir={"": "src"},
    package_data={"": ["datasets/*"]},
    include_package_data=True,
    zip_safe=False,
    tests_require=["pytest"],
    install_requires=["numpy", "pandas"],
    python_requires=">=3.6",
    extras_require=get_extra_requires("extra_requirements.txt"),
    entry_points={"console_scripts": ["olympus = olympus.cli.main:entry_point"]},
)
