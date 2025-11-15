#include "dynamic_library.hpp"
#include "static_library.hpp"

int main(void) {
    std::cout << sum(34, 35) << std::endl;
    print_sum(100, -31);
    std::cout << divide(512, 2) << std::endl;
    print_divide(500, 2);
    return 0;
}