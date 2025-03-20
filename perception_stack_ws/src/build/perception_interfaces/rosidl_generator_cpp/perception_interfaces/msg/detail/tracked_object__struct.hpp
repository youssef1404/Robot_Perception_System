// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from perception_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#ifndef PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_HPP_
#define PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__perception_interfaces__msg__TrackedObject __attribute__((deprecated))
#else
# define DEPRECATED__perception_interfaces__msg__TrackedObject __declspec(deprecated)
#endif

namespace perception_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TrackedObject_
{
  using Type = TrackedObject_<ContainerAllocator>;

  explicit TrackedObject_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->track_id = 0l;
      this->class_name = "";
      std::fill<typename std::array<float, 4>::iterator, float>(this->bbox.begin(), this->bbox.end(), 0.0f);
    }
  }

  explicit TrackedObject_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : class_name(_alloc),
    bbox(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->track_id = 0l;
      this->class_name = "";
      std::fill<typename std::array<float, 4>::iterator, float>(this->bbox.begin(), this->bbox.end(), 0.0f);
    }
  }

  // field types and members
  using _track_id_type =
    int32_t;
  _track_id_type track_id;
  using _class_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _class_name_type class_name;
  using _bbox_type =
    std::array<float, 4>;
  _bbox_type bbox;

  // setters for named parameter idiom
  Type & set__track_id(
    const int32_t & _arg)
  {
    this->track_id = _arg;
    return *this;
  }
  Type & set__class_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->class_name = _arg;
    return *this;
  }
  Type & set__bbox(
    const std::array<float, 4> & _arg)
  {
    this->bbox = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    perception_interfaces::msg::TrackedObject_<ContainerAllocator> *;
  using ConstRawPtr =
    const perception_interfaces::msg::TrackedObject_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<perception_interfaces::msg::TrackedObject_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<perception_interfaces::msg::TrackedObject_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      perception_interfaces::msg::TrackedObject_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<perception_interfaces::msg::TrackedObject_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      perception_interfaces::msg::TrackedObject_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<perception_interfaces::msg::TrackedObject_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<perception_interfaces::msg::TrackedObject_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<perception_interfaces::msg::TrackedObject_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__perception_interfaces__msg__TrackedObject
    std::shared_ptr<perception_interfaces::msg::TrackedObject_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__perception_interfaces__msg__TrackedObject
    std::shared_ptr<perception_interfaces::msg::TrackedObject_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TrackedObject_ & other) const
  {
    if (this->track_id != other.track_id) {
      return false;
    }
    if (this->class_name != other.class_name) {
      return false;
    }
    if (this->bbox != other.bbox) {
      return false;
    }
    return true;
  }
  bool operator!=(const TrackedObject_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TrackedObject_

// alias to use template instance with default allocator
using TrackedObject =
  perception_interfaces::msg::TrackedObject_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace perception_interfaces

#endif  // PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_HPP_
