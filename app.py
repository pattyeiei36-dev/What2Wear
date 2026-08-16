import streamlit as st
import random
import os

# --- CONFIG & INITIAL SETUP ---
st.set_page_config(page_title="Modern Outfit Picker", page_icon="🛍️", layout="centered")

USER_DB = {"user1": "1234", "admin": "password"}

# คลังชุดแต่งกายสไตล์วัยรุ่นยุคใหม่ (อัปเดตใช้ Local Image Path)
MODERN_OUTFITS = [
    # --- 🧢 Gorpcore & Techwear ---
    {
        "category": "🧢 Gorpcore & Techwear",
        "name": "Gorpcore Utility Trail",
        "desc": "เสื้อแจ็กเก็ตกันลม Arc'teryx + กางเกงคาร์โก้ผ้า Ripstop + รองเท้า Salomon XT-6 + แว่น Oakley",
        # ใช้ r"..." เพื่อรองรับ Path บน Windows (ใส่ตัว r ด้านหน้า)
        "img": r"Gemini_Generated_Image_yk5vbwyk5vbwyk5v.jpg"
    },
    {
        "category": "🧢 Gorpcore & Techwear",
        "name": "Tactical Outdoor Layer",
        "desc": "เสื้อกั๊ก Utility มีกระเป๋าเยอะ + เสื้อยืดสีพื้นทรง Oversized + หมวก Bucket ผ้ากันน้ำ",
        "img": r"Gemini_Generated_Image_9oxyag9oxyag9oxy.jpg"
    },
    {
        "category": "🧢 Gorpcore & Techwear",
        "name": "Mountain Minimalist",
        "desc": "เสื้อขนแกะ (Fleece Jacket) สีทูโทน + กางเกงขาสั้นลุยป่า + ถุงเท้าข้อยาว + รองเท้า Trail Running",
        "img": r"Gemini_Generated_Image_tn0lhwtn0lhwtn0l.jpg"
    },
    {
        "category": "🧢 Gorpcore & Techwear",
        "name": "Urban Anorak Fit",
        "desc": "เสื้อ Anorak สวมหัวสีเอิร์ธโทน + กางเกงชิโน่ขากว้าง + กระเป๋าคาดอก Paracord",
        "img": r"Gemini_Generated_Image_fkrceafkrceafkrc.jpg"
    },
    {
        "category": "🧢 Gorpcore & Techwear",
        "name": "Modern Hiker Vibe",
        "desc": "เสื้อกั๊กผ้านวม (Puffer Vest) + เสื้อฮู้ดดี้คอตตอนหนา + กางเกงยีนส์ฟอก + บูทลุยหิมะ/ป่า",
        "img": r"Gemini_Generated_Image_q81jtiq81jtiq81j.jpg"
    },

    # --- ✨ Clean Girl & Old Money ---
    {
        "category": "✨ Clean Girl & Old Money",
        "name": "Quiet Luxury Linen",
        "desc": "เดรสยาวผ้าฝ้ายเรียบสีขาวทรงคอกลม/คอเหลี่ยม + เสื้อคาร์ดิแกนไหมพรมสีเบจผูกเอวหรือพาดไหล่ + รองเท้าคัทชูพื้นแบน (Ballerina Flats) สีดำ + ต่างหูมุกขนาดเล็ก",
        "img": r"Gemini_Generated_Image_blda67blda67blda.jpg"
    },
    {
        "category": "✨ Clean Girl & Old Money",
        "name": "Tennis Club Aesthetic",
        "desc": "เสื้อไหมพรมคอวีถักลายเคเบิล + กระโปรงเทนนิสอัดจีบ + ถุงเท้าข้อยาวสีขาว + รองเท้าผ้าใบคลีนๆ",
        "img": r"Gemini_Generated_Image_lrueellrueellrue.jpg"
    },

    # --- ⚽ Blokecore & Sporty ---
    {
        "category": "⚽ Blokecore & Sporty",
        "name": "Vintage Football Blokecore",
        "desc": "เสื้อบอลวินเทจยุค 90s + กางเกงยีนส์บากี้หลวมๆ + รองเท้า Adidas Samba / Gazelle",
        "img": r"Gemini_Generated_Image_4i1y554i1y554i1y.jpg"
    },

    # --- 🖤 Acubi & Modern Y2K ---
    {
        "category": "🖤 Acubi & Modern Y2K",
        "name": "Acubi Minimal Layering",
        "desc": "เสื้อซีทรูแขนยาวทับสายเดี่ยวแบบเฉียง + กางเกงคาร์โก้เอวต่ำสีเทา/ดำ + สร้อยคอเงินแท่งมินิมอล",
        "img": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600"
    },

    # --- ☕ Korean Cityboy & Minimal ---
    {
        "category": "☕ Korean Cityboy & Minimal",
        "name": "Cityboy Wide Silhouette",
        "desc": "เสื้อเชิ้ต Oxford ทรงหลวมพิเศษ + กางเกงยีนส์ทรงขากระบอกใหญ่ + รองเท้า Clark Wallabee",
        "img": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=600"
    }
]

# โหลดชุดลงใน Session State
if "outfits" not in st.session_state:
    st.session_state.outfits = MODERN_OUTFITS

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- LOGIN & LOGOUT SYSTEM ---
def login():
    st.sidebar.title("🔐 เข้าสู่ระบบ")
    user_input = st.sidebar.text_input("Username")
    pass_input = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if user_input in USER_DB and USER_DB[user_input] == pass_input:
            st.session_state.logged_in = True
            st.session_state.username = user_input
            st.rerun()
        else:
            st.sidebar.error("Username หรือ Password ไม่ถูกต้อง")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# --- SIDEBAR CONTROLS ---
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.write(f"👤 ยินดีต้อนรับ, **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        logout()
    
    st.sidebar.divider()
    
    # ฟอร์มเพิ่มลุคใหม่
    st.sidebar.subheader("➕ เพิ่มลุคใหม่เข้าคลัง")
    categories = list(set([o["category"] for o in st.session_state.outfits]))
    new_cat = st.sidebar.selectbox("เลือกหมวดหมู่", categories)
    new_name = st.sidebar.text_input("ชื่อสไตล์/ลุค")
    new_desc = st.sidebar.text_area("รายละเอียดชุด")
    new_img = st.sidebar.text_input("Path รูปภาพในเครื่อง หรือ URL")
    
    if st.sidebar.button("บันทึกชุดใหม่"):
        if new_name and new_desc and new_img:
            st.session_state.outfits.append({
                "category": new_cat,
                "name": new_name,
                "desc": new_desc,
                "img": new_img
            })
            st.sidebar.success("เพิ่มชุดใหม่เข้าคลังสำเร็จ!")
        else:
            st.sidebar.warning("กรุณากรอกข้อมูลให้ครบทุกช่อง")

# --- MAIN APP DISPLAY ---
st.title("🛍️ Trend & Aesthetic Outfit Picker")
st.write("สุ่มไอเดียจัดเซ็ตเสื้อผ้าสำหรับเทรนด์วัยรุ่นยุคใหม่")

categories_list = ["สุ่มจากทุกหมวดหมู่ (All Categories)"] + sorted(list(set([o["category"] for o in st.session_state.outfits])))
selected_cat = st.selectbox("🎯 เลือกสไตล์ที่ชอบ:", categories_list)

if st.button("✨ สุ่มลุคแต่งตัว!", type="primary"):
    if selected_cat == "สุ่มจากทุกหมวดหมู่ (All Categories)":
        available_outfits = st.session_state.outfits
    else:
        available_outfits = [o for o in st.session_state.outfits if o["category"] == selected_cat]
    
    if available_outfits:
        st.session_state.current_outfit = random.choice(available_outfits)

# แสดงผลชุดที่สุ่มได้
if "current_outfit" in st.session_state:
    outfit = st.session_state.current_outfit
    
    st.markdown("---")
    st.caption(f"หมวดหมู่: {outfit['category']}")
    st.subheader(f"⚡ ลุคแนะนำ: **{outfit['name']}**")
    st.write(f"🧺 **ชิ้นส่วนในเซ็ต:** {outfit['desc']}")
    
    # เช็กว่ารูปภาพมาจาก URL หรือ Local File Path ในเครื่อง
    img_path = outfit['img']
    if img_path.startswith("http://") or img_path.startswith("https://"):
        st.image(img_path, caption=f"Outfit Visual: {outfit['name']}", use_container_width=True)
    else:
        # ตรวจสอบว่ามีไฟล์อยู่จริงในเครื่องก่อนแสดงผล
        if os.path.exists(img_path):
            st.image(img_path, caption=f"Outfit Visual: {outfit['name']}", use_container_width=True)
        else:
            st.error(f"ไม่พบไฟล์รูปภาพในเครื่องตามตำแหน่ง: {img_path}")
