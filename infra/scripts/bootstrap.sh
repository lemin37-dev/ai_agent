#!/bin/bash
set -euxo pipefail

# EC2 최초 부팅 시 Agent 서비스를 자동 구성하는 Bootstrap Script
# Terraform user_data에서 변수 값을 전달받아 실행됩니다.

# 1. Docker / AWS CLI 설치
dnf update -y
dnf install -y docker awscli unzip
systemctl enable --now docker

# 2. 배포 디렉터리 준비
mkdir -p /opt/agent-course
cd /opt/agent-course

# 3. Terraform이 S3에 올린 프로젝트 ZIP 다운로드
aws s3 cp "s3://${source_bucket}/${source_key}" /tmp/agent-course.zip --region "${aws_region}"
unzip -o /tmp/agent-course.zip -d /opt/agent-course

# 4. SSM Parameter Store에서 DB 접속정보 조회
DATABASE_URL=$(aws ssm get-parameter \
  --name "${database_url_parameter}" \
  --with-decryption \
  --query 'Parameter.Value' \
  --output text \
  --region "${aws_region}")

# 5. Agent 실행 환경변수 생성
cat > .env <<ENVEOF
AWS_REGION=${aws_region}
BEDROCK_CHAT_MODEL=${chat_model}
BEDROCK_EMBED_MODEL=${embed_model}
DATABASE_URL=$DATABASE_URL
AGENT_USER_ID=student-01
LANGSMITH_TRACING=false
LANGSMITH_PROJECT=agent-course-lab
ENVEOF
chmod 600 .env

# 6. Agent Docker Image Build
docker build -t agent-course:latest .

# 7. 새 RDS에 Schema / pgvector 구성
docker run --rm --env-file .env agent-course:latest python -m scripts.migrate

# 8. RAG 문서 Embedding 후 PostgreSQL + pgvector 적재
docker run --rm --env-file .env agent-course:latest python -m steps.step07_document_ingestion

# 9. FastAPI + LangGraph Agent 서비스 실행
docker rm -f agent-course 2>/dev/null || true
docker run -d \
  --name agent-course \
  --restart unless-stopped \
  --env-file .env \
  -p 8000:8000 \
  agent-course:latest