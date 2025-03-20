// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from perception_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "perception_interfaces/msg/detail/tracked_object__rosidl_typesupport_introspection_c.h"
#include "perception_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "perception_interfaces/msg/detail/tracked_object__functions.h"
#include "perception_interfaces/msg/detail/tracked_object__struct.h"


// Include directives for member types
// Member `class_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  perception_interfaces__msg__TrackedObject__init(message_memory);
}

void perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_fini_function(void * message_memory)
{
  perception_interfaces__msg__TrackedObject__fini(message_memory);
}

size_t perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__size_function__TrackedObject__bbox(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_const_function__TrackedObject__bbox(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_function__TrackedObject__bbox(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__fetch_function__TrackedObject__bbox(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_const_function__TrackedObject__bbox(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__assign_function__TrackedObject__bbox(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_function__TrackedObject__bbox(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_member_array[3] = {
  {
    "track_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(perception_interfaces__msg__TrackedObject, track_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "class_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(perception_interfaces__msg__TrackedObject, class_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bbox",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(perception_interfaces__msg__TrackedObject, bbox),  // bytes offset in struct
    NULL,  // default value
    perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__size_function__TrackedObject__bbox,  // size() function pointer
    perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_const_function__TrackedObject__bbox,  // get_const(index) function pointer
    perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_function__TrackedObject__bbox,  // get(index) function pointer
    perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__fetch_function__TrackedObject__bbox,  // fetch(index, &value) function pointer
    perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__assign_function__TrackedObject__bbox,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_members = {
  "perception_interfaces__msg",  // message namespace
  "TrackedObject",  // message name
  3,  // number of fields
  sizeof(perception_interfaces__msg__TrackedObject),
  perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_member_array,  // message members
  perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_init_function,  // function to initialize message memory (memory has to be allocated)
  perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_type_support_handle = {
  0,
  &perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_perception_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, perception_interfaces, msg, TrackedObject)() {
  if (!perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_type_support_handle.typesupport_identifier) {
    perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &perception_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
