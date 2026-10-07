# 버킷 생성명 -> 랜덤
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# 버킷 생성
resource "aws_s3_bucket" "deploy" {
  bucket        = "${var.project_name}-deploy-${random_id.bucket_suffix.hex}"
  force_destroy = true
  tags          = { Name = "${var.project_name}-deploy-s3" }
}

# 버킷에 비공개 설정
resource "aws_s3_bucket_public_access_block" "deploy" {
  bucket                  = aws_s3_bucket.deploy.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 버킷 리소스 암호화
resource "aws_s3_bucket_server_side_encryption_configuration" "deploy" {
  bucket = aws_s3_bucket.deploy.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 현재 프로젝트 압축 -> S3 비공개 버킷 업로드
data "archive_file" "source" {
  type        = "zip"
  source_dir  = "${path.module}/../.."
  output_path = "${path.module}/agent-source.zip"
  excludes = [
    ".git",
    ".env",
    "__pycache__",
    "infra/terraform/.terraform",
    "infra/terraform/.terraform-build",
    "infra/terraform/agent-source.zip",
    "infra/terraform/terraform.tfstate",
    "infra/terraform/terraform.tfstats.backup",
  ]
}

# 버킷에 zip 파일 업로드
resource "aws_s3_object" "source" {
  bucket = aws_s3_bucket.deploy.id
  key    = "release/agent-source-${data.archive_file.source.output_md5}.zip"
  source = data.archive_file.source.output_path
  etag   = data.archive_file.source.output_md5
}

