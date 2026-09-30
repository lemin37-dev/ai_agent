'''
# 기존 fixed-size 청킹
    - [v]fixed-size 단위 청킹 처리 하는 모듈
    - 최대 길이는 700 설정(글자수), 토큰 최대는 1024이므로, 범위안에 여유있게 들어옴
    - 청킹의 trade-off
        - chunk가 작으면 -> 검색 정밀도 상승 -> 문맥이 자릴수 있음
        - chunk가 크면   -> 문맥 보전 상승   -> 불필요한 내용 같이 포함될 수 있음 
    - 청크 사이즈는 rag 성능의 하이퍼파라미터 => 검색 평가를 통해서 최적 크기는 결정
    - 고정크기 -> overlap -> token 기반 -> 시멘틱/구조 기반 청킹 or 청킹 에이전트 개발 반영
# 시멘틱 청킹
    - 말뭉치 -> 문장/문단 단위로 분절
'''
import math
import re
from app.embedding import get_embeddings
from typing import Sequence


# 350(설정값)자를 초과하는 문단을 분절
def _split_sentences(block:str) -> list[str]:
    # 1. 좌우 공백 제거
    block = block.strip()
    # 2. 값 체크
    if not block: return []
    # 3. 줄 단위로 분절 -> 제목/목록 등 문서 형식에 따라 의미가 있는 경우
    lines = [
        line.strip()
        for line in block.splitlines()
        if line.strip()
    ]
    # 최종 분절 데이터를 담는 그릇
    units:list[str] = list()

    # 라인별 순회하며 문장의 끝 기호(.!?。 ！ ？)를 체크 -> 기호를 기반으로 순회를 하여 units에 포함
    for line in lines:
        # 후방 검색(?<=[탐색문자])
        setences = re.split(r"(?<=[.!?。 ！ ？])\s+", line)
        units.extend(
            s.strip()
            for s in setences
            if s.strip()
        )

    return units

    
# 시멘틱에 맞게 데이터를 담는 작업
def _semantic_units(text:str) -> list[str]:
    # 1. 문단의 끝 단위를 1차로 쪼개기 -> 개행문자 (r"\n\s*\n")
    blocks = [
        # 문단을 리스트의 멤버로 구성
        block.strip()
        for block in re.split(r"\n\s*\n", text)
        if block.strip()
    ]
    # 2. chunking 단위 데이터를 담는 그릇
    units:list[str] = list()

    # 3. 문단단위로 순회 -> 1차적으로 청킹 진행(최소 글자수 단위 구성)
    for block in blocks:
        if len(block) <= 350:
            units.append(block)
        else: # 350자 초과
            units.append(_split_sentences(block))

    return units

# cosine 유사도 검사 함수
def _cosine_similarity(
    vector_a: Sequence[float],
    vector_b: Sequence[float],
) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    norm_a = math.sqrt(
        sum(
            value * value
            for value in vector_a
        )
    )

    norm_b = math.sqrt(
        sum(
            value * value
            for value in vector_b
        )
    )

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)

# 시멘틱 청킹 함수
# 원문, 임계값(0.6이하면 청킹), 최소 글자수, 최대 글자수(유사도가 0.6을 넘도록 유지되어도 1200자가 넘을 경우 청킹 )
def semantic_split_text(text:str, threshold:float=0.60, max_chars:int=1200) -> list:
    # 1. semantic 유닛 단위 분할
    units = _semantic_units(text)

    # 2. 값 체크
    if not units: return []
    if len(units) == 1: return units

    # 3. 쪼개진 문자 혹은 문장 조각 -> 임베딩 처리
    embeddings = get_embeddings().embed_documents(units)

    # 4. 담는 그릇
    chunks:list[str] = list()
    current = units[0]

    # 5. 유닛에서 이전벡터와 현재 인덱스의 벡터 간 유사도 검사
    for idx in range(1, len(units)):
        # 5-1. 유사도 검사 대상 추출
        pre_vec = embeddings[idx-1]
        cur_vec = embeddings[idx]

        # 5-2. 유사도 검사
        similarity = _cosine_similarity(pre_vec, cur_vec)

        # 5-3. 청킹 후보 텍스트 준비
        candidate = (
            current
            + "\n\n"
            + units[idx]
        )

        # 5-4. 판별
        # 유사도가 입게값보다 낮거나 candidate의 글자수가 max_chars 범위 밖에 있는 경우
        if similarity < threshold or len(candidate) > max_chars:
            chunks.append(current)
            # 현재 문장은 다음 문장으로 세팅
            current = units[idx]
        else:   # 유사도가 임계값을 넘고 max_chars 범위 안에 있는 경우
            # 이전 문장 + 현재 문장으로 병합
            current = candidate

    # 6. 모두 순회했음에도 남아있을 경우
    if current:
        chunks.append(current)

    return chunks



def split_text(text:str, max_chars:int = 700):
    # 청크별로 모으는 그릇, 현재 순서상 문서 데이터
    chunks, current_doc = [], ""
    # \n\n 를 기준으로 분할 => 문서마다 상이함
    #print( text.split('\n\n') )
    paragraphs = [ p.strip() for p in text.split('\n\n') if p.strip() ] # 공백 제거 처리, 노이즈 제거

    # 순회 하면서 청킹 처리
    for p in paragraphs:
        # 1. 청킹 후보 (현재 보관문서 + 줄바꿈 + 하나씩뽑아낸문단)
        candidate_doc = (current_doc + "\n\n" + p).strip()

        # 2. 청킹후보에 대한 길이 체크(처킹의 분할 기준이 문자수=700)
        if current_doc and len(candidate_doc) > max_chars:
            # 3. 청크에 추가 -> 청크 1개 확정
            chunks.append( current_doc ) # 현재 누적된 doc에 새로운 문단 추가하면 700을 넘어간다 => 새로 추가분 제외
            # 4. 리셋
            current_doc = p
        else:
            # 현재 보관문서에 후보군 문서를 설정
            current_doc = candidate_doc

    # 마지막까지 다 체크를 했는데, 마지막에서 700이 않넘었다 => 남은 문단이 존재함
    if current_doc:
        chunks.append( current_doc )

    # 청크 묶음 반환
    return chunks