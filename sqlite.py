# import Library yang Dibutuhkan
import sqlite3  # mengimpor modul sqlite3 untuk bisa menggunakan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # mengimpor komponen-komponen GUI dari modul tkinter


# fungsi untuk membuat database dan table
def create_database():
    # membuat koneksi ke database 'nilai_siswa.db'
    # jika database dengan nama tersebut belum ada, maka akan otomatis dibuat
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()  # membuat cursor untuk menjalankan perintah SQL
    # membuat tabel nilai_siswa jika belum ada
    # tabel memiliki kolom: id (auto increment), nama_siswa, nilai biologi, fisika, inggris, dan prediksi fakultas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()  # commit() memastikan bahwa perubahan disimpan dalam database
    conn.close()   # menutup koneksi ke database setelah selesai digunakan


# fungsi untuk mengambil semua data dari tabel 'nilai_siswa' di database
def fetch_data():
    # membuka koneksi ke database
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()  # membuat cursor untuk menjalankan perintah SQL
    # mengambil semua data dari tabel 'nilai_siswa'
    cursor.execute("SELECT * FROM nilai_siswa")
    # menyimpan hasil query (semua baris data) ke dalam variabel 'rows'
    rows = cursor.fetchall()  # fetchall() akan mengambil semua data hasil query
    # menutup koneksi ke database setelah data diambil
    conn.close() 
    # mengembalikan data yang diambil dalam bentuk daftar baris (list of rows)
    return rows


# fungsi untuk menyimpan data baru ke dalam tabel 'nilai_siswa' di database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    # membuka koneksi ke database
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()  # membuat cursor untuk menjalankan perintah SQL
    # memasukkan data baru ke dalam tabel 'nilai_siswa' dengan nilai yang diberikan
    # parameter yang dimasukkan adalah: nama siswa, nilai biologi, nilai fisika, nilai inggris, dan prediksi fakultas
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  
    # menyimpan perubahan pada database
    conn.commit()
    # menutup koneksi ke database setelah data baru berhasil disimpan
    conn.close()

# fungsi untuk memperbarui data siswa berdasarkan ID pada tabel 'nilai_siswa'
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    # membuka koneksi ke database 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()  # membuat cursor untuk menjalankan perintah SQL
    # membuat perintah SQL untuk memperbarui data di tabel 'nilai_siswa' berdasarkan ID
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  
    # menyimpan perubahan ke database setelah memperbarui data
    conn.commit()
    # menutup koneksi ke database setelah selesai
    conn.close()


 # fungsi untuk menghapus data siswa dari tabel 'nilai_siswa' berdasarkan ID
def delete_database(record_id):    
    # membuka koneksi ke database 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()  # membuat cursor untuk menjalankan perintah SQL
    # membuat perintah SQL untuk menghapus data dari tabel 'nilai_siswa' berdasarkan ID
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  
    # menyimpan perubahan ke database setelah menghapus data
    conn.commit()
    # menutup koneksi ke database setelah selesai
    conn.close()

# membuat fungsi untuk menentukan prediksi fakultas berdasarkan nilai tertinggi dari tiga mata pelajaran
def calculate_prediction(biologi, fisika, inggris):
    # membandingkan nilai dari setiap mata pelajaran untuk menentukan fakultas yang sesuai
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # jika nilai biologi tertinggi, maka prediksi fakultas adalah "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # jika nilai fisika tertinggi, maka prediksi fakultas adalah "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # jika nilai bahasa Inggris tertinggi, maka prediksi fakultas adalah "Bahasa"
    else:
        return "Tidak Diketahui"  # jika tidak ada nilai yang lebih tinggi dari yang lain, maka prediksi tidak dapat ditentukan


# fungsi untuk menambahkan data baru ke database
def submit():
    try:
        # mengambil nilai dari data yang telah diisi oleh pengguna
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # memeriksa apakah kolom nama kosong. jika kosong, akan muncul pesan error
        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        # menghitung prediksi fakultas berdasarkan nilai tertinggi siswa dan menyimpan data lengkap ke dalam database
        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        # menampilkan pesan bahwa data telah berhasil disimpan, dan prediksi fakultas untuk siswa tersebut
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        # membersihkan form setelah data disimpan agar form siap digunakan kembali
        clear_inputs()  
        # mengupdate tampilan tabel di aplikasi dengan data terbaru yang telah dimasukkan
        populate_table()  
    except ValueError as e:
        # membaca error jika input yang dimasukkan bukan angka yang valid
        messagebox.showerror("Error", f"Input tidak valid: {e}")


 # fungsi untuk memperbarui data yang sudah ada dalam tabel berdasarkan ID yang dipilih
def update():
    try:
        # memeriksa apakah ada data yang dipilih. Jika tidak, akan muncul pesan error
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        # mengambil nilai dari form sesuai dengan data yang diisi oleh pengguna
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # memvaalidasi agar kolom nama tidak boleh kosong
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        # menghitung prediksi fakultas berdasarkan nilai terbaru, kemudian memperbarui data di database dengan data yang telah diperbarui
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        # menampilkan pesan bahwa data telah berhasil diperbarui
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        # membersihkan form setelah data diperbarui agar form bisa digunakan lagi
        clear_inputs()
        # memperbarui tampilan tabel di aplikasi dengan data terbaru yang telah di-update
        populate_table()
    except ValueError as e:
        # membaca error jika input yang dimasukkan tidak valid.
        messagebox.showerror("Error", f"Kesalahan: {e}")


# fungsi untuk menghapus data dari tabel berdasarkan ID yang dipilih
def delete():
    try:
        # memastikan pengguna telah memilih data yang ingin dihapus dari tabel
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        # mengambil ID data yang dipilih dari tabel untuk dihapus
        record_id = int(selected_record_id.get())
        delete_database(record_id)  # memanggil fungsi untuk menghapus data dari database
        # menampilkan pesan bahwa data telah berhasil dihapus.
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        # membersihkan form dan memperbarui tabel setelah data dihapus
        clear_inputs()
        populate_table()
    except ValueError as e:
        # membaca error jika ada kesalahan dalam input atau penghapusan data
        messagebox.showerror("Error", f"Kesalahan: {e}")


# fungsi untuk membersihkan semua inputan form setelah data disimpan, diperbarui, atau dihapus
def clear_inputs():
    nama_var.set("")  # mengosongkan input nama siswa
    biologi_var.set("")  # mengosongkan input nilai biologi
    fisika_var.set("")  # mengosongkan input nilai fisika
    inggris_var.set("")  # mengosongkan input nilai bahasa Inggris
    selected_record_id.set("")  # mengosongkan ID data yang dipilih

 # fungsi untuk mengisi tabel dengan data terbaru dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row)  # menghapus data lama dari tabel, jika ada
    for row in fetch_data():
        # memasukkan setiap baris data baru dari database ke dalam tabel
        tree.insert('', 'end', values=row)

# fungsi untuk mengisi form dengan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        # mengambil item yang dipilih di tabel
        selected_item = tree.selection()[0]
        # mendapatkan nilai (data) dari item yang dipilih
        selected_row = tree.item(selected_item)['values']

        # mengisi form input berdasarkan data yang dipilih dari tabel
        selected_record_id.set(selected_row[0])  #menyimpan ID data yang dipilih
        nama_var.set(selected_row[1])  # mengisi input nama dengan data yang dipilih
        biologi_var.set(selected_row[2])  # mengisi input nilai biologi
        fisika_var.set(selected_row[3])  # mengisi input nilai fisika
        inggris_var.set(selected_row[4])  # mengisi input nilai bahasa Inggris
    except IndexError:
        # menampilkan pesan error jika tidak ada data valid yang dipilih.
        messagebox.showerror("Error", "Pilih data yang valid!")

#inisialisasi database
create_database()

# membuat GUI dengan tkinter
root = Tk()  
root.title("Prediksi Fakultas Siswa")  

# Variabel tkinter
nama_var = StringVar()  # variabel untuk menyimpan input nama siswa
biologi_var = StringVar()  # variabel untuk menyimpan input nilai biologi
fisika_var = StringVar()  # variabel untuk menyimpan input nilai fisika
inggris_var = StringVar()  # variabel untuk menyimpan input nilai bahasa Inggris
selected_record_id = StringVar()   # untuk menyimpan ID record yang dipilih



# membuat label dan input, ini akan menampilkan dan menerima data dari pengguna untuk setiap kolom yang dibutuhkan.
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)  # label untuk nama siswa
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)  # input untuk nama siswa

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)  # label untuk nilai biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)  # input untuk nilai biologi

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)  # label untuk nilai fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)  # input untuk nilai fisika

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)  # label untuk nilai bahasa Inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)  # input untuk nilai bahasa Inggris


# membuat tombol-tombol yang digunakan untuk menambah, memperbarui, dan menghapus data dari database
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)  # tombol untuk menambahkan data
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)  # tombol untuk memperbarui data yang dipilih
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)  # tombol untuk menghapus data yang dipilih

# tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")  # kolom-kolom tabel
tree = ttk.Treeview(root, columns=columns, show='headings')  # membuat objek tabel dengan kolom yang sudah didefinisikan

# mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())  
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # menampilkan tabel di grid

# menambahkan event ketika baris tabel diklik
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# untuk mengisi tabel dengan data yang ada di database saat aplikasi pertama kali dibuka
populate_table()

# untuk menjalankan aplikasi
root.mainloop()
