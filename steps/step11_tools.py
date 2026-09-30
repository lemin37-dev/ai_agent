'''
등록된 툴 테스트
'''
from app.tools.sql_tools import sales_summary, top_products
from app.tools.rag_tools import search_company_policy

print(sales_summary.invoke({"start_date": "2026-09-01", "end_date": "2026-09-05"}))
print(top_products.invoke({"start_date": "2026-09-01", "end_date": "2026-09-05", "limit": 3}))
print(search_company_policy.invoke({"query": "연차 규정", "department": "HR"}))