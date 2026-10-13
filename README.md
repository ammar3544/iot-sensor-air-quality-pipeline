# IoT Pipeline: Pembersihan Data Sensor & Peringatan Dini Lingkungan

Repositori ini berisi studi kasus penanganan data sensor mentah, kalibrasi, dan sistem *alert* pada infrastruktur *Internet of Things (IoT)* (mengacu pada materi kuliah umum HPC & AI mengenai integrasi data lokal dan penanganan tantangan lapangan).

## Fitur Proyek
- **Data Cleaning (Garbage In, Garbage Out Mitigation)**: Menangani nilai error sensor (`-999.0`) dan data kosong (`NaN`) sebelum dikirim ke server pusat.
- **Sensor Calibration**: Penyesuaian nilai pembacaan alat agar selaras dengan standar lingkungan.
- **Threshold Alert System**: Sistem deteksi otomatis untuk peringatan dini kualitas udara buruk.

## Cara Menjalankan
1. Install dependencies: `pip install -r requirements.txt`
2. Jalankan skrip: `python main.py`