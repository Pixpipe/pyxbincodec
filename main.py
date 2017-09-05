import struct
import json
import CodecUtils
import PixBinDecoder

def readPixbin( filePath ):
    with open(filePath, mode='rb') as file: # b is important -> binary
        buff = file.read()
        
        currentOffset = 0
        expectedMagicNumber = "PIXPIPE_PIXBIN"
        actualMagicNumber = CodecUtils.buffToAsciiString( buff, currentOffset, len(expectedMagicNumber) )
        
        if( not expectedMagicNumber == actualMagicNumber ):
            print("This file is not a PixBin file. Wrong magic number.")
            return 0;

        currentOffset += len(expectedMagicNumber)

        # endianess: 1 for little, 0 for big
        isLittleEndian = CodecUtils.getUint8(buff, currentOffset)
        currentOffset += 1

        pixBinHeaderByteLength = CodecUtils.getUint32(buff, currentOffset)
        currentOffset += 4

        print(pixBinHeaderByteLength)

        obj = CodecUtils.buffToDict(buff, currentOffset, pixBinHeaderByteLength)
        
        if( not obj ):
            return;
        
        print( obj["pixblocksInfo"][0]["description"] )

        exit()

        stringCode = list(struct.unpack(("<" if isLittleEndian else ">") +  str(pixBinHeaderByteLength//2) + "H", buff[currentOffset:currentOffset+pixBinHeaderByteLength]))

        print(len(stringCode))
        #exit()
        pixBinHeader = ""
        for c in stringCode:
            print(str(c) + " -> ")
            print(chr(c))
            #pixBinHeader += chr(c)

        #print(pixBinHeader)

def readPixbin2( filePath ):
    with open(filePath, mode='rb') as file: # b is important -> binary
        buff = file.read()
        pixBinDecoder = PixBinDecoder.PixBinDecoder()
        pixBinDecoder.setInput( buff )

        if( not pixBinDecoder.isValid() ):
            print("The file is not valid")
            return

        nbBlocks = pixBinDecoder.getNumberOfBlocks()

        print("\nNumber of blocks:")
        print(nbBlocks)
        
        print("\nBin creation date:")
        print(pixBinDecoder.getBinCreationDate())
        
        print("\nBin description:")
        print(pixBinDecoder.getBinDescription())
        
        for i in range(0, nbBlocks):
            print("\nDescription of block #" + str(i))
            print(pixBinDecoder.getBlockDescription(i))
            
            print("\nType of block #" + str(i))
            print(pixBinDecoder.getBlockType(i))
            
        
        
if __name__ == "__main__":
    filePath = "data/testFile.pixb"
    #readPixbin( filePath )
    readPixbin2( filePath )
    
