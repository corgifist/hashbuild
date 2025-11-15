#include "dynamic_library.hpp"

extern "C" {
    LIBRARY_API int sum(int a, int b) {
        return a + b;
    }

    LIBRARY_API void print_sum(int a, int b) {
        std::cout << "sum of " << a << " and " << b << " is " << sum(a, b) << std::endl;
    }
}