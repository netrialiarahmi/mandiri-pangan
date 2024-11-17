import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Data Pangan",
    page_icon="🍚",
    layout="wide",
)

# CSS Kustom untuk styling
st.markdown(
    """
    <style>
    /* CSS Kustom */
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    h1, h2, h3 {
        color: #2E4053;
        font-weight: 700;
    }

    .stButton>button {
        background-color: #2E86C1;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }

    .stButton>button:hover {
        background-color: #1A5276;
        color: white;
    }

    .css-1offfwp.e1fqkh3o3 {
        background-color: #EBF5FB;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul dan Deskripsi
st.title('📊 Dashboard Data Pangan')
st.markdown('''
Selamat datang di **Dashboard Data Pangan**! Dashboard ini menampilkan visualisasi interaktif dari **data rumah tangga**, **data kemandirian pangan per rumah tangga**, dan **data kemandirian pangan per dusun**.

Silakan unggah data Anda pada tab yang sesuai di bawah ini.
''')

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file):
    try:
        if file.type == 'text/csv':
            df = pd.read_csv(file, encoding='utf-8', header=1)  # Header pada baris kedua
        else:
            df = pd.read_excel(file, header=1)  # Header pada baris kedua
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
    return df

# Fungsi untuk mengekstrak Latitude dan Longitude dari format 'Longitude, Latitude, Altitude, Accuracy'
def extract_lat_lon(coord):
    try:
        parts = coord.split(',')
        lon = float(parts[0].strip())
        lat = float(parts[1].strip())
        # Jika diperlukan, Anda dapat menangani Altitude dan Accuracy di sini
        return pd.Series({'Latitude': lat, 'Longitude': lon})
    except:
        return pd.Series({'Latitude': None, 'Longitude': None})

# Membuat Tab
tabs = st.tabs(['🏠 Data Rumah Tangga', '🍛 Kemandirian Pangan Rumah Tangga', '🌾 Kemandirian Pangan Dusun'])
with tabs[0]:
    st.header('🏠 Data Rumah Tangga')
    # Upload dan tampilkan data_rumah_tangga
    data_rumah_tangga_file = st.file_uploader('Upload Data Rumah Tangga (CSV atau Excel)', type=['csv', 'xlsx'], key='data_rumah_tangga')
    if data_rumah_tangga_file is not None:
        data_rumah_tangga = load_data(data_rumah_tangga_file)
        if data_rumah_tangga is not None:
            with st.expander("🔍 Lihat Data Rumah Tangga"):
                st.write(data_rumah_tangga)
            
            # Opsi Filter
            if 'Dusun' in data_rumah_tangga.columns:
                st.subheader('📍 Filter Berdasarkan Dusun')
                dusun_list = data_rumah_tangga['Dusun'].dropna().unique()
                selected_dusun = st.selectbox('Pilih Dusun', options=dusun_list, index=0)
                filtered_data = data_rumah_tangga[data_rumah_tangga['Dusun'] == selected_dusun]
                st.markdown(f'### Data Rumah Tangga untuk Dusun **{selected_dusun}**')
                st.dataframe(filtered_data)
            else:
                filtered_data = data_rumah_tangga
            
            # Visualisasi
            st.subheader('📈 Visualisasi Data Rumah Tangga')
            col1, col2 = st.columns(2)
            
            with col1:
                if 'Pendapatan Bulanan (Rp.)' in filtered_data.columns:
                    st.markdown('**Distribusi Pendapatan Bulanan**')
                    # Mengonversi kolom 'Pendapatan Bulanan (Rp.)' menjadi numerik
                    filtered_data['Pendapatan Bulanan (Rp.)'] = pd.to_numeric(filtered_data['Pendapatan Bulanan (Rp.)'], errors='coerce')
                    fig = px.histogram(filtered_data, x='Pendapatan Bulanan (Rp.)', nbins=20, color_discrete_sequence=['#1ABC9C'])
                    fig.update_layout(title='Distribusi Pendapatan Bulanan', xaxis_title='Pendapatan Bulanan (Rp.)', yaxis_title='Jumlah Rumah Tangga')
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'Jumlah Anggota Keluarga (jiwa)' in filtered_data.columns:
                    st.markdown('**Distribusi Jumlah Anggota Keluarga**')
                    filtered_data['Jumlah Anggota Keluarga (jiwa)'] = pd.to_numeric(filtered_data['Jumlah Anggota Keluarga (jiwa)'], errors='coerce')
                    fig = px.pie(filtered_data, names='Jumlah Anggota Keluarga (jiwa)', color_discrete_sequence=px.colors.sequential.RdBu)
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(title='Persentase Jumlah Anggota Keluarga')
                    st.plotly_chart(fig, use_container_width=True)
            
            # Menampilkan Peta
            if 'Koordinat GPS' in filtered_data.columns:
                st.subheader('🗺️ Peta Sebaran Rumah Tangga')
                # Memisahkan latitude dan longitude
                coords = filtered_data['Koordinat GPS'].apply(extract_lat_lon)
                filtered_data = filtered_data.join(coords)
                filtered_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])
                
                fig = px.scatter_mapbox(
                    filtered_data,
                    lat='Latitude',
                    lon='Longitude',
                    hover_name='Nama Kepala Keluarga',
                    zoom=12,
                    height=500,
                    mapbox_style='open-street-map',
                    color_discrete_sequence=['#FF5733']
                )
                fig.update_layout(title='Peta Sebaran Rumah Tangga')
                st.plotly_chart(fig, use_container_width=True)
            
            # Visualisasi Tambahan: Produksi dan Konsumsi Pangan
            st.subheader('🍚 Analisis Produksi dan Konsumsi Pangan')
            
            # Konversi kolom produksi dan konsumsi menjadi numerik
            produksi_karbohidrat_cols = ['Beras Lokal (Sawah/Ladang dalam Kg)', 'Singkong', 'Jagung Lokal', 'Jagung Hibrida', 'Umbi-umbian lain', 'Sorgum', 'Jewawut/Weteng']
            produksi_protein_cols = ['Ikan dan Boga Laut Segar', 'Ikan dan Boga Laut Kering', 'Telor', 'Ayam', 'Daging (Sapi/Kerbau/Kambing/Babi,dll)', 'Kacang-kacangan']
            konsumsi_protein_cols = ['Ikan dan Boga Laut Segar.1', 'Ikan dan Boga Laut Kering.1', 'Telor.1', 'Ayam.1', 'Kacang-kacangan.1']
            konsumsi_sayur_buah_cols = ['Daun Ubi', 'Kangkung', 'Kubis', 'Sawi', 'Bayam', 'Brokoli', 'Wortel', 'Jantung Pisang', 'Kelor', 'Bunga dan Daun Pepaya', 'Pakis/Paku', 'Rebung', 'Mangga', 'Alpukat', 'Jeruk', 'Anggur', 'Buah Naga', 'Mete', 'Pisang', 'Rambutan', 'Nanas', 'Salak', 'Pepaya', 'Kelapa', 'Tomat', 'Timun', 'Labu', 'Kemangi']
            
            # Pastikan kolom-kolom tersebut ada dalam data
            available_produksi_karbo_cols = [col for col in produksi_karbohidrat_cols if col in filtered_data.columns]
            available_produksi_protein_cols = [col for col in produksi_protein_cols if col in filtered_data.columns]
            available_konsumsi_protein_cols = [col for col in konsumsi_protein_cols if col in filtered_data.columns]
            available_konsumsi_sayur_buah_cols = [col for col in konsumsi_sayur_buah_cols if col in filtered_data.columns]
            
            # Mengonversi data produksi dan konsumsi menjadi numerik
            for col in available_produksi_karbo_cols + available_produksi_protein_cols + available_konsumsi_protein_cols + available_konsumsi_sayur_buah_cols:
                filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
            
            # Analisis Produksi Protein per Rumah Tangga
            filtered_data['Total Produksi Protein (Kg)'] = filtered_data[available_produksi_protein_cols].sum(axis=1)
            
            st.markdown('**Produksi Protein per Rumah Tangga**')
            fig = px.bar(filtered_data, x='Nama Kepala Keluarga', y='Total Produksi Protein (Kg)', color='Total Produksi Protein (Kg)', color_continuous_scale='Sunset')
            fig.update_layout(title='Produksi Protein per Rumah Tangga', xaxis_title='Nama Kepala Keluarga', yaxis_title='Total Produksi Protein (Kg)')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Analisis Konsumsi Protein per Rumah Tangga
            filtered_data['Total Konsumsi Protein (Kg)'] = filtered_data[available_konsumsi_protein_cols].sum(axis=1)
            
            st.markdown('**Konsumsi Protein per Rumah Tangga**')
            fig = px.bar(filtered_data, x='Nama Kepala Keluarga', y='Total Konsumsi Protein (Kg)', color='Total Konsumsi Protein (Kg)', color_continuous_scale='Teal')
            fig.update_layout(title='Konsumsi Protein per Rumah Tangga', xaxis_title='Nama Kepala Keluarga', yaxis_title='Total Konsumsi Protein (Kg)')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Analisis Konsumsi Sayur dan Buah per Rumah Tangga
            filtered_data['Total Konsumsi Sayur dan Buah (Kg)'] = filtered_data[available_konsumsi_sayur_buah_cols].sum(axis=1)
            
            st.markdown('**Konsumsi Sayur dan Buah per Rumah Tangga**')
            fig = px.bar(filtered_data, x='Nama Kepala Keluarga', y='Total Konsumsi Sayur dan Buah (Kg)', color='Total Konsumsi Sayur dan Buah (Kg)', color_continuous_scale='Greens')
            fig.update_layout(title='Konsumsi Sayur dan Buah per Rumah Tangga', xaxis_title='Nama Kepala Keluarga', yaxis_title='Total Konsumsi Sayur dan Buah (Kg)')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Korelasi Pendapatan dengan Produksi dan Konsumsi
            st.subheader('📊 Analisis Korelasi Pendapatan dengan Produksi dan Konsumsi')
            if 'Pendapatan Bulanan (Rp.)' in filtered_data.columns:
                # Mengonversi Pendapatan menjadi numerik
                filtered_data['Pendapatan Bulanan (Rp.)'] = pd.to_numeric(filtered_data['Pendapatan Bulanan (Rp.)'], errors='coerce')
                
                # Scatter Plot Pendapatan vs Total Produksi Karbohidrat
                st.markdown('**Pendapatan vs Total Produksi Karbohidrat**')
                fig = px.scatter(filtered_data, x='Pendapatan Bulanan (Rp.)', y='Total Produksi Karbohidrat (Kg)', trendline='ols', color_discrete_sequence=['#2E86C1'])
                fig.update_layout(xaxis_title='Pendapatan Bulanan (Rp.)', yaxis_title='Total Produksi Karbohidrat (Kg)')
                st.plotly_chart(fig, use_container_width=True)
                
                # Scatter Plot Pendapatan vs Total Konsumsi Karbohidrat
                st.markdown('**Pendapatan vs Total Konsumsi Karbohidrat**')
                fig = px.scatter(filtered_data, x='Pendapatan Bulanan (Rp.)', y='Total Konsumsi Karbohidrat (Kg)', trendline='ols', color_discrete_sequence=['#D35400'])
                fig.update_layout(xaxis_title='Pendapatan Bulanan (Rp.)', yaxis_title='Total Konsumsi Karbohidrat (Kg)')
                st.plotly_chart(fig, use_container_width=True)
            
            # Visualisasi Kepemilikan Ternak
            st.subheader('🐄 Kepemilikan Ternak per Rumah Tangga')
            ternak_cols = ['Sapi', 'Kerbau', 'Kambing', 'Ayam', 'Bebek', 'Babi', 'Kuda']
            available_ternak_cols = [col for col in ternak_cols if col in filtered_data.columns]
            for col in available_ternak_cols:
                filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
            filtered_data['Total Ternak'] = filtered_data[available_ternak_cols].sum(axis=1)
            
            fig = px.bar(filtered_data, x='Nama Kepala Keluarga', y='Total Ternak', color='Total Ternak', color_continuous_scale='OrRd')
            fig.update_layout(title='Total Ternak per Rumah Tangga', xaxis_title='Nama Kepala Keluarga', yaxis_title='Jumlah Ternak')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Top 5 Rumah Tangga dengan Kepemilikan Ternak Tertinggi
            top5_ternak = filtered_data.nlargest(5, 'Total Ternak')[['Nama Kepala Keluarga', 'Total Ternak']]
            st.markdown('**🏆 Top 5 Rumah Tangga dengan Kepemilikan Ternak Tertinggi**')
            st.table(top5_ternak)
            
            # Konsumsi per Kapita
            st.subheader('👨‍👩‍👧‍👦 Konsumsi per Kapita Karbohidrat')
            filtered_data['Konsumsi Karbohidrat per Kapita (Kg)'] = filtered_data['Total Konsumsi Karbohidrat (Kg)'] / filtered_data['Jumlah Anggota Keluarga (jiwa)']
            fig = px.bar(filtered_data, x='Nama Kepala Keluarga', y='Konsumsi Karbohidrat per Kapita (Kg)', color='Konsumsi Karbohidrat per Kapita (Kg)', color_continuous_scale='Purples')
            fig.update_layout(title='Konsumsi Karbohidrat per Kapita', xaxis_title='Nama Kepala Keluarga', yaxis_title='Konsumsi per Kapita (Kg)')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Konsumsi per Kapita Protein
            st.subheader('👨‍👩‍👧‍👦 Konsumsi per Kapita Protein')
            filtered_data['Konsumsi Protein per Kapita (Kg)'] = filtered_data['Total Konsumsi Protein (Kg)'] / filtered_data['Jumlah Anggota Keluarga (jiwa)']
            fig = px.bar(filtered_data, x='Nama Kepala Keluarga', y='Konsumsi Protein per Kapita (Kg)', color='Konsumsi Protein per Kapita (Kg)', color_continuous_scale='Blues')
            fig.update_layout(title='Konsumsi Protein per Kapita', xaxis_title='Nama Kepala Keluarga', yaxis_title='Konsumsi per Kapita (Kg)')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Ringkasan Dashboard
            st.subheader('📊 Ringkasan')
            total_rumah_tangga = filtered_data['Nama Kepala Keluarga'].nunique()
            total_penduduk = filtered_data['Jumlah Anggota Keluarga (jiwa)'].sum()
            total_produksi_karbohidrat = filtered_data['Total Produksi Karbohidrat (Kg)'].sum()
            total_konsumsi_karbohidrat = filtered_data['Total Konsumsi Karbohidrat (Kg)'].sum()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Rumah Tangga", total_rumah_tangga)
            col2.metric("Total Penduduk", int(total_penduduk))
            col3.metric("Total Produksi Karbohidrat (Kg)", int(total_produksi_karbohidrat))
            col4.metric("Total Konsumsi Karbohidrat (Kg)", int(total_konsumsi_karbohidrat))
            
        else:
            st.error('Gagal memuat data. Pastikan format file benar dan sesuai.')
    else:
        st.info('Silakan upload file **Data Rumah Tangga** pada tab ini.')
with tabs[1]:
    st.header('🍛 Data Kemandirian Pangan Per Rumah Tangga')
    data_kemandirian_rumah_tangga_file = st.file_uploader('Upload Data Kemandirian Pangan Per Rumah Tangga (CSV atau Excel)', type=['csv', 'xlsx'], key='data_kemandirian_rumah_tangga')
    if data_kemandirian_rumah_tangga_file is not None:
        data_kemandirian_rumah_tangga = load_data(data_kemandirian_rumah_tangga_file)
        if data_kemandirian_rumah_tangga is not None:
            # Membersihkan kolom 'Rata-rata'
            if 'Rata-rata' in data_kemandirian_rumah_tangga.columns:
                data_kemandirian_rumah_tangga['Rata-rata'] = data_kemandirian_rumah_tangga['Rata-rata'].astype(str).str.replace('%', '').str.strip()
                data_kemandirian_rumah_tangga['Rata-rata'] = pd.to_numeric(data_kemandirian_rumah_tangga['Rata-rata'], errors='coerce')
            with st.expander("🔍 Lihat Data Kemandirian Pangan Per Rumah Tangga"):
                st.write(data_kemandirian_rumah_tangga)
            
            # Visualisasi
            # Menggunakan kolom 'Data' sebagai pengganti 'Nama Kepala Keluarga'
            if 'Data' in data_kemandirian_rumah_tangga.columns and 'Rata-rata' in data_kemandirian_rumah_tangga.columns:
                st.subheader('🌟 Kemandirian Pangan Per Rumah Tangga')
                fig = px.bar(data_kemandirian_rumah_tangga, x='Data', y='Rata-rata', color='Rata-rata', color_continuous_scale='Blues')
                fig.update_layout(title='Kemandirian Pangan Per Rumah Tangga', xaxis_title='Nama Kepala Keluarga', yaxis_title='Rata-rata Kemandirian Pangan (%)')
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Top 5 Keluarga dengan Kemandirian Tertinggi
                top5 = data_kemandirian_rumah_tangga.nlargest(5, 'Rata-rata')
                st.markdown('**🏆 Top 5 Keluarga dengan Kemandirian Pangan Tertinggi**')
                st.table(top5[['Data', 'Rata-rata']])
            else:
                st.warning('Kolom "Data" atau "Rata-rata" tidak ditemukan dalam data.')
        else:
            st.error('Gagal memuat data. Pastikan format file benar dan sesuai.')
    else:
        st.info('Silakan upload file **Data Kemandirian Pangan Per Rumah Tangga** pada tab ini.')

with tabs[2]:
    st.header('🌾 Data Kemandirian Pangan Per Dusun')
    data_kemandirian_dusun_file = st.file_uploader('Upload Data Kemandirian Pangan Per Dusun (CSV atau Excel)', type=['csv', 'xlsx'], key='data_kemandirian_dusun')
    if data_kemandirian_dusun_file is not None:
        data_kemandirian_dusun = load_data(data_kemandirian_dusun_file)
        if data_kemandirian_dusun is not None:
            # Membersihkan kolom 'Rata-rata'
            if 'Rata-rata' in data_kemandirian_dusun.columns:
                data_kemandirian_dusun['Rata-rata'] = data_kemandirian_dusun['Rata-rata'].astype(str).str.replace('%', '').str.strip()
                data_kemandirian_dusun['Rata-rata'] = pd.to_numeric(data_kemandirian_dusun['Rata-rata'], errors='coerce')
            with st.expander("🔍 Lihat Data Kemandirian Pangan Per Dusun"):
                st.write(data_kemandirian_dusun)
            
            # Visualisasi
            if 'Data' in data_kemandirian_dusun.columns and 'Rata-rata' in data_kemandirian_dusun.columns:
                st.subheader('🌾 Kemandirian Pangan Per Dusun')
                fig = px.treemap(data_kemandirian_dusun, path=['Data'], values='Rata-rata', color='Rata-rata', color_continuous_scale='Viridis')
                fig.update_layout(title='Kemandirian Pangan Per Dusun')
                st.plotly_chart(fig, use_container_width=True)
                
                # Rata-rata Kemandirian Pangan
                avg_kemandirian = data_kemandirian_dusun['Rata-rata'].mean()
                st.markdown(f'**📊 Rata-rata Kemandirian Pangan:** {avg_kemandirian:.2f}%')
            else:
                st.warning('Kolom "Data" atau "Rata-rata" tidak ditemukan dalam data.')
        else:
            st.error('Gagal memuat data. Pastikan format file benar dan sesuai.')
    else:
        st.info('Silakan upload file **Data Kemandirian Pangan Per Dusun** pada tab ini.')

# Footer
st.markdown(
    """
    <hr>
    <div style='text-align: center;'>
        <small>© 2023 Dashboard Data Pangan. All rights reserved.</small>
    </div>
    """,
    unsafe_allow_html=True
)
