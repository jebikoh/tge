#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>

static void bresenhams_line(int x0, int y0, float z0, int x1, int y1,
                            float z1) {
  dx = abs(x1 - x0);
  dy = -abs(y1 - y0);
  sx = x0 < x1 ? 1 : -1;
  sy = y0 < y1 ? 1 : -1;

  err = dx + dy;

  while (1) {
    }
}

static PyObject *edge_walk(PyObject *self, PyObject *args) {
  PyArrayObject *v0, *v1, *v2;
  float z0, z1, z2;
  int w, h;
  int mlen;

  if (!PyArg_ParseTuple(args, "O!O!0!fffiii", &PyArray_Type, &v0, &PyArray_Type,
                        &v1, &z0, &z1, &w, &h, &mlen)) {
    return NULL;
  }
  // Unpack vertices
  int *x0 = (int *)PyArray_GETPTR1(v0, 0);
  int *y0 = (int *)PyArray_GETPTR1(v0, 1);
  int *x1 = (int *)PyArray_GETPTR1(v1, 0);
  int *y1 = (int *)PyArray_GETPTR1(v1, 1);
  int *x2 = (int *)PyArray_GETPTR1(v2, 0);
  int *y2 = (int *)PyArray_GETPTR1(v2, 1);

  // Buffer to track visited edge points
  char *edge_buf;
  edge_buf = (char *)calloc(w * h * sizeof(char));

  // Output array
  npy_intp dims[2] = {mlen * 3, 2};
  PyObject *edge_pts = PyArray_SimpleNew(2, dims, NPY_INT32);

  // Add logic
  //   int *x0 = (int *)PyArray_GETPTR1(v0, 0);
  //   int *y0 = (int *)PyArray_GETPTR1(v0, 1);
  //   int *x1 = (int *)PyArray_GETPTR1(v1, 0);
  //   int *y1 = (int *)PyArray_GETPTR1(v1, 1);

  //   int dx = abs(*x1 - *x0);
  //   int dy = -abs(*y1 - *y0);

  //   int sx = *x0 < *x1 ? 1 : -1;
  //   int sy = *y0 < *y1 ? 1 : -1;

  //   int err = dx + dy;

  Py_RETURN_NONE;
}

static PyMethodDef EdgeWalkMethods[] = {
    {"edge_walk", bresenhams_line, METH_VARARGS,
     "Edge walk algorithm using bresehams line algorithm."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef tgec = {PyModuleDef_HEAD_INIT, "tgec", NULL, -1,
                                  EdgeWalkMethods};

PyMODINIT_FUNC PyInit_tgec(void) {
  import_array();
  return PyModule_Create(&tgec);
}