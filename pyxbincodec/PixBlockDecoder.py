import zlib
import numpy as np
#import CodecUtils
from pyxbincodec import CodecUtils

class PixBlockDecoder:

    def __init__(self):
        print()

    def reset(self):
        self._input = None
        self._output = {}
        
        
    def setInput(self, buff):
        self.reset()
        if( type(buff) is not bytes ):
            print("Input should be a valid ArrayBuffer")
            return;
        self._input = buff;
        
        
    def getOutput(self):
        return self._output;


    def _getDataTypeFromByteStreamInfo(self, bsi ):
        # default object is a simple dictionary, but in this case,
        # the returned value of this method will not be used
        dataType = None;

        if( bsi["type"] == "int" ):
            #dataType = bsi.signed ? "uint" : "int";
            dataType = "uint" if bsi["signed"] else "int"
            dataType += str(bsi["bytesPerElements"] * 8);

        elif( bsi["type"] == "float" ):
            dataType = "float";
            dataType += str(bsi["bytesPerElements"] * 8);
        
        return ( dataType )
  

    def run(self):
        inputData = self._input;
        readingByteOffset = 0;

        # primer, part 1
        # get the endianess used to encode the file
        isLittleEndian = CodecUtils.getUint8(inputData, 0)
        readingByteOffset += 1

        # primer, part 2
        # get the length of the string buffer (unicode json) that follows
        pixBlockHeaderBufferByteLength = CodecUtils.getUint32(inputData, 1)
        readingByteOffset += 4;

        #get the string buffer
        #pixBlockHeaderBuffer = inputData.slice( readingByteOffset, readingByteOffset + pixBlockHeaderBufferByteLength )
        #pixBlockHeader = CodecUtils.ArrayBufferToObject( pixBlockHeaderBuffer );
        pixBlockHeader = CodecUtils.buffToDict(inputData, readingByteOffset, pixBlockHeaderBufferByteLength)
        readingByteOffset += pixBlockHeaderBufferByteLength;

        # fetching the metadata
        #metadataBuffer = inputData.slice( readingByteOffset, readingByteOffset + pixBlockHeader.metadataByteLength );
        #metadataObject = CodecUtils.ArrayBufferToObject( metadataBuffer );
        metadataObject = CodecUtils.buffToDict(inputData, readingByteOffset, pixBlockHeader["metadataByteLength"])
        readingByteOffset += pixBlockHeader["metadataByteLength"];

        # the data streams are the byte streams when they are converted back to actual typedArrays/Objects
        dataStreams = []

        #for(var i=0; i<pixBlockHeader.byteStreamInfo.length; i++){
        for i in range(0, len(pixBlockHeader["byteStreamInfo"])):
            # act as a flag: if not null, it means data were compressed
            compressedByteLength = pixBlockHeader["byteStreamInfo"][i]["compressedByteLength"]

            # the dtype used at the construction of a numpy array
            streamDtype = self._getDataTypeFromByteStreamInfo( pixBlockHeader["byteStreamInfo"][i] )
            dt = np.dtype(streamDtype)
            dt = dt.newbyteorder("<" if isLittleEndian else ">")
          
            # know if it's a typed array or a complex object
            isTypedArray = pixBlockHeader["byteStreamInfo"][i]["isTypedArray"]

            # meaning, the stream is compresed
            if( compressedByteLength ):
                # fetch the compresed dataStream
                #compressedByteStream = new Uint8Array( inputData, readingByteOffset, compressedByteLength );
                compressedByteStream = inputData[readingByteOffset : readingByteOffset+compressedByteLength]
                # inflate the dataStream
                #inflatedByteStream = pako.inflate( compressedByteStream );
                inflatedByteStream = zlib.decompress( compressedByteStream )
                dataStream = None;
                
                if( isTypedArray ):
                    #dataStream = new streamDtype( inflatedByteStream.buffer );
                    dataStream = np.frombuffer(inflatedByteStream, dtype=dt)
                else:
                    dataStream = CodecUtils.buffToDict( inflatedByteStream  )

                dataStreams.append( dataStream )
                readingByteOffset += compressedByteLength

            # the stream were NOT compressed
            else:
                dataStream = None
                dataStreamBuffer = inputData[readingByteOffset : readingByteOffset + pixBlockHeader["byteStreamInfo"][i]["byteLength"] ]
                
                
                if( isTypedArray ):
                    dataStream = np.frombuffer(dataStreamBuffer, dtype=dt)
                else:
                    dataStream = CodecUtils.buffToDict( dataStreamBuffer );

                dataStreams.append( dataStream )
                readingByteOffset += pixBlockHeader["byteStreamInfo"][i]["byteLength"];
              
            # If data is a single typed array (= not composed of a subset)
            # we get rid of the useless wrapping array
            outputDataStream = None
            if( len(dataStreams) == 1):
                outputDataStream = dataStreams[0]
            else:
                outputDataStream = dataStreams
        
            self._output["originalBlockType"] = pixBlockHeader["originalBlockType"]
            self._output["_data"] = outputDataStream
            self._output["_metadata"] = metadataObject

  
