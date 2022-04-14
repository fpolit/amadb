cmake_minimum_required(VERSION 3.5)

project(amadb
  VERSION 1.0.3
  DESCRIPTION "Ama-Framework database"
  HOMEPAGE_URL https://github.com/fpolit/amadb
)

set(PROJECT_LICENSE "GPLv3")
# options
option(CMAKE_BUILD_TESTS  "Build unittest" OFF)

# Finding dependencies
find_package(Protobuf REQUIRED)
find_package(Python3  COMPONENTS Interpreter Development REQUIRED)

## enviroment INFO
message(DEBUG "PROJECT_VERSION: ${CMAKE_PROJECT_VERSION}")
message(DEBUG "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")
message(DEBUG "CMAKE_BUILD_TESTS: ${CMAKE_BUILD_TESTS}")
message(DEBUG "GIT_UPDATE_SUBMODULES: ${GIT_UPDATE_SUBMODULES}")
message(DEBUG "CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message(DEBUG "CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")
message(DEBUG "Python3_VERSION: ${Python3_VERSION}")
message(DEBUG "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")

# Updating git submodules
find_package(Git)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/.git")
    # Update submodules as needed
    option(GIT_UPDATE_SUBMODULES "Check submodules during build" ON)
    message(DEBUG "GIT_EXECUTABLE: ${GIT_EXECUTABLE}")
    if(GIT_UPDATE_SUBMODULES)
      execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init --recursive
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      RESULT_VARIABLE GIT_SUBMOD_RESULT)
    if(NOT GIT_SUBMOD_RESULT EQUAL "0")
      message(FATAL_ERROR "git submodule update --init --recursive failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
    endif()
  endif()
endif()

# python package (amadb)
set(PYTHON_PKG_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/amadb")
set(PYTHON_PKG_PROTO_DIR "${PYTHON_PKG_SOURCE_DIR}/proto")
set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
set(INIT_PY_IN  "${PYTHON_PKG_SOURCE_DIR}/__init__.py.in")
set(INIT_PY     "${PYTHON_PKG_SOURCE_DIR}/__init__.py")
set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build")
set(TIMESTAMP   "${OUTPUT}/timestamp")

if(${CMAKE_BUILD_TYPE} STREQUAL "Debug")
  set(REQUIREMENTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements-dev.txt")
else()
  set(REQUIREMENTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt")
endif()

# protobuf generation and copy to AMADB_PY_PROTO_DESTINATION
if(NOT CMAKE_BUILD_AMADB_PY_PROTO AND NOT CMAKE_BUILD_AMADB_CXX_PROTO)
  message(FATAL_ERROR "No proto buffer files will be generated (Enable at least one variable: CMAKE_BUILD_AMADB_PY_PROTO  or CMAKE_BUILD_AMADB_CXX_PROTO)")
endif()

set(AMADB_PROTO_DESTINATION ${PYTHON_PKG_PROTO_DIR})
add_subdirectory(proto) # generated target: amadb_protos


message(DEBUG "PYTHON_PKG_PROTO_DIR: ${PYTHON_PKG_PROTO_DIR}")
message(DEBUG "PYTHON_PKG_SOURCE_DIR: ${PYTHON_PKG_SOURCE_DIR}")
message(DEBUG "Python requirements: ${REQUIREMENTS}")

configure_file(${SETUP_PY_IN} ${SETUP_PY})
configure_file(${INIT_PY_IN} ${INIT_PY})

add_custom_target(pybuild ALL
  COMMAND ${Python3_EXECUTABLE} ${SETUP_PY} build --verbose
  DEPENDS amadb_protos
)

# add_custom_target(pybuild ALL DEPENDS ${TIMESTAMP})
install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} -m pip install -r ${REQUIREMENTS})")
install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} ${SETUP_PY} install --verbose)")

if(CMAKE_BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
  add_custom_target(pytest
    COMMAND ${Python3_EXECUTABLE} -m pytest -v ${CMAKE_CURRENT_SOURCE_DIR}/tests)
endif()
