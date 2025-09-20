import streamlit as st
import pandas as pd

# Statik örnek veri - Gerçek emlak verileri formatında
SAMPLE_DATA = [
    {
        "title": "Kadıköy Merkez'de Yeni Bina 2+1",
        "price": 6500000,
        "location": "İstanbul/Kadıköy/Merkez",
        "details": "2+1, 90 m², 5.kat, 2020 yapım",
        "features": ["Asansör", "Otopark", "Güvenlik", "Ankastre Mutfak"]
    },
    {
        "title": "Bağdat Caddesi'nde Lüks 3+1",
        "price": 12000000,
        "location": "İstanbul/Kadıköy/Caddebostan",
        "details": "3+1, 145 m², 3.kat, 2022 yapım",
        "features": ["Deniz Manzarası", "Yerden Isıtma", "Akıllı Ev", "Havuz"]
    },
    {
        "title": "Moda'da Tarihi Bina",
        "price": 8500000,
        "location": "İstanbul/Kadıköy/Moda",
        "details": "3+1, 120 m², 2.kat, Restore Edilmiş",
        "features": ["Yüksek Tavan", "Balkon", "Parke Zemin"]
    },
    {
        "title": "Fenerbahçe'de Site İçi",
        "price": 9750000,
        "location": "İstanbul/Kadıköy/Fenerbahçe",
        "details": "2+1, 100 m², 8.kat, 2015 yapım",
        "features": ["Site İçi", "Spor Salonu", "Kapalı Otopark"]
    }
]

def calculate_estimated_value(location, size, features):
    """Basit bir değerleme algoritması"""
    base_value = 5000000  # Temel değer
    
    # Lokasyon katsayıları
    location_multipliers = {
        "Merkez": 1.0,
        "Caddebostan": 1.4,
        "Moda": 1.2,
        "Fenerbahçe": 1.3
    }
    
    # Özelliklere göre değer artışı
    feature_values = {
        "Deniz Manzarası": 1000000,
        "Otopark": 200000,
        "Site İçi": 500000,
        "Asansör": 100000,
        "Güvenlik": 300000
    }
    
    # Lokasyon çarpanını uygula
    for loc, multiplier in location_multipliers.items():
        if loc in location:
            base_value *= multiplier
            break
    
    # Metrekare değeri ekle (ortalama 50,000 TL/m²)
    base_value += size * 50000
    
    # Özelliklere göre değer ekle
    for feature in features:
        if feature in feature_values:
            base_value += feature_values[feature]
    
    return base_value

def format_price(price):
    """Fiyatı formatlı göster"""
    return f"{price:,.0f} TL"

# Streamlit arayüzü
st.title("🏠 Emlak Değerleme Sistemi v2")

# Yan menü
with st.sidebar:
    st.header("Filtreler")
    min_price = st.number_input("Minimum Fiyat (TL)", 0, 20000000, 0, 500000)
    max_price = st.number_input("Maximum Fiyat (TL)", 0, 20000000, 20000000, 500000)
    selected_location = st.multiselect(
        "Lokasyon",
        ["Merkez", "Caddebostan", "Moda", "Fenerbahçe"],
        []
    )

# Ana panel
tab1, tab2 = st.tabs(["📋 İlanlar", "💰 Değerleme"])

with tab1:
    st.header("Mevcut İlanlar")
    
    # Verileri filtrele
    filtered_data = [
        item for item in SAMPLE_DATA 
        if min_price <= item["price"] <= max_price and
        (not selected_location or any(loc in item["location"] for loc in selected_location))
    ]
    
    # İlanları göster
    for item in filtered_data:
        with st.expander(f"{item['title']} - {format_price(item['price'])}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("📍 **Konum:**", item["location"])
                st.write("📝 **Detaylar:**", item["details"])
            with col2:
                st.write("✨ **Özellikler:**")
                for feature in item["features"]:
                    st.write(f"- {feature}")

with tab2:
    st.header("Değerleme Hesaplama")
    
    col1, col2 = st.columns(2)
    with col1:
        loc = st.selectbox("Lokasyon", ["Merkez", "Caddebostan", "Moda", "Fenerbahçe"])
        size = st.number_input("Metrekare", 50, 300, 100)
    
    with col2:
        features = st.multiselect(
            "Özellikler",
            ["Deniz Manzarası", "Otopark", "Site İçi", "Asansör", "Güvenlik"],
            []
        )
    
    if st.button("Değer Hesapla"):
        estimated_value = calculate_estimated_value(loc, size, features)
        st.success(f"Tahmini Değer: {format_price(estimated_value)}")
        
        # Karşılaştırma
        similar_listings = [
            item for item in SAMPLE_DATA 
            if loc in item["location"] and
            abs(int(item["details"].split(" m²")[0].split(", ")[1]) - size) < 30
        ]
        
        if similar_listings:
            st.subheader("Benzer İlanlar")
            for item in similar_listings:
                st.write(f"- {item['title']}: {format_price(item['price'])}")

st.sidebar.info("""
    💡 **İpucu:** Bu demo sürümünde statik veriler kullanılmaktadır. 
    Gerçek verilere geçildiğinde daha kapsamlı analizler yapılabilecektir.
""")
