resource "aws_s3_bucket" "bucket" {
  bucket = "firehose-delivery-stream-destination-bis"
  acl = "private"
}