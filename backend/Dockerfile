# Gunakan image Python 3.9 yang ringan
FROM python:3.9-slim

# Tentukan direktori kerja dalam container
WORKDIR /app

# Salin file requirements.txt dan install dependensi
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua kode backend ke dalam container
COPY . .

# Tentukan port yang akan digunakan
EXPOSE 5000

# Jalankan aplikasi Flask saat container dijalankan
CMD ["python", "app.py"]
