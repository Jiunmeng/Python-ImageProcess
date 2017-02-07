from osgeo import gdal, gdal_array
import numpy as np

# "Before" image
im1 = "D:\\Python36\\testdata\\before.tif"
# "After" image
im2 = "D:\\Python36\\testdata\\after.tif"
#Output image name
output = "D:\\Python36\\testdata\\change.tif"
# Load before and after into arrays
ar1 = gdal_array.LoadFile(im1).astype(np.int8)
ar2 = gdal_array.LoadFile(im2)[1].astype(np.int8)
# Perform a simple array difference on the images
diff = ar2 - ar1
# Set up our classification scheme to try
# and isolate significant changes
classes = np.histogram(diff, bins=5)[1]
# The color black is repeated to mask insignificant changes
lut = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 0], [255, 0, 0]]
# Starting value for classification
start = 1
# Set up the output image
rgb = np.zeros((3, diff.shape[0], diff.shape[1], ), np.int8)
# Process all classes and assign colors
for i in range(len(classes)):
    mask = np.logical_and(start <= diff, diff <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = np.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1
# Save the output image
gdal_array.SaveArray(rgb, output, format="GTiff",  
  prototype=im2)
output = None
