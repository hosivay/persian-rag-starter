"""
Example: Shiraz city guide using Persian RAG Starter
"""
from core import Retriever, chunk_text

# داده
info = """
شیراز پایتخت استان فارس است.
آرامگاه حافظ و سعدی در شیراز قرار دارد.
ارگ کریم‌خان در مرکز شیراز واقع شده است.
مسجد نصیرالملک به مسجد صورتی معروف است.
باغ ارم شیراز در یونسکو ثبت شده است.
تخت جمشید ۵۷ کیلومتر از شیراز فاصله دارد.
"""

# index کردن
retriever = Retriever(collection_name="shiraz", db_path="./shiraz_db")
chunks = chunk_text(info)
retriever.add(chunks)

# جستجو
query = "ارگ کریم خان کجاست؟"
results = retriever.search(query)
for r in results:
    print(r)
    print("---")