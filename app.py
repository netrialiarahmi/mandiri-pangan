import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Data Pangan", page_icon="🍚", layout="wide")

# Inisialisasi Session State untuk Menyimpan Data
if "rumah_tangga_total" not in st.session_state:
    st.session_state["rumah_tangga_total"] = "Belum ada data"

if "kemandirian_tinggi" not in st.session_state:
    st.session_state["kemandirian_tinggi"] = "Belum ada data"

if "data_terbaru" not in st.session_state:
    st.session_state["data_terbaru"] = "Belum ada data"

# Sidebar Navigasi
st.sidebar.title("📂 Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Dashboard Utama", "📊 Data Rumah Tangga", "🍛 Kemandirian Pangan RT", "🌾 Kemandirian Pangan Dusun"],
)

# Halaman Dashboard Utama
if menu == "🏠 Dashboard Utama":
    st.title("📊 Dashboard Data Pangan")
    st.markdown(
        """
        Selamat datang di **Dashboard Data Pangan**!  
        Dashboard ini menampilkan visualisasi interaktif dari:
        - **Data rumah tangga**
        - **Data kemandirian pangan per rumah tangga**
        - **Data kemandirian pangan per dusun**
        """
    )

    # Menampilkan Metrics Cards
    st.markdown("### 📈 Statistik Utama")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🏠 Total Rumah Tangga")
        st.metric(label="", value=st.session_state["rumah_tangga_total"])
    with col2:
        st.markdown("#### 🍛 Kemandirian Tinggi")
        st.metric(label="", value=st.session_state["kemandirian_tinggi"])
    with col3:
        st.markdown("#### 🌾 Data Terbaru")
        st.metric(label="", value=st.session_state["data_terbaru"])

    st.info("Silakan pilih halaman di **sidebar** untuk memperbarui data.")

# Halaman Data Rumah Tangga
elif menu == "📊 Data Rumah Tangga":
    st.title("📊 Data Rumah Tangga")
    st.markdown(
        """
        Unggah data rumah tangga untuk melihat jumlah total keluarga yang terdata.
        """
    )

    uploaded_file = st.file_uploader("Unggah file data rumah tangga (CSV):", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write(data)

        # Perbarui jumlah rumah tangga di session state
        st.session_state["rumah_tangga_total"] = len(data)
        st.success(f"Total rumah tangga berhasil diperbarui: {len(data)} keluarga.")
    else:
        st.info("Silakan unggah file data rumah tangga untuk memulai.")

# Halaman Kemandirian Pangan RT
elif menu == "🍛 Kemandirian Pangan RT":
    st.title("🍛 Kemandirian Pangan Rumah Tangga")
    st.markdown(
        """
        Unggah data kemandirian pangan rumah tangga untuk menghitung rata-rata kemandirian pangan.
        """
    )

    uploaded_file = st.file_uploader("Unggah file data kemandirian pangan RT (CSV):", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write(data)

        # Perbarui persentase kemandirian tinggi
        if "Kemandirian (%)" in data.columns:
            rata_kemandirian = data["Kemandirian (%)"].mean()
            st.session_state["kemandirian_tinggi"] = f"{rata_kemandirian:.2f}%"
            st.success(f"Kemandirian tinggi diperbarui: {rata_kemandirian:.2f}%.")
        else:
            st.warning("Kolom 'Kemandirian (%)' tidak ditemukan dalam data.")
    else:
        st.info("Silakan unggah file data kemandirian pangan rumah tangga untuk memulai.")

# Halaman Kemandirian Pangan Dusun
elif menu == "🌾 Kemandirian Pangan Dusun":
    st.title("🌾 Kemandirian Pangan Dusun")
    st.markdown(
        """
        Unggah data kemandirian pangan per dusun untuk melihat tahun data terbaru.
        """
    )

    uploaded_file = st.file_uploader("Unggah file data kemandirian pangan dusun (CSV):", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write(data)

        # Perbarui data terbaru di session state
        if "Tahun" in data.columns:
            tahun_terbaru = data["Tahun"].max()
            st.session_state["data_terbaru"] = str(tahun_terbaru)
            st.success(f"Data terbaru berhasil diperbarui: {tahun_terbaru}.")
        else:
            st.warning("Kolom 'Tahun' tidak ditemukan dalam data.")
    else:
        st.info("Silakan unggah file data kemandirian pangan per dusun untuk memulai.")
