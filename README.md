las.py
======

python functions for reading lidar point clouds from .las files

returns a list containing all points as dictionarys each having the keys:
x
y
z
intensity
classification
returnnum
numreturns

"optimized" mode returns only x, y, and z values in a tuple to save memory
