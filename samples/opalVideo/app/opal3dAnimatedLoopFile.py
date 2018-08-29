# -*- coding: utf-8 -*-
"""
@author: hahnml
"""

import sys
import numpy as np
import matplotlib
# (Un)comment to use non-interactive back end mode or not
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from itertools import product, combinations

arguments = sys.argv

if len(arguments) == 2:
    numberOfFiles = arguments[1]
else:
    sys.exit('The script should be invoked like this: \'python opal3dAnimatedLoopFile.py $numberOfFilesToAnimate\'!')


def determine_FileContentLength(fileIdx):
    number = str(fileIdx)
    
    num_lines = sum(1 for line in open('abcd'+number+'.dat','r'))

    return num_lines

def read_File(fileIdx):
    number = str(fileIdx)
    
    # Points stored in the file
    print('Read file: abcd' + number + '.dat')
    pullData = open('abcd'+ number +'.dat','r').read()
    dataArray = pullData.split('\n')

    n = len(dataArray)

    points = np.zeros(shape=(3, n))

    index = 0
    for eachLine in dataArray:
        if len(eachLine)>1:
            lar = eachLine.split()

            x = int(lar[2])
            y = int(lar[3])
            z = int(lar[4])

            lx = 64
            ly = 64
            lz = 64

            xpos = float(((1.0/(lx)) * x) - 0.5) * 2
            ypos = float(((1.0/(ly)) * y) - 0.5) * 2
            zpos = float(((1.0/(lz)) * z) - 0.5) * 2

            points[0][index] = xpos
            points[1][index] = ypos
            points[2][index] = zpos

            index = index + 1

    return points

# Attaching 3D axis to the figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Disable interactive mode
plt.ioff()

# Setting the axes properties
ax.set_xlim3d([-1.0, 1.0])
ax.set_xlabel('X')

ax.set_ylim3d([-1.0, 1.0])
ax.set_ylabel('Y')

ax.set_zlim3d([-1.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('Opal Cluster XYZ')

# Initialize the points array with zeros
n = determine_FileContentLength(1)
points = np.empty(shape=(3, n))

x_values = points[0]
y_values = points[1]
z_values = points[2]

# Create a Path3DCollection which we can use in the animation to update
sc = ax.scatter(x_values, y_values, z_values, c='r', marker='o')

# initialization function: plot the background of each frame
def init():
    # Initially rotate the axes
    ax.view_init(elev=10, azim=55)

def animate(i, points, sc):
    # Read the i-th file
    points = read_File(i+1)

    sc._offsets3d = points

    # (Un)comment to create an image file per snapshot or not
    #fig.savefig('opalCluster'+str(i+1)+'.png')

    return sc

# Creating the Animation object
point_ani = animation.FuncAnimation(fig, animate, init_func=init, fargs=(points, sc),
                               frames=int(numberOfFiles), interval=500, blit=False)

# Save the animation to an *.mp4 file
# (Un)comment to create a video of the animation or not
point_ani.save('opalClusterSnapshots.mp4', fps=5,
          extra_args=['-vcodec', 'h264',
                      '-pix_fmt', 'yuv420p'])

plt.show()
