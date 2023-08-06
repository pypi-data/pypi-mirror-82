/*
 * termial-random - A termial random implementation.
 * Copyright(C) 2020 Fridolin Pokorny
 *
 * This program is free software: you can redistribute it and / or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * See:
 *  https://medium.com/@fridex/termial-random-for-prioritized-picking-an-item-from-a-list-a65a4f563224
 *  https://medium.com/@fridex/optimizing-termial-random-by-removing-binomial-coefficient-e39b9ca7aaa3
 */

#include <Python.h>

#include <math.h>
#include <stdlib.h>
#include <time.h>

static PyObject *termial_seed_init(PyObject *self) {
  time_t t;
  srand((unsigned)time(&t));
  Py_RETURN_NONE;
}

static PyObject *termial_seed(PyObject *self, PyObject *num) {
  unsigned long n;

  if (!PyArg_ParseTuple(num, "l", &n))
    return NULL;

  srand(n);
  Py_RETURN_NONE;
}

static PyObject *termial_random(PyObject *self, PyObject *num) {
  unsigned long n;

  if (!PyArg_ParseTuple(num, "k", &n))
    return NULL;

  unsigned long termial_of_n = ((n * n) + n) >> 1;
  unsigned long choice = rand() % termial_of_n;
  return PyLong_FromUnsignedLong(
      n - 1 - (unsigned long)(-0.5 + sqrt(0.25 + (choice << 1))));
}

PyMethodDef random_funcs[] = {
    {"random", (PyCFunction)termial_random, METH_VARARGS,
     "Compute termial random of the given N."},
    {"seed_init", (PyCFunction)termial_seed_init, METH_NOARGS,
     "Initialize random number generator."},
    {"seed", (PyCFunction)termial_seed, METH_VARARGS,
     "Initialize random number generator with the given integer."},
    {NULL}};

PyModuleDef random_mod = {PyModuleDef_HEAD_INIT,
                          "random",
                          "Implementation of termial random generator.",
                          -1,
                          random_funcs,
                          NULL,
                          NULL,
                          NULL,
                          NULL};

PyMODINIT_FUNC PyInit_random(void) { return PyModule_Create(&random_mod); }
