# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "subscriber: 1 messages, 1 services")

set(MSG_I_FLAGS "-Isubscriber:/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(subscriber_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg/Num.msg" NAME_WE)
add_custom_target(_subscriber_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "subscriber" "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg/Num.msg" ""
)

get_filename_component(_filename "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/srv/AddTwoInts.srv" NAME_WE)
add_custom_target(_subscriber_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "subscriber" "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/srv/AddTwoInts.srv" ""
)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(subscriber
  "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/subscriber
)

### Generating Services
_generate_srv_cpp(subscriber
  "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/subscriber
)

### Generating Module File
_generate_module_cpp(subscriber
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/subscriber
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(subscriber_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(subscriber_generate_messages subscriber_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg/Num.msg" NAME_WE)
add_dependencies(subscriber_generate_messages_cpp _subscriber_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(subscriber_generate_messages_cpp _subscriber_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(subscriber_gencpp)
add_dependencies(subscriber_gencpp subscriber_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS subscriber_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(subscriber
  "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/subscriber
)

### Generating Services
_generate_srv_lisp(subscriber
  "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/subscriber
)

### Generating Module File
_generate_module_lisp(subscriber
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/subscriber
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(subscriber_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(subscriber_generate_messages subscriber_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg/Num.msg" NAME_WE)
add_dependencies(subscriber_generate_messages_lisp _subscriber_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(subscriber_generate_messages_lisp _subscriber_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(subscriber_genlisp)
add_dependencies(subscriber_genlisp subscriber_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS subscriber_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(subscriber
  "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/subscriber
)

### Generating Services
_generate_srv_py(subscriber
  "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/subscriber
)

### Generating Module File
_generate_module_py(subscriber
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/subscriber
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(subscriber_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(subscriber_generate_messages subscriber_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg/Num.msg" NAME_WE)
add_dependencies(subscriber_generate_messages_py _subscriber_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(subscriber_generate_messages_py _subscriber_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(subscriber_genpy)
add_dependencies(subscriber_genpy subscriber_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS subscriber_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/subscriber)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/subscriber
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(subscriber_generate_messages_cpp std_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/subscriber)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/subscriber
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(subscriber_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/subscriber)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/subscriber\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/subscriber
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(subscriber_generate_messages_py std_msgs_generate_messages_py)
