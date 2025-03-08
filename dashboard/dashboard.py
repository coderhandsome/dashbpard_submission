import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Muat dataset
day_data = pd.read_csv("day_data.csv")  # Ganti dengan path dataset harian
hour_data = pd.read_csv("hour_data.csv")  # Ganti dengan path dataset per jam
# Ubah kolom tanggal menjadi datetime
day_data["dteday"] = pd.to_datetime(day_data["dteday"])
# Ubah nilai tahun dari 0,1 menjadi 2011,2012
day_data["yr"] = day_data["yr"].map({0: 2011, 1: 2012})
hour_data["yr"] = hour_data["yr"].map({0: 2011, 1: 2012})
# Buat Sidebar filter
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun:", ["Semua"] + sorted(day_data["yr"].unique().tolist()))
# Kondisi saat tahun dipilih
if selected_year != "Semua":
    day_filtered = day_data[day_data["yr"] == selected_year]
    hour_filtered = hour_data[hour_data["yr"] == selected_year]
else:
    day_filtered = day_data
    hour_filtered = hour_data

# ----- DASHBOARD -----
st.title("Dashboard Penyewaan Sepeda")
# ---- Menentukan skala ----
max_y_monthly = day_data.groupby(["yr", "mnth"])["cnt"].mean().max()
max_y_weekly = day_data.groupby("weekday")["cnt"].mean().max()

# ---- VISUALISASI 1: Tren Penyewaan Sepeda Bulanan ----
st.subheader("Tren Penyewaan Sepeda Bulanan")
monthly_trend = day_filtered.groupby(["yr", "mnth"])["cnt"].mean().reset_index()
fig, ax = plt.subplots()
colors = {2011: "blue", 2012: "red"}
for year in monthly_trend["yr"].unique():
    ax.plot(
        monthly_trend[monthly_trend["yr"] == year]["mnth"],
        monthly_trend[monthly_trend["yr"] == year]["cnt"],
        marker="o", linestyle="-", color=colors[year], label=str(year)
    )
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Tren penyewaan sepeda bulanan")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.legend()
ax.grid(True)
ax.set_ylim(0, max_y_monthly + 500)
st.pyplot(fig)

# ---- VISUALISASI 2: Rata-rata penyewaan perpari ----
st.subheader("Rata-rata Penyewaan Per Hari dalam Seminggu")
hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
day_filtered["weekday"] = day_filtered["weekday"].apply(lambda x: hari[x])
weekday_avg = day_filtered.groupby("weekday")["cnt"].mean().reset_index()
# Urutan untuk hari agar terurut
weekday_avg["weekday"] = pd.Categorical(weekday_avg["weekday"], categories=hari, ordered=True)
weekday_avg = weekday_avg.sort_values("weekday")
colors = ["#89CFF0" if day != "Jumat" else "blue" for day in weekday_avg["weekday"]]
fig, ax = plt.subplots()
sns.barplot(x="weekday", y="cnt", data=weekday_avg, palette=colors, ax=ax)
ax.set_xlabel("Hari")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Rata-rata Penyewaan sepeda per hari dalam seminggu")
ax.grid(axis="y", linestyle="-")
ax.set_ylim(0, max_y_weekly + 1500)
plt.xticks(rotation=45)
st.pyplot(fig)

# ---- VISUALISASI 3: Rata-rata Penyewaan per Jam ----
st.subheader("Rata-rata Penyewaan Sepeda per Jam")
hour_avg = hour_filtered.groupby("hr")["cnt"].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x="hr", y="cnt", data=hour_avg, color="blue", ax=ax)
ax.set_xlabel("Jam dalam sehari")
ax.set_ylabel("Rata-rata penyewaan sepeda")
ax.set_title("Rata-rata penyewaan berdasarkan jam dalam sehari")
ax.set_xticks(range(0, 24))
ax.grid(axis="y", linestyle="-")
ax.set_ylim(0, 600)
ax.set_yticks(range(0, 601, 100))
st.pyplot(fig)

# ---- Kesimpulan ----
st.subheader("Kesimpulan")
st.markdown("""
- Conclution pertanyaan 1: Kapan jumlah penyewaan sepeda mencapai tingkat tertinggi dan terendah?
    - Peminjaman tahun 2012 lebih tinggi dibandingkan tahun 2011
    - Mei-Agustus memiliki penyewaan tertinggi dan Desember-Februari memiliki penyewaan terendah.
- Conclution pertanyaan 2: Bagaimana variasi jumlah penyewaan sepeda pada setiap hari dalam seminggu?
    - Hari kerja (senin sampai jum'at) cenderung memiliki jumlah penyewaan lebih tinggi dibandingkan akhir peka.
    - Sabtu & minggu memiliki penyewaan lebih rendah
    - Penyewaan terbanyak biasanya terjadi pada hari kerja
- Conclution pertanyaan 3: Pada jam berapa dalam sehari jumlah penyewaan sepeda paling tinggi dan paling rendah?
    - Dua puncak penyewaan pada pagi hari (07.00-09.00) dan sore hari (17.00-19.00)
    - Penyewaan paling sedikit terhadi pada pukul 00.00-05.00.
    - Setelah pukul 21.00 penyewaan menurun drastis.
""")