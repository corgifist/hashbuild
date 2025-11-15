#include "static_library.hpp"
#include "basic.hpp"

extern "C" {
    LIBRARY_API int divide(int a, int b) {
        return a / b;
    }

    LIBRARY_API void print_divide(int a, int b) {
        std::cout << a << " divided by " << b << " is " << divide(a, b) << std::endl;
    }
}