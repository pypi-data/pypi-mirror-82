#include "word_freq_utils.hpp"

#include <vector>
#include <string>
#include <boost/regex.hpp>


const static boost::regex esc("[.^$|()\\[\\]{}*+?\\\\]");


void merge_pair_in_py_dict_impl(PyObject* py_dict_str_long, PyObject* py_tuple_pair)
{
    const char* first_c_str = PyBytes_AsString(PyTuple_GetItem(py_tuple_pair, 0));
    const char* second_c_str = PyBytes_AsString(PyTuple_GetItem(py_tuple_pair, 1));
    std::string first(first_c_str);
    std::string second(second_c_str);
    std::string merged = first + second;

    std::string bigrams = boost::regex_replace(first + " " + second, esc, "\\\\&", boost::match_default | boost::format_sed);

    std::string reg_string = "(?<!\\S)" + bigrams + "(?!\\S)";
    boost::regex reg(reg_string);


    PyObject* key, * value;
    Py_ssize_t pos = 0;
    PyObject* py_dict_copy = PyDict_Copy(py_dict_str_long);
    while (PyDict_Next(py_dict_str_long, &pos, &key, &value))
    {
        const char* current_key_c_str = PyBytes_AsString(key);

        const std::string current_key(current_key_c_str);

        const std::string new_key = boost::regex_replace(current_key, reg, merged);

        PyObject* py_key_bytes = PyBytes_FromString(current_key.c_str());
        PyObject* py_new_key_bytes = PyBytes_FromString(new_key.c_str());
        PyDict_DelItem(py_dict_str_long, py_key_bytes);
        PyDict_SetItem(py_dict_str_long, py_new_key_bytes, value);
        Py_DECREF(py_key_bytes);
        Py_DECREF(py_new_key_bytes);
    }

    Py_DECREF(py_dict_copy);
}
