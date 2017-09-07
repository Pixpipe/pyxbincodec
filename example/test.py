import PixBinDecoder

def readPixbin( filePath ):
    with open(filePath, mode='rb') as file: # b is important -> binary
        buff = file.read()
        pixBinDecoder = PixBinDecoder.PixBinDecoder()
        pixBinDecoder.setInput( buff )
        
        # optional, perform a md5 verification when calling fetchBlock()
        pixBinDecoder.enableBlockVerification( True )

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
        
        print("\nUser object:")
        print(pixBinDecoder.getBinUserObject())
        
        for i in range(0, nbBlocks):
        #for i in range(3, 4):
            print("\n-------------------- BLOCK " + str(i) + " ----------")
            
            print("\nDescription of block #" + str(i))
            print(pixBinDecoder.getBlockDescription(i))
            
            print("\nType of block #" + str(i))
            print(pixBinDecoder.getBlockType(i))
            
            block = pixBinDecoder.fetchBlock(i, )
            
            if( block is None ):
                print("Invalid block")
                continue
            
            print("\nBlock type (from block info):")
            print(block["originalBlockType"])
            print("\nBlock metadata:")
            print(block["_metadata"])
            print("\nBlock data:")
            print(block["_data"])
        
        
if __name__ == "__main__":
    #filePath = "data/testFile_uncomp.pixb"
    #filePath = "data/testFile_comp.pixb"
    #filePath = "data/testFile_50k25_uncomp.pixb"
    filePath = "data/testFile_50k25_comp.pixb"
    
    readPixbin( filePath )
    
