variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

# AWS Resource 간 공통 prefix
variable "project_name" {
  description = "Project Name"
  type        = string
  default     = "agent-de-ai-19"
}

# VPC 대역
variable "vpc_cidr" {
  description = "VPC CIDR"
  type        = string
  default     = "10.30.0.0/16"
}
# fastapi port - 8000 접속 IP CIDR
variable "api_cidr" {
  description = "FastAPI CIDR"
  type        = string
  default     = "0.0.0.0/0"
}

# EC2 instance type
variable "ec2_instance_type" {
  description = "Agent EC2"
  type        = string
  default     = "t3.micro"
}

# Database(RDS) name
variable "db_name" {
  description = "Vector database name"
  type        = string
  default     = "agentlab"
}
# Database(RDS) user name
variable "db_username" {
  description = "Vector database username"
  type        = string
  default     = "agent"
}
# RDS Instance 사양
variable "db_isntance_class" {
  description = "RDS Instance type"
  type        = string
  default     = "db.t4g.small"
}

# PostgreSQL 엔진 버전
variable "postgre_version" {
  description = "PostgreSQL 엔진 버전"
  type        = string
  default     = "16"
}

# bedrock Model ID
variable "bedrock_chat_model" {
  description = "anthropic base model"
  type        = string
  default     = "us.anthropic.claude-sonnet-5"
}
# embedding Model ID
variable "bedrock_embedding_model" {
  description = "embedding model"
  type        = string
  default     = "amazon.titan-embed-text-v2:0"
}
# Agent Memory에 대한 사용자 ID
variable "user_id" {
  description = "임시 사용자 ID"
  type        = string
  default     = "demo-user-19"

}



# SSH 관련
# SSH 접근 IP 대역