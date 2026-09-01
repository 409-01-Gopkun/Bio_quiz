import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="เกมทายโครงสร้างสารชีวโมเลกุล",
    page_icon="🧬",
    layout="centered"
)

# URL สำหรับดึงรูปภาพจาก GitHub (อย่าลืมเปลี่ยน USERNAME และ REPO)
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/409-01-Gopkun/Bio_quiz/main/Images/"

# คลังข้อมูลข้อสอบ (ต้องมี options 4 ตัวเลือกเสมอ)
QUIZ_DATA = [
    {
        "image": GITHUB_RAW_BASE + "glucose.png",
        "options": ["ก. Glucose", "ข. Fructose", "ค. Galactose", "ง. Ribose"],
        "answer": "ก. Glucose",
        "hint": "เป็นน้ำตาลโมเลกุลเดี่ยวที่เป็นแหล่งพลังงานหลักของร่างกาย"
    },
    {
        "image": GITHUB_RAW_BASE + "dna.png",
        "options": ["ก. RNA", "ข. DNA", "ค. ATP", "ง. Protein"],
        "answer": "ข. DNA",
        "hint": "มีโครงสร้างเป็นสายคู่เกลียวสลับเวียนขวา (Double Helix)"
    },
    {
        "image": GITHUB_RAW_BASE + "cholesterol.png",
        "options": ["ก. Phospholipid", "ข. Triglyceride", "ค. Cholesterol", "ง. Prostaglandin"],
        "answer": "ค. Cholesterol",
        "hint": "เป็นลิพิดกลุ่มสเตียรอยด์ที่เป็นองค์ประกอบสำคัญของเยื่อหุ้มเซลล์"
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

def next_question():
    st.session_state.current_question += 1
    st.session_state.answered = False
    st.session_state.selected_option = None

def restart_game():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_option = None

# UI หลัก
st.title("🧬 เกมทายโครงสร้างสารชีวโมเลกุล")

if st.session_state.current_question < len(QUIZ_DATA):
    q_idx = st.session_state.current_question
    q_data = QUIZ_DATA[q_idx]

    # แถบแสดงสถานะ
    st.caption(f"ข้อที่ {q_idx + 1} / {len(QUIZ_DATA)}  |  คะแนนสะสม: {st.session_state.score}")
    
    # แสดงรูปภาพโครงสร้างสาร
    st.image(q_data["image"], caption="ภาพโครงสร้างโมเลกุล", use_column_width=True)
    st.markdown("### **เลือกคำตอบที่ถูกต้อง:**")

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
            st.success(f"✅ **ถูกต้อง!** {q_data['hint']}")
        else:
            st.error(f"❌ **ยังไม่ถูกต้อง!** คำตอบที่ถูกคือ **{q_data['answer']}**")
        
        st.button("ข้อถัดไป ➔", on_click=next_question, type="primary")

else:
    # หน้าสรุปผลลัพธ์เมื่อทำครบทุกข้อ
    st.balloons()
    st.header("🏆 สรุปผลการเล่น")
    st.subheader(f"คุณทำได้ **{st.session_state.score}** จาก **{len(QUIZ_DATA)}** คะแนน")
    
    st.button("🔄 เล่นใหม่อีกครั้ง", on_click=restart_game, type="primary")
