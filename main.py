import struct
import json



def readPixbin( filePath ):
    with open(filePath, mode='rb') as file: # b is important -> binary
        buff = file.read()

        currentOffset = 0
        expectedMagicNumber = "PIXPIPE_PIXBIN"
        actualMagicNumber = buff[currentOffset:currentOffset+len(expectedMagicNumber)].decode('ascii')

        if( not expectedMagicNumber == actualMagicNumber ):
            print("This file is not a PixBin file. Wrong magic number.")
            return 0;

        currentOffset += len(expectedMagicNumber)

        # endianess: 1 for little, 0 for big
        isLittleEndian = struct.unpack("b", buff[currentOffset:currentOffset+1])[0]
        currentOffset += 1

        pixBinHeaderByteLength = struct.unpack("I", buff[currentOffset:currentOffset+4])[0]
        currentOffset += 4

        print(pixBinHeaderByteLength)

        #pixBinHeaderUnicode = buff[currentOffset:currentOffset+pixBinHeaderByteLength].decode('utf-8')
        #print(pixBinHeaderUnicode)

        strBuff = buff[currentOffset:currentOffset+pixBinHeaderByteLength];
        jsonStr = strBuff.decode("utf-8")
        obj = json.loads( jsonStr )
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

if __name__ == "__main__":
    filePath = "data/testFile.pixb"
    readPixbin( filePath )
