#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:30:13 2023

@author: kunalpathak9826
"""

#Import all the modules we'll need later on
#%matplotlib inline
import numpy as np # Numpy is Python's main numeric processind library
import datetime # Allows handling of dates
import matplotlib.pyplot as plt # Add the plotting libraies

import pyproj
import rasterio
import rasterio.features
import folium



import ee
from IPython import display

def ChangeDetection():

    # The paths to the Australian Seasonal Landsat Mosaics on the Queensland RDSI Node
    refDataPath = '/vsicurl/http://qld.auscover.org.au/public/data/landsat/surface_reflectance/aus/l8olre_aus_m201609201611_dbia2.vrt'

    # Open the  surface reflectance data using rasterio (Could also use GDAL or RIOS or rsgislib etc)
    refDataSet = rasterio.open(refDataPath)

    # The dataset object contains metadata about the raster data
    print("Bands:\t ", refDataSet.count)
    print("Height:\t ", refDataSet.height)
    print("Width:\t ", refDataSet.width)
    print("Number of MegaPixels:\t ", refDataSet.height*refDataSet.width/1e6,0)
    print("BoundingBox: ", refDataSet.bounds)
    print("CRS:\t ", refDataSet.crs)

    # This takes a subset over an AOI with the bounding box in EPSG:3577 (Australian Albers)
    # Brisbane
    topLeft = (2030000,-3140000)
    bottomRight = (2070000,-3160000)

    # Compute the image coordinates from the real world coordinates using an inverse transform
    y1, x1 =  ~refDataSet.transform * topLeft
    y2, x2 =  ~refDataSet.transform * bottomRight

    # Read in the SWIR, NIR and Red bands within the specified bounding box
    refDataSubset = refDataSet.read([5,4,3], window=((int(x1),int(x2)), (int(y1),int(y2))))

    # Print some information on the subset
    print('Data extract shape: {0}, dtype: {1}'.format(refDataSubset.shape, refDataSubset.dtype))

    # Stretch and scale the data from 0 to 255 as an unsigned 8 bit integer for display
    refDataSubsetScaled=np.clip(refDataSubset / 4000.0 * 255.0, 0, 255).astype('uint8')

    # Plot the image using matplotlib
    plt.figure(figsize=(16,10))

    # Rearrange the axes so that it works with matplotlib that likes BIP not BSQ data
    plt.imshow(np.rollaxis(refDataSubsetScaled,0,3))

    # Add a title to the plot
    plt.title('Landsat Surface Reflectance (Bands 5,4,3)', fontsize=18)

    # Function to convert geographical to projected coordinates
    def ll2albers(x,y):
       inProj = pyproj.Proj(init='epsg:4326')
       outProj = pyproj.Proj(init='epsg:3577')
       return pyproj.transform(inProj,outProj,x,y)

       # Utility Query Mapping function
       # Takes a topLeft and bottomRight Tuple
    def mapQuery(topLeft, bottomRight):
        map_hybrid = folium.Map(
            location=[np.mean([topLeft[1],bottomRight[1]]), np.mean([topLeft[0],bottomRight[0]])],
            zoom_start=12,
            tiles=" http://mt1.google.com/vt/lyrs=y&z={z}&x={x}&y={y}",
            attr="Google")
        map_hybrid.add_children(folium.features.PolyLine(
           locations=[
             (topLeft[1],topLeft[0]),
             (bottomRight[1],topLeft[0]),
             (bottomRight[1],bottomRight[0]),
             (topLeft[1],bottomRight[0]),
             (topLeft[1],topLeft[0])],
            color='red', opacity=0.5))
        map_hybrid.add_children(folium.features.LatLngPopup())
        return map_hybrid
    mapQuery((150.3727,-26.9819),(150.4963,-27.0767))

    # This is a subset west of Tara where Coal Seam Gas development has been happening
    topLeft = ll2albers(150.3727,-26.9819)
    bottomRight = ll2albers(150.4963,-27.0767)


    # The paths to the 2007 Australian Seasonal Landsat Mosaics on the Queensland RDSI Node
    date1DataPath = '/vsicurl/http://qld.auscover.org.au/public/data/landsat/surface_reflectance/aus/lztmre_aus_m200703200705_dbia2.vrt'

    # The paths to the 2017 Australian Seasonal Landsat Mosaics on the Queensland RDSI Node
    date2DataPath = '/vsicurl/http://qld.auscover.org.au/public/data/landsat/surface_reflectance/aus/l8olre_aus_m201703201705_dbia2.vrt'

    # Compute the image coordinates from the real world coordinates using an inverse transform
    y1, x1 =  ~refDataSet.transform * topLeft
    y2, x2 =  ~refDataSet.transform * bottomRight

    # Read in the SWIR, NIR and Red bands within the specified bounding box
    date1DataSubset = rasterio.open(date1DataPath).read([5,4,3], window=((int(x1),int(x2)), (int(y1),int(y2))))
    date2DataSubset = rasterio.open(date2DataPath).read([5,4,3], window=((int(x1),int(x2)), (int(y1),int(y2))))

    # Setup the plot
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,10))

    # Rearrange and scale the data
    ax1.imshow(np.rollaxis(np.clip(date1DataSubset / 5000.0 * 255.0, 0, 255).astype('uint8'),0,3), aspect=1)
    ax2.imshow(np.rollaxis(np.clip(date2DataSubset / 5000.0 * 255.0, 0, 255).astype('uint8'),0,3), aspect=1)

    # Add some titles
    ax1.set_title('Autumn 2007 Landsat', fontsize=18)
    ax2.set_title('Autumn 2017 Landsat', fontsize=18)

    # Allow division by zero
    np.seterr(divide='ignore', invalid='ignore')

    # Create a function to compute the ndvi from the red and NIR bands
    def makeNDVI(b4,b3):
        # Calculate NDVI
        ndvi = (b4.astype(float) - b3.astype(float)) / (b4.astype(float) + b3.astype(float))
        # Make the NoData values NaN so they get masked from the analysis
        ndvi[b4 == 32767] = np.nan
        return ndvi

    # Use the function to produce NDVI images
    # Watch the band ordering - remember we've read in bands 5,4,3
    date1NDVI = makeNDVI(date1DataSubset[1],date1DataSubset[2])
    date2NDVI = makeNDVI(date2DataSubset[1],date2DataSubset[2])


    # Setup the plot
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,10))

    # Rearrange and scale the data
    ax1.imshow(date1NDVI, cmap='brg',clim=(-0.1,0.7))
    ax2.imshow(date2NDVI, cmap='brg',clim=(-0.1,0.7))

    # Add some titles
    ax1.set_title('Autumn 2007 NDVI', fontsize=18)
    ax2.set_title('Autumn 2017 NDVI', fontsize=18)

    # Remove the axis labels for clarity
    ax1.yaxis.set_visible(False)
    ax2.yaxis.set_visible(False)
    ax1.xaxis.set_visible(False)
    ax2.xaxis.set_visible(False)

    # Compute the NDVI change between the dates
    ndviChange = date1NDVI - date2NDVI

    # Standardise the change
    ndviChangeNorm = ((date1NDVI - np.nanmean(date1NDVI)) / np.nanstd(date1NDVI)) - \
                     ((date2NDVI - np.nanmean(date2NDVI)) / np.nanstd(date2NDVI))



    # Setup the plots
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,10))

    # Rearrange and scale the data
    ax1.hist(ndviChange.ravel(), bins=256, range=(-0.5, 0.5),color = "cyan")
    ax2.hist(ndviChangeNorm.ravel(), bins=256, range=(-3, 3),color = "blue")

    # Add some titles
    ax1.set_title('2017 - 2007 NDVI Change', fontsize=18)
    ax2.set_title('Standardised NDVI', fontsize=18)

    # Add some grids
    ax1.grid()
    ax2.grid()

    plt.figure(figsize=(12,12))
    plt.imshow(ndviChangeNorm, cmap='RdYlGn_r',clim=(-3.8,3.8))
    # Add a title to the plot
    plt.title('10 year Standardised NDVI Change', fontsize=18)

    # Check where we are
    mapQuery((150.4436,-27.0037),(150.4458,-27.0062))

    ChangeDetection()

