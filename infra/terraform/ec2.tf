# AMI 정보 획득
data "aws_ssm_parameter" "al2023_ami" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# 인스턴스 구성
resource "aws_instance" "agent" {
  ami                    = data.aws_ssm_parameter.al2023_ami.value
  instance_type          = var.ec2_instance_type
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.ec2.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2.name # AWS 다른 서비스 API 호출 권한을 가진 Role
  user_data = templatefile("${path.module}/../scripts/bootstrap.sh", {
    source_bucket          = aws_s3_bucket.deploy.bucket
    source_key             = aws_s3_object.source.key
    aws_region             = var.aws_region
    database_url_parameter = aws_ssm_parameter.database_url.name
    chat_model             = var.bedrock_chat_model
    embed_model            = var.bedrock_embedding_model
    user_id                = var.user_id
  })

  # EBS 디스크 설정
  root_block_device {
    volume_type = "gp3"
    volume_size = 12
    encrypted   = true
  }

  # 메타데이터 서비스 보안 설정 -옵션
  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  # ec2 생성전 반드시 구성되어야할 리소스 명시
  depends_on = [
    aws_s3_object.source,
    aws_db_instance.postgres,
    aws_iam_role_policy.agent,
    aws_iam_role_policy_attachment.ssm_core
  ]

  tags = {
    Name = "${var.project_name}-agent-ec2"
  }
}