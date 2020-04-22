provider "aws" {
  region = var.region
}

module "buckets" {
  source = "./buckets"
}

resource "aws_iam_role" "firehose_role" {
  name = "firehose_test_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3-full-access-policy-attachment" {
  role = aws_iam_role.firehose_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_kinesis_firehose_delivery_stream" "firehose_streams_to_s3" {
  for_each = {
    (var.car_stream_name) = "cables/"
    (var.user_stream_name) = "users/"
  }

  name = each.key
  destination = "extended_s3"
  server_side_encryption {
    enabled = true
  }


  extended_s3_configuration {
    role_arn = aws_iam_role.firehose_role.arn
    bucket_arn = module.buckets.s3_bucket_name
    prefix = each.value
    buffer_interval = 60
    buffer_size = 128
  }
}
