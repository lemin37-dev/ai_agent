'''
- 메타데이터와 본문(규정)을 분리
'''
from pathlib import Path
import yaml

def load_markdown(path:Path):
  '''
  parameters
    - path : 원소스(*.md)의 실제 경로
  returns
    - meta 데이터(yaml -> dict)
    - body 본문 규정 데이터(텍스트)
  '''
  # 1. markdown 전체를 읽은 후 yaml front formatter 존재하는지 체크(---)
  text = path.read_text(encoding='utf-8')
  # 2. 구분자 체크(---)
  if not text.startswith("---"):
    # 메타데이터가 없는 규정집 문서
    return {}, text
  # 3. 최대 2회만 분할
  _, meta, body = text.split('---', 2)
  # 4. 반환 (dict, text)
  # yaml.safe_load() -> 키:값 -> 파싱하여 dict 변환
  return yaml.safe_load(meta) or {}, body.strip()
