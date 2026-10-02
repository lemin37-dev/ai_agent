'''
RAG 검색 성능 테스트 진행
'''

from app.evaluation.retrieval_eval import main

# Top-k의 검색결과에 기대문서가 포함되어있는지 카운팅
main(5)