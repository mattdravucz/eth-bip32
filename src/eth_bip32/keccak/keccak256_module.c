#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "keccak256.h"

static PyObject* py_keccak256(PyObject* self, PyObject* args) {
    const char* input;
    Py_ssize_t input_len;

    if (!PyArg_ParseTuple(args, "s#", &input, &input_len)) {
        return NULL;
    }

    unsigned char output[32];
    SHA3_CTX ctx;
    keccak_init(&ctx);
    keccak_update(&ctx, (unsigned char*)input, (uint16_t)input_len);
    keccak_final(&ctx, output);

    return Py_BuildValue("y#", output, 32);
}

static PyMethodDef KeccakMethods[] = {
    {"keccak256", py_keccak256, METH_VARARGS, "Calculate the Keccak-256 hash of the input"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef keccak256module = {
    PyModuleDef_HEAD_INIT,
    "_keccak256",
    NULL,
    -1,
    KeccakMethods
};

PyMODINIT_FUNC PyInit__keccak256(void) {
    return PyModule_Create(&keccak256module);
}
