import random
import streamlit as st
from PIL import Image

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Outfit Randomizer", page_icon="👗", layout="centered")

st.title("👗 Daily Outfit Randomizer")
st.write("ช่วยสุ่มชุดประจำวันหรือเลือก outfit สำหรับแต่งตัวไปงานต่างๆ")

# ==================== 1. โหลดรูปภาพตั้งต้นจากโฟลเดอร์ ====================
# หากมีรูปอยู่ในโฟลเดอร์เดียวกับ app.py สามารถใช้ Image.open("ชื่อไฟล์.jpg") ได้
# ถ้าหาไฟล์ไม่พบ ระบบจะใส่เป็น None ให้อัตโนมัติ (ไม่ทำให้โค้ดค้าง/พัง)
def load_default_image(file_name):
    try:
        return Image.open(file_name)
    except Exception:
        return None

# ตัวอย่างการโหลดรูปตั้งต้น (เปลี่ยน "sample1.jpg" เป็นชื่อไฟล์รูปที่มีในเครื่องได้เลย)
img_sample1 = load_default_image("sample1.jpg")
img_sample2 = load_default_image("sample2.jpg")

# ==================== 2. INITIALIZE SESSION STATE ====================
if "outfits" not in st.session_state:
    st.session_state.outfits = {
        "ไปเรียน / ทำงาน": [
            {"text": "เสื้อเชิ้ตสีขาว + กางเกงสแล็คสีดำ + รองเท้าผ้าใบ", "image": Image.open(r"C:\Users\ADMIN\Downloads\Gemini_Generated_Image_kro3m6kro3m6kro3.jpg")},
            {"text": "เสื้อโปโลสีน้ำเงิน + กางเกงชิโน่สีน้ำตาล + รองเท้าผ้าใบ", "image": Image.open(r"C:\Users\ADMIN\Downloads\Gemini_Generated_Image_kisu8zkisu8zkisu.jpg")},
            {"text": "เสื้อเบลเซอร์ + เสื้อยืดข้างใน + กางเกงยีนส์ทรงกระบอก", "image": Image.open(r"C:\Users\ADMIN\Downloads\ชุด3.jpg")},
        ],
        "ไปเที่ยวชิลๆ": [
            {"text": "เสื้อยืด Oversize + กางเกงขาสั้น + รองเท้าแตะแฟชั่น", "image": Image.open(r"C:\Users\ADMIN\Downloads\Gemini_Generated_Image_eo43h1eo43h1eo43.jpg")},
            {"text": "เสื้อสายเดี่ยว/เสื้อกล้าม + กางเกงยีนส์เอวสูง + รองเท้าผ้าใบ", "image": load_default_image("Gemini_Generated_Image_1a4aex1a4aex1a4a.jpg")},

        "ไปงานแต่ง / งานทางการ": [
            {"text": "ชุดสูทสากลสีเทา/กรมท่า + เนกไท + รองเท้าหนัง", "image": None},
            {"text": "ชุดเดรสยาวออกงาน + เครื่องประดับเรียบหรู + รองเท้าส้นสูง", "image": None},
            {"text": "ชุดไทยจิตรลดา / ชุดประยุกต์สุภาพ", "image": None}
        ]
    }

# ==================== 3. SIDEBAR: เพิ่มลุคใหม่ + อัปโหลดรูป ====================
st.sidebar.header("➕ เพิ่มลุคใหม่ของคุณ")

categories = list(st.session_state.outfits.keys())
selected_cat_to_add = st.sidebar.selectbox("เลือกหมวดหมู่ที่ต้องการเพิ่ม:", categories)

# ช่องกรอกรายละเอียดชุด
new_outfit_text = st.sidebar.text_input("รายละเอียดชุด (เช่น เสื้อ... + กางเกง...):")

# ช่องอัปโหลดไฟล์รูปภาพจากเครื่อง/โทรศัพท์
uploaded_file = st.sidebar.file_uploader("🖼️ แนบรูปภาพชุด (JPG, PNG):", type=["jpg", "jpeg", "png"])

# แสดงตัวอย่างรูปภาพทันทีเมื่อเลือกไฟล์ใน Sidebar
if uploaded_file is not None:
    preview_img = Image.open(uploaded_file)
    st.sidebar.image(preview_img, caption="ตัวอย่างรูปที่เลือก", use_container_width=True)

if st.sidebar.button("💾 บันทึกชุดใหม่", use_container_width=True):
    if new_outfit_text.strip():
        img_data = None
        if uploaded_file is not None:
            img_data = Image.open(uploaded_file)
        
        # เพิ่มข้อมูลชุดใหม่ลง Session State
        st.session_state.outfits[selected_cat_to_add].append({{
            "text": new_outfit_text.strip(),
            "image": img_data
        })
        st.sidebar.success(f"บันทึก '{new_outfit_text}' เรียบร้อยแล้ว!")
    else:
        st.sidebar.warning("กรุณากรอกรายละเอียดชุดก่อนกดบันทึก")

# ==================== 4. MAIN PAGE: สุ่มชุดและแสดงผล ====================
st.divider()

selected_category = st.selectbox("🎯 เลือกโอกาส/งานที่ต้องการไป:", categories)

if st.button("🎲 สุ่มชุดแต่งตัว!", type="primary", use_container_width=True):
    available_outfits = st.session_state.outfits[selected_category]
    
    if available_outfits:
        chosen_outfit = random.choice(available_outfits)
        
        st.success(f"### ✨ ชุดที่คุณได้วันนี้:\n**{chosen_outfit['text']}**")
        
        # แสดงรูปภาพถ้ามี
        if chosen_outfit["image"] is not None:
            st.image(chosen_outfit["image"], caption=chosen_outfit["text"], use_container_width=True)
        else:
            st.info("💡 ชุดนี้ยังไม่มีรูปภาพประกอบ คุณสามารถเพิ่มรูปภาพได้จาก Sidebar ทางซ้ายมือครับ")
    else:
        st.error("หมวดหมู่นี้ยังไม่มีรายการชุด")

# แสดงรายการชุดทั้งหมดที่มีในระบบ
with st.expander("👀 ดูรายการชุดทั้งหมดตามหมวดหมู่"):
    for cat, items in st.session_state.outfits.items():
        st.write(f"**{cat}** ({len(items)} ชุด)")
        for item in items:
            has_img_tag = " 🖼️ (มีรูปภาพ)" if item["image"] is not None else ""
            st.write(f"- {item['text']}{has_img_tag}")