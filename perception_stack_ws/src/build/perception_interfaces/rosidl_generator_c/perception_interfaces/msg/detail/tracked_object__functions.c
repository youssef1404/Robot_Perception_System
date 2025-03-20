// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from perception_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice
#include "perception_interfaces/msg/detail/tracked_object__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `class_name`
#include "rosidl_runtime_c/string_functions.h"

bool
perception_interfaces__msg__TrackedObject__init(perception_interfaces__msg__TrackedObject * msg)
{
  if (!msg) {
    return false;
  }
  // track_id
  // class_name
  if (!rosidl_runtime_c__String__init(&msg->class_name)) {
    perception_interfaces__msg__TrackedObject__fini(msg);
    return false;
  }
  // bbox
  return true;
}

void
perception_interfaces__msg__TrackedObject__fini(perception_interfaces__msg__TrackedObject * msg)
{
  if (!msg) {
    return;
  }
  // track_id
  // class_name
  rosidl_runtime_c__String__fini(&msg->class_name);
  // bbox
}

bool
perception_interfaces__msg__TrackedObject__are_equal(const perception_interfaces__msg__TrackedObject * lhs, const perception_interfaces__msg__TrackedObject * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // track_id
  if (lhs->track_id != rhs->track_id) {
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->class_name), &(rhs->class_name)))
  {
    return false;
  }
  // bbox
  for (size_t i = 0; i < 4; ++i) {
    if (lhs->bbox[i] != rhs->bbox[i]) {
      return false;
    }
  }
  return true;
}

bool
perception_interfaces__msg__TrackedObject__copy(
  const perception_interfaces__msg__TrackedObject * input,
  perception_interfaces__msg__TrackedObject * output)
{
  if (!input || !output) {
    return false;
  }
  // track_id
  output->track_id = input->track_id;
  // class_name
  if (!rosidl_runtime_c__String__copy(
      &(input->class_name), &(output->class_name)))
  {
    return false;
  }
  // bbox
  for (size_t i = 0; i < 4; ++i) {
    output->bbox[i] = input->bbox[i];
  }
  return true;
}

perception_interfaces__msg__TrackedObject *
perception_interfaces__msg__TrackedObject__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  perception_interfaces__msg__TrackedObject * msg = (perception_interfaces__msg__TrackedObject *)allocator.allocate(sizeof(perception_interfaces__msg__TrackedObject), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(perception_interfaces__msg__TrackedObject));
  bool success = perception_interfaces__msg__TrackedObject__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
perception_interfaces__msg__TrackedObject__destroy(perception_interfaces__msg__TrackedObject * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    perception_interfaces__msg__TrackedObject__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
perception_interfaces__msg__TrackedObject__Sequence__init(perception_interfaces__msg__TrackedObject__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  perception_interfaces__msg__TrackedObject * data = NULL;

  if (size) {
    data = (perception_interfaces__msg__TrackedObject *)allocator.zero_allocate(size, sizeof(perception_interfaces__msg__TrackedObject), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = perception_interfaces__msg__TrackedObject__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        perception_interfaces__msg__TrackedObject__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
perception_interfaces__msg__TrackedObject__Sequence__fini(perception_interfaces__msg__TrackedObject__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      perception_interfaces__msg__TrackedObject__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

perception_interfaces__msg__TrackedObject__Sequence *
perception_interfaces__msg__TrackedObject__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  perception_interfaces__msg__TrackedObject__Sequence * array = (perception_interfaces__msg__TrackedObject__Sequence *)allocator.allocate(sizeof(perception_interfaces__msg__TrackedObject__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = perception_interfaces__msg__TrackedObject__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
perception_interfaces__msg__TrackedObject__Sequence__destroy(perception_interfaces__msg__TrackedObject__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    perception_interfaces__msg__TrackedObject__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
perception_interfaces__msg__TrackedObject__Sequence__are_equal(const perception_interfaces__msg__TrackedObject__Sequence * lhs, const perception_interfaces__msg__TrackedObject__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!perception_interfaces__msg__TrackedObject__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
perception_interfaces__msg__TrackedObject__Sequence__copy(
  const perception_interfaces__msg__TrackedObject__Sequence * input,
  perception_interfaces__msg__TrackedObject__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(perception_interfaces__msg__TrackedObject);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    perception_interfaces__msg__TrackedObject * data =
      (perception_interfaces__msg__TrackedObject *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!perception_interfaces__msg__TrackedObject__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          perception_interfaces__msg__TrackedObject__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!perception_interfaces__msg__TrackedObject__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
