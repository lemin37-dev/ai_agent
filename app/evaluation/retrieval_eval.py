'''
RAG 검색 성능을 MRR, 일치되면 히트 수 기준으로 평가
'''

from app.evaluation.dataset import CASES # 데이터셋
from app.retrieval import advanced_search # 검색

# 성능평가
def main(k:int=5):
  # hits : 기대문서가 Top-K 검색결과에 포함되어 있는지 기록
  # reciprocal : 기대문서의 검색순위에 대한 역순위 기록 (1/rank)
  hits, reciprocal = list(), list()

  for case in CASES:
    rows = advanced_search(case['question'], k=k)

    # 문서코드 추출
    codes = [row[0] for row in rows]

    # expected 문서코드 획득
    expected = case['expected_source']

    # 평가
    hit = expected in codes
    hits.append(int(hit))

    # 역순위(reciprocal)
    # expected 몇번째에 검색되었는지 체크, 없다면 None
    rank = (codes.index(expected)+1) if hit else None
    reciprocal.append(1/rank if rank else 0)

    # 질문별 검색결과, 정답문서 순위 등 출력
    print( f"{case['question']} -> {codes} | expected={expected} | rank={rank}")

  print(f"HitRate@{k} = {sum(hits)/len(hits):.3f}") # 종합
  print(f"MRR = {sum(reciprocal)/len(reciprocal):.3f}") # MRR

# 직접 실행대비
if __name__ == '__main__':
  main()