import streamlit as st
import sqlite3
import os

# --- KONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(
    page_title="Zephyr Register System", 
    page_icon="📝", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Sembunyikan Elemen Bawaan Streamlit (Header & Footer) ---
# Ini sangat berguna agar saat di-embed via iframe di index.html terlihat bersih menyatu
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background: transparent;
    }
    /* Kustomisasi gaya form agar estetik seperti tema Zephyr */
    .stButton>button {
        width: 100%;
        background-color: #38bdf8;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #0284c7;
        border: none;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISASI DATABASE SQLITE ---
def init_db():
    conn = sqlite3.connect('zephyr_users.db')
    c = conn.cursor()
    # Membuat tabel user jika belum ada
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan user baru ke database
def add_user(username, password):
    try:
        conn = sqlite3.connect('zephyr_users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Username sudah ada (Unique Constraint Voilation)
        return False

# Jalankan inisialisasi database
init_db()

# --- TAMPILAN ANTARMUKA REGISTRASI ---
st.title("📝 Buat Akun Zephyr")
st.write("Silakan daftarkan username unik kamu untuk ruang kerja produktivitas pribadi.")

# Membuat Form Registrasi
with st.form(key='register_form', clear_on_submit=True):
    reg_user = st.text_input("Buat Username Baru", placeholder="Contoh: baybay777")
    reg_pass = st.text_input("Buat Password Baru", type="password", placeholder="Masukkan password aman")
    reg_pass_confirm = st.text_input("Konfirmasi Password Baru", type="password", placeholder="Ketik ulang password")
    
    submit_button = st.form_submit_button(label='Daftar Akun Baru')

# --- LOGIKA VALIDASI PENDAFTARAN ---
if submit_button:
    # Hilangkan spasi di awal/akhir username
    username_clean = reg_user.strip()
    
    if username_clean == "" or reg_pass == "":
        st.error("⚠️ Username dan Password tidak boleh kosong!")
    elif len(reg_pass) < 6:
        st.warning("🔒 Password minimal harus terdiri dari 6 karakter!")
    elif reg_pass != reg_pass_confirm:
        st.error("❌ Konfirmasi password tidak cocok! Pastikan pengetikan sudah benar.")
    else:
        # Proses memasukkan data ke database SQLite
        is_success = add_user(username_clean, reg_pass)
        
        if is_success:
            st.success(f"🎉 Akun dengan username **'{username_clean}'** berhasil dibuat!")
            st.balloons()
            st.info("💡 Sekarang kamu bisa menggunakan akun ini untuk login.")
        else:
            st.error("⚠️ Username tersebut sudah terdaftar! Silakan pilih nama lain.")