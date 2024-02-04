import requests

# Ganti URL dengan URL tempat aplikasi Flask berjalan
url = "http://localhost:5000/api/pricing"

# Ganti dengan token otentikasi yang sesuai
headers = {
    'Authorization': 'Bearer admin123',
    'X-User-Role': 'admin'  # Ganti dengan role yang sesuai
}

# Data yang akan dikirim ke API
data = [
    {'productid': 23, 'date': '2024-02-04 11:13:17.071'},
    {'productid': 16, 'date': '2022-02-4 11:13:17.021'},
    {'productid': 12, 'date': '2022-02-4 11:13:17.031'}
]

# Mengirim permintaan POST ke API
response = requests.post(url, json=data, headers=headers)

# Memeriksa status response
if response.status_code == 200:
    # Menampilkan hasil jika permintaan berhasil
    print(response.json())
else:
    # Menampilkan pesan kesalahan jika permintaan gagal
    print(f"Error: {response.status_code}, {response.text}")
