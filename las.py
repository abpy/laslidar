import struct
import time

# aug - 2018, las 1.4 support

class LAS():
    def __init__(self, filename):
        self.las = open(filename, "rb")
        # read header
        self.las.seek(24)
        version = struct.unpack("<BB", self.las.read(2))
        version = "{0}.{1}".format(*version)
        self.version = version
        self.las.seek(96)
        self.offset = struct.unpack("<L", self.las.read(4))[0]
        self.las.seek(4, 1)
        self.form = struct.unpack("<B", self.las.read(1))[0]
        self.length = struct.unpack("<H", self.las.read(2))[0]
        n_points = struct.unpack("<L", self.las.read(4))[0]
        self.las.seek(20, 1)
        self.xscale = struct.unpack("<d", self.las.read(8))[0]
        self.yscale = struct.unpack("<d", self.las.read(8))[0]
        self.zscale = struct.unpack("<d", self.las.read(8))[0]
        self.xofst = struct.unpack("<d", self.las.read(8))[0]
        self.yofst = struct.unpack("<d", self.las.read(8))[0]
        self.zofst = struct.unpack("<d", self.las.read(8))[0]
        self.maxx = struct.unpack("<d", self.las.read(8))[0]
        self.minx = struct.unpack("<d", self.las.read(8))[0]
        self.maxy = struct.unpack("<d", self.las.read(8))[0]
        self.miny = struct.unpack("<d", self.las.read(8))[0]
        self.maxz = struct.unpack("<d", self.las.read(8))[0]
        self.minz = struct.unpack("<d", self.las.read(8))[0]

        #las 1.4 n_points
        if version == "1.4":
            self.las.seek(20, 1)
            n_points = struct.unpack("<Q", self.las.read(8))[0]
        self.n_points = n_points

        # find center and scale of data
        self.cx = (self.maxx + self.minx) / 2.0
        self.cy = (self.maxy + self.miny) / 2.0
        self.cz = (self.maxz + self.minz) / 2.0

        self.scx = self.maxx - self.minx
        self.scy = self.maxy - self.miny
        self.scz = self.maxz - self.minz
        self.range = max(self.scx, self.scy, self.scz)
        self.scale = min(2 / self.scx, 2 / self.scy, 2 / self.scz)

        #pre load point data #not much faster
        #self.las.seek(self.offset)
        #self.data = self.las.read(self.length * self.n_points)

    def centerscale(self, px, py, pz):
        px = (px - self.cx) * self.scale
        py = (py - self.cy) * self.scale
        pz = (pz - self.cz) * self.scale
        return px, py, pz

    def points(self):
        self.las.seek(self.offset)

        idx = 0
        while idx < self.n_points:
            point = {}
            pdata = struct.unpack("<lllHBBB", self.las.read(self.length)[:17])
            px = ((pdata[0] * self.xscale) + self.xofst)
            py = ((pdata[1] * self.yscale) + self.yofst)
            pz = ((pdata[2] * self.zscale) + self.zofst)
            
            #px, py, pz = self.centerscale(px, py, pz)

            point["x"] = px
            point["y"] = py
            point["z"] = pz
            point["intensity"] = pdata[3]

            if self.form == 6:
                point["classification"] = pdata[6]
                rb = pdata[4]
                returnnumber = (rb & 0b00001111)
                numberofreturns = (rb & 0b11110000) >> 4
            else:
                point["classification"] = pdata[5] & 0b00011111
                rb = pdata[4]
                returnnumber = (rb & 0b00000111)
                numberofreturns = (rb & 0b00111000) >> 3
            
            point["returnnum"] = returnnumber
            point["numreturns"] = numberofreturns

            yield point
            idx += 1

    def points_tuple(self, scale=False, scaleZ=True):
        self.las.seek(self.offset)

        idx = 0
        while idx < self.n_points:
            pdata = struct.unpack("<lll", self.las.read(self.length)[:12])
            px = ((pdata[0] * self.xscale) + self.xofst)
            py = ((pdata[1] * self.yscale) + self.yofst)
            pz = ((pdata[2] * self.zscale) + self.zofst)

            if scale:
                if scaleZ:
                    px, py, pz = self.centerscale(px, py, pz)
                else:
                    px, py, n_pz = self.centerscale(px, py, pz)

            yield (px, py, pz)
            idx += 1

    def points_tuple_p(self):
        idx = 0
        didx = 0
        while idx < self.n_points:
            pdata = struct.unpack("<lll", self.data[idx:idx + 12])
            px = ((pdata[0] * self.xscale) + self.xofst)
            py = ((pdata[1] * self.yscale) + self.yofst)
            pz = ((pdata[2] * self.zscale) + self.zofst)

            px, py, pz = self.centerscale(px, py, pz)

            yield (px, py, pz)
            idx += 1
            didx += self.length

    def close(self):
        self.las.close()

if __name__ == "__main__":
    filenane = "file.las"
    lidar = LAS(filenane)
    
    print(lidar.version)
    print(lidar.n_points)
    
    t1 = time.time()
    p = lidar.points_tuple(scale=True, scaleZ=False)
    list(p)
    print(time.time() - t1)

    lidar.close()

