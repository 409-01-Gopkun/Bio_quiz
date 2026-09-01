import time
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="เกมทายโครงสร้างสารชีวโมเลกุล by NongGluay56",
    page_icon="🧬",
    layout="centered"
)

# กำหนดเวลารวมของเกม (วินาที)
TOTAL_TIME_LIMIT = 120

# URL สำหรับดึงรูปภาพจาก GitHub
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/409-01-Gopkun/Bio_quiz/main/Images/"

# คลังข้อมูลข้อสอบ
QUIZ_DATA = [
    {
        "image": GITHUB_RAW_BASE + "glucose.png",
        "options": ["ก. Glucose", "ข. Fructose", "ค. Galactose", "ง. Ribose"],
        "answer": "ก. Glucose",
        "hint": "คําใบ้ ไม่มีนะจ่ะ"
    },
    {
        "image": GITHUB_RAW_BASE + "dna.jpg",
        "options": ["ก. Ribose", "ข. Deoxyribose", "ค. Aldehyde", "ง. Ketone"],
        "answer": "ข. Deoxyribose",
        "hint": "คําใบ้ ไม่มีนะจ่ะ"
    },
    {
        "image": GITHUB_RAW_BASE + "cholesterol.png",
        "options": ["ก. Phospholipid", "ข. Triglyceride", "ค. Cholesterol", "ง. Estrogen"],
        "answer": "ค. Cholesterol",
        "hint": "คําใบ้ ไม่มีนะจ่ะ"
    },
    {
        "image": GITHUB_RAW_BASE + "rna.jpg",
        "options": ["ก. RNA", "ข. DNA", "ค. Deoxyribose", "ง. Ribose"],
        "answer": "ง. Ribose",
        "hint": "คําใบ้ ไม่มีนะจ่ะ"
    },
    {
        "image": GITHUB_RAW_BASE + "pyrimidines.png",
        "options": ["ก. Purines", "ข. Pyrimidines", "ค. Pentoses", "ง. Aldehyde"],
        "answer": "ข. Pyrimidines",
        "hint": "คําใบ้ ไม่มีนะจ่ะ"
    },
    {
        "image": GITHUB_RAW_BASE + "amino-acid.jpg",
        "options": ["ก. Amino Acid", "ข. Hexoses", "ค. Lipids", "ง. Carbohydrates"],
        "answer": "ก. Amino Acid",
        "hint": "คําใบ้ ไม่มีนะจ่ะ"
    }
]

# ตัวจัดการ State ของเกม
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "game_over_by_time" not in st.session_state:
    st.session_state.game_over_by_time = False

def next_question():
    st.session_state.current_question += 1
    st.session_state.answered = False
    st.session_state.selected_option = None

def restart_game():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.start_time = time.time()
    st.session_state.game_over_by_time = False

# คำนวณเวลาที่เหลือ
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(0, int(TOTAL_TIME_LIMIT - elapsed_time))

if remaining_time <= 0:
    st.session_state.game_over_by_time = True

# UI หลัก
st.title("🧬 เกมทายโครงสร้างสารชีวโมเลกุล by NongGluay56")

# ตรวจสอบว่าเกมจบหรือยัง (ทำครบทุกข้อ หรือ หมดเวลา)
is_game_finished = (st.session_state.current_question >= len(QUIZ_DATA)) or st.session_state.game_over_by_time

if not is_game_finished:
    q_idx = st.session_state.current_question
    q_data = QUIZ_DATA[q_idx]

    # แถบแสดงสถานะและตัวจับเวลา
    col_info, col_timer = st.columns([2, 1])
    with col_info:
        st.caption(f"ข้อที่ {q_idx + 1} / {len(QUIZ_DATA)}  |  คะแนนสะสม: {st.session_state.score}")
    with col_timer:
        st.markdown(f"⏱️ **เวลาที่เหลือ: {remaining_time} วินาที**")
    
    # แสดงรูปภาพโครงสร้างสาร
    st.image(q_data["image"], caption="ภาพโครงสร้างโมเลกุล", use_container_width=True)
    st.markdown("### **เดาข้อที่คิดว่าใช่:**")

    # จัดวางปุ่ม 4 ตัวเลือกเป็น 2 แถว แถวละ 2 ปุ่ม (Grid 2x2)
    col1, col2 = st.columns(2)
    
    with col1:
        btn_a = st.button(q_data["options"][0], use_container_width=True, disabled=st.session_state.answered)
        btn_c = st.button(q_data["options"][2], use_container_width=True, disabled=st.session_state.answered)
        
    with col2:
        btn_b = st.button(q_data["options"][1], use_container_width=True, disabled=st.session_state.answered)
        btn_d = st.button(q_data["options"][3], use_container_width=True, disabled=st.session_state.answered)

    # เช็กการกดปุ่มของผู้เล่น
    choice = None
    if btn_a: choice = q_data["options"][0]
    if btn_b: choice = q_data["options"][1]
    if btn_c: choice = q_data["options"][2]
    if btn_d: choice = q_data["options"][3]

    if choice and not st.session_state.answered:
        st.session_state.answered = True
        st.session_state.selected_option = choice
        if choice == q_data["answer"]:
            st.session_state.score += 1

    # แสดงผลลัพธ์หลังเลือกคำตอบ
    if st.session_state.answered:
        if st.session_state.selected_option == q_data["answer"]:
            st.success(f"✅ **ถูกได้ไงวะ ใช่ AI หรอ!** {q_data['hint']}")
        else:
            st.error(f"❌ **ผิดไอ่โง่ ง่ายชิบหาย!** ข้อถูกคือ **{q_data['answer']}**")
        
        st.button("ข้อถัดไป ➔", on_click=next_question, type="primary")

else:
    # หน้าสรุปผลลัพธ์เมื่อทำครบทุกข้อหรือหมดเวลา
    if st.session_state.game_over_by_time:
        st.error("⏰ **Time Up ไอ่ดํา!**")
    else:
        st.balloons()
        st.success("🎉 **Very Goodทำครบทุกข้อแล้ว!**")
        
    st.header("🏆 สรุปผลการเล่น")
    st.subheader(f"Youทำได้ **{st.session_state.score}** จาก **{len(QUIZ_DATA)}** คะแนน")
    
    st.button("🔄 ลองอีกครั้ง", on_click=restart_game, type="primary")
