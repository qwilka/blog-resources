
import logging
import numpy as np
import struct

logger = logging.getLogger(__name__)

def wav2array(wavfile):
    logger.info("Extracting data from {}".format(wavfile))
    fid = open(wavfile, 'rb')
    str1 = fid.read(4)
    if str1 == b'RIFF':
        logger.info("{} is RIFF".format(wavfile))
    logger.info(str1)
    logger.info(str1.decode("utf-8"))
    fmt = '<I'
    fsize = struct.unpack(fmt, fid.read(4))[0] + 8
    print("fsize = {} ".format(fsize))
    str2 = fid.read(4)
    if str2 == b'WAVE':
        print("{} is WAVE".format(wavfile))
    print(str2)
    while (fid.tell() < fsize):
        chunk_id = fid.read(4)
        if chunk_id == b'fmt ':
            fmt = '<'
            res = struct.unpack(fmt+'iHHIIHH',fid.read(20))
            size, comp, noc, rate, sbytes, ba, bits = res
        elif chunk_id == b'data':
            fmt = '<i'
            size = struct.unpack(fmt,fid.read(4))[0]
            print("size = {} ".format(size))
            _bytes = bits//8
            dtype = '<'
            dtype += 'i%d' % _bytes
            start = fid.tell()
            data = np.fromstring(fid.read(size), dtype=dtype)
            fid.seek(start + size)                         
        else:
            print("Cannot handle this!!")
            continue
    fid.close()
    return rate, data 





