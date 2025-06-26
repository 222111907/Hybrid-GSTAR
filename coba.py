import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# === CONFIG STREAMLIT ===
st.set_page_config(page_title="Dashboard", layout="wide")

# === TITLE DASHBOARD ===
st.markdown(
    """
    <h1 style='text-align: center;'>
        Peramalan Jumlah Wisatawan di Kabupaten/Kota di Provinsi DI Yogyakarta Menggunakan GSTAR-GLS-SVR
    </h1>
    """,
    unsafe_allow_html=True
)

# === LOAD DATA ===
file_path = "C:/Users/Administrator/OneDrive/Dokumen/SKRIPSI NINIS/forecasting/hasil forecast svr/rekap svr.xlsx"
fitted_df = pd.read_excel(file_path, sheet_name='fitted value', index_col=0)
aktual_df = pd.read_excel(file_path, sheet_name='asli', index_col=0)
ramal_df = pd.read_excel(file_path, sheet_name='forecast', index_col=0)
tanggal_forecast = pd.read_excel(file_path, sheet_name='forecast')[['Bulan-tahun']]

# === DROPDOWN WILAYAH ===

daftar_wilayah = {
    "Kulon Progo": "KP",
    "Bantul": "BT",
    "Gunung Kidul": "GK",
    "Sleman": "SL",
    "Kota Yogyakarta": "KY"
}

wilayah_pilihan = st.selectbox("Pilih Wilayah:", list(daftar_wilayah.keys())
                               , placeholder="Pilih Wilayah")  # Teks yang muncul saat belum memilih
kolom = daftar_wilayah[wilayah_pilihan]

# =============JIKA ADA MAIN PAGE====================
# wilayah_pilihan = st.selectbox(
#     "Pilih Wilayah", 
#     options=list(daftar_wilayah.keys()), 
#     index=None,               # Tidak ada pilihan default
#     placeholder="Pilih Wilayah"  # Teks yang muncul saat belum memilih
# )

# if wilayah_pilihan is not None:
#     kolom = daftar_wilayah[wilayah_pilihan]
#     st.write(f"Anda memilih wilayah: {wilayah_pilihan} ({kolom})")
# else:
#     st.info("Silakan pilih wilayah terlebih dahulu.")



# Ambil data berdasarkan wilayah yang dipilih
fitted = fitted_df[[kolom]]
aktual = aktual_df[[kolom]]
ramal = ramal_df[[kolom]]

# Atur index ramal sebagai tanggal forecast
forecast_index = tanggal_forecast.iloc[-len(ramal):]['Bulan-tahun']
ramal.index = forecast_index

# Pastikan index dalam format datetime
aktual.index = pd.to_datetime(aktual.index)
ramal.index = pd.to_datetime(ramal.index)

# === PLOT UTAMA (GARIS) ===
st.markdown(""" """)
st.markdown(""" """)
st.markdown(""" """)
fig, ax = plt.subplots(figsize=(8, 3.5))  # Ukuran lebih kecil dan lebar
ax.plot(aktual, label='Data Aktual', color='blue', linewidth=1.5)
ax.plot(fitted, linestyle='--', color='orange', label='Model Fitting', linewidth=1.5)
ax.plot(ramal, label='Forecast', color='red', linestyle='--', linewidth=1.5)

# === GARIS PEMISAH ANTARA FITTED & FORECAST ===
tanggal_mulai_forecast = ramal.index[0]  # Asumsikan index sudah datetime
ax.axvline(x=tanggal_mulai_forecast, color='black', linestyle=':', linewidth=1)

# === Set xticks secara manual ===
# Gabungkan semua index dari aktual dan ramal untuk tahu rentang tahunnya
all_dates = pd.date_range(start=aktual.index.min(), end=ramal.index.max(), freq='YS')  # YS = Year Start
years = [pd.to_datetime(str(date.year)) for date in all_dates]  # Buat list tanggal 1 Januari tiap tahun

ax.set_xticks(years)
ax.set_xticklabels([str(date.year) for date in years], fontsize=6, rotation=45)

ax.set_title(f"Peramalan Hybrid Jumlah Wisatawan - {wilayah_pilihan}", fontsize=10)
ax.set_xlabel("Tahun", fontsize=6)
ax.set_ylabel("Jumlah Wisatawan", fontsize=6)
ax.tick_params(axis='x', labelsize=6)
ax.tick_params(axis='y', labelsize=6)
ax.legend(fontsize=6)
ax.grid(True, linestyle='--', linewidth=0.5)
plt.xticks(rotation=45)

# === TAMPILKAN PLOT GARIS ===
st.pyplot(fig)

# === PERHITUNGAN DAN VISUALISASI DONUT ===
if 2023 in aktual.index.year:
    aktual_2023 = aktual[aktual.index.year == 2023]
    total_2023 = aktual_2023[kolom].sum()

    ramal_2024 = ramal[ramal.index.year == 2024]
    total_2024 = ramal_2024[kolom].sum()

    # Hitung selisih dan persentase
    selisih = total_2024 - total_2023
    persentase = (selisih / total_2023) * 100
    persen_donut = max(0, min(abs(persentase), 100))

    warna_utama = '#44B46F' if persentase >= 0 else '#FF6B6B'
    sizes = [persen_donut, 100 - persen_donut]
    colors = [warna_utama, '#D3D3D3']

    fig_donut, ax_donut = plt.subplots(figsize=(2.5, 2.5), dpi=150)
    wedges, texts = ax_donut.pie(
        sizes,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.3)
    )

    arrow = "▲" if persentase >= 0 else "▼"
    arrow_color = '#44B46F' if persentase >= 0 else '#FF6B6B'
    
    # Format persentase pakai koma untuk desimal
    persentase_str = f"{abs(persentase):.1f}".replace(".", ",")

    # Tampilkan di tengah donat
    ax_donut.text(
        0, 0, 
        f"{arrow} {persentase_str}%", 
        ha='center', va='center', 
        fontsize=12, fontweight='bold', color=arrow_color
    )

    ax_donut.axis('equal')

    # === LAYOUT BAWAH: DONUT & INTERPRETASI ===
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(
            "<h3 style='text-align: center; font-size: 24px;'>Peramalan Persentase Jumlah Wisatawan (2024)</h3>",
            unsafe_allow_html=True
        )
        # st.markdown("##### Peramalan Persentase Jumlah Wisatawan (2024)")
        st.pyplot(fig_donut)

    with col2:
        # Format angka ke format ribuan dengan titik sebagai pemisah
        total_2024_str = f"{total_2024:,.0f}".replace(",", ".")
        total_2023_str = f"{total_2023:,.0f}".replace(",", ".")
        persentase_str = f"{abs(persentase):.2f}".replace(".", ",")

        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        # st.markdown(
        #     "<h3 style='text-align: center; font-size: 24px;'>Interpretasi Hasil Peramalan</h3>",
        #     unsafe_allow_html=True
        # )

        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        st.markdown(""" """)
        
        st.markdown(
            """
            <div style='
                font-size: 15px;
                text-align: justify;
                margin-top: 30px;  /* Geser ke bawah */
            '>
            """, unsafe_allow_html=True
        )

        if persentase >= 0:
            st.markdown(
                f"""<div style='text-align: center; font-size: 18px; line-height: 1.6;'>
                Jumlah wisatawan di <b>{wilayah_pilihan}</b> pada tahun <b>2024</b> diperkirakan mencapai <b>{total_2024_str}</b>, 
                mengalami <b>kenaikan</b> sekitar <b>{persentase_str}%</b> dibandingkan tahun <b>2023</b> yang tercatat sebanyak <b>{total_2023_str}</b> wisatawan. 
                Sementara itu, hingga Mei 2025, hasil peramalan jumlah kunjungan wisatawan menunjukkan kecenderungan terus <b>meningkat</b>. 
                Hasil peramalan menunjukkan <b>pola musiman</b> yang sama dengan tahun sebelumnya, yakni terdapat lonjakan jumlah wisatawan pada bulan <b>Desember</b>.
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                Jumlah wisatawan di <b>{wilayah_pilihan}</b> pada tahun <b>2024</b> diperkirakan mencapai <b>{total_2024_str}</b>, 
                mengalami <b>penurunan</b> sekitar <b>{persentase_str}%</b> dibandingkan tahun <b>2023</b> yang tercatat sebanyak <b>{total_2023_str}</b> wisatawan. 
                Sementara itu, hingga Mei 2025, hasil peramalan jumlah kunjungan wisatawan menunjukkan kecenderungan yang sama. Hasil peramalan 
                menunjukkan <b>pola musiman</b> yang sama dengan tahun sebelumnya yakni terdapat lonjakan jumlah wisatawan pada bulan <b>Desember</b>.
.
                """, unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("Data tahun 2023 tidak tersedia untuk wilayah ini.")
