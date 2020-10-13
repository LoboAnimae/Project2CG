import struct


def char(c):
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    return struct.pack("=h", w)


def dword(d):
    return struct.pack("=l", d)




def writebmp(filename, width, height, frame):
    with open(filename, 'bw') as outputfile:
        outputfile.write(char("B"))
        outputfile.write(char("M"))
        outputfile.write(dword(14 + 40 + width * height * 3))
        outputfile.write(dword(0))
        outputfile.write(dword(14 + 40))
        outputfile.write(dword(40))
        outputfile.write(dword(width))
        outputfile.write(dword(height))
        outputfile.write(word(1))
        outputfile.write(word(24))
        outputfile.write(dword(0))
        outputfile.write(dword(width * height * 3))
        outputfile.write(dword(0))
        outputfile.write(dword(0))
        outputfile.write(dword(0))
        outputfile.write(dword(0))
        for x in range(height):
            for y in range(width):
                outputfile.write(frame[x][y].toBytes())
