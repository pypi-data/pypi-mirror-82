#include <pybind11/pybind11.h>
#include <math.h>
using namespace std;

constexpr double PI = 3.14159265358979323846;

double real(double k, double n, double tolerance=1e-20, int max_iterations=100)
{
  double kn = sqrt(1-k);

  double a0 = 1;
  double g0 = kn;
  double z0 = 0;
  double dn = (1 - n)/kn;
  double en = n/(1-n);
  double zn = z0;
  double an = a0;
  double gn = g0;

  int i = 0;
  while ( i < max_iterations && (abs(an - gn) > tolerance || abs(dn-1) > tolerance)) {
    z0 = (en + zn)/2;
    en = (dn*en + zn)/(1+dn);
    zn = z0;
    a0 = (an + gn)/2;
    g0 = sqrt(an*gn);
    an = a0;
    gn = g0;
    dn = gn*(2 + dn + (1/dn))/(4*an);
    i++;
  }
      
  return PI*(1+zn)/(2*an);
}

namespace py = pybind11;

PYBIND11_MODULE(elliptic_third, m) {
    m.doc() = R"pbdoc(
        Elliptic function of Third kind
        -------------------------------

        .. currentmodule:: elliptic_third

        .. autosummary::
           :toctree: _generate

           eval
    )pbdoc";

    m.def("eval", &real, R"pbdoc(
        Evaluate the elliptic function of third kind

    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
