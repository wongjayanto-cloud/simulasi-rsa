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

# Styling antarmuka. Bagian ini hanya mengubah tampilan, bukan logika RSA.
st.markdown(
    """
<style>
:root {
    --rsa-bg: #07111f;
    --rsa-surface: rgba(15, 27, 46, 0.88);
    --rsa-surface-soft: rgba(23, 39, 65, 0.72);
    --rsa-border: rgba(148, 163, 184, 0.18);
    --rsa-text: #f8fafc;
    --rsa-muted: #a8b4c7;
    --rsa-primary: #38bdf8;
    --rsa-secondary: #6366f1;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 15% 0%, rgba(56, 189, 248, 0.12), transparent 34rem),
        radial-gradient(circle at 90% 20%, rgba(99, 102, 241, 0.13), transparent 30rem),
        linear-gradient(145deg, #07111f 0%, #0b1424 55%, #0b1020 100%);
    color: var(--rsa-text);
}

.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: rgba(7, 17, 31, 0.97);
    border-right: 1px solid var(--rsa-border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

h1 {
    font-size: clamp(2.1rem, 4vw, 3.3rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.045em !important;
    margin-bottom: 0.2rem !important;
}

h2, h3 {
    color: var(--rsa-text) !important;
    letter-spacing: -0.025em !important;
}

p, label, [data-testid="stCaptionContainer"] {
    color: #cbd5e1;
}

[data-baseweb="input"] > div,
[data-baseweb="textarea"],
[data-baseweb="select"] > div {
    background: rgba(15, 27, 46, 0.82) !important;
    border-color: rgba(148, 163, 184, 0.25) !important;
    border-radius: 12px !important;
}

[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    color: var(--rsa-text) !important;
    -webkit-text-fill-color: var(--rsa-text) !important;
}

[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: rgba(56, 189, 248, 0.9) !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.13) !important;
}

[data-testid="stRadio"] > div {
    gap: 0.65rem;
}

[data-testid="stRadio"] label {
    background: rgba(23, 39, 65, 0.76);
    border: 1px solid var(--rsa-border);
    border-radius: 10px;
    padding: 0.45rem 0.8rem;
}

[data-testid="stSlider"] [role="slider"] {
    background-color: var(--rsa-primary) !important;
}

.stButton > button {
    min-height: 2.7rem;
    padding: 0.55rem 1.15rem;
    border-radius: 11px;
    border: 1px solid rgba(148, 163, 184, 0.25);
    background: rgba(23, 39, 65, 0.82);
    color: var(--rsa-text);
    font-weight: 650;
    transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    border-color: rgba(56, 189, 248, 0.72);
    background: rgba(30, 52, 84, 0.96);
    color: white;
}

.stButton > button[kind="primary"] {
    border: none;
    background: linear-gradient(135deg, #0284c7, var(--rsa-secondary));
    box-shadow: 0 10px 28px rgba(2, 132, 199, 0.2);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0ea5e9, #818cf8);
}

.stButton > button:disabled {
    transform: none;
    opacity: 0.45;
}

[data-testid="stProgress"] > div > div {
    background: rgba(30, 41, 59, 0.85);
    border-radius: 999px;
}

[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, var(--rsa-primary), var(--rsa-secondary));
    border-radius: 999px;
}

[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid var(--rsa-border);
}

[data-testid="stCode"] {
    border: 1px solid var(--rsa-border);
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stCode"] pre {
    background: #050c17 !important;
}

[data-testid="stExpander"] {
    background: var(--rsa-surface);
    border: 1px solid var(--rsa-border);
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    font-weight: 650;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--rsa-border);
    border-radius: 14px;
    overflow: hidden;
}

hr {
    border-color: var(--rsa-border) !important;
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
        padding-top: 1rem;
    }

    h1 {
        font-size: 2.1rem !important;
    }

    .stButton > button {
        width: 100%;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# Ukuran bilangan prima dibatasi agar simulasi tetap responsif di website.
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
    st.session_state["cipher_in"] = ", ".join(
        map(str, enkripsi("Hello World!", k["e"], k["n"]))
    )


def navigasi(i: int, total: int, bisa_lanjut: bool = True):
    kiri, _, kanan = st.columns([1, 3, 1])
    if i > 0:
        kiri.button("Kembali", on_click=pindah, args=(i - 1,), key=f"back{i}")
    if i < total - 1:
        kanan.button(
            "Lanjut",
            on_click=pindah,
            args=(i + 1,),
            key=f"next{i}",
            type="primary",
            disabled=not bisa_lanjut,
        )
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
        bits = st.slider(
            "Panjang bit tiap bilangan prima",
            MIN_BIT,
            MAKS_BIT,
            MAKS_BIT,
            help="Jumlah bit digunakan untuk menentukan ukuran kunci.",
        )
    else:
        c1, c2 = st.columns(2)
        p = c1.number_input(
            "p (prima)", min_value=2, max_value=MAKS_PRIMA_MANUAL, value=61, step=1
        )
        q = c2.number_input(
            "q (prima)", min_value=2, max_value=MAKS_PRIMA_MANUAL, value=53, step=1
        )

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
        st.success(
            "Kunci sudah dibuat. Klik **Lanjut** untuk memakainya, "
            "atau generate ulang bila ingin kunci baru."
        )
        with st.expander("Langkah perhitungan", expanded=True):
            st.markdown(
                f"""
1. Dua bilangan prima: **p = {k['p']}**, **q = {k['q']}**
2. n = p × q = **{k['n']}**
3. m = (p − 1)(q − 1) = **{k['m']}**
4. e dengan gcd(e, m) = 1 → **e = {k['e']}**
5. d ≡ e⁻¹ (mod m) → **d = {k['d']}**
"""
            )


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
            cipher = [
                int(x)
                for x in st.session_state["cipher_in"].replace(",", " ").split()
            ]
        except ValueError:
            cipher = None
            st.error("Ciphertext harus berisi angka dipisah koma.")

        if cipher is not None:
            if not cipher:
                st.error("Ciphertext tidak boleh kosong.")
            elif any(c < 0 or c >= k["n"] for c in cipher):
                st.error(
                    f"Setiap angka ciphertext harus berada di rentang 0 sampai "
                    f"{k['n'] - 1} (c < n)."
                )
            else:
                try:
                    with st.spinner("Menghitung..."):
                        teks = dekripsi(cipher, k["d"], k["n"])
                        teks.encode("utf-8")
                    st.session_state["plain_out"] = dict(cipher=cipher, teks=teks)
                except (ValueError, OverflowError):
                    st.session_state.pop("plain_out", None)
                    st.error(
                        "Dekripsi gagal. Pastikan ciphertext dibuat dengan kunci publik "
                        "yang cocok dengan kunci ini."
                    )

    hasil = st.session_state.get("plain_out")
    if hasil:
        st.success("Hasil dekripsi (plaintext):")
        st.text(hasil["teks"])
        with st.expander("Langkah per karakter"):
            st.dataframe(
                [
                    {"c": str(c), "m = c^d mod n": str(ord(ch)), "karakter": ch}
                    for c, ch in zip(hasil["cipher"], hasil["teks"])
                ]
            )


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
                st.error(
                    f"Karakter {' '.join(terlalu_besar)} punya kode ≥ n ({k['n']}), "
                    "sehingga tidak bisa dienkripsi dengan benar. Gunakan karakter ASCII "
                    "biasa atau buat kunci baru."
                )
            else:
                st.session_state["cipher_out"] = dict(
                    pesan=pesan,
                    cipher=enkripsi(pesan, k["e"], k["n"]),
                )

    hasil = st.session_state.get("cipher_out")
    if hasil:
        st.markdown("**Ciphertext:**")
        st.code(", ".join(map(str, hasil["cipher"])))
        with st.expander("Langkah per karakter"):
            st.dataframe(
                [
                    {
                        "karakter": ch,
                        "m = ord": str(ord(ch)),
                        "c = m^e mod n": str(c),
                    }
                    for ch, c in zip(hasil["pesan"], hasil["cipher"])
                ]
            )


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
        st.code(
            f"p = {k['p']}\nq = {k['q']}\nn = {k['n']}\n"
            f"m = {k['m']}\ne = {k['e']}\nd = {k['d']}"
        )
        st.caption(
            "m = (p−1)(q−1). Kunci publik: (e, n). "
            "Kunci privat: (d, n)."
        )
    else:
        st.info("Belum ada kunci. Lakukan Generate Key dulu.")

st.title("🔐 Simulasi RSA")
st.caption(
    "Visualisasi pembentukan kunci, enkripsi, dan dekripsi "
    "menggunakan algoritma Rivest–Shamir–Adleman."
)
st.progress(
    (step + 1) / len(LANGKAH),
    text=f"Langkah {step + 1} dari {len(LANGKAH)}: {LANGKAH[step][0]}",
)

LANGKAH[step][1]()

st.divider()
navigasi(step, len(LANGKAH), bisa_lanjut="key" in st.session_state)
