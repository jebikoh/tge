#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>

// static int bresenhams_line(int x0, int y0, float z0, int x1, int y1, float
// z1,
//                            char *edge_buf, PyArrayObject *edge_pts,
//                            PyArrayObject *edge_zs, int i, int w, int h) {
//   int dx = abs(x1 - x0);
//   int dy = -abs(y1 - y0);
//   int sx = x0 < x1 ? 1 : -1;
//   int sy = y0 < y1 ? 1 : -1;

//   int err = dx + dy;

//   int t = 0;
//   while (1) {
//     if (x0 >= 0 && x0 < w && y0 >= 0 && y0 < h && !edge_buf[x0 + y0 * w]) {
//       edge_buf[x0 + y0 * w] = 1;
//       int *edge_pt = (int *)PyArray_GETPTR2(edge_pts, i, 0);
//       edge_pt[0] = x0;
//       edge_pt[1] = y0;
//       float *edge_z = (float *)PyArray_GETPTR1(edge_zs, i);
//       edge_z[0] = z0 + (z1 - z0) * t;
//       i++;
//     }

//     if (x0 == x1 && y0 == y1) {
//       break;
//     }

//     int e2 = 2 * err;
//     if (e2 >= dy) {
//       err += dy;
//       x0 += sx;
//     }
//     if (e2 <= dx) {
//       err += dx;
//       y0 += sy;
//     }
//     t += 1;
//   }
//   return i;
// }

static PyObject *edge_walk(PyObject *self, PyObject *args) {
  // PyArrayObject *edge_pts, *edge_zs;
  // PyArrayObject *v0, *v1, *v2;
  // float z0, z1, z2;
  // int w, h;

  // if (!PyArg_ParseTuple(args, "O!O!O!O!O!fffii", &PyArray_Type, &edge_pts,
  //                       &PyArray_Type, &edge_zs, &PyArray_Type, &v0,
  //                       &PyArray_Type, &v1, &PyArray_Type, &v2, &z0, &z1,
  //                       &z2, &w, &h)) {
  //   return NULL;
  // }

  // // Unpack vertices
  // int x0 = *(int *)PyArray_GETPTR1(v0, 0);
  // int y0 = *(int *)PyArray_GETPTR1(v0, 1);
  // int x1 = *(int *)PyArray_GETPTR1(v1, 0);
  // int y1 = *(int *)PyArray_GETPTR1(v1, 1);
  // int x2 = *(int *)PyArray_GETPTR1(v2, 0);
  // int y2 = *(int *)PyArray_GETPTR1(v2, 1);

  // // Buffer to track visited edge points
  // char *edge_buf;
  // edge_buf = (char *)calloc(w * h, sizeof(char));

  // int i = 0;
  // i = bresenhams_line(x0, y0, z0, x1, y1, z1, edge_buf, edge_pts, edge_zs, i,
  // w,
  //                     h);
  // i = bresenhams_line(x1, y1, z1, x2, y2, z2, edge_buf, edge_pts, edge_zs, i,
  // w,
  //                     h);
  // i = bresenhams_line(x2, y2, z2, x0, y0, z0, edge_buf, edge_pts, edge_zs, i,
  // w,
  //                     h);

  // free(edge_buf);

  return Py_BuildValue("i", 0);
}

static PyMethodDef EdgeWalkMethods[] = {
    {"edge_walk", edge_walk, METH_VARARGS,
     "Edge walk algorithm using bresehams line algorithm."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef tgec = {PyModuleDef_HEAD_INIT, "tgec", NULL, -1,
                                  EdgeWalkMethods};

PyMODINIT_FUNC PyInit_tgec(void) {
  import_array();
  if (PyErr_Occurred()) {
    return NULL;
  }
  return PyModule_Create(&tgec);
}