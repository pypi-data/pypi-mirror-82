#ifndef WORD_FREQ_UTILS_HPP
#define WORD_FREQ_UTILS_HPP
#ifdef __cplusplus
extern "C" {
#endif
#include <Python.h>
#ifdef __cplusplus
}

void merge_pair_in_py_dict_impl(PyObject* py_dict_str_long, PyObject* py_tuple_pair);

#endif
#endif // !WORD_FREQ_UTILS_HPP
