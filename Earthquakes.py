'''
CIS 210 W20 Project 8: World-wide Earthquake Watch

Author: Brianna Vago

Credits: N/A

Use file prossesing and data mining to discover pattersn of earthquake activity
around the world in 2019; plot on map.
'''
import math
import random
import turtle

def readFile(fname):
    '''
    (str) -> (dict)

    Reads the file and makes a dictionary of the latitude and longitude
    values of each earthquake.
    '''
    with open(fname, 'r') as mystats:
        mystats.readline()
        myEQlist = mystats.readlines()
        
        eqdict = {}

        for i in range(len(myEQlist)):
            value1 = float(myEQlist[i].strip().split(',')[1])
            value2 = float(myEQlist[i].strip().split(',')[2])

            eqdict[i] = [value1,value2]

    return eqdict




def euclidD(point1, point2):
    '''
    (list, list) -> float

    This is the equation function. It is used in the createClusters() to
    help organize the different lists.
    '''

    dist = math.sqrt((point1[0] - point2[0])**2 + (point1[1]-point2[1])**2)
    return dist


def createCentroids(k, eqdict):
    '''
    (int, dict) -> list (of lists)

    Picks k random points in the dictionary to put in a list.
    '''
    
    centroids = []
    centroidCount = 0
    centroidKeys = []

    while centroidCount < k:
        rkey = random.randint(1, len(eqdict))
        if rkey not in centroidKeys:
            centroids.append(eqdict[rkey])
            centroidKeys.append(rkey)
            centroidCount += 1

    return centroids



def createClusters(k, centroids, datadict, repeats):
    '''
    (int, list (of lists), dictionary, int) -> list of lists (of keys)

    This makes clusters basded on the centroids and the data that we get.
    It also repeats the code as many times as inputed.    
    '''
    for i in range(repeats):
        
        # create initial list of k empty clusters
        clusters = []
        for j in range(k):
            clusters.append([])

        for akey in datadict:
            distances = []
            for centroidsIndex in range(k):
                dist = euclidD(datadict[akey],centroids[centroidsIndex])
                distances.append(dist)

            mindist = min(distances)
            index = distances.index(mindist)

            clusters[index].append(akey)

        dimensions = len(datadict[1])
        for clusterIndex in range(k):
            sums = [0] * dimensions
            for akey in clusters[clusterIndex]:
                datapoints = datadict[akey]
                for i in range(len(datapoints)):
                    sums[i] += datapoints[i]

            for i in range(len(sums)):
                clusterLen = len(clusters[clusterIndex])
                if clusterLen != 0:
                    sums[i] = sums[i] / clusterLen

            centroids[clusterIndex] = sums
    return clusters



def visualizeQuakes(dataFile,k,reps):
    '''
    Runs all the code and calls eq draw to draw out the clusters on
    a graph.
    '''
    datadict = readFile(dataFile)
    quakeCentroids = createCentroids(k,datadict)
    clusters = createClusters(k,quakeCentroids,datadict,reps)

    eqDraw(k,datadict,clusters)




def eqDraw(k,datadict,clusters):
    '''
    Called by visualizeQuakes() to do the work of plotting the
    results of the k-means analysis on a world map.
    '''
    quakeT = turtle.Turtle()
    quakeWin = turtle.Screen()
    quakeWin.bgpic('worldmap.gif')
    quakeWin.screensize(448,266)

    wFactor = (quakeWin.screensize()[0]/2)/180
    hFactor = (quakeWin.screensize()[1]/2)/90

    quakeT.hideturtle()
    quakeT.up()

    colorlist = ['red','green','blue','orange','cyan','yellow','purple']

    for clusterIndex in range(k):
        quakeT.color(colorlist[clusterIndex])
        for akey in clusters[clusterIndex]:
            lon = datadict[akey][0]
            lat = datadict[akey][1]
            quakeT.goto(lon*wFactor,lat*hFactor)
            quakeT.dot()
    quakeWin.exitonclick()
    


def main():
    '''
    '''
    k = 4
    r = 6
    visualizeQuakes('Data.txt',k,r)



main()
    




