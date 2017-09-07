# pyxbincodec's setup.py
from setuptools import setup

DEPS = ["numpy"]
       
setup(
    name = "pyxbincodec",
    packages = ["pyxbincodec"],
    version = "0.1.0b0",
    description = "A PixBin file decoder for Python 3",
    author = "Jonathan Lurie",
    author_email = "lurie.jo@gmail.com",
    url = "https://github.com/Pixpipe/pyxbincodec",
    download_url = "https://github.com/Pixpipe/pyxbincodec/archive/master.zip",
    keywords = ["file", "decoding", "pixpipe"],
    #install_requires = DEPS,
    #setup_requires = DEPS,
    setup_requires = DEPS,
    install_requires = DEPS,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: only",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT license",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Packaging"
        ],
    )
