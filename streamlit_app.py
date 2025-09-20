import streamlit as st
import requests
import pandas as pd

st.title("Emlak Gerçek İlanlar Testi")

city = st.text_input("Şehir", "istanbul")
district = st.text_input("İlçe", "kadikoy")
page = st.number_input("Sayfa", min_value=1, value=1, step=1)

if st.button("Veri Çek ve Göster"):
    url = f"http://localhost:5000/api/fetch-listings?city={city}&district={district}&page={page}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.warning("Veri bulunamadı.")
    except Exception as e:
        st.error(f"Hata: {e}")

st.markdown("""
---
**Not:** 
- Backend (`app.py`) çalışır durumda olmalı.
- Eğer farklı bir port veya sunucu kullanıyorsan, URL'yi güncelle.
""")