import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Data Pangan",
    page_icon=":bar_chart:",
    layout="wide",
)

# CSS Kustom untuk styling
st.markdown(
    """
    <style>
    /* CSS Kustom */
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1 {
        color: #4B6A9B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul dan Deskripsi
st.title('Dashboard Data Pangan')
st.markdown('''
Selamat datang di **Dashboard Data Pangan**. Dashboard ini menampilkan visualisasi interaktif dari **data rumah tangga**, **data kemandirian pangan per rumah tangga**, dan **data kemandirian pangan per dusun**.
''')

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file, encoding='latin-1')
    return df

# Membuat Tab
tabs = st.tabs(['Data Rumah Tangga', 'Data Kemandirian Pangan Per Rumah Tangga', 'Data Kemandirian Pangan Per Dusun'])

with tabs[0]:
    st.header('Data Rumah Tangga')
    # Upload dan tampilkan data_rumah_tangga
    data_rumah_tangga_file = st.file_uploader('Upload Data Rumah Tangga', type=['csv'], key='data_rumah_tangga')
    if data_rumah_tangga_file is not None:
        data_rumah_tangga = load_data(data_rumah_tangga_file)
        with st.expander("Lihat Data Rumah Tangga"):
            st.write(data_rumah_tangga)
        
        # Opsi Filter
        if 'Dusun' in data_rumah_tangga.columns:
            dusun_list = data_rumah_tangga['Dusun'].unique()
            selected_dusun = st.selectbox('Pilih Dusun', options=dusun_list, index=0)
            filtered_data = data_rumah_tangga[data_rumah_tangga['Dusun'] == selected_dusun]
            st.write(f'Data Rumah Tangga untuk Dusun **{selected_dusun}**')
            st.write(filtered_data)
        else:
            filtered_data = data_rumah_tangga
        
        # Visualisasi
        st.subheader('Visualisasi Data Rumah Tangga')
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Pendapatan Bulanan (Rp.)' in filtered_data.columns:
                st.markdown('**Distribusi Pendapatan Bulanan**')
                fig = px.histogram(filtered_data, x='Pendapatan Bulanan (Rp.)', nbins=20, title='Distribusi Pendapatan Bulanan', color_discrete_sequence=['#4B6A9B'])
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Jumlah Anggota Keluarga (jiwa)' in filtered_data.columns:
                st.markdown('**Distribusi Jumlah Anggota Keluarga**')
                fig = px.histogram(filtered_data, x='Jumlah Anggota Keluarga (jiwa)', nbins=10, title='Distribusi Jumlah Anggota Keluarga', color_discrete_sequence=['#F26419'])
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info('Silakan upload file **Data Rumah Tangga** pada tab ini.')

with tabs[1]:
    st.header('Data Kemandirian Pangan Per Rumah Tangga')
    data_kemandirian_rumah_tangga_file = st.file_uploader('Upload Data Kemandirian Pangan Per Rumah Tangga', type=['csv'], key='data_kemandirian_rumah_tangga')
    if data_kemandirian_rumah_tangga_file is not None:
        data_kemandirian_rumah_tangga = load_data(data_kemandirian_rumah_tangga_file)
        with st.expander("Lihat Data Kemandirian Pangan Per Rumah Tangga"):
            st.write(data_kemandirian_rumah_tangga)
        
        # Visualisasi
        if 'Nama Kepala Keluarga' in data_kemandirian_rumah_tangga.columns and 'Rata-rata' in data_kemandirian_rumah_tangga.columns:
            st.subheader('Kemandirian Pangan Per Rumah Tangga')
            fig = px.bar(data_kemandirian_rumah_tangga, x='Nama Kepala Keluarga', y='Rata-rata', title='Kemandirian Pangan Per Rumah Tangga', color='Rata-rata', color_continuous_scale='Viridis')
            fig.update_layout(xaxis_tickangle=-90)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning('Kolom "Nama Kepala Keluarga" atau "Rata-rata" tidak ditemukan dalam data.')
    else:
        st.info('Silakan upload file **Data Kemandirian Pangan Per Rumah Tangga** pada tab ini.')

with tabs[2]:
    st.header('Data Kemandirian Pangan Per Dusun')
    data_kemandirian_dusun_file = st.file_uploader('Upload Data Kemandirian Pangan Per Dusun', type=['csv'], key='data_kemandirian_dusun')
    if data_kemandirian_dusun_file is not None:
        data_kemandirian_dusun = load_data(data_kemandirian_dusun_file)
        with st.expander("Lihat Data Kemandirian Pangan Per Dusun"):
            st.write(data_kemandirian_dusun)
        
        # Visualisasi
        if 'Data' in data_kemandirian_dusun.columns and 'Rata-rata' in data_kemandirian_dusun.columns:
            st.subheader('Kemandirian Pangan Per Dusun')
            fig = px.bar(data_kemandirian_dusun, x='Data', y='Rata-rata', title='Kemandirian Pangan Per Dusun', color='Rata-rata', color_continuous_scale='Plasma')
            fig.update_layout(xaxis_tickangle=-90)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning('Kolom "Data" atau "Rata-rata" tidak ditemukan dalam data.')
    else:
        st.info('Silakan upload file **Data Kemandirian Pangan Per Dusun** pada tab ini.')
