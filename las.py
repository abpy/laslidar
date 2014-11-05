import struct

def read_las(filename, mode="normal"):
    las = open(filename, "rb")
    # read header
    las.seek(96)
    offset = struct.unpack("<L", las.read(4))[0]
    las.seek(4, 1)
    form = struct.unpack("<B", las.read(1))[0]
    length = struct.unpack("<H", las.read(2))[0]
    n_points = struct.unpack("<L", las.read(4))[0]
    las.seek(20, 1)
    xscale = struct.unpack("<d", las.read(8))[0]
    yscale = struct.unpack("<d", las.read(8))[0]
    zscale = struct.unpack("<d", las.read(8))[0]
    xofst = struct.unpack("<d", las.read(8))[0]
    yofst = struct.unpack("<d", las.read(8))[0]
    zofst = struct.unpack("<d", las.read(8))[0]
    maxx = struct.unpack("<d", las.read(8))[0]
    minx = struct.unpack("<d", las.read(8))[0]
    maxy = struct.unpack("<d", las.read(8))[0]
    miny = struct.unpack("<d", las.read(8))[0]
    maxz = struct.unpack("<d", las.read(8))[0]
    minz = struct.unpack("<d", las.read(8))[0]

    # find center od data
    cx = (maxx + minx) / 2.0
    cy = (maxy + miny) / 2.0
    cz = (maxz + minz) / 2.0

    # get points
    las.seek(offset)
    points = []

    if mode == "normal":
        while len(points) < n_points:
            point = {}
            pdata = struct.unpack("<LLLHBB", las.read(length)[:16])
            px = ((pdata[0] * xscale) + xofst)
            py = ((pdata[1] * yscale) + yofst)
            pz = ((pdata[2] * zscale) + zofst)
            #center and scale
            px = (px - cx) * 0.0004
            py = (py - cy) * 0.0004
            pz = (pz - cz) * 0.0004

            point["x"] = px
            point["y"] = py
            point["z"] = pz
            point["intensity"] = pdata[3]
            point["classification"] = pdata[5]
            rb = pdata[4]
            returnnumber = (rb & 0b00000111)
            numberofreturns = (rb & 0b00111000) >> 3
            point["returnnum"] = returnnumber
            point["numreturns"] = numberofreturns
            points.append(point)
    elif mode == "optimized": #no dict for less memory
        while len(points) < n_points:
            pdata = struct.unpack("<LLLHBB", las.read(length)[:16])
            px = (((pdata[0] * xscale) + xofst) - cx) * 0.0004
            py = (((pdata[1] * yscale) + yofst) - cy) * 0.0004
            pz = (((pdata[2] * zscale) + zofst) - cz) * 0.0004
            points.append((px, py, pz))

    las.close()
    print len(points)
    return points

def exportcsv(name, points, classification="all", separator=","):
    d = separator
    data = ""
    for p in points:
        x = p["x"]
        y = p["y"]
        z = p["z"]
        point = ("%s" + d + "%s" + d + "%s\n") % (x, y, z)
        if classification == "all":
            data += point
        else:
            if p["classification"] == classification:
                data += point

    asc = open(name, "w")
    asc.write(data[:-2])
    asc.close()
