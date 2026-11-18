import streamlit as st
import sympy as sy
import math


def get_prime(bits: int):
    return sy.randprime(pow(2, (bits - 1)), pow(2, bits))


def hitung_n(p, q):
    return p * q


def hitung_m(p, q):
    return (p - 1) * (q - 1)


def cari_e(m):
    for e in range(2, m):
        if math.gcd(e, m) == 1:
            return e
    return None


def cari_d(e, m):
    return pow(e, -1, m)


def enkripsi(x, e, n):
    daftar = [ord(c) for c in x]
    hasil = []
    for i in daftar:
        hasil.append(pow(i, e, n))
    return hasil


def dekripsi(x, d, n):
    hasil = []
    for i in x:
        hasil.append(chr(pow(i, d, n)))
    return "".join(hasil)


# =====================================================================
# Di bawah ini adalah kode antarmuka Streamlit (memanggil fungsi di atas)
# =====================================================================
st.set_page_config(page_title="Simulasi RSA", page_icon="🔐", layout="wide")

# Desain RSA Cipher Lab. Bagian ini hanya mengubah tampilan.
st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #e7edf7;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.block-container::before {
    content: "RSA SYSTEM / ACTIVE";
    display: block;
    width: fit-content;
    margin-bottom: 1rem;
    padding: 5px 10px;
    color: #5eead4;
    background-color: #101d2f;
    border: 1px solid #2a3a52;
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
    letter-spacing: 1px;
}

h1 {
    color: #f8fafc !important;
    font-size: 2.6rem !important;
    font-weight: 750 !important;
    letter-spacing: -1px !important;
}

h2, h3 {
    color: #e7edf7 !important;
}

p, label, [data-testid="stCaptionContainer"] {
    color: #b2c0d4;
}

[data-testid="stSidebar"] {
    background-color: #0f1929;
    border-right: 1px solid #2a3a52;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #5eead4 !important;
    font-family: monospace;
    letter-spacing: 1px;
}

.stButton > button {
    min-height: 42px;
    background-color: #162338;
    color: #dce7f5;
    border: 1px solid #344760;
    border-radius: 5px;
    font-family: monospace;
    font-weight: 700;
    letter-spacing: 0.4px;
}

.stButton > button:hover {
    color: #5eead4;
    border-color: #5eead4;
    background-color: #172a3d;
}

.stButton > button[kind="primary"] {
    background-color: #5eead4;
    color: #07111d;
    border-color: #5eead4;
}

.stButton > button[kind="primary"]:hover {
    background-color: #99f6e4;
    color: #07111d;
    border-color: #99f6e4;
}

[data-baseweb="input"] > div,
[data-baseweb="textarea"] {
    background-color: #101b2b !important;
    border-color: #344760 !important;
    border-radius: 5px !important;
}

[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    color: #e7edf7 !important;
    -webkit-text-fill-color: #e7edf7 !important;
    font-family: monospace;
}

[data-testid="stRadio"] label {
    padding: 7px 11px;
    background-color: #111c2e;
    border: 1px solid #2a3a52;
    border-radius: 5px;
}

[data-testid="stSlider"] [role="slider"] {
    background-color: #5eead4 !important;
}

[data-testid="stProgress"] > div > div {
    background-color: #172338;
}

[data-testid="stProgress"] > div > div > div {
    background-color: #5eead4;
}

[data-testid="stCode"] {
    border: 1px solid #2a3a52;
    border-left: 4px solid #f4c95d;
    border-radius: 5px;
    overflow: hidden;
}

[data-testid="stCode"] pre {
    background-color: #080f1b !important;
    color: #b7f7dc !important;
}

[data-testid="stExpander"] {
    background-color: #111c2e;
    border: 1px solid #2a3a52;
    border-radius: 5px;
}

[data-testid="stExpander"] summary {
    color: #f4c95d;
    font-family: monospace;
    font-weight: 700;
}

[data-testid="stAlert"] {
    border-radius: 5px;
    border: 1px solid #344760;
}

[data-testid="stDataFrame"] {
    border: 1px solid #2a3a52;
    border-radius: 5px;
    overflow: hidden;
}

hr {
    border-color: #2a3a52 !important;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1 {
        font-size: 2rem !important;
    }

    .stButton > button {
        width: 100%;
    }
}
</style>
""", unsafe_allow_html=True)

# Ukuran bilangan prima tetap sama seperti kode awal.
MIN_BIT = 6
MAKS_BIT = 512
MAKS_PRIMA_MANUAL = 255  # setara 8 bit


# ---------------------------------------------------------------
# Navigasi antar langkah
# ---------------------------------------------------------------
def pindah(ke: int):
    st.session_state["step"] = ke


def mulai_ulang():
    st.session_state.clear()
    st.session_state["step"] = 0


def isi_contoh_cipher():
    k = st.session_state["key"]
    st.session_state["cipher_in"] = ", ".join(map(str, enkripsi("Hello World!", k["e"], k["n"])))


def navigasi(i: int, total: int, bisa_lanjut: bool = True):
    kiri, _, kanan = st.columns([1, 3, 1])
    if i > 0:
        kiri.button("Kembali", on_click=pindah, args=(i - 1,), key=f"back{i}")
    if i < total - 1:
        kanan.button("Lanjut", on_click=pindah, args=(i + 1,), key=f"next{i}",
                     type="primary", disabled=not bisa_lanjut)
    else:
        kanan.button("Mulai ulang", on_click=mulai_ulang, key="reset")


# ---------------------------------------------------------------
# Langkah 1: Generate key
# ---------------------------------------------------------------
def halaman_key():
    st.subheader("Langkah 1: Pembangkitan Kunci")
    mode = st.radio("Cara memilih p dan q", ["Acak", "Manual"], horizontal=True)

    p = q = bits = None
    if mode == "Acak":
        bits = st.slider("Panjang bit tiap bilangan prima", MIN_BIT, MAKS_BIT, MAKS_BIT,
                         help="Jumlah bits digunakan untuk menentukan ukuran Key.")
    else:
        c1, c2 = st.columns(2)
        p = c1.number_input("p (prima)", min_value=2, max_value=MAKS_PRIMA_MANUAL, value=61, step=1)
        q = c2.number_input("q (prima)", min_value=2, max_value=MAKS_PRIMA_MANUAL, value=53, step=1)

    if st.button("Generate Key", type="primary"):
        if mode == "Acak":
            p, q = int(get_prime(bits)), int(get_prime(bits))
            while q == p:
                q = int(get_prime(bits))
        else:
            p, q = int(p), int(q)

        galat = None
        if not sy.isprime(p):
            galat = f"p = {p} bukan bilangan prima."
        elif not sy.isprime(q):
            galat = f"q = {q} bukan bilangan prima."
        elif p == q:
            galat = "p dan q harus berbeda."
        elif hitung_n(p, q) <= 127:
            galat = "n = p × q harus > 127 agar semua karakter ASCII dapat dienkripsi."

        if galat:
            st.error(galat)
        else:
            n = int(hitung_n(p, q))
            m = int(hitung_m(p, q))
            e = cari_e(m)
            if e is None or not (1 < e < m) or math.gcd(e, m) != 1:
                st.error("e tidak valid: harus 1 < e < m dan gcd(e, m) = 1.")
            else:
                d = int(cari_d(e, m))
                st.session_state["key"] = dict(p=p, q=q, n=n, m=m, e=int(e), d=d)
                for s in ("cipher_in", "plain_out", "cipher_out"):
                    st.session_state.pop(s, None)
                st.rerun()

    k = st.session_state.get("key")
    if k:
        st.success("Kunci sudah dibuat. Klik **Lanjut** untuk memakainya, atau generate ulang bila ingin kunci baru.")
        with st.expander("Langkah perhitungan", expanded=True):
            st.markdown(f"""
1. Dua bilangan prima: **p = {k['p']}**, **q = {k['q']}**
2. n = p × q = **{k['n']}**
3. m = (p − 1)(q − 1) = **{k['m']}**
4. e dengan gcd(e, m) = 1 → **e = {k['e']}**
5. d ≡ e⁻¹ (mod m) → **d = {k['d']}**
""")


# ---------------------------------------------------------------
# Langkah 3: Dekripsi
# ---------------------------------------------------------------
def halaman_dekripsi():
    k = st.session_state["key"]
    st.subheader("Langkah 3: Dekripsi")
    st.markdown("Rumus: **m = cᵈ mod n**, lalu m diubah menjadi karakter dengan `chr(m)`.")
    st.code(f"d = {k['d']}\nn = {k['n']}")

    st.text_area("Ciphertext (angka dipisah koma)", key="cipher_in", height=120)
    st.button("Isi contoh ciphertext (pesan 'Hello World!')", on_click=isi_contoh_cipher)

    if st.button("Dekripsi", type="primary"):
        try:
            cipher = [int(x) for x in st.session_state["cipher_in"].replace(",", " ").split()]
        except ValueError:
            cipher = None
            st.error("Ciphertext harus berisi angka dipisah koma.")
        if cipher is not None:
            if not cipher:
                st.error("Ciphertext tidak boleh kosong.")
            elif any(c < 0 or c >= k["n"] for c in cipher):
                st.error(f"Setiap angka ciphertext harus berada di rentang 0 sampai {k['n'] - 1} (c < n).")
            else:
                try:
                    with st.spinner("Menghitung..."):
                        teks = dekripsi(cipher, k["d"], k["n"])
                        teks.encode("utf-8")
                    st.session_state["plain_out"] = dict(cipher=cipher, teks=teks)
                except (ValueError, OverflowError):
                    st.session_state.pop("plain_out", None)
                    st.error("Dekripsi gagal. Pastikan ciphertext dibuat dengan kunci publik yang cocok dengan kunci ini.")

    hasil = st.session_state.get("plain_out")
    if hasil:
        st.success("Hasil dekripsi (plaintext):")
        st.text(hasil["teks"])
        with st.expander("Langkah per karakter"):
            st.dataframe([{"c": str(c), "m = c^d mod n": str(ord(ch)), "karakter": ch}
                          for c, ch in zip(hasil["cipher"], hasil["teks"])])


# ---------------------------------------------------------------
# Langkah 2: Enkripsi
# ---------------------------------------------------------------
def halaman_enkripsi():
    k = st.session_state["key"]
    st.subheader("Langkah 2: Enkripsi")
    st.markdown("Rumus: **c = mᵉ mod n**, dengan m = `ord(karakter)`.")
    st.code(f"e = {k['e']}\nn = {k['n']}")

    st.text_area("Pesan (plaintext)", key="pesan_in", height=120)

    if st.button("Enkripsi", type="primary"):
        pesan = st.session_state["pesan_in"]
        if not pesan:
            st.error("Pesan tidak boleh kosong.")
        else:
            terlalu_besar = sorted({ch for ch in pesan if ord(ch) >= k["n"]})
            if terlalu_besar:
                st.session_state.pop("cipher_out", None)
                st.error(f"Karakter {' '.join(terlalu_besar)} punya kode ≥ n ({k['n']}), sehingga tidak bisa "
                         "dienkripsi dengan benar. Gunakan karakter ASCII biasa atau buat kunci baru.")
            else:
                st.session_state["cipher_out"] = dict(pesan=pesan, cipher=enkripsi(pesan, k["e"], k["n"]))

    hasil = st.session_state.get("cipher_out")
    if hasil:
        st.markdown("**Ciphertext:**")
        st.code(", ".join(map(str, hasil["cipher"])))
        with st.expander("Langkah per karakter"):
            st.dataframe([{"karakter": ch, "m = ord": str(ord(ch)), "c = m^e mod n": str(c)}
                          for ch, c in zip(hasil["pesan"], hasil["cipher"])])


# ---------------------------------------------------------------
# Urutan langkah
# ---------------------------------------------------------------
LANGKAH = [
    ("🔑 Generate Key", halaman_key),
    ("🔒 Enkripsi", halaman_enkripsi),
    ("🔓 Dekripsi", halaman_dekripsi),
]


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
st.session_state.setdefault("step", 0)
st.session_state.setdefault("cipher_in", "")
st.session_state.setdefault("pesan_in", "Halo RSA!")

for _k in ("cipher_in", "pesan_in"):
    st.session_state[_k] = st.session_state[_k]

if "key" not in st.session_state:
    st.session_state["step"] = 0

step = st.session_state["step"]

with st.sidebar:
    st.header("📦 Variabel RSA")
    k = st.session_state.get("key")
    if k:
        st.code(f"p = {k['p']}\nq = {k['q']}\nn = {k['n']}\nm = {k['m']}\ne = {k['e']}\nd = {k['d']}")
        st.caption("m = (p−1)(q−1). Kunci publik: (e, n). Kunci privat: (d, n).")
    else:
        st.info("Belum ada kunci. Lakukan Generate Key dulu.")

st.title("🔐 Simulasi RSA")
st.caption("Eksperimen pembangkitan kunci, enkripsi, dan dekripsi menggunakan algoritma RSA.")
st.progress((step + 1) / len(LANGKAH), text=f"Langkah {step + 1} dari {len(LANGKAH)}: {LANGKAH[step][0]}")

LANGKAH[step][1]()

st.divider()
navigasi(step, len(LANGKAH), bisa_lanjut="key" in st.session_state)
