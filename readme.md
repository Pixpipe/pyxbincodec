# PyxBinCodec
Notice: For the moment, just the decoder is available.  

This project is a Python version [PixBinCodec](https://github.com/Pixpipe/pixbincodec) (originaly in Javascript). To know more about this format [here is an in-depth description](https://github.com/Pixpipe/pixbincodec/blob/master/pixbinformat.md).  

## TL;DR
PixBin format is a generic binary format that can handle multiple modalities, named *PixBlocks* (or just *blocks*). In addition, a *bin* can carry:
- a description field
- a creation date
- a generic custom object (Python *dictionary*), called *user object*, to store whatever additional piece of information

Each block contain:
- a `_metadata` object
- a `_data` object

Each `_data` object can be:
- a numerical array: TypedArray in Javascript, Numpy array in Python, but they are really just low-level buffer
- a generic object (*dictionary* in Python, *Object* in Javascript)
- a list that contains both numerical arrays and generic objects

And the `_metadata` object is a Python *dictionary*.

# Install
[not yet on pip]  
Still, you can install a local copy as a link in your `site-packages` (dev mode).

```bash
$ git clone https://github.com/Pixpipe/pyxbincodec.git
$ cd pyxbincodec
# install a dev link
$ pip3 install -e .
```

# How to use
The following is sort of a step-by-step tut, but you can find it all in this [example](example/test.py).

## Reading a PixBin file
To decode a PixBin file in Python, this file must be read as a binary stream:
```python
# A path to a local file
filePath = "data/testFile_uncomp.pixb"

with open(filePath, mode='rb') as file: # b is important -> binary
  # buff stores the file content as a 'bytes' object,
  # in other word: a generic buffer
  buff = file.read()
```
We decided to let the user deal with the file opening for two reasons:
1. To ne consistant with the Javascript library
2. Because the binary buffer may come from a diferent source (http request, internal buffer that was never written on disc, etc.)

## Decoding
First, we need to import the module `pyxbincodec`:
```python
import pyxbincodec
```

Once the `buff` is ready, it can be decoded:
```python
# create a decoder instance
pixBinDecoder = pyxbincodec.PixBinDecoder()

# optional: enable block checksum control
pixBinDecoder.enableBlockVerification( True )

# feed it with the buffer
pixBinDecoder.setInput( buff )

# make sure the input is compatible before you go further
if( not pixBinDecoder.isValid() ):
  print("The file is not valid")
  exit()
```

Then, you can access the data inside the PixBin file using simple methods:

```python
# Get the number of blocks encoded in the file (integer)
nbBlocks = pixBinDecoder.getNumberOfBlocks()

# Get the date when the PixBin file was created (String)
dateCreation = pixBinDecoder.getBinCreationDate()

# Get the description associated with the PixBin file (String of None)
binDescription = pixBinDecoder.getBinDescription()

# Get the user object
usrObj = pixBinDecoder.getBinUserObject()
```

Now it's time to fetch each block's data and metadata:

```python
# For each block in the Bin
for i in range(0, nbBlocks):
  print("\n-------------------- BLOCK " + str(i) + " ----------")
  
  # Get the description of this block (if any, None otherwise)
  print( pixBinDecoder.getBlockDescription(i) )
  
  # Get the original object type that this block encoded (see next section)
  # accessible without having to fetch the block
  print( pixBinDecoder.getBlockType(i) )
  
  # Get the block itself, containing _data and _metadata 
  block = pixBinDecoder.fetchBlock(i, )
  
  # if checksum control is enabled, and if the sums do not match
  # None will be returned instead of a block
  if( block is None ):
    print("Invalid block")
    continue
  
  # Original object type, same as pixBinDecoder.getBlockType(i),
  # but from the block rather that from the bin
  print( block["originalBlockType"] )
  
  # Get the block _metadata object (Python dictionary)
  blockMeta = block["_metadata"]
  
  # get the block _data object (a Numpy Array or a list of Numpy array or a dictionary)
  blockData = block["_data"]
```

# A word about block types
The PixBin file format was originally created to handle [Pixpipe](https://github.com/Pixpipe/pixpipejs) internal data types. They can be very diverse, spatial, time series, vectorial, frequential, etc. the need for a generic format was obvious. To make sure what kind of data was originally encoded as a *block*, we decided to keep a field named `originalBlockType`, still, it is to the discretion of the user of this library to interpret the data.  

If the block comes from Pixpipe, the `originalBlockType` will probably be one of the following:
- `Image2D`
- `Image3D`
- `MniVolume`
- `Signal1D`
- `LineString`

Still, it is possible that it is simple `Object`.

# License
MIT
