"""
========================
Fuzzy c-means clustering
========================

Fuzzy logic principles can be used to cluster multidimensional data, assigning
each point a *membership* in each cluster center from 0 to 100 percent. This
can be very powerful compared to traditional hard-thresholded clustering where
every point is assigned a crisp, exact label.

Fuzzy c-means clustering is accomplished via ``skfuzzy.cmeans``, and the
output from this function can be repurposed to classify new data according to
the calculated clusters (also known as *prediction*) via
``skfuzzy.cmeans_predict``

Data generation and setup
-------------------------

In this example we will first undertake necessary imports, then define some
test data to work with.

"""
from ulab import numpy as np
from bipes import databoard as db
import _cmeans
import normalize_columns
import math
import random
import gc

# Enable garbage collection
gc.enable()

NV_MAGICCONST = 4 * math.exp(-0.5)/2.0**.5

# Number os points per cluster
POINTS = 50


# Define three cluster centers
centers = [[4, 2],
           [1, 7],
           [5, 6]]

# Define three cluster sigmas in x and y, respectively
sigmas = [[0.8, 0.3],
          [0.3, 0.5],
          [1.1, 0.7]]

# Generate test data
xpts = np.zeros(1)
ypts = np.zeros(1)
labels = np.zeros(1)

def hstack_1d(a,b):
    ca = a.size
    cb = b.size

    _hstack = np.zeros(ca+cb)

    for i in range(0, ca+cb):
        if i < ca:
            _hstack[i] = a[i]
        else:
            _hstack[i] = b[i-ca]
    return _hstack

def normalvariate(x):
    """Normal distribution.

    mu is the mean, and sigma is the standard deviation.
    `source <https://microbit-micropython.readthedocs.io/en/latest/_modules/random.html>`_

    """
    # Uses Kinderman and Monahan method. Reference: Kinderman,
    # A.J. and Monahan, J.F., "Computer generation of random
    # variables using the ratio of uniform deviates", ACM Trans
    # Math Software, 3, (1977), pp257-260.

    mu = 1
    sigma = 1

    while 1:
        u1 = random.random()
        u2 = 1.0 - random.random()
        z = NV_MAGICCONST*(u1-0.5)/u2
        zz = z*z/4.0
        if zz <= -math.log(u2):
            break
    return mu + z*sigma

for i, ((xmu, ymu), (xsigma, ysigma)) in enumerate(zip(centers, sigmas)):

    u0 = np.zeros(POINTS)
    vrand = np.vectorize(normalvariate)
    u0 = vrand(u0)
    u1 = np.zeros(POINTS)
    vrand = np.vectorize(normalvariate)
    u1 = vrand(u1)

    xpts = hstack_1d(xpts, u0 * xsigma + xmu)
    ypts = hstack_1d(ypts, u1 * ysigma + ymu)
    labels = hstack_1d(labels, np.ones(POINTS) * i)

# Print test data
for label in range(0,3):
    db.push(xpts[labels == label], ypts[labels == label], label, 'clusters0')

gc.collect()

"""

Clustering
----------

Above is our test data. We see three distinct blobs. However, what would happen
if we didn't know how many clusters we should expect? Perhaps if the data were
not so clearly clustered?

Let's try clustering our data several times, with between 2 and 5 clusters.

"""
def vstack_1d(a,b):
    ca = a.size
    cb = b.size

    _hstack = np.zeros(1,ca+cb)

    for i in range(0, ca+cb):
        if i < ca:
            _hstack[i] = a[i]
        else:
            _hstack[i] = b[i-ca]
# Set up the loop and plot
alldata = _cmeans.vstack(xpts, ypts)
fpcs = []

for ncenters in range(2, 6):
    cntr, u, u0, d, jm, p, fpc = _cmeans.cmeans(
        alldata, ncenters, 2, error=0.005, maxiter=1000, init=None)

    # Store fpc values for later
    fpcs.append(fpc)

    # Plot assigned clusters, for each data point in training set
    cluster_membership = np.argmax(u, axis=0)
    _comma = ','
    for j in range(ncenters):
        db.push(xpts[cluster_membership == j], ypts[cluster_membership == j], j, 'clusters1_' + str(ncenters))


    # Mark the center of each fuzzy cluster
    i = 0
    for pt in cntr:
        db.push(pt[0], pt[1], ncenters + i, 'clusters1_' + str(ncenters))
        i+=1

    gc.collect()


"""

The fuzzy partition coefficient (FPC)
-------------------------------------

The FPC is defined on the range from 0 to 1, with 1 being best. It is a metric
which tells us how cleanly our data is described by a certain model. Next we
will cluster our set of data - which we know has three clusters - several
times, with between 2 and 9 clusters. We will then show the results of the
clustering, and plot the fuzzy partition coefficient. When the FPC is
maximized, our data is described best.

"""

label_ = np.zeros(len(fpcs))
for i_ in range(0,len(fpcs)):
    label_[i_] = i_+2

db.push(label_, fpcs, 0, 'clusters2_fpc')

"""

As we can see, the ideal number of centers is 3. This isn't news for our
contrived example, but having the FPC available can be very useful when the
structure of your data is unclear.

Note that we started with *two* centers, not one; clustering a dataset with
only one cluster center is the trivial solution and will by definition return
FPC == 1.


====================
Classifying New Data
====================

Now that we can cluster data, the next step is often fitting new points into
an existing model. This is known as prediction. It requires both an existing
model and new data to be classified.

Building the model
------------------

We know our best model has three cluster centers. We'll rebuild a 3-cluster
model for use in prediction, generate new uniform data, and predict which
cluster to which each new data point belongs.

"""
# Regenerate fuzzy model with 3 cluster centers - note that center ordering
# is random in this clustering algorithm, so the centers may change places
cntr, u_orig, _, _, _, _, _ = _cmeans.cmeans(
    alldata, 3, 2, error=0.005, maxiter=1000)

# Show 3-cluster model
for j in range(3):
    db.push(xpts[np.argmax(u_orig, axis=0) == j], ypts[np.argmax(u_orig, axis=0) == j], j, 'clusters3')

"""

Prediction
----------

Finally, we generate uniformly sampled data over this field and classify it
via ``cmeans_predict``, incorporating it into the pre-existing model.

"""

# Generate uniformly sampled data spread across the range [0, 10] in x and y
newdata = np.zeros((2,100))
vrand = np.vectorize(_cmeans.rand)
newdata = vrand(u0) * 10

# Predict new cluster membership with `cmeans_predict` as well as
# `cntr` from the 3-cluster model
u, u0, d, jm, p, fpc = _cmeans.cmeans_predict(
    newdata, cntr, 2, error=0.005, maxiter=1000)

# Plot the classified uniform data. Note for visualization the maximum
# membership value has been taken at each point (i.e. these are hardened,
# not fuzzy results visualized) but the full fuzzy result is the output
# from cmeans_predict.
cluster_membership = np.argmax(u, axis=0)  # Hardening for visualization

for j in range(3):
    db.push(newdata[0][cluster_membership == j],
             newdata[1][cluster_membership == j], j, 'clusters4')

