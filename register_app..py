import streamlit as st
import sqlite3

# --- KONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(
    page_title="Zephyr Auth System", 
    page_icon="🔐", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- GAYA CSS KUSTOM (Menyesuaikan Tema Gelap Estetik Zephyr) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background: transparent; }
    
    /* Mengubah warna teks deskripsi agar putih/terang di latar belakang gelap */
    .stMarkdown p { color: #cbd5e1 !important; }
    
    /* Gaya tombol utama login/register */
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
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI DATABASE SQLITE ---
def init_db():
    conn = sqlite3.connect('zephyr_users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password):
    try:
        conn = sqlite3.connect('zephyr_users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user(username, password):
    conn = sqlite3.connect('zephyr_users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Jalankan inisialisasi database
init_db()

# --- ANTARMUKA UTAMA (TAB SYSTEM) ---
st.title("✨ Selamat Datang di Zephyr")
st.write("Silakan masuk ke akun kamu atau daftarkan akun baru untuk mengamankan ruang kerja produktivitas.")

# Membuat Navigasi Tab Penuh untuk Login dan Register
tab_login, tab_register = st.tabs(["🔒 Masuk (Login)", "📝 Daftar (Register)"])

# ==================== 1. HALAMAN LOGIN ====================
with tab_login:
    st.subheader("Masuk ke Workspace")
    
    if "login_success" not in st.session_state:
        st.session_state.login_success = False

    if not st.session_state.login_success:
        with st.form(key='login_form'):
            login_user = st.text_input("Username", placeholder="Masukkan username kamu")
            login_pass = st.text_input("Password", type="password", placeholder="Masukkan password")
            login_submit = st.form_submit_button(label='Masuk Sekarang')
            
        if login_submit:
            user_valid = check_user(login_user.strip(), login_pass)
            if user_valid:
                st.session_state.login_success = True
                st.rerun()
            else:
                st.error("❌ Username atau Password salah! Silakan periksa kembali.")
    else:
        st.success("🎉 Verifikasi Akun Berhasil!")
        
        st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: #cbd5e1 !important; font-size: 15px; margin-bottom: 15px;">
                    Akun kamu valid! Silakan klik tombol di bawah untuk masuk:
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Menggunakan tombol resmi Streamlit untuk memicu pengalihan aman
        if st.button("🚀 Buka Zephyr Workspace Sekarang", key="btn_redirect_final"):
            st.markdown("""
                <script>
                    // Mengirim sinyal aman keluar dari iframe menuju halaman auth.html
                    window.parent.postMessage("login_sukses_redirect", "*");
                </script>
            """, unsafe_allow_html=True)
        
        # --- PERBAIKAN LINK ABSOLUT GITHUB PAGES ---
        st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: #cbd5e1 !important; font-size: 15px; margin-bottom: 15px;">
                    Akun kamu valid. Klik tombol di bawah ini untuk membuka lembar kerja produktivitasmu:
                </p>
                <a href="https://baybay777.github.io/zephyrr/product.html" target="_top" style="
                    display: block;
                    width: 100%;
                    background-color: #10b981;
                    color: white !important;
                    text-align: center;
                    padding: 12px 20px;
                    font-weight: 700;
                    font-size: 16px;
                    text-decoration: none;
                    border-radius: 10px;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
                    transition: background 0.2s;
                ">
                    Buka Zephyr Workspace Sekarang →
                </a>
            </div>
        """, unsafe_allow_html=True)
# ==================== 2. HALAMAN REGISTER ====================
with tab_register:
    st.subheader("Buat Akun Baru")
    with st.form(key='register_form', clear_on_submit=True):
        reg_user = st.text_input("Buat Username Baru", placeholder="Contoh: baybay777")
        reg_pass = st.text_input("Buat Password Baru", type="password", placeholder="Minimal 6 karakter")
        reg_pass_confirm = st.text_input("Konfirmasi Password Baru", type="password", placeholder="Ketik ulang password")
        reg_submit = st.form_submit_button(label='Daftar Akun Baru')
        
    if reg_submit:
        username_clean = reg_user.strip()
        if username_clean == "" or reg_pass == "":
            st.error("⚠️ Data tidak boleh kosong!")
        elif len(reg_pass) < 6:
            st.warning("🔒 Password minimal harus 6 karakter!")
        elif reg_pass != reg_pass_confirm:
            st.error("❌ Konfirmasi password tidak cocok!")
        else:
            is_success = add_user(username_clean, reg_pass)
            if is_success:
                st.success(f"🎉 Akun **'{username_clean}'** berhasil dibuat! Silakan pindah ke tab 'Masuk' untuk login.")
                st.balloons()
            else:
                st.error("⚠️ Username tersebut sudah terdaftar! Gunakan nama lain.")
