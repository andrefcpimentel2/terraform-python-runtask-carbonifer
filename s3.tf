resource "random_pet" "lambda_bucket_name" {
  prefix = "learn-terraform-functions"
  length = 4
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = random_pet.lambda_bucket_name.id
}

resource "aws_s3_bucket_ownership_controls" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "lambda_bucket" {
  depends_on = [aws_s3_bucket_ownership_controls.lambda_bucket]

  bucket = aws_s3_bucket.lambda_bucket.id
  acl    = "private"
}

#
# This configuration uses the archive_file data source to generate a zip archive and an 
# aws_s3_object resource to upload the archive to your S3 bucket.
#


data "archive_file" "lambda_carbonifer" {
  type = "zip"

  source_dir  = "${path.module}/carbonifer"
  output_path = "${path.module}/carbonifer.zip"
}

resource "aws_s3_object" "lambda_carbonifer" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "carbonifer.zip"
  source = data.archive_file.lambda_carbonifer.output_path

  etag = filemd5(data.archive_file.lambda_carbonifer.output_path)
}