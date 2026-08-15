import random
import sqlite3
import io
import streamlit as st
from PIL import Image

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Outfit Randomizer", page_icon="👗", layout="centered")

# ==================== 1. ระบบจัดการฐานข้อมูล (DATABASE) ====================
DB_NAME = "outfit_app.db"

def init_db():
    """สร้างตารางในฐานข้อมูลหากยังไม่มี"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # ตารางผู้ใช้งาน
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    # ตารางชุดแต่งตัว
    c.execute('''
        CREATE TABLE IF NOT EXISTS outfits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            text TEXT NOT NULL,
            image_blob BLOB,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    conn.commit()
    conn.close()

def seed_default_data():
    """ใส่ข้อมูลชุดเริ่มต้น 4-5 ชุดในแต่ละหัวข้อ (สำหรับยูสเซอร์ทดลองเล่น admin)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # ตรวจสอบว่ามีผู้ใช้ admin หรือยัง
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        # สร้างผู้ใช้ทดสอบ admin / 1234
        c.execute("INSERT INTO users (username, password) VALUES ('admin', '1234')")
        
        # รายการชุดเริ่มต้น 4-5 ชุดต่อหมวดหมู่
        default_outfits = [
            # --- หมวดหมู่ 1: ไปเรียน / ทำงาน (5 ชุด) ---
            ("admin", "📚 ไปเรียน / ทำงาน", "เสื้อเชิ้ตสีขาวเรียบ + กางเกงสแล็คสีดำ + รองเท้าคัทชู/หุ้มส้น", None),
            ("admin", "📚 ไปเรียน / ทำงาน", "เสื้อโปโลสีน้ำเงิน + กางเกงชิโน่สีครีม + รองเท้าสนีกเกอร์สีขาว", None),
            ("admin", "📚 ไปเรียน / ทำงาน", "เสื้อเบลเซอร์สีกรมทับเสื้อยืด + กางเกงยีนส์ทรงสเตรท + รองเท้าโลฟเฟอร์", None),
            ("admin", "📚 ไปเรียน / ทำงาน", "ชุดยูนิฟอร์ม / เสื้อเชิ้ตพับแขน + กางเกงทรงกระบอก + นาฬิกาข้อมือ", None),
            ("admin", "📚 ไปเรียน / ทำงาน", "เสื้อไหมพรมแขนยาวโทนสีมินิมอล + กางเกงผ้าสแล็คสีเทา", None),

            # --- หมวดหมู่ 2: ไปเที่ยวชิลๆ / Streetwear (5 ชุด) ---
            ("admin", "ไปเที่ยวชิลๆ", "เสื้อยืด Oversize สีดำ + กางเกงยีนส์ขากว้าง (Baggy) + หมวกแก๊ป", None),
            ("admin", "ไปเที่ยวชิลๆ", "เสื้อสเวตเตอร์ / เสื้อฮู้ด + กางเกงวอร์มขารวบ + รองเท้าผ้าใบสตรีท", None),
            ("admin", "ไปเที่ยวชิลๆ", "เสื้อกล้าม/เสื้อยืดขาว + สวมแจ็คเก็ตยีนส์ทับ + กางเกงคาร์โก้", None),
            ("admin", "ไปเที่ยวชิลๆ", "เสื้อฮาวายลายสวยๆ + กางเกงขาสั้นระดับเข่า + แว่นกันแดด", None),
            ("admin", "ไปเที่ยวชิลๆ", "เสื้อแขนยาวลายทาง + กางเกงยีนส์ขาสั้น + กระเป๋าคาดอก", None),

            # --- หมวดหมู่ 3: ไปงานแต่ง / งานทางการ (4 ชุด) ---
            ("admin", "✨ ไปงานแต่ง / งานทางการ", "ชุดสูทสีกรมท่า/เทาเข้ม + เชิ้ตขาว + เนกไท + รองเท้าหนัง", None),
            ("admin", "✨ ไปงานแต่ง / งานทางการ", "ชุดเดรสยาว / เดรสสั้นสีพาสเทล + กระเป๋าคลัตช์ + ส้นสูง", None),
            ("admin", "✨ ไปงานแต่ง / งานทางการ", "เสื้อเชิ้ตคอจีนแขนยาว + กางเกงสแล็คสีสว่าง + เข็มขัดหนัง", None),
            ("admin", "✨ ไปงานแต่ง / งานทางการ", "เบลเซอร์กระดุมคู่ + กางเกงเข้าชุด + รองเท้าหนังบราวน์/ดำ", None),
        ]
        
        c.executemany(
            "INSERT INTO outfits (username, category, text, image_blob) VALUES (?, ?, ?, ?)",
            default_outfits
        )
        conn.commit()
    
    conn.close()

def register_user(username, password):
    """ลงทะเบียนผู้ใช้ใหม่"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    """ตรวจสอบการเข้าสู่ระบบ"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def get_user_outfits(username):
    """ดึงรายการชุดของผู้ใช้ที่เข้าสู่ระบบ"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT category, text, image_blob FROM outfits WHERE username = ?", (username,))
    rows = c.fetchall()
    conn.close()
    
    outfits = {}
    for cat, text, img_blob in rows:
        img = None
        if img_blob:
            img = Image.open(io.BytesIO(img_blob))
        if cat not in outfits:
            outfits[cat] = []
        outfits[cat].append({"text": text, "image": img})
        
    return outfits

def add_user_outfit(username, category, text, image_file):
    """บันทึกชุดใหม่ลงฐานข้อมูล"""
    img_blob = None
    if image_file is not None:
        img_blob = image_file.read()
        
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO outfits (username, category, text, image_blob) VALUES (?, ?, ?, ?)",
        (username, category, text, img_blob)
    )
    conn.commit()
    conn.close()

# เรียกใช้งานการตั้งค่าฐานข้อมูลและสร้างข้อมูลเริ่มต้น
init_db()
seed_default_data()

# ==================== 2. SESSION STATE & LOGIN CONTROLLER ====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- หน้าจอ LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    st.title("👗 Daily Outfit Randomizer")
    st.subheader("กรุณาเข้าสู่ระบบ หรือ สมัครสมาชิกเพื่อเริ่มต้นใช้งาน")
    st.info("💡 **ทดลองใช้งานกดเข้าสู่ระบบได้ทันทีด้วย:** Username: `admin` | Password: `1234`")
    
    tab1, tab2 = st.tabs(["🔑 เข้าสู่ระบบ", "📝 สมัครสมาชิก"])
    
    with tab1:
        login_user = st.text_input("ชื่อผู้ใช้งาน (Username)", key="login_user")
        login_pass = st.text_input("รหัสผ่าน (Password)", type="password", key="login_pass")
        if st.button("เข้าสู่ระบบ", type="primary", use_container_width=True):
            if authenticate_user(login_user, login_pass):
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success("เข้าสู่ระบบสำเร็จ!")
                st.rerun()
            else:
                st.error("ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง")
                
    with tab2:
        reg_user = st.text_input("ตั้งชื่อผู้ใช้งาน (Username)", key="reg_user")
        reg_pass = st.text_input("ตั้งรหัสผ่าน (Password)", type="password", key="reg_pass")
        if st.button("สมัครสมาชิก", use_container_width=True):
            if reg_user.strip() and reg_pass.strip():
                if register_user(reg_user.strip(), reg_pass.strip()):
                    st.success("สมัครสมาชิกสำเร็จ! กรุณาสลับไปหน้าเข้าสู่ระบบ")
                else:
                    st.warning("ชื่อผู้ใช้นี้มีในระบบแล้ว กรุณาใช้ชื่ออื่น")
            else:
                st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")

# ---------------- หน้าจอหลักของแอปพลิเคชัน (หลัง LOGIN) ----------------
else:
    user_outfits = get_user_outfits(st.session_state.username)
    
    # Header & ปุ่ม Logout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("👗 Daily Outfit Randomizer")
        st.write(f"ยินดีต้อนรับคุณ **{st.session_state.username}** 👋")
    with col2:
        st.write("")
        if st.button("🚪 ออกจากระบบ"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # ==================== SIDEBAR: เพิ่มลุคใหม่ ====================
    st.sidebar.header("➕ เพิ่มลุคใหม่")
    
    # หมวดหมู่เริ่มต้นหากยังไม่มี
    default_categories = ["📚 ไปเรียน / ทำงาน", "ค ไปเที่ยวชิลๆ", "✨ ไปงานแต่ง / งานทางการ"]
    existing_categories = list(user_outfits.keys())
    all_categories = list(set(default_categories + existing_categories))
    
    selected_cat_to_add = st.sidebar.selectbox("เลือกหมวดหมู่:", all_categories)
    new_cat_custom = st.sidebar.text_input("หรือ พิมพ์ชื่อหมวดหมู่ใหม่ที่ต้องการ:")
    
    final_cat = new_cat_custom.strip() if new_cat_custom.strip() else selected_cat_to_add
    new_outfit_text = st.sidebar.text_input("รายละเอียดชุด (เช่น เสื้อ... + กางเกง...):")
    uploaded_file = st.sidebar.file_uploader("🖼️ แนบรูปภาพชุด (JPG, PNG):", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        preview_img = Image.open(uploaded_file)
        st.sidebar.image(preview_img, caption="ตัวอย่างรูปที่เลือก", use_container_width=True)

    if st.sidebar.button("💾 บันทึกชุดใหม่", use_container_width=True):
        if new_outfit_text.strip():
            add_user_outfit(
                st.session_state.username, 
                final_cat, 
                new_outfit_text.strip(), 
                uploaded_file
            )
            st.sidebar.success(f"บันทึก '{new_outfit_text}' เรียบร้อยแล้ว!")
            st.rerun()
        else:
            st.sidebar.warning("กรุณากรอกรายละเอียดชุดก่อนกดบันทึก")

    # ==================== MAIN PAGE: สุ่มชุดและแสดงผล ====================
    st.divider()
    
    selectable_categories = all_categories if user_outfits == {} else list(user_outfits.keys())
    selected_category = st.selectbox("🎯 เลือกโอกาส/หมวดหมู่ที่ต้องการ:", selectable_categories)

    if st.button("🎲 สุ่มชุดแต่งตัว!", type="primary", use_container_width=True):
        available_outfits = user_outfits.get(selected_category, [])
        
        if available_outfits:
            chosen_outfit = random.choice(available_outfits)
            st.success(f"### ✨ ชุดที่คุณได้วันนี้:\n**{chosen_outfit['text']}**")
            
            if chosen_outfit["image"] is not None:
                st.image(chosen_outfit["image"], caption=chosen_outfit["text"], use_container_width=True)
            else:
                st.info("💡 ชุดนี้ยังไม่มีรูปภาพประกอบ คุณสามารถอัปโหลดรูปเพิ่มเติมได้ที่ Sidebar ซ้ายมือครับ")
        else:
            st.warning("หมวดหมู่นี้ยังไม่มีรายการชุดของคุณ ลองเพิ่มชุดใหม่ทาง Sidebar ซ้ายมือได้เลยครับ!")

    # แสดงรายการชุดทั้งหมดที่มีของผู้ใช้งานคนนี้
    if user_outfits:
        with st.expander("👀 ดูรายการชุดทั้งหมดของคุณตามหมวดหมู่"):
            for cat, items in user_outfits.items():
                st.write(f"### {cat} ({len(items)} ชุด)")
                for idx, item in enumerate(items, 1):
                    has_img_tag = " 🖼️ (มีรูปภาพ)" if item["image"] is not None else ""
                    st.write(f"{idx}. {item['text']}{has_img_tag}")
