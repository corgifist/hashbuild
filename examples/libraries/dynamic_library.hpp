#pragma once

#include "basic.hpp"

extern "C" {
    LIBRARY_API int sum(int a, int b);
    LIBRARY_API void print_sum(int a, int b);
}