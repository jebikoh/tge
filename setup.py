from setuptools import setup, Extension, find_packages
import subprocess
import numpy

python_cflags = subprocess.getoutput("python3-config --cflags").split()
python_ldflags = subprocess.getoutput("python3-config --ldflags").split() + [
    "-lpython3.12"
]
numpy_include = numpy.get_include()

# Define the extension module
tgec_module = Extension(
    "tge.tgec",
    sources=["tgec/src/edge_walk.c"],
    include_dirs=[numpy_include],
    extra_compile_args=["-Wall", "-Werror", "-fPIC"] + python_cflags,
    extra_link_args=python_ldflags,
    language="c",
)

setup(name="tgec", version="0.0.1", packages=find_packages(), ext_modules=[tgec_module])
