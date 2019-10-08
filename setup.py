from setuptools import setup, find_packages
import sys
import os

if not os.path.exists(os.path.join(sys.prefix, 'memo')):
    os.mkdir(os.path.join(sys.prefix, 'memo'))
if not os.path.exists(os.path.join(sys.prefix, 'memo', 'data')):
    os.mkdir(os.path.join(sys.prefix, 'memo', 'data'))
if not os.path.exists(os.path.join(sys.prefix, 'memo', 'data', 'local')):
    os.mkdir(os.path.join(sys.prefix, 'memo', 'data', 'local'))


setup(
    name = "memo",
    version = "1.0",
    keywords = ("memo"),
    description = "A shell memo tool",
    long_description = "A shell memo tool",
    license = "MIT Licence",
    zip_safe = False,

    url = "None",
    author = "Wilight",
    author_email = "wilighthasaki@gmail.com",

    packages = ["memo"],
    platforms = "any",
    install_requires = ["npyscreen"],
    data_files=[(os.path.join(sys.prefix, 'memo', 'data'), ["memo/memo.conf"])],

    scripts = [],
    entry_points = {
        'console_scripts': [
            'memo=memo.run_memo:main'
        ]
    }
)
