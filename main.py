import numpy as np
import pandas as pd

# Menjaga konsistensi data simulasi
np.random.seed(42)

print('=== SIMULASI PIPELINE DATA SENSOR IoT (PM 2.5 & LINGKUNGAN) ===')

# ================= ================= =================
# 1. SIMULASI STREAMING DATA SENSOR MENTAH (RAW DATA)
# ================= ================= =================
n_records = 1500
timestamps = pd.date_range(start='2026-06-01', periods=n_records, freq='h')

raw_data = {
    'timestamp': timestamps,
    'sensor_id': np.random.choice(['ENV-NODE-01', 'ENV-NODE-02', 'ENV-NODE-03'], size=n_records),
    # Simulasi pembacaan PM 2.5 dengan beberapa nilai anomali/noise ekstrem
    'pm25_level': np.random.normal(loc=35.0, scale=10.0, size=n_records),
    'temperature': np.random.normal(loc=28.0, scale=3.0, size=n_records),
    'humidity': np.random.normal(loc=75.0, scale=8.0, size=n_records),
}

df_raw = pd.DataFrame(raw_data)

# Sengaja menyisipkan anomali/nilai error sensor (Garbage In)
df_raw.loc[df_raw.sample(frac=0.03, random_state=42).index, 'pm25_level'] = -999.0  # Sensor error
df_raw.loc[df_raw.sample(frac=0.02, random_state=42).index, 'pm25_level'] = np.nan   # Missing value

print(f'Total Data Sensor Mentah Masuk: {len(df_raw)} baris')
print(f"Jumlah Nilai Anomali/Missing Terdeteksi: {df_raw['pm25_level'].isna().sum() + (df_raw['pm25_level'] == -999.0).sum()}\n")

# ================= ================= =================
# 2. DATA PREPROCESSING & KALIBRASI DI EDGE/GATEWAY
# ================= ================= =================
# Langkah Pembersihan: Mengatasi nilai error (-999.0) dan missing values (NaN)
df_clean = df_raw.copy()
df_clean.loc[df_clean['pm25_level'] < 0, 'pm25_level'] = np.nan
df_clean['pm25_level'] = df_clean['pm25_level'].fillna(df_clean['pm25_level'].mean())

# Kalibrasi sederhana: Koreksi offset sensor lingkungan
df_clean['pm25_calibrated'] = df_clean['pm25_level'] * 0.95 

# ================= ================= =================
# 3. SISTEM PERINGATAN DINI (THRESHOLD & ALERT)
# ================= ================= =================
# Menentukan status kualitas udara berdasarkan ambang batas bahaya (Misal: > 50.0)
HAZARD_THRESHOLD = 50.0
df_clean['status_bahaya'] = df_clean['pm25_calibrated'].apply(
    lambda x: 'BERBAHAYA/ALERT' if x > HAZARD_THRESHOLD else 'Normal'
)

# Menampilkan ringkasan hasil pemrosesan
alert_count = (df_clean['status_bahaya'] == 'BERBAHAYA/ALERT').sum()
print('--- LAPORAN PEMPROSESAN DATA SENSOR IOT ---')
print(f"Data Berhasil Dibersihkan & Dikalibrasi: {len(df_clean)} baris")
print(f"Total Peringatan Dini (Alert) Terpicu: {alert_count} kejadian")
print(df_clean[['timestamp', 'sensor_id', 'pm25_calibrated', 'status_bahaya']].tail(5))