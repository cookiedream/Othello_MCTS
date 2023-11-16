from setuptools import setup
from Cython.Build import cythonize
import numpy as np
setup(
    ext_modules = cythonize("./CY_OthelloUtil.pyx", annotate=True, language_level=3),
    include_dirs=[np.get_include()]
)
#python setup.py build_ext --inplace
