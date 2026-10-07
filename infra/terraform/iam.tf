# EC2 기본권한
data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}
# Role 생성 - EC2
resource "aws_iam_role" "ec2" {
  name               = "${var.project_name}-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

# SSH 키 없이 Session Manager로 접속 가능
resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
# Agent 활용을 위힌 추가 권한 생성
data "aws_iam_policy_document" "agent" {
  statement {
    sid       = "ReadDeploymentSource"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.deploy.arn}/*"]
  }

  statement {
    sid       = "ReadDatabaseUrl"
    actions   = ["ssm:GetParameter"]
    resources = [aws_ssm_parameter.database_url.arn]
  }

  statement {
    sid = "UseBedrock"
    actions = [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream"
    ]
    resources = ["*"]
  }
}
# Agent를 위해 추가 생성한 권한을 EC2 Role에 연결
resource "aws_iam_role_policy" "agent" {
  name   = "${var.project_name}-agent-policy"
  role   = aws_iam_role.ec2.id
  policy = data.aws_iam_policy_document.agent.json
}
# Instance Profile 생성 - EC2 Role
resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2.name
}