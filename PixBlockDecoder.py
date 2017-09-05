import zlib
import CodecUtils

class PixBlockDecoder:

    def __init__(self):
        print()

    def reset(self):
        self._input = None
        self._output = None
        
        
    def setInput(self, buff):
        if( type(buff) is not bytes ):
            print("Input should be a valid ArrayBuffer")
            return;
        self._input = buff;
        
        
    def getOutput(self):
        return self._output;


    def _getDataTypeFromByteStreamInfo(self, bsi ):
        # default object is a simple dictionary
        dataType = dict;

        if( bsi.type === "int" ):
            dataType = bsi.signed ? "uint" : "int";
            dataType += bsi.bytesPerElements*8;

        else if( bsi.type === "float" ):
            dataType = "float";
            dataType += bsi.bytesPerElements*8;
        
        return ( dataType )
  



        def run(self):

            inputData = this._input;
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
            pixBlockHeader = CodecUtils.buffToDict(readingByteOffset, pixBlockHeaderBufferByteLength)
            readingByteOffset += pixBlockHeaderBufferByteLength;

            # fetching the metadata
            #metadataBuffer = inputData.slice( readingByteOffset, readingByteOffset + pixBlockHeader.metadataByteLength );
            #metadataObject = CodecUtils.ArrayBufferToObject( metadataBuffer );
            metadataObject = CodecUtils.buffToDict(readingByteOffset, pixBlockHeader["metadataByteLength"])
            readingByteOffset += pixBlockHeader.metadataByteLength;

            # the data streams are the byte streams when they are converted back to actual typedArrays/Objects
            dataStreams = []

            #for(var i=0; i<pixBlockHeader.byteStreamInfo.length; i++){
            for i in range(0, len(pixBlockHeader["byteStreamInfo"])):
              # act as a flag: if not null, it means data were compressed
              compressedByteLength = pixBlockHeader["byteStreamInfo"][i]["compressedByteLength"]

              # the dtype used at the construction of a numpy array
              streamDtype = self._getDataTypeFromByteStreamInfo( pixBlockHeader["byteStreamInfo"][i] )

              # know if it's a typed array or a complex object
              isTypedArray = pixBlockHeader["byteStreamInfo"][i]["isTypedArray"]

              # meaning, the stream is compresed
              if( compressedByteLength ){
                print("The stream is compressed")
              
                # fetch the compresed dataStream
                #compressedByteStream = new Uint8Array( inputData, readingByteOffset, compressedByteLength );
                compressedByteStream = inputData[readingByteOffset : readingByteOffset+compressedByteLength]
                
                # inflate the dataStream
                #inflatedByteStream = pako.inflate( compressedByteStream );
                inflatedByteStream = zlib.decompress( compressedByteStream )

                dataStream = None;
                
                # if( streamDtype === Object){
                #   dataStream = CodecUtils.ArrayBufferToObject( inflatedByteStream.buffer  );
                # }else{
                #   dataStream = new streamDtype( inflatedByteStream.buffer );
                # }
                
                if( isTypedArray ){
                  #dataStream = new streamDtype( inflatedByteStream.buffer );
                  dt = np.dtype(streamDtype)
                  dt = dt.newbyteorder("<" if isLittleEndian else ">")
                  dataStream = numpy.frombuffer(inflatedByteStream, dtype=dt)       # TODO continue from here
                }else{
                  dataStream = CodecUtils.ArrayBufferToObject( inflatedByteStream.buffer  );
                }

                dataStreams.push( dataStream )
                readingByteOffset += compressedByteLength;

              }
              # the stream were NOT compressed
              else{
                dataStream = null;
                if( isTypedArray ){
                 dataStream = CodecUtils.extractTypedArray(
                   inputData,
                   readingByteOffset,
                   this._getDataTypeFromByteStreamInfo(pixBlockHeader.byteStreamInfo[i]),
                   pixBlockHeader.byteStreamInfo[i].length
                 )
                }else{
                  objectBuffer = CodecUtils.extractTypedArray(
                   inputData,
                   readingByteOffset,
                   Uint8Array,
                   pixBlockHeader.byteStreamInfo[i].byteLength
                  )
                  dataStream = CodecUtils.ArrayBufferToObject( objectBuffer.buffer );
                }


                dataStreams.push( dataStream )
                readingByteOffset += pixBlockHeader.byteStreamInfo[i].byteLength;
              }
            }

            # If data is a single typed array (= not composed of a subset)
            # we get rid of the useless wrapping array
            if( dataStreams.length == 1){
              dataStreams = dataStreams[0]
            }

            this._output = {
              originalBlockType: pixBlockHeader.originalBlockType,
              _data: dataStreams,
              _metadata: metadataObject
            };
  
