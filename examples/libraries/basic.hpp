#pragma once

#include <iostream>

#ifdef EXPORTING_SYMBOLS
    #ifdef WIN32
        #define LIBRARY_API __declspec(dllexport)
    #else
        #define LIBRARY_API 
    #endif
#else
    #ifdef WIN32
        #define LIBRARY_API __declspec(dllimport)
    #else
        #define LIBRARY_API
    #endif
#endif // EXPORTING_SYMBOLS