# HashBuild - sane way of writing build scripts
HashBuild allows you to write build recipes in Python using an easy-to-use, yet powerful API.
HashBuild's API is a mix of low-level build systems (such as Make and Ninja) and higher-level build systems (CMake, Meson etc.) which results in a pretty comfortable API which doesn't stand in your way.
For now, only C / C++ are supported, but that may change in the future!
Even if HashBuild doesn't support the language you would like to use, it would be very easy
to create custom build rules and invoke the compiler yourself