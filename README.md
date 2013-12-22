KMeans Implementation in Python
===============================

This is a naive kmeans implementation in Python, which was a project in CS362 (Data Structures) at IUPUI.
Included is a simple kmeans and a probabilistic kmeans program.

To build kmeans, first run:

::
    $ ./configure

To run simple kmeans on an image, use the following (replace '/path/to/image.jpg' with the path of the image to process):

::
    $ cat /path/to/image.jpg | convert - -colorspace gray -compress none -depth 8 pgm:- | ./kmean-simple $k | convert - result_simple_image.jpg


For probabilistic kmeans:

::
    $ cat /path/to/image.jpg | convert - -colorspace gray -compress none -depth 8 pgm:- | ./kmean-prob $k | convert - result_probabilistic_image.jpg


Included is a file called "test.sh", which can run kmeans on all images in a specified directory.
