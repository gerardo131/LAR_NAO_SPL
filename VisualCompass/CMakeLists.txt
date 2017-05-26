cmake_minimum_required(VERSION 2.8)
project(VisualCompass)

find_package(qibuild)

option(VISUALCOMPASS_IS_REMOTE
  "El módulo es compilado como un módulo remoto (ON u OFF)"
  ON)


# Create a list of source files
set(_srcs
  visualcompass.cpp
  visualcompass.h
  main.cpp)

if(VISUALCOMPASS_IS_REMOTE)
  add_definitions( " -DVISUALCOMPASS_IS_REMOTE ")

  # Create a executable named VisualCompass
  # with the source file: main.cpp
  qi_create_bin(VisualCompass ${_srcs})

  # Add a simple test:
  # enable_testing()
  # qi_create_test(test_VisualCompass "test.cpp")

  # Tell CMake that myproject depends on ALCOMMON.
  # This will set the libraries to link myproject with,
  # the include paths, and so on
  qi_use_lib(VisualCompass ALCOMMON OPENCV2_CORE OPENCV2_HIGHGUI)
else()
  # Create a plugin, that is a shared library, and make
  # sure it is built in lib/naoqi
  qi_create_lib(VisualCompass SHARED ${_srcs} SUBFOLDER naoqi)

  # Tell CMake that mymodule depends on ALCOMMON.
  # This will set the libraries to link mymodule with,
  # the include paths, and so on
  qi_use_lib(VisualCompass ALCOMMON BOOST)
endif()
