
# 🧠 Indodax Trailing Stop-Loss Bot

Bot ini berfungsi untuk **memantau harga koin di Indodax secara real-time** dan melakukan penjualan otomatis jika harga turun dari puncak (peak) lebih dari persentase yang ditentukan (misalnya 5%). Bot ini berguna untuk **mengamankan profit saat harga mulai turun**.

## 🚀 Fitur
- Memantau harga koin setiap 5 detik
- Mencatat harga tertinggi sejak bot dijalankan
- Menjual otomatis jika harga turun dari puncaknya sesuai `STOP_LOSS_PERCENT`
- Menampilkan saldo dan nilai portofolio kamu secara real-time

## ⚙️ Cara Kerja
1. Bot dijalankan dan mencatat harga saat itu sebagai **harga puncak pertama (peak)**.
2. Jika harga naik, bot memperbarui nilai **peak** dan **batas stop-loss**.
3. Jika harga turun ke bawah batas stop-loss, bot akan memberi opsi untuk menjual seluruh saldo koin.
4. Menampilkan saldo, estimasi nilai koin, dan total aset secara real-time.

## 🛠️ Setup

### 1. Install Library
Bot ini menggunakan Python. Pastikan sudah ter-install `requests`:
```bash
pip install requests
```

### 2. Ganti Konfigurasi API
Edit file Python dan ganti bagian berikut:
```python
API_KEY = 'GANTI_DENGAN_API_KEY_KAMU'
API_SECRET = 'GANTI_DENGAN_API_SECRET_KAMU'
PAIR = 'rvm_idr'  # Ganti dengan pair yang kamu gunakan
STOP_LOSS_PERCENT = 5  # Misalnya trailing stop-loss 5%
BUY_PRICE = 100000  # Harga beli untuk hitung profit
```

### 3. Jalankan Bot
```bash
python nama_file_bot.py
```

## 📌 Catatan
- Pastikan API Indodax kamu memiliki izin **Trade** dan **Info**.
- Gunakan hanya untuk eksperimen dan jangan gunakan di akun utama jika belum paham risikonya.
- Selalu test dulu di market yang volumenya kecil atau akun dummy.

## 💡 Contoh Output
```
Harga Sekarang: Rp 407 | Peak: Rp 442 | Stop-Loss: Rp 419
[Saldo] RVM: 380.32941176 (~Rp 100,000) | IDR: Rp 0 | Total: Rp 1000,000

🚨 Harga menyentuh batas trailing stop-loss!
Apakah kamu ingin menjual sekarang? (y/n):
```

## 🧾 Lisensi
Open-source dan bebas dimodifikasi. Gunakan dengan tanggung jawab pribadi.


## Dukung Saya di Trakteer

Scan QR code berikut untuk memberikan dukungan:

![Trakteer QR](./trakteer-qr.png)

Atau klik langsung: [https://trakteer.id/Syalpra/link](https://trakteer.id/Syalpra/link)
