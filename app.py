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
            df = pd.read_csv(file, encoding='utf-8', header=1)  # Header pada baris pertama
        else:
            df = pd.read_excel(file, header=1)  # Header pada baris pertama
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
            st.subheader('📍 Filter Data')
            filter_option = st.selectbox('Pilih Opsi Filter', ['Semua Data', 'Dusun', 'Desa/Kelurahan', 'Kecamatan'])
            if filter_option == 'Dusun':
                if 'Dusun' in data_rumah_tangga.columns:
                    dusun_list = data_rumah_tangga['Dusun'].dropna().unique()
                    selected_dusun = st.multiselect('Pilih Dusun', options=dusun_list, default=dusun_list)
                    filtered_data = data_rumah_tangga[data_rumah_tangga['Dusun'].isin(selected_dusun)]
                else:
                    st.warning('Kolom "Dusun" tidak ditemukan dalam data.')
                    filtered_data = data_rumah_tangga
            elif filter_option == 'Desa/Kelurahan':
                if 'Desa/Kelurahan' in data_rumah_tangga.columns:
                    desa_list = data_rumah_tangga['Desa/Kelurahan'].dropna().unique()
                    selected_desa = st.multiselect('Pilih Desa/Kelurahan', options=desa_list, default=desa_list)
                    filtered_data = data_rumah_tangga[data_rumah_tangga['Desa/Kelurahan'].isin(selected_desa)]
                else:
                    st.warning('Kolom "Desa/Kelurahan" tidak ditemukan dalam data.')
                    filtered_data = data_rumah_tangga
            elif filter_option == 'Kecamatan':
                if 'Kecamatan' in data_rumah_tangga.columns:
                    kecamatan_list = data_rumah_tangga['Kecamatan'].dropna().unique()
                    selected_kecamatan = st.multiselect('Pilih Kecamatan', options=kecamatan_list, default=kecamatan_list)
                    filtered_data = data_rumah_tangga[data_rumah_tangga['Kecamatan'].isin(selected_kecamatan)]
                else:
                    st.warning('Kolom "Kecamatan" tidak ditemukan dalam data.')
                    filtered_data = data_rumah_tangga
            else:
                filtered_data = data_rumah_tangga

            # 1. Visualisasi Data Rumah Tangga
            st.subheader('1️⃣ Visualisasi Data Rumah Tangga')
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

            # 2. Peta Sebaran Rumah Tangga
            st.subheader('2️⃣ Peta Sebaran Rumah Tangga')
            if 'Koordinat GPS' in filtered_data.columns:
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
            else:
                st.warning('Kolom "Koordinat GPS" tidak ditemukan dalam data.')

            # 3. 🍚 Analisis Produksi
            st.subheader('3️⃣ 🍚 Analisis Produksi')
            produksi_cols = {
                'Produksi Karbohidrat': ['Beras Lokal (Sawah/Ladang dalam Kg)', 'Singkong', 'Jagung Lokal', 'Jagung Hibrida', 'Umbi-umbian lain', 'Sorgum', 'Jewawut/Weteng'],
                'Produksi Pertanian': ['Nama Tanaman', 'Jenis Pangan', 'Varietas', 'Luas Lahan', 'Produktivitas'],
                'Minyak Masak': ['Minyak Masak', 'Minyak Kelapa'],
                'Bumbu dan Rempah': ['Cabai Besar', 'Cabai Kecil', 'Kemiri', 'Kunyit', 'Jahe', 'Sereh', 'Lengkuas', 'Jeruk Nipis', 'Mete', 'Lain-lain']
            }
            col1, col2 = st.columns(2)
            with col1:
                for category, cols in produksi_cols.items():
                    available_cols = [col for col in cols if col in filtered_data.columns]
                    if available_cols:
                        st.markdown(f'**{category}**')
                        for col in available_cols:
                            filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
                        total_produksi = filtered_data[available_cols].sum()
                        produksi_df = total_produksi.reset_index()
                        produksi_df.columns = ['Komoditas', 'Jumlah']
                        fig = px.bar(produksi_df, x='Komoditas', y='Jumlah', color='Jumlah', color_continuous_scale='Viridis')
                        fig.update_layout(title=f'Produksi {category}', xaxis_title='Komoditas', yaxis_title='Jumlah')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f'Tidak ada data untuk {category}.')

            # 4. Analisis Konsumsi Pangan
            
            konsumsi_cols = {
                'Konsumsi Karbohidrat': ['Beras Lokal (Sawah/Ladang)', 'Singkong.1', 'Jagung Lokal.1', 'Jagung Hibrida.1', 'Umbi-umbian lain.1', 'Sorgum.1', 'Jewawut/Weteng.1'],
                'Konsumsi Pertanian': ['Nama Tanaman', 'Jenis Pangan', 'Varietas', 'Luas Lahan', 'Produktivitas'],
                'Minyak Masak': ['Minyak Masak.1', 'Minyak Kelapa.1'],
                'Bumbu dan Rempah': ['Cabai Besar.1', 'Cabai Kecil.1', 'Kemiri.1', 'Kunyit.1', 'Jahe.1', 'Sereh.1', 'Lengkuas.1', 'Jeruk Nipis.1', 'Mete.1', 'Lain-lain.1'],
                'Konsumsi Sayur dan Buah': ['Daun Ubi', 'Kangkung', 'Kubis', 'Sawi', 'Bayam', 'Brokoli', 'Wortel', 'Jantung Pisang', 'Kelor', 'Bunga dan Daun Pepaya', 'Pakis/Paku', 'Rebung', 'Mangga', 'Alpukat', 'Jeruk', 'Anggur', 'Buah Naga', 'Mete', 'Pisang', 'Rambutan', 'Nanas', 'Salak', 'Pepaya', 'Kelapa', 'Tomat', 'Timun', 'Labu', 'Kemangi'],
                'Makanan dan Minuman Olahan': ['Susu (Bubuk/UHT)', 'Kental Manis', 'Minuman Kemasan', 'Minuman Fermentasi', 'Gula Pasir', 'Kopi', 'Teh', 'Mie Instan', 'Biskuit/Roti/Kue Kemasan'],
                'Konsumsi Lain-lain': ['Rokok Kemasan', 'Tembakau', 'Pinang', 'Daun Sirih'],
                'Bahan Bakar': ['Minyak Tanah', 'Gas', 'Biaya Listrik', 'BBM']
            }
            with col2:
                st.subheader('4️⃣ Analisis Konsumsi Pangan')
                for category, cols in konsumsi_cols.items():
                    available_cols = [col for col in cols if col in filtered_data.columns]
                    if available_cols:
                        st.markdown(f'**{category}**')
                        for col in available_cols:
                            filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
                        total_konsumsi = filtered_data[available_cols].sum()
                        konsumsi_df = total_konsumsi.reset_index()
                        konsumsi_df.columns = ['Komoditas', 'Jumlah']
                        fig = px.bar(konsumsi_df, x='Komoditas', y='Jumlah', color='Jumlah', color_continuous_scale='Cividis')
                        fig.update_layout(title=f'Konsumsi {category}', xaxis_title='Komoditas', yaxis_title='Jumlah')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f'Tidak ada data untuk {category}.')

            # 5. Analisis Input Pertanian
            st.subheader('5️⃣ Analisis Input Pertanian')
            input_pertanian_cols = ['Pupuk', 'Pestisida/Herbisida/Fungisida', 'Benih', 'Upah Buruh', 'Sewa Alat dan Mesin Pertanian']
            available_input_cols = [col for col in input_pertanian_cols if col in filtered_data.columns]
            if available_input_cols:
                for col in available_input_cols:
                    filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
                total_input = filtered_data[available_input_cols].sum()
                input_df = total_input.reset_index()
                input_df.columns = ['Input Pertanian', 'Jumlah']
                fig = px.pie(input_df, names='Input Pertanian', values='Jumlah', color_discrete_sequence=px.colors.sequential.Blues)
                fig.update_layout(title='Proporsi Penggunaan Input Pertanian')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Tidak ada data untuk Input Pertanian.')

            # 6. Analisis Peternakan
            st.subheader('6️⃣ Analisis Peternakan')
            ternak_cols = ['Sapi', 'Kerbau', 'Kambing', 'Ayam', 'Bebek', 'Babi', 'Kuda']
            available_ternak_cols = [col for col in ternak_cols if col in filtered_data.columns]
            if available_ternak_cols:
                for col in available_ternak_cols:
                    filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
                total_ternak = filtered_data[available_ternak_cols].sum()
                ternak_df = total_ternak.reset_index()
                ternak_df.columns = ['Jenis Ternak', 'Jumlah']
                fig = px.bar(ternak_df, x='Jenis Ternak', y='Jumlah', color='Jumlah', color_continuous_scale='OrRd')
                fig.update_layout(title='Total Kepemilikan Ternak', xaxis_title='Jenis Ternak', yaxis_title='Jumlah')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Tidak ada data untuk Peternakan.')

            # 7. Analisis Perikanan
            st.subheader('7️⃣ Analisis Perikanan')
            perikanan_cols = ['Ikan dan Boga Laut Segar', 'Ikan dan Boga Laut Kering', 'Jenis Ikan', 'Jumlah Hasil']
            available_perikanan_cols = [col for col in perikanan_cols if col in filtered_data.columns]
            if available_perikanan_cols:
                for col in ['Ikan dan Boga Laut Segar', 'Ikan dan Boga Laut Kering', 'Jumlah Hasil']:
                    if col in filtered_data.columns:
                        filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
                total_perikanan = filtered_data[['Ikan dan Boga Laut Segar', 'Ikan dan Boga Laut Kering', 'Jumlah Hasil']].sum()
                perikanan_df = total_perikanan.reset_index()
                perikanan_df.columns = ['Komoditas Perikanan', 'Jumlah']
                fig = px.bar(perikanan_df, x='Komoditas Perikanan', y='Jumlah', color='Jumlah', color_continuous_scale='Teal')
                fig.update_layout(title='Total Produksi Perikanan', xaxis_title='Komoditas Perikanan', yaxis_title='Jumlah')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Tidak ada data untuk Perikanan.')

            # 8. Analisis Limbah
            st.subheader('8️⃣ Analisis Limbah')
            limbah_cols = ['Sumber Limbah', 'Pengolahan', 'Hasil Daur Ulang']
            
            if set(limbah_cols).issubset(filtered_data.columns):
                limbah_data = filtered_data[limbah_cols].copy()
                
                # Preprocessing Data Limbah
                limbah_data = limbah_data.fillna('')  # Isi nilai kosong dengan string kosong
                limbah_data['Sumber Limbah'] = limbah_data['Sumber Limbah'].str.capitalize()
                limbah_data['Pengolahan'] = limbah_data['Pengolahan'].str.capitalize().replace({'Tidak ada': 'Tidak diolah'})
                limbah_data['Hasil Daur Ulang'] = limbah_data['Hasil Daur Ulang'].str.capitalize().replace(
                    {'': 'Dibakar', 'Di buang': 'Dibakar', '0': 'Dibakar', 'Nan': 'Dibakar'}
                )
            
                # Pastikan tidak ada nilai numerik atau anonim
                def clean_numeric_values(value, default):
                    try:
                        float(value)  # Jika nilai numerik, ganti dengan default
                        return default
                    except ValueError:
                        return value
            
                limbah_data['Sumber Limbah'] = limbah_data['Sumber Limbah'].apply(lambda x: clean_numeric_values(x, 'Tidak diketahui'))
                limbah_data['Pengolahan'] = limbah_data['Pengolahan'].apply(lambda x: clean_numeric_values(x, 'Tidak diolah'))
                limbah_data['Hasil Daur Ulang'] = limbah_data['Hasil Daur Ulang'].apply(lambda x: clean_numeric_values(x, 'Dibakar'))
            
                # Visualisasi Sumber Limbah
                st.markdown('**Distribusi Sumber Limbah**')
                sumber_counts = limbah_data['Sumber Limbah'].value_counts().reset_index()
                sumber_counts.columns = ['Sumber Limbah', 'Jumlah']
                fig_sumber = px.pie(
                    sumber_counts, 
                    names='Sumber Limbah', 
                    values='Jumlah', 
                    hole=0.5, 
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                fig_sumber.update_traces(textposition='inside', textinfo='percent+label')
                fig_sumber.update_layout(title='Distribusi Sumber Limbah')
                st.plotly_chart(fig_sumber, use_container_width=True)
            
                # Visualisasi Pengolahan Limbah
                st.markdown('**Distribusi Pengolahan Limbah**')
                pengolahan_counts = limbah_data['Pengolahan'].value_counts().reset_index()
                pengolahan_counts.columns = ['Pengolahan', 'Jumlah']
                fig_pengolahan = px.pie(
                    pengolahan_counts, 
                    names='Pengolahan', 
                    values='Jumlah', 
                    hole=0.5, 
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                fig_pengolahan.update_traces(textposition='inside', textinfo='percent+label')
                fig_pengolahan.update_layout(title='Distribusi Pengolahan Limbah')
                st.plotly_chart(fig_pengolahan, use_container_width=True)
            
                # Visualisasi Hasil Daur Ulang
                st.markdown('**Distribusi Hasil Daur Ulang**')
                hasil_counts = limbah_data['Hasil Daur Ulang'].value_counts().reset_index()
                hasil_counts.columns = ['Hasil Daur Ulang', 'Jumlah']
                fig_hasil = px.pie(
                    hasil_counts, 
                    names='Hasil Daur Ulang', 
                    values='Jumlah', 
                    hole=0.5, 
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                fig_hasil.update_traces(textposition='inside', textinfo='percent+label')
                fig_hasil.update_layout(title='Distribusi Hasil Daur Ulang')
                st.plotly_chart(fig_hasil, use_container_width=True)
            
                # Menampilkan Data Limbah dalam tabel
                st.markdown('**Detail Data Limbah**')
                st.dataframe(limbah_data)
            else:
                st.warning('Tidak ada data untuk Limbah.')


            # 9. Analisis Pendidikan
            st.subheader('9️⃣ Analisis Pendidikan')
            pendidikan_cols = ['SPP (Iuran Sekolah)', 'Peralatan Sekolah/ATK', 'Transportasi/Kos/Jajan']
            available_pendidikan_cols = [col for col in pendidikan_cols if col in filtered_data.columns]
            if available_pendidikan_cols:
                for col in available_pendidikan_cols:
                    filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
                total_pendidikan = filtered_data[available_pendidikan_cols].sum()
                pendidikan_df = total_pendidikan.reset_index()
                pendidikan_df.columns = ['Pengeluaran Pendidikan', 'Jumlah']
                fig = px.bar(pendidikan_df, x='Pengeluaran Pendidikan', y='Jumlah', color='Jumlah', color_continuous_scale='Purples')
                fig.update_layout(title='Total Pengeluaran Pendidikan', xaxis_title='Jenis Pengeluaran', yaxis_title='Jumlah')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Tidak ada data untuk Pendidikan.')
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
