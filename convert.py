import las

from Tkinter import Tk
import tkFileDialog
Tk().withdraw()

openname = tkFileDialog.askopenfilename(initialdir="/Users/Aaron/Downloads/lidar", title="Choose a .las")

print "reading points"
points = las.read_las(openname)

savename = tkFileDialog.asksaveasfilename(title="Save File")

print "writing"
las.exportcsv(savename, points)#, classification="all", separator=",")
