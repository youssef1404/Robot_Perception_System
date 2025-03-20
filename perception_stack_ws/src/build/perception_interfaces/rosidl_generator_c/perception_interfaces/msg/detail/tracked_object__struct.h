// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from perception_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#ifndef PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_
#define PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'class_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/TrackedObject in the package perception_interfaces.
typedef struct perception_interfaces__msg__TrackedObject
{
  int32_t track_id;
  rosidl_runtime_c__String class_name;
  float bbox[4];
} perception_interfaces__msg__TrackedObject;

// Struct for a sequence of perception_interfaces__msg__TrackedObject.
typedef struct perception_interfaces__msg__TrackedObject__Sequence
{
  perception_interfaces__msg__TrackedObject * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} perception_interfaces__msg__TrackedObject__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_
