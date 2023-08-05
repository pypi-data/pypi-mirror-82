import codecs
import os
from setuptools import setup


name = 'cryptoyaml3'
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


LONG = (
    read("README.rst") + "\n\n" +
    "Release Information\n" +
    "===================\n\n" +
    read("CHANGES.rst") + "\n\n"
)


setup(
    name=name,
    version_format='{tag}',
    url='https://github.com/dflupu/cryptoyaml3.git',
    author='Senic GmbH',
    author_email='tom@senic.com',
    description='A python library to manage encrypted YAML files.',
    license='BSD 2-Clause License',
    long_description=LONG,
    classifiers=[
        "Programming Language :: Python",
    ],
    packages=[name],
    include_package_data=True,
    package_dir={name: 'cryptoyaml'},
    package_data={
        name: [
            '.coveragerc',
            'tests/*.py',
            'tests/data/*.*',
        ],
    },
    zip_safe=False,
    setup_requires=[
        'setuptools-git >= 0',
        'setuptools-git-version'
    ],
    install_requires=[
        'click',
        'PyYAML',
        'cryptography',
    ],
    extras_require={
        'development': [
            'devpi-client',
            'docutils',
            'pyflakes',
            'flake8',
            'mock',
            'pbr',
            'pdbpp',
            'pep8 < 1.6',
            'pytest',
            'pytest-cov',
            'pytest-flakes',
            'pytest-pep8',
            'pytest-sugar',
            'repoze.sphinx.autointerface',
            'setuptools-git',
            'Sphinx',
            'tox',
        ],
    },
    entry_points="""
        [console_scripts]
        cryptoyaml = cryptoyaml.commands:main
        [pytest11]
        cryptoyaml = cryptoyaml.testing
    """,
)
