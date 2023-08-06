#include "word_freq_utils.hpp"
#include "string_utils.hpp"
#include <exception>


#ifdef __cplusplus
extern "C" {
#endif


#include <string.h>


PyObject* merge_pair_in_py_dict_method(PyObject* self, PyObject* args)
{
    PyObject* py_dict = NULL;
    PyObject* py_tuple = NULL;

    if (!PyArg_ParseTuple(args, "OO", &py_dict, &py_tuple))
        return NULL;

    merge_pair_in_py_dict_impl(py_dict, py_tuple);

    Py_RETURN_NONE;
}


PyObject* py_dict_make_symbol_freqs_from_WordFreq_dict_c_impl(PyObject* word_freq)
{
    PyObject* symbol_freqs = PyDict_New();

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while (PyDict_Next(word_freq, &pos, &key, &value))
    {
        const char* word = PyBytes_AsString(key);
        size_t element_num;
        char** symbols = split_word(word, &element_num);

        if (!symbols)
            return nullptr;

        for (size_t i = 1; i < element_num; ++i)
        {
            unsigned long long update_freq = PyLong_AsUnsignedLongLong(value);
            PyObject* symbol_pair_key = PyTuple_New(2);

            if (!symbol_pair_key)
            {
                for (size_t i = 0; i < element_num; ++i)
                    free(symbols[i]);
                free(symbols);

                return NULL;
            }

            try
            {
                PyObject* first = PyBytes_FromString(symbols[i - 1]);
                PyObject* second = PyBytes_FromString(symbols[i]);

                PyTuple_SetItem(symbol_pair_key, 0, first);
                PyTuple_SetItem(symbol_pair_key, 1, second);

                PyObject* py_old_freq = PyDict_GetItem(symbol_freqs, symbol_pair_key);
                if (py_old_freq)
                {
                    unsigned long long old_freq = PyLong_AsUnsignedLongLong(py_old_freq);
                    PyObject* py_long = PyLong_FromUnsignedLongLong(old_freq + update_freq);
                    PyDict_SetItem(symbol_freqs, symbol_pair_key, py_long);
                    Py_DECREF(py_long);
                }
                else
                {
                    PyObject* py_long = PyLong_FromUnsignedLongLong(update_freq);
                    PyDict_SetItem(symbol_freqs, symbol_pair_key, py_long);
                    Py_DECREF(py_long);
                }

                Py_DECREF(symbol_pair_key);
            }
            catch (const std::exception& err)
            {
                for (size_t i = 0; i < element_num; ++i)
                    free(symbols[i]);
                free(symbols);

                return NULL;
            }
        }

        for (size_t i = 0; i < element_num; ++i)
            free(symbols[i]);
        free(symbols);
    }

    return symbol_freqs;
}


PyObject* py_dict_make_symbol_freqs_from_WordFreq_dict_method(PyObject* self, PyObject* args)
{
    PyObject* word_freq = NULL;

    if (!PyArg_ParseTuple(args, "O", &word_freq))
        return NULL;

    return py_dict_make_symbol_freqs_from_WordFreq_dict_c_impl(word_freq);
}


char* split_bytes_and_add_boundary(const char* bytes, const char* left_bound, const char* right_bound)
{
    // 'split_me' -> '<w> s p l i t _ m e <w>'
    const size_t length = strlen(bytes);
    if (length <= 0)
    {
        char* empty_string = (char*)malloc(sizeof(char));

        if (!empty_string)
            return NULL;

        empty_string[0] = '\x0';
        return empty_string;
    }

    size_t left_pad = strlen(left_bound);
    size_t right_pad = strlen(right_bound);
    const size_t new_length = 2 * length - 1 + left_pad + right_pad + 2;

    char* splitted_with_bounds = (char*)malloc((new_length + 1) * sizeof(char));

    if (!splitted_with_bounds)
        return NULL;

    for (size_t i = 0; i < length; ++i)
    {
        splitted_with_bounds[2 * i + left_pad + 1] = bytes[i];
        splitted_with_bounds[2 * i + left_pad + 2] = ' ';
    }
    strcpy(splitted_with_bounds, left_bound);
    splitted_with_bounds[left_pad] = ' ';
    strcpy(splitted_with_bounds + (new_length - right_pad), right_bound);


    splitted_with_bounds[new_length] = '\x0';
    return splitted_with_bounds;
}


PyObject* py_split_bytes_in_py_iterable_and_add_boundary_impl(PyObject* py_iterable, const char* left_bound, const char* right_bound)
{
    Py_ssize_t size;
    if ((size = PyObject_Length(py_iterable)) < 0)
        return NULL;

    PyObject* py_list = PyList_New(size);
    PyObject* iterator = PyObject_GetIter(py_iterable);
    PyObject* item = NULL;
    Py_ssize_t index = 0;
    while ((item = PyIter_Next(iterator)))
    {
        const char* bytes = PyBytes_AsString(item);
        char* split_bytes = split_bytes_and_add_boundary(bytes, left_bound, right_bound);

        PyList_SET_ITEM(py_list, index, PyBytes_FromString(split_bytes));
        ++index;

        free(split_bytes);
        Py_DECREF(item);
    }
    Py_DECREF(iterator);

    return py_list;
}


PyObject* py_split_bytes_in_py_iterable_and_add_boundary_method(PyObject* self, PyObject* args)
{
    PyObject* iterable;
    const char* left_bound;
    const char* right_bound;

    if (!PyArg_ParseTuple(args, "Oyy", &iterable, &left_bound, &right_bound))
        return NULL;

    return py_split_bytes_in_py_iterable_and_add_boundary_impl(iterable, left_bound, right_bound);
}


PyMethodDef bpelibc_methods[] = {
    {
        "make_symbol_freqs_from_WordFreq",
        py_dict_make_symbol_freqs_from_WordFreq_dict_method, METH_VARARGS,
        "Python interface for extracting symbols from a WordFreq dictionary."
    },
    {
        "split_bytes_in_iterable_and_add_boundary",
        py_split_bytes_in_py_iterable_and_add_boundary_method, METH_VARARGS,
        "Python interface for splitting whitespace delimited byte-string and adding <start_of_word> and <end_of_word> tokens at the boundaries."
    },
    {
        "merge_pair_in_dict",
        merge_pair_in_py_dict_method, METH_VARARGS,
        "Python interface for merging pairs inside dictionary keys."
    },
    {NULL, NULL, 0, NULL}
};


struct PyModuleDef bpelibc_module = {
    PyModuleDef_HEAD_INIT,
    "bpelibc",
    "Python interface for the bpelibc C library functions",
    -1,
    bpelibc_methods
};

PyMODINIT_FUNC PyInit_bpelibc(void)
{ return PyModule_Create(&bpelibc_module); }


#ifdef __cplusplus
}
#endif