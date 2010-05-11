#from __future__ import generators

# Ensure the user is running the version of python we require.
import sys
if not hasattr(sys, "version_info") or sys.version_info < (2,3):
    raise RuntimeError("Aristoxenus requires Python 2.3 or later.")
del sys

__version__ = "0.1.0"
__author__ = "Pedro Kroger <pedro.kroger@gmail.com"
__license__ = "GPL"

