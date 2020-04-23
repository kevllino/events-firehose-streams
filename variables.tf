variable "region" {
  type = string
  default = "eu-west-2"
}

variable "car_stream_name" {
  type = string
  default = "car-firehose-stream"
}

variable "user_stream_name" {
  type = string
  default = "user-firehose-stream"
}