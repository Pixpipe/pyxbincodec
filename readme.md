# PyxBinCodec
Notice: For the moment, just the decoder is available.  

This project is a Python version [PixBinCodec](https://github.com/Pixpipe/pixbincodec) (originaly in Javascript). To know more about this format [here is an in-depth description](https://github.com/Pixpipe/pixbincodec/blob/master/pixbinformat.md).  

# How to use
## Reading a file
To decode a PixBin file in Python, this file must be read as a binary stream:
```python
# A path to a local file
filePath = "data/testFile_uncomp.pixb"

with open(filePath, mode='rb') as file: # b is important -> binary
      # buff stores the file content as a 'bytes' object,
      # in other word: a generic buffer
      buff = file.read()
```

## Decoding
First, we need to import PyxBinCodec:
```python
import PixBinDecoder
```

Once the `buff` is ready, it can be decoded:
```python
# create a decoder instance
pixBinDecoder = PixBinDecoder.PixBinDecoder()

# feed it with the buffer
pixBinDecoder.setInput( buff )

# make sure the input is compatible before you go further
if( not pixBinDecoder.isValid() ):
  print("The file is not valid")
  exit()
```
