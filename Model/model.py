import psycopg2
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Fungsi untuk mendapatkan data dari PostgreSQL
def get_data_from_postgres():
    # Ganti dengan informasi koneksi PostgreSQL Anda
    conn = psycopg2.connect(
        host="localhost",
        database="dataengineer",
        user="postgres",
        password="barabai123"
    )

    # Membuat objek cursor untuk melakukan operasi database
    cursor = conn.cursor()

    # Misalnya, asumsikan data yang diambil dari tabel 'your_table_name'
    query = "SELECT * FROM pricerecommendation;"
    cursor.execute(query)

    # Mendapatkan hasil query
    data = cursor.fetchall()

    # Menutup kursor dan koneksi
    cursor.close()
    conn.close()

    return data

# Fungsi untuk mengonversi tanggal menjadi nilai numerik
def convert_date_to_numeric(date_value):
    # Jika tanggal dalam bentuk datetime, konversi ke timestamp UNIX
    if isinstance(date_value, datetime):
        timestamp = int(date_value.timestamp())
    else:
        # Jika tanggal dalam bentuk string, gunakan strptime
        date_object = datetime.strptime(date_value, "%Y-%m-%d")
        timestamp = int(date_object.timestamp())

    return timestamp

# Fungsi untuk melatih model
def train_model(data):
    # Memisahkan data menjadi fitur (features) dan target
    X = [(int(row[0]), convert_date_to_numeric(row[2])) for row in data]
    y = [int(row[1]) for row in data]

    print(X)
    print(y)

    # Bagi data menjadi data pelatihan dan pengujian
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inisialisasi model regresi linear
    model = LinearRegression()

    # Latih model
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Evaluasi model jika diperlukan
    score = model.score(X_test, y_test)
    print(y_pred)
    print(f"Model Score: {score}")

    joblib.dump(model, 'model.pkl')

    return model

# Memanggil fungsi untuk mendapatkan data
data_from_postgres = get_data_from_postgres()

# Memanggil fungsi untuk melatih model
trained_model = train_model(data_from_postgres)