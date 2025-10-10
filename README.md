# Prediksi Produksi Padi di Wilayah Sumatera

Proyek ini bertujuan untuk memprediksi jumlah produksi padi di wilayah Sumatera menggunakan model pembelajaran mesin. Proyek ini terdiri dari frontend (HTML, CSS, JavaScript) dan backend (Flask, Python).

## Instalasi

Ikuti langkah-langkah berikut untuk menjalankan proyek ini secara lokal:

### Prasyarat

Pastikan Anda memiliki perangkat lunak berikut terinstal:
- Python 3.10.11
- pip (Python package installer)

### Langkah-langkah Instalasi

1. **Clone repositori ini:**

   ```bash
   git clone https://github.com/namauser/namaproject.git
   cd namaproject

2. **Install Dependensi:**
pip install -r requirements.txt

3. **Pastikan model dan file scaler tersedia:**
- best_model.pkl
- scaler_y.pkl
- scaler_X.pkl
- ohe_encoder.pkl
- feature_names.pkl
Tempatkan file-file tersebut di direktori proyek yang sesuai.

4. **Jalankan aplikasi:**
python app.py

### Penggunaan
1. **Buka browser dan akses http://127.0.0.1:5000/.**
2. **Isi formulir dengan data yang diperlukan:**
- Provinsi
- Tahun
- Luas Panen (ha)
- Curah Hujan (mm)
- Kelembapan (%)
- Suhu Rata-rata (°C)
3. **Klik tombol "Predict" untuk mendapatkan prediksi jumlah produksi padi.**

### Struktur Proyek
- index.html: Halaman utama aplikasi yang berisi formulir input.
- style.css: File CSS untuk styling halaman web.
- script.js: File JavaScript untuk menangani logika frontend.
- app.py: Backend Flask yang menangani prediksi menggunakan model machine learning.
=======
# BMGTSH_PROJECT
Prediksi Produksi Padi Menggunakan LightGBM.

