"""

Example of using time.time() for checking which parts of the code
take the longest to run.

"""

import time
import numpy as np

t0=time.time()
A=np.random.uniform(0, 1, [1000, 2000])
B=np.random.uniform(0, 1, [A.shape[1], 300])
t1=time.time()
print("Making matrices: %.3f sec" % (t1-t0))

C=np.dot(A, B)
t2=time.time()
print("Matrix multiplication: %.3f sec" % (t2-t1))

pInv=np.linalg.pinv(A)
t3=time.time()
print("Pseudo-inverse: %.3f sec" % (t3-t2))

u, s, vh=np.linalg.svd(A)
t4=time.time()
print("SVD: %.3f sec" % (t4-t3))

print("All: %.3f sec" % (t4-t0))

# Output when running this code on my laptop:
#
#   Making matrices: 0.054 sec
#   Matrix multiplication: 0.094 sec
#   Pseudo-inverse: 1.642 sec
#   SVD: 1.931 sec
#   All: 3.721 sec
#
# These are not super-accurate benchmarks, but the idea is to look at the
# order-of-magnitude, if you are deciding which parts of the code could use
# a speed-up (if possible)
#
# For individual routines like this, you could use %timeit in IPython instead
# (which will give acccurate benchmarks)
