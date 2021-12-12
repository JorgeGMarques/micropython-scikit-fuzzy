"""
===============
Defuzzification
===============

Fuzzy logic calculations are excellent tools, but to use them the fuzzy result
must be converted back into a single number. This is known as defuzzification.

There are several possible methods for defuzzification, exposed via
`skfuzzy.defuzz`.

"""
from ulab import numpy as np
from bipes import databoard as db
import defuzz as fuzz
import fuzzy_ops

from generatemf import trapmf


# Generate trapezoidal membership function on range [0, 1]
x = np.arange(0, 5.05, 0.1)
mfx = trapmf(x, [2, 2.5, 3, 4.5])

# Defuzzify this membership function five ways
defuzz_centroid = fuzz.defuzz(x, mfx, 'centroid')  # Same as skfuzzy.centroid
defuzz_bisector = fuzz.defuzz(x, mfx, 'bisector') # :
defuzz_mom = fuzz.defuzz(x, mfx, 'mom')
defuzz_som = fuzz.defuzz(x, mfx, 'som')
defuzz_lom = fuzz.defuzz(x, mfx, 'lom')

# Collect info for vertical lines
labels = ['centroid', 'bisector', 'mean of maximum', 'min of maximum',
          'max of maximum']
xvals = [defuzz_centroid,
         defuzz_bisector,
         defuzz_mom,
         defuzz_som,
         defuzz_lom]
colors = ['r', 'b', 'g', 'c', 'm']
ymax = [fuzzy_ops.interp_membership(x, mfx, i) for i in xvals]

# Display and compare defuzzification results against membership function

db.push(x, mfx, 0, 'defuzz0')
for i, (xv, y) in enumerate(zip(xvals, ymax)):
    # To make a line, push (xv,0)
    db.push(xv, 0, 1+i, 'defuzz0')
    db.push(xv, y[0], 1+i, 'defuzz0')
