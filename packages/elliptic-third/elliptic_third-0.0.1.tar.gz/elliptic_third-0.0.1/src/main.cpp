#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

namespace py = pybind11;

PYBIND11_MODULE(elliptic_third, m) {
    m.doc() = R"pbdoc(
        Elliptic function of Third kind
        -------------------------------

        .. currentmodule:: elliptic_third

        .. autosummary::
           :toctree: _generate

           add
    )pbdoc";

    m.def("add", &add, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
