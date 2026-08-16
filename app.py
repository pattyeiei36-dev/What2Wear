import streamlit as st
import random
import os

# --- CONFIG & INITIAL SETUP ---
st.set_page_config(page_title="Modern Outfit Picker", page_icon="🛍️", layout="centered")

# --- 1. CSS ธีมสีชมพู & เอฟเฟกต์ไอคอนร่วงหล่นภายในหน้าเว็บ ---
st.markdown("""
<style>
    /* พื้นหลังแอปสีชมพูสดใส */
    .stApp {
        background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 50%, #FFA7A7 100%) !important;
        overflow-x: hidden;
    }
    
    /* ตกแต่งหัวข้อหลัก */
    h1 {
        color: #FF1493 !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 8px rgba(255, 255, 255, 0.8);
        text-align: center;
    }
    
    /* การ์ดผลลัพธ์ */
    .outfit-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 12px 30px rgba(255, 20, 147, 0.25);
        border: 3px solid #FF69B4;
        margin-top: 20px;
        margin-bottom: 25px;
    }

    /* ปุ่มสุ่มสีชมพูกราเดียนต์ */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #FF007F, #FF758C, #FF7EB3) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 14px 35px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        box-shadow: 0 6px 20px rgba(255, 0, 127, 0.4) !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 8px 25px rgba(255, 0, 127, 0.6) !important;
    }

    /* สร้างกล่องจำลองฝนเสื้อผ้าร่วงหล่นแบบเสถียรบน Cloud */
    .rain-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        overflow: hidden;
        z-index: 999;
    }

    .falling-item {
        position: absolute;
        top: -10%;
        user-select: none;
        animation-name: fallAnimation;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
    }

    @keyframes fallAnimation {
        0% {
            transform: translateY(-10vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(110vh) rotate(360deg);
            opacity: 0.3;
        }
    }
</style>

<!-- สร้างสลัดไอคอนร่วงหล่นด้วย CSS Pure Animation เพื่อให้รันบน Cloud ได้ชัวร์ -->
<div class="rain-container">
    <div class="falling-item" style="left: 5%; font-size: 24px; animation-duration: 5s; animation-delay: 0s;">👕</div>
    <div class="falling-item" style="left: 15%; font-size: 28px; animation-duration: 7s; animation-delay: 2s;">👗</div>
    <div class="falling-item" style="left: 25%; font-size: 22px; animation-duration: 6s; animation-delay: 1s;">👟</div>
    <div class="falling-item" style="left: 35%; font-size: 26px; animation-duration: 8s; animation-delay: 3s;">🧢</div>
    <div class="falling-item" style="left: 45%; font-size: 25px; animation-duration: 5.5s; animation-delay: 0.5s;">🕶️</div>
    <div class="falling-item" style="left: 55%; font-size: 27px; animation-duration: 6.5s; animation-delay: 2.5s;">👜</div>
    <div class="falling-item" style="left: 65%; font-size: 23px; animation-duration: 7.5s; animation-delay: 1.5s;">🧥</div>
    <div class="falling-item" style="left: 75%; font-size: 26px; animation-duration: 6s; animation-delay: 3.5s;">👖</div>
    <div class="falling-item" style="left: 85%; font-size: 24px; animation-duration: 5s; animation-delay: 1s;">🎀</div>
    <div class="falling-item" style="left: 92%; font-size: 29px; animation-duration: 8s; animation-delay: 0.2s;">✨</div>
</div>
""", unsafe_allow_html=True)

USER_DB = {"user1": "1234", "admin": "password"}

# คลังชุดแต่งกายสไตล์วัยรุ่นยุคใหม่
MODERN_OUTFITS = [
    # --- 🧢 Gorpcore & Techwear ---
    {
        "category": "🧢 Gorpcore & Techwear",
        "name": "Gorpcore Utility Trail",
        "desc": "เสื้อแจ็กเก็ตกันลม Arc'teryx + กางเกงคาร์โก้ผ้า Ripstop + รองเท้า Salomon XT-6 + แว่น Oakley",
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
    {
        "category": "⚽ Blokecore & Sporty",
        "name": "Sporty Track Crop Fit",
        "desc": "เสื้อโปโลครอปเอวลอยทรงสปอร์ตสกรีนเบอร์/โลโก้ + กางเกงวอร์มวิดเทจผ้าร่มทรงขากว้างกองพื้น (Track Pants) + รองเท้าสนีกเกอร์พื้นหนา (Chunky Sneakers) + หมวกเบสบอลปักลาย",
        "img": r"Gemini_Generated_Image_pk8leepk8leepk8l.jpg"
    },
    {
        "category": "⚽ Blokecore & Sporty",
        "name": "Retro Jersey & Cargo",
        "desc": "เสื้อกล้ามครอปผ้าร่องสีขาว สวมทับด้วยเสื้อเชิ้ตบอลวินเทจแขนสั้นทรง Oversized (ติดกระดุมเม็ดบนเม็ดเดียว) + กางเกงยีนส์เอวต่ำทรงคาร์โก้ขากว้างกองพื้นสีเทาฟอก + รองเท้าสนีกเกอร์สไตล์เรโทร + หมวกไหมพรม (Beanie) สีเข้ม",
        "img": r"Gemini_Generated_Image_ngxsarngxsarngxs.jpg"
    },

    # --- 🖤 Acubi & Modern Y2K ---
    {
        "category": "🖤 Acubi & Modern Y2K",
        "name": "Acubi Minimal Layering",
        "desc": "เสื้อซีทรูแขนยาวทับสายเดี่ยวแบบเฉียง + กางเกงคาร์โก้เอวต่ำสีเทา/ดำ + สร้อยคอเงินแท่งมินิมอล",
        "img": r"Gemini_Generated_Image_tg0of9tg0of9tg0o.jpg"
    },
    {
        "category": "🖤 Acubi & Modern Y2K",
        "name": "Metallic Y2K Knit Fit",
        "desc": "เสื้อไหมพรมถักโปร่งตัวสั้นโทนสีดำ/เทาฟอก สวมทับเสื้อสายเดี่ยวครอปสีขาว + กางเกงยีนส์เอวต่ำทรงขากว้างฟอกซีดกองพื้น + เข็มขัดหัวโลหะรูปดาว + รองเท้าสนีกเกอร์พื้นหนาโทนสีเงินเมทัลลิก",
        "img": r"Gemini_Generated_Image_l0qhrwl0qhrwl0qh.jpg"
    },

    # --- ☕ Korean Cityboy & Minimal ---
    {
        "category": "☕ Korean Cityboy & Minimal",
        "name": "Cafe Chills Cityboy",
        "desc": "เสื้อเชิ้ต Oxford ทรงหลวมพิเศษ + กางเกงยีนส์ทรงขากระบอกใหญ่ + รองเท้า Clark Wallabee",
        "img": r"Gemini_Generated_Image_9n8oei9n8oei9n8o.jpg"
    },
    {
        "category": "☕ Korean Cityboy & Minimal",
        "name": "Earth Tone Cardigan Layer",
        "desc": "เสื้อคาร์ดิแกนไหมพรมกระดุมหน้าสีน้ำตาลเอิร์ธโทน สวมทับเสื้อกล้ามคอเหลี่ยมสีขาว + กางเกงคาร์โก้เอวสูงสีดำทรงหลวม + รองเท้าสนีกเกอร์ทรงสปอร์ต + แว่นตาเลนส์ใสกรอบบาง",
        "img": r"Gemini_Generated_Image_gxoz4wgxoz4wgxoz.jpg"
    },
    {
        "category": "☕ Korean Cityboy & Minimal",
        "name": "Baby Tee Chill Day",
        "desc": "เสื้อยืด Baby Tee + กางเกงยีนส์ขาสั้นสีขาว + รองเท้าแตะชิลๆน่ารักๆ + กระเป๋าสะพายไหล่ใบเล็ก",
        "img": r"Gemini_Generated_Image_eupb1qeupb1qeupb.jpg"
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
    categories = sorted(list(set([o["category"] for o in st.session_state.outfits])))
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
            st.rerun()
        else:
            st.sidebar.warning("กรุณากรอกข้อมูลให้ครบทุกช่อง")

# --- MAIN APP DISPLAY ---
st.title("🛍️ Trend & Aesthetic Outfit Picker")
st.markdown("<p style='text-align: center; color: #4A4A4A; font-weight: 600;'>💖 สุ่มไอเดียจัดเซ็ตเสื้อผ้าสำหรับเทรนด์วัยรุ่นยุคใหม่</p>", unsafe_allow_html=True)

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
    
    st.markdown(f"""
    <div class="outfit-card">
        <span style="background: linear-gradient(45deg, #FF007F, #FF69B4); color: white; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: bold;">
            {outfit['category']}
        </span>
        <h2 style="color: #FF1493; margin-top: 15px; margin-bottom: 8px;">⚡ ลุคแนะนำ: <b>{outfit['name']}</b></h2>
        <p style="color: #333333; font-size: 16px; line-height: 1.6;">🧺 <b>ชิ้นส่วนในเซ็ต:</b> {outfit['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # เช็กว่ารูปภาพมาจาก URL หรือ Local File Path ในเครื่อง
    img_path = outfit['img']
    if img_path.startswith("http://") or img_path.startswith("https://"):
        st.image(img_path, caption=f"Outfit Visual: {outfit['name']}", use_container_width=True)
    else:
        if os.path.exists(img_path):
            st.image(img_path, caption=f"Outfit Visual: {outfit['name']}", use_container_width=True)
        else:
            st.error(f"ไม่พบไฟล์รูปภาพในเครื่องตามตำแหน่ง: {img_path}")
