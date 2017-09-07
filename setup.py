# pyxbincodec's setup.py
from distutils.core import setup

VERSION = "0.1.0b"
DEPS = [
        "numpy",
       ]

setup(
    name = "pyxbincodec",
    packages = ["pyxbincodec"],
    version = VERSION,
    description = "A PixBin file decoder for Python 3",
    author = "Jonathan Lurie",
    author_email = "lurie.jo@gmail.com",
    url = "https://github.com/Pixpipe/pyxbincodec",
    download_url = "https://github.com/Pixpipe/pyxbincodec/archive/master.zip",
    keywords = ["file", "decoding", "pixpipe"],
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
    long_description = """\
Decodes PixBin files.
PixBin format is a generic binary format that can handle multiple modalities, named PixBlocks (or just blocks). In addition, a bin can carry:
- a description field
- a creation date
- a generic custom object (Python dictionary), called user object, to store whatever additional piece of information

Each block contain:
- a _metadata object
- a _data object

Each _data object can be:
- a numerical array: TypedArray in Javascript, Numpy array in Python, but they are really just low-level buffer
- a generic object (dictionary in Python, Object in Javascript)
- a list that contains both numerical arrays and generic objects

And the _metadata object is a Python dictionary.
"""
)
