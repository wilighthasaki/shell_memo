from setuptools import setup, find_packages
import sys


setup(
    name = "memo",
    version = "1.0",
    keywords = ("memo"),
    description = "A shell memo tool",
    long_description = "A shell memo tool",
    license = "MIT Licence",

    url = "None",
    author = "wilight",
    author_email = "wilighthasaki@gmail.com",

    packages = ["src"],
    platforms = "any",
    install_requires = ["npyscreen"],
    data_files={sys.prefix: ["data/*", "src/memo.conf"]},

    scripts = [],
    entry_points = {
        'console_scripts': [
            'memo = src.run_memo:main'
        ]
    }
)
