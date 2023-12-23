# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.title('Proyek Analisis Data: Bike Sharing')
    
    st.header('Bike Sharing')
    st.subheader('Latar Belakang ')
    st.markdown("""
    Sistem peminjaman sepeda merupakan generasi baru dari penyewaan sepeda tradisional di mana seluruh proses, mulai dari keanggotaan, peminjaman, hingga pengembalian, menjadi otomatis. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari posisi tertentu dan mengembalikannya di posisi lain. Saat ini, ada lebih dari 500 program peminjaman sepeda di seluruh dunia yang terdiri dari lebih dari 500 ribu sepeda. Sistem ini menarik perhatian besar karena perannya yang penting dalam masalah lalu lintas, lingkungan, dan kesehatan.
                
    Selain aplikasi dunia nyata yang menarik dari sistem peminjaman sepeda, karakteristik data yang dihasilkan oleh sistem ini membuatnya menarik untuk penelitian. Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan, posisi keberangkatan, dan posisi kedatangan secara eksplisit dicatat dalam sistem ini. Fitur ini menjadikan sistem peminjaman sepeda sebagai jaringan sensor virtual yang dapat digunakan untuk mendeteksi mobilitas di kota. Oleh karena itu, diharapkan bahwa sebagian besar peristiwa penting di kota dapat dideteksi melalui pemantauan data ini.
    """)

    st.subheader('Pertanyaan Analisis')
    st.markdown("""
    1. Analisis perbandingan jumlah peminjaman perbulan antara tahun 2011 dan 2012, apakah ada peningkatan?
    2. Pada jam berapa peminjaman sepeda tertinggi, kenapa hal tersebut bisa terjadi?
    """)

    st.subheader('Exploratory Data Analysis (EDA)')
    st.markdown('##### EDA Pertanyaan 1')
    day_df = pd.read_csv('data/day.csv')

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    day_df['tahun'] = day_df['dteday'].dt.year
    day_df['bulan'] = day_df['dteday'].dt.month

    total_rentals_by_month = day_df.groupby(['tahun', 'bulan'])['cnt'].sum().reset_index()

    total_rentals_by_month = total_rentals_by_month.rename(columns={'bulan': 'bulan', 'cnt': 'jumlah'})

    df_2011 = total_rentals_by_month[total_rentals_by_month['tahun'] == 2011].drop('tahun', axis=1)
    df_2012 = total_rentals_by_month[total_rentals_by_month['tahun'] == 2012].drop('tahun', axis=1)

    st.text('Tabel jumlah peminjaman sepeda pada tahun 2011:')
    st.dataframe(df_2011, width=200, height=460, hide_index=True)
    st.text('Tabel jumlah peminjaman sepeda pada tahun 2012:')
    st.dataframe(df_2012, width=200, height=460, hide_index=True)
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])


    day_df['year'] = day_df['dteday'].dt.year

    total_rentals_by_year = day_df.groupby('year')['cnt'].sum().reset_index()

    for index, row in total_rentals_by_year.iterrows():
        st.text(f'Total peminjaman sepeda pada tahun {row["year"]} sebanyak: {row["cnt"]:,}')

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    day_df['year'] = day_df['dteday'].dt.year

    total_rentals_by_year = day_df.groupby('year')['cnt'].sum().reset_index()


    total_presentation = (total_rentals_by_year['cnt'][total_rentals_by_year['year'] == 2012].values[0] - total_rentals_by_year['cnt'][total_rentals_by_year['year'] == 2011].values[0]) / total_rentals_by_year['cnt'][total_rentals_by_year['year'] == 2011].values[0] * 100


    st.write('Presentase perbedaan jumlah peminjaman dari tahun 2011 ke 2012 sebanyak ', f"{total_presentation:.2f}%")

    st.markdown('##### EDA Pertanyaan 2')

    hour_df = pd.read_csv('data/hour.csv')

    total_rentals_by_hour = hour_df.groupby('hr')['cnt'].sum().reset_index()


    total_rentals_by_hour = total_rentals_by_hour.rename(columns={'hr': 'jam', 'cnt': 'jumlah'})


    max_rentals_hour = total_rentals_by_hour['jam'][total_rentals_by_hour['jumlah'].idxmax()]


    st.write("\nTotal Jumlah Peminjaman per Jam pada tahun 2011 dan 2012:")
    st.dataframe(total_rentals_by_hour, width=200, height=890, hide_index=True)
    st.write("Peminjaman tertinggi ada pada jam: ", max_rentals_hour.max())

    st.subheader('Visualization & Explanatory Analysis')
    st.markdown("##### Pertanyaan 1")

    day_df = pd.read_csv('data/day.csv')

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    day_df['year'] = day_df['dteday'].dt.year
    day_df['month'] = day_df['dteday'].dt.month

    total_rentals_by_month = day_df.groupby(['year', 'month'])['cnt'].sum().reset_index()

    plt.figure(figsize=(12, 8))
    sns.barplot(x='month', y='cnt', hue='year', data=total_rentals_by_month, palette='viridis')
    plt.title('Analisis perbandingan jumlah peminjaman per bulan antara tahun 2011 dan 2012')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Peminjaman')
    plt.legend(title='Tahun', loc='upper right')

    st.pyplot(plt)

    total_rentals_by_year = day_df.groupby('year')['cnt'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x='year', y='cnt', hue='year', data=total_rentals_by_year,
                palette={2011: 'lightcoral', 2012: 'red'}, alpha=0.7)
    plt.title('Total Peminjaman Sepeda per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Total Peminjaman')

    st.pyplot(plt)

    st.markdown("##### Pertanyaan 2")

    hour_df = pd.read_csv('data/hour.csv')

    total_rentals_by_hour = hour_df.groupby('hr')['cnt'].sum().reset_index()

    max_rentals_hour = total_rentals_by_hour['hr'][total_rentals_by_hour['cnt'].idxmax()]

    plt.figure(figsize=(10, 6))
    plt.bar(total_rentals_by_hour['hr'], total_rentals_by_hour['cnt'], color='skyblue')
    plt.title('Jumlah Peminjaman Sepeda per Jam')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Peminjaman')

    st.pyplot(plt)

    st.subheader('Conclusion')
    st.markdown("""
    - Kesimpulan dari hasil analisis pertanyaan pertama, bahwa terjadi perkembangan dalam jumlah peminjaman jika dibandingkan jumlah bulanan antara tahun 2011 dan 2012. Yang dimana total peminjaman pada tahun 2011 ada sebanyak 1,243,103, sedangkan pada tahun 2012 sebanyak 2,049,576. Ketertarikan dalam peminjaman sepeda sebagai moda transportasi meningkat hingga 64,8% pada tahun 2012.

    - Kesimpulan dari hasil analisis pertanyaan kedua, peminjaman tertinggi terjadi pada jam 17, yang dimana pada jam tersebut adalah jam berakhirnya aktifitas (waktu pulang) bila merunut pada jam kerja universal (9 to 5), dikarenakan selain pada jam 17 (posisi pertama jumlah peminjaman tertinggi) dan 18 (posisi kedua jumlah peminjaman tertinggi), terjadi kenaikkan peminjaman juga pada jam 8 (posisi ketiga jumlah peminjaman tertinggi) yang dimana pada jam tersebut biasanya adalah awal untuk memulai aktifitas.
    """)


if __name__ == "__main__":
    run()
