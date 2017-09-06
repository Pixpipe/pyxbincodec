import CodecUtils
import PixBlockDecoder

class PixBinDecoder:
    
    """docstring for """
    def __init__(self):
        self.MAGIC_NUMBER = "PIXPIPE_PIXBIN"
        
        self._verifyChecksum = False
        self._input = None
        self._output = None
        self._binMeta = None
        self._parsingInfo = {
          "offsetToReachFirstBlock": -1,
          "isLittleEndian": -1,
        }
        
        self._decodedBlocks = {}
        self._isValid = False
        
    """
    reset I/O and data to query
    """
    def reset(self):
        self._verifyChecksum = False
        self._isValid = False
        self._input = None
        self._output = None
        self._binMeta = None
        self._parsingInfo = {
          "offsetToReachFirstBlock": -1,
          "isLittleEndian": -1,
        }
        self._decodedBlocks = {}
      

    """
    Specify an input
    @param {ArrayBuffer} buff - the input
    """
    def setInput(self, buff ):
        self.reset()

        if( type(buff) is not bytes ):
            print("The input mus be of type 'bytes'.")
            return;
            
        self._input = buff
        self._isValid = self._parseIndex()
        
  
    def _parseIndex(self):
        inputData = self._input

        if( inputData is None ):
          print("Input cannot be None")
          return False
        

        inputByteLength = len(inputData)
        magicNumberToExpect = self.MAGIC_NUMBER

        # control 1: the file must be large enough
        if( inputByteLength < (len(magicNumberToExpect) + 5) ):
          print("This buffer does not match a PixBin file.")
          return False
        
        movingByteOffset = 0
        magicNumber = CodecUtils.buffToAsciiString(inputData, movingByteOffset, len(magicNumberToExpect) )

        # control 2: the magic number
        if( magicNumber != magicNumberToExpect):
          print("This file is not of PixBin type. (wrong magic number)")
          return False

        movingByteOffset = len(magicNumberToExpect)
        isLittleEndian = CodecUtils.getUint8(inputData, movingByteOffset )

        # control 3: the endianess must be 0 or 1
        if(isLittleEndian != 0 and isLittleEndian != 1):
          print("This file is not of PixBin type. (wrong endianess code)")
          return False
        
        movingByteOffset += 1
        pixBinIndexBinaryStringByteLength = CodecUtils.getUint32(inputData, movingByteOffset )
        movingByteOffset += 4
        pixBinIndexDict = CodecUtils.buffToDict(inputData, movingByteOffset, pixBinIndexBinaryStringByteLength)
        movingByteOffset += pixBinIndexBinaryStringByteLength
        
        self._parsingInfo["offsetToReachFirstBlock"] = movingByteOffset
        self._parsingInfo["isLittleEndian"] = isLittleEndian
        self._binMeta = pixBinIndexDict
        return True;
  
  
    def isValid(self):
        return self._isValid

    
    def getOutput(self):
        return self._output


    def getNumberOfBlocks(self):
        return len(self._binMeta["pixblocksInfo"])

    
    def getBinCreationDate(self):
        return self._binMeta["date"];
        
        
    def getBinDescription(self):
        return self._binMeta["description"]
 
 
    def getBlockDescription( self, n ):
        if( n<0 or n >= self.getNumberOfBlocks() ):
            print("The block index is out of range.")
            return None
        return self._binMeta["pixblocksInfo"][n]["description"]
      
    
    def getBlockType(self, n ):
        if( n<0 or n >= self.getNumberOfBlocks() ):
            print("The block index is out of range.")
            return None
        return self._binMeta["pixblocksInfo"][n]["type"]


    def enableBlockVerification(self, b ):
        self._verifyChecksum = b;


    def fetchBlock(self, n , forceDecoding=False ):
        nbBlocks = self.getNumberOfBlocks()
        
        if( n<0 or n >= nbBlocks ):
          print("The block index is out of range.");
          return None;
        
        if( n in self._decodedBlocks and (not forceDecoding)):
          return self._decodedBlocks[ n ];
        
        offset = self._parsingInfo["offsetToReachFirstBlock"];
        
        for i in range(0, n):
          offset += self._binMeta["pixblocksInfo"][i]["byteLength"];
        
        blockInfo = self._binMeta["pixblocksInfo"][n];
        #pixBlockBuff = self._input.slice(offset, offset + blockInfo.byteLength);
        pixBlockBuff = self._input[ offset : offset + blockInfo["byteLength"] ]
        
        # MD5 checksum
        # if( self._verifyChecksum && md5( pixBlockBuff ) !== blockInfo.checksum){
        #   print("The block #" + n + " is corrupted.");
        #   return none;
        # }

        blockDecoder = PixBlockDecoder.PixBlockDecoder();
        blockDecoder.setInput( pixBlockBuff )
        blockDecoder.run();
        decodedBlock = blockDecoder.getOutput();
        
        if( decodedBlock is None ):
          print("The block #" + str(n) + " could not be decoded.");
          return None;
        
        self._decodedBlocks[ n ] = decodedBlock;
        return decodedBlock;
  
