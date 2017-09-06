import struct
import json

def buffToAsciiString( buff, byteOffset, byteLength ):
    asciiStr = None
    if( len(buff) >= (byteOffset + byteLength) ):
        asciiStr = buff[byteOffset:(byteOffset + byteLength)].decode('ascii')
    return asciiStr


def buffToUnicodeString( buff, byteOffset=0, byteLength=-1 ):
    if( byteLength == -1 ):
        byteLength = len(buff)
        
    unicodeStr = None
    if( len(buff) >= (byteOffset + byteLength) ):
        unicodeStr = buff[byteOffset:(byteOffset + byteLength)].decode('utf-8')
    return unicodeStr


def buffToDict( buff, byteOffset=0, byteLength=-1, useUnicode = True ):
    if( byteLength == -1 ):
        byteLength = len(buff)
        
    jsonStr = None
    if( useUnicode ):
        jsonStr = buffToUnicodeString( buff, byteOffset, byteLength )
    else:
        jsonStr = buffToAsciiString( buff, byteOffset, byteLength )

    try:
        return json.loads( jsonStr )
    except json.decoder.JSONDecodeError:
        print("ERROR: invalid JSON string. Cannot create a dict.")
    
    return None


def _getNumericalData(buff, byteOffset, byteLength, strFormat, howMany=1, isLittleEndian=True):
    if( len(buff) >= (byteOffset + byteLength) ):
        numbers = struct.unpack(("<" if isLittleEndian else ">") + str(howMany) + strFormat, buff[byteOffset:byteOffset+byteLength*howMany])
        if(howMany == 1):
            return numbers[0]
        else:
            return list( numbers )
    else:
        print("WARN: byte offset is out of bound.")
        return None
        
        
def getUint8(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 1, "B", howMany, isLittleEndian)

def getInt8(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 1, "b", howMany, isLittleEndian)

def getUint16(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 2, "H", howMany, isLittleEndian)
    
def getInt16(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 2, "h", howMany, isLittleEndian)

def getUint32(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 4, "i", howMany, isLittleEndian)
    
def getInt32(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 4, "I", howMany, isLittleEndian)
    
def getUint64(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 8, "q", howMany, isLittleEndian)
    
def getInt64(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 8, "Q", howMany, isLittleEndian)

def getFloat32(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 4, "f", howMany, isLittleEndian)
    
def getFloat64(buff, byteOffset, howMany=1, isLittleEndian=True):
    return _getNumericalData(buff, byteOffset, 8, "d", howMany, isLittleEndian)
