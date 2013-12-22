#!/bin/env python

""" 
Program: kmean-prob
Author: Travis Cunningham
"""

import random
import sys
from collections import Counter


class PGMImage(object):
    """ 
    Represents the PGM image. 
    For the contents parameter, specify an array of pixels. 
    """
    def __init__(self, width, height, max_grayscale, contents):
        self._width = width
        self._height = height
        self._max_grayscale = max_grayscale
        self._contents = contents

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def max_grayscale(self):
        return self._max_grayscale

    @property
    def contents(self):
        return self._contents

    def raw(self):
        """ Build the raw PGM image. """
        imagecontents = ""
        for value in self._contents:
            imagecontents += str(value) + "\n"
        raw_output = ("P2\n" + str(self.width) + " " + str(self.height) +
                "\n" + str(self.max_grayscale) + "\n" +
                imagecontents)
        return raw_output


class KMeansProb(object):
    """ 
    A better KMeans class that determines which cluster a pixel belongs to by
    calculating the probability of the p)xel to be in any cluster.
    """
    def __init__(self, image):
        self.image = image
        self.num_clusters = 0

        self.new_image = []
        self.clusters = []

        self.cluster_counter = []
        # For each pixel in the image, assign a counter
        total_pixels = self.image.height * self.image.width
        for x in range(total_pixels):
            self.cluster_counter.append(Counter())

    def generate(self, k):
        """ Runs KMeans on the image. Repeats until convergence. """
        # First generate k amount of random clusters
        self.generate_random_clusters(k)
        i = 1
        all_changed = True
        while all_changed:
            # Assign all the points to a cluster
            self.assign_to_clusters()
                # Recalculate centroid positions for each cluster
            # Recalculate centroid positions for each cluster
            for cluster in self.clusters:
                cluster.recalculate_centroid()
                # Check if the points have changed,
            # Check if the points have changed, but for the first iteration
            if i is not 1:
                for cluster in self.clusters:
                    if not cluster.has_changed():
                        all_changed = False
                        break
                # If some have changed, clear each cluster
            # If some have changed, clear each cluster and the new image array
            if all_changed:
                # Clear the points in each cluster
                for cluster in self.clusters:
                    cluster.clear()
            else:
                # Otherwise, generate an image
                for counter in self.cluster_counter:
                    most_common = counter.most_common(1)[0][0]
                    color = self.clusters[most_common].color
                    self.new_image.append(color)
            i += 1


    def generate_random_clusters(self, num_clusters):
        """ Generates random clusters and populates the clusters array. """
        self.num_clusters = num_clusters
        colors = self.generate_colors()
        for i in range(num_clusters):
            random_color = random.choice(colors)
            # make sure the same color is not picked again
            colors.remove(random_color)
            new_cluster = Cluster(random_color)

            # Add the cluster to the array
            self.clusters.append(new_cluster)

    def generate_colors(self):
        """ Generates a list of unique colors within the image. """
        unique_colors = set()
        values = self.image.contents
        for pixel in values:
            unique_colors.add(pixel)
        colors = list(unique_colors)
        return colors

    def assign_to_clusters(self):
        """ Assigns each pixel in the image to a cluster. """
        for pixel_number, value in enumerate(self.image.contents):
            self.find_cluster(pixel_number, value)

    def find_cluster(self, pixel_number, color):
        """ Finds which cluster to assign a pixel to. """
        cluster_distances = []
        for cluster in self.clusters:
            cluster_distances.append(abs(cluster.color - color))

        # Find the closest cluster
        closest = cluster_distances.index(min(cluster_distances))

        # Increase the counter for this pixel for the closest cluster index
        self.cluster_counter[pixel_number][closest] += 1

        # Add the point to the cluster
        self.clusters[closest].add_point(Point(pixel_number, color))

    def generate_image(self):
        """ Returns a new PGMImage. """
        new_pgm = PGMImage(width=self.image.width, height=self.image.height,
                max_grayscale=self.image.max_grayscale, contents=self.new_image)
        return new_pgm


class Cluster(object):
    """ Represents a cluster, containing a color and an array of points. """
    def __init__(self, color):
        self.color = color
        self.points = set()
        self.previous_points = set()

    def add_point(self, point):
        """ Adds a point to the cluster. """
        self.points.add(point)

    def clear(self):
        """ Clears all points in the cluster. """
        self.points.clear()

    def recalculate_centroid(self):
        """ 
        Recalculates the centroid position by averaging all values in the
        points array. 
        """
        sum_of_list = 0
        for point in self.points:
            sum_of_list += point.color
        if len(self.points) is not 0:
            self.color = sum_of_list/len(self.points)

        self.previous_points.clear()
        # Move the current points into the previous points set
        self.previous_points.update(self.points)

    def has_changed(self):
        """ Checks if the previous points match the current points. """
        differences = self.previous_points.symmetric_difference(self.points)
        if len(differences) is 0:
            return False
        else:
            return True


class Point(object):
    def __init__(self, number, color):
        self.number = number
        self.color = color


def main():
    # Grab the input, split it by =
    try:
        input = sys.argv[1].split('=')
        args = {input[0]: input[1]}

        # Number of clusters
        k = int(args['k'])
    except IndexError:
        # If k was not specified, the default value is 5
        k = 5

    # Put the image into an array
    image = []

    # Parse the image
    line_number = 1
    for line in sys.stdin:
        if line_number is 1:
            # skip the first line
            line_number += 1
        elif line_number is 2:
            # read the x and y values from the image
            x = int(line.split(" ")[0])
            y = int(line.split(" ")[1])
            line_number += 1
        elif line_number is 3:
            # read the max_grayscale value
            max_grayscale = int(line)
            line_number += 1
        else:
            # read the pixel contents
            values = line.split(" ")
            for value in values:
                if value != '\n':
                    # store the pixel into the array
                    image.append(int(value))

    # Create a new image object
    pgm = PGMImage(width=x, height=y, max_grayscale=max_grayscale,
                   contents=image)


    kmeans = KMeansProb(pgm)
    kmeans.generate(k)
    # Send the new generated image to stdout
    sys.stdout.write(kmeans.generate_image().raw())


main()
