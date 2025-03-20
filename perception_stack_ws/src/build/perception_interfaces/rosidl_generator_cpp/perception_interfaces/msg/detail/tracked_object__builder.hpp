// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from perception_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#ifndef PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_
#define PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "perception_interfaces/msg/detail/tracked_object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace perception_interfaces
{

namespace msg
{

namespace builder
{

class Init_TrackedObject_bbox
{
public:
  explicit Init_TrackedObject_bbox(::perception_interfaces::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  ::perception_interfaces::msg::TrackedObject bbox(::perception_interfaces::msg::TrackedObject::_bbox_type arg)
  {
    msg_.bbox = std::move(arg);
    return std::move(msg_);
  }

private:
  ::perception_interfaces::msg::TrackedObject msg_;
};

class Init_TrackedObject_class_name
{
public:
  explicit Init_TrackedObject_class_name(::perception_interfaces::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_bbox class_name(::perception_interfaces::msg::TrackedObject::_class_name_type arg)
  {
    msg_.class_name = std::move(arg);
    return Init_TrackedObject_bbox(msg_);
  }

private:
  ::perception_interfaces::msg::TrackedObject msg_;
};

class Init_TrackedObject_track_id
{
public:
  Init_TrackedObject_track_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrackedObject_class_name track_id(::perception_interfaces::msg::TrackedObject::_track_id_type arg)
  {
    msg_.track_id = std::move(arg);
    return Init_TrackedObject_class_name(msg_);
  }

private:
  ::perception_interfaces::msg::TrackedObject msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::perception_interfaces::msg::TrackedObject>()
{
  return perception_interfaces::msg::builder::Init_TrackedObject_track_id();
}

}  // namespace perception_interfaces

#endif  // PERCEPTION_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_
