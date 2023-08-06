/*****************************************************************************
 * Copyright 2017 SoundHound, Incorporated.  All rights reserved.
 *****************************************************************************/
#include <Python.h>
#include "PhraseSpotterAPI.h"


#if PY_MAJOR_VERSION >= 3
#define FORMAT_S "y#"
#else 
#define FORMAT_S "s#"
#endif


static PyObject* okhound_ProcessSamples(PyObject* self, PyObject* args)
{
  char* samples;
  int size;

  if (!PyArg_ParseTuple(args, FORMAT_S, &samples, &size))
  {
    PyErr_SetString(PyExc_TypeError, "processSamples() takes a byte string");
    return NULL;
  }

  int result = PhraseSpotterProcessSamples(reinterpret_cast<int16_t*>(samples), size / 2);

  PyObject* ret = Py_BuildValue("i", result);

  return ret;
}


static PyObject* okhound_getThreshold(PyObject* self, PyObject* args)
{
  float result = PhraseSpotterGetThreshold();

  PyObject* ret = Py_BuildValue("f", result);

  return ret;
}


static PyObject*  okhound_setThreshold(PyObject* self, PyObject* args)
{
  float threshold;

  if (!PyArg_ParseTuple(args, "f", &threshold))
  {
    PyErr_SetString(PyExc_TypeError, "setThreshold() takes a float.");
    return NULL;
  }

  PhraseSpotterSetThreshold(threshold);
  return Py_None;
}


static PyMethodDef OkHoundMethods[] = {
  { "processSamples", okhound_ProcessSamples, METH_VARARGS, "Process 16 bit 16 kHz audio chunk, return true if the phrase is spotted." },
  { "getThreshold", okhound_getThreshold, METH_VARARGS, "Get sensitivity setting of phrase spotting." },
  { "setThreshold", okhound_setThreshold, METH_VARARGS, "Set sensitivity setting of phrase spotting." },
  { NULL, NULL, 0, NULL }
};


#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "okhound",
  NULL,
  -1,
  OkHoundMethods,
  NULL,
  NULL,
  NULL,
  NULL
};

PyMODINIT_FUNC PyInit_okhound(void)
{
  PyObject *module = PyModule_Create(&moduledef);
  return module;
}

#else

PyMODINIT_FUNC initokhound(void)
{
  Py_InitModule("okhound", OkHoundMethods);
}

#endif




