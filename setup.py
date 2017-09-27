from distutils.core import setup

setup(
    name = "vglanguage",
    version = "0.0.1",
    author = "Jake Burga",
    author_email = "jrburga@mit.edu",
    description = ("A game engine wrapper"),
    license = "MIT",
    keywords = "game engine",
    url = "http://packages.python.org/vgengine",
    packages = ['vgparser', 'vgparser.grammar',],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)