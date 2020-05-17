cmake_minimum_required(VERSION 3.16.5)

project(mod_xsendfile)

link_directories(${APACHE2_ROOT}/bin)
link_directories(${APACHE2_ROOT}/lib)

include_directories(${APACHE2_ROOT}/include)

add_library(mod_xsendfile MODULE mod_xsendfile.c)

if (_DEBUG)
add_definitions(-D_DEBUG=${_DEBUG})
endif()

target_link_libraries(mod_xsendfile libhttpd libaprutil-1 libapr-1)
set_target_properties(mod_xsendfile PROPERTIES PREFIX "" SUFFIX ".so")

if (NOT INSTALL_DIRECTORY)
    set(INSTALL_DIRECTORY ${APACHE2_ROOT}/modules)
endif ()

install(TARGETS mod_xsendfile DESTINATION ${INSTALL_DIRECTORY})
