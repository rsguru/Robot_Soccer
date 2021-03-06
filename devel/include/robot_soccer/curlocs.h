// Generated by gencpp from file robot_soccer/curlocs.msg
// DO NOT EDIT!


#ifndef ROBOT_SOCCER_MESSAGE_CURLOCS_H
#define ROBOT_SOCCER_MESSAGE_CURLOCS_H

#include <ros/service_traits.h>


#include <robot_soccer/curlocsRequest.h>
#include <robot_soccer/curlocsResponse.h>


namespace robot_soccer
{

struct curlocs
{

typedef curlocsRequest Request;
typedef curlocsResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct curlocs
} // namespace robot_soccer


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::robot_soccer::curlocs > {
  static const char* value()
  {
    return "0c8e4620cde9c3b16d1cfbdddb8c721c";
  }

  static const char* value(const ::robot_soccer::curlocs&) { return value(); }
};

template<>
struct DataType< ::robot_soccer::curlocs > {
  static const char* value()
  {
    return "robot_soccer/curlocs";
  }

  static const char* value(const ::robot_soccer::curlocs&) { return value(); }
};


// service_traits::MD5Sum< ::robot_soccer::curlocsRequest> should match 
// service_traits::MD5Sum< ::robot_soccer::curlocs > 
template<>
struct MD5Sum< ::robot_soccer::curlocsRequest>
{
  static const char* value()
  {
    return MD5Sum< ::robot_soccer::curlocs >::value();
  }
  static const char* value(const ::robot_soccer::curlocsRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::robot_soccer::curlocsRequest> should match 
// service_traits::DataType< ::robot_soccer::curlocs > 
template<>
struct DataType< ::robot_soccer::curlocsRequest>
{
  static const char* value()
  {
    return DataType< ::robot_soccer::curlocs >::value();
  }
  static const char* value(const ::robot_soccer::curlocsRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::robot_soccer::curlocsResponse> should match 
// service_traits::MD5Sum< ::robot_soccer::curlocs > 
template<>
struct MD5Sum< ::robot_soccer::curlocsResponse>
{
  static const char* value()
  {
    return MD5Sum< ::robot_soccer::curlocs >::value();
  }
  static const char* value(const ::robot_soccer::curlocsResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::robot_soccer::curlocsResponse> should match 
// service_traits::DataType< ::robot_soccer::curlocs > 
template<>
struct DataType< ::robot_soccer::curlocsResponse>
{
  static const char* value()
  {
    return DataType< ::robot_soccer::curlocs >::value();
  }
  static const char* value(const ::robot_soccer::curlocsResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // ROBOT_SOCCER_MESSAGE_CURLOCS_H
