# Multivariate Deep Learning Framework for Indonesian Rupiah (USD/IDR) Exchange Rate Prediction

Penelitian ini mengimplementasikan kerangka kerja **Multivariate Deep Learning** untuk memprediksi pergerakan nilai tukar Rupiah terhadap Dolar Amerika Serikat (USD/IDR) dengan memanfaatkan indikator makroekonomi terintegrasi dan pengujian signifikansi statistik.

---

## 📌 Ringkasan Penelitian

- **Topik**: Prediksi Nilai Tukar USD/IDR (Exchange Rate Forecasting)
- **Metodologi**: Multivariate Time-Series Deep Learning
- **Model yang Diuji**:
  - **BiLSTM** (Bidirectional Long Short-Term Memory)
  - **LSTM** (Long Short-Term Memory)
  - **GRU** (Gated Recurrent Unit)
  - **CNN-LSTM** (Hybrid Convolutional & Recurrent Neural Network)
- **Fitur / Indikator Multivariat**:
  - Kurs Historis USD/IDR
  - Indikator Makroekonomi Indonesia (IHSG, BI Rate / Suku Bunga, Inflasi, Cadangan Devisa)
  - Indeks Global & Komoditas (DXY, Crude Oil, Emas)

---

## 📁 Struktur Direktori

```text
├── Deep_Learning_Rupiah_Prediction_v2.ipynb       # Notebook eksperimen utama prediksi kurs
├── Sentiment_Trend_Analysis_Indo_Economy.ipynb    # Notebook analisis sentimen ekonomi
├── indonesian_economic_indicators_final.csv       # Dataset indikator makroekonomi
├── best_bilstm_model.keras                        # Model bobot BiLSTM terlatih
├── best_gru_model.keras                           # Model bobot GRU terlatih
├── best_lstm_model.keras                          # Model bobot LSTM terlatih
├── best_cnn_lstm_model.keras                      # Model bobot CNN-LSTM terlatih
├── generate_figures.py                            # Script visualisasi & grafik publikasi
├── fig1_usdidr_trend.png                          # Visualisasi tren nilai tukar
├── fig2_correlation_heatmap.png                   # Korelasi antar fitur ekonomi
├── fig3_framework_architecture.png                # Arsitektur framework deep learning
├── fig4_model_comparison.png                      # Perbandingan performa model
├── fig5_actual_vs_predicted.png                   # Grafik aktual vs prediksi
├── fig6_feature_importance.png                    # Analisis kontribusi fitur
└── README.md                                      # Dokumentasi repositori
```

---

## 🚀 Cara Menjalankan

### 1. Prasyarat (Dependencies)
Pastikan Python 3.9+ telah terpasang, lalu instal paket berikut:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn tensorflow keras jupyter
```

### 2. Menjalankan Notebook Eksperimen
Jalankan Jupyter Notebook untuk mereproduksi hasil pelatihan model:
```bash
jupyter notebook Deep_Learning_Rupiah_Prediction_v2.ipynb
```

### 3. Menghasilkan Gambar & Grafik Publikasi
```bash
python generate_figures.py
```

---

## 📊 Hasil Evaluasi & Temuan Utama
- Framework multivariat menunjukkan peningkatan akurasi prediksi dibandingkan pemodelan univariat.
- Model **BiLSTM** dan **CNN-LSTM** mampu menangkap dinamika temporal jangka panjang dan fitur lokal dari fluktuasi ekonomi makro dengan RMSE dan MAPE yang kompetitif.

---

## 👨‍💻 Peneliti
- **Asep Surahman** — Program Magister (S2), Universitas Nusa Putra
