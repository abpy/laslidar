las.py
======

### Simple python library for reading lidar point clouds from .las files

In this new version: object based, uses generators, las 1.4 support

#### basic documentation

basic usage:

to load a las file:
```
import las
lidar = las.LAS(filename)
```
to get the points as a generator:
```
points = lidar.points()
```

the generator yeilds each point as a dictionary each having the keys:
  * "x"
  * "y"
  * "z"
  * "intensity"
  * "classification"
  * "returnnum"
  * "numreturns"


```lidar.points_tuple()``` returns only x, y, and z values in a tuple to save memory:

this method has options to center points around 0 and scale proportionally to ~ -1 - 1 range:
```
scale=True, scaleZ=False
```

```lidar.points_tuple_p()``` is the same but without options
