import time
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="เกมทายโครงสร้างสารชีวโมเลกุล by NongGluay56",
    page_icon="🧬",
    layout="centered"
)

TOTAL_TIME_LIMIT = 120
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/409-01-Gopkun/Bio_quiz/main/Images/"

QUIZ_DATA = [
    {
        "image": GITHUB_RAW_BASE + "glucose.png",
        "options": ["ก. Glucose", "ข. Fructose", "ค. Galactose", "ง. Ribose"],
        "answer": "ก. Glucose",
        "hint": "ไม่มี"
    },
    {
        "image": GITHUB_RAW_BASE + "dna.jpg",
        "options": ["ก. Ribose", "ข. Deoxyribose", "ค. Aldehyde", "ง. Ketone"],
        "answer": "ข. Deoxyribose",
        "hint": "ไม่มี"
    },
    {
        "image": GITHUB_RAW_BASE + "cholesterol.png",
        "options": ["ก. Phospholipid", "ข. Triglyceride", "ค. Cholesterol", "ง. Estrogen"],
        "answer": "ค. Cholesterol",
        "hint": "ไม่มี"
    },
    {
        "image": GITHUB_RAW_BASE + "rna.jpg",
        "options": ["ก. RNA", "ข. DNA", "ค. Deoxyribose", "ง. Ribose"],
        "answer": "ง. Ribose",
        "hint": "ไม่มี"
    },
    {
        "image": GITHUB_RAW_BASE + "pyrimidines.png",
        "options": ["ก. Purines", "ข. Pyrimidines", "ค. Pentoses", "ง. Aldehyde"],
        "answer": "ข. Pyrimidines",
        "hint": "ไม่มี"
    },
    {
        "image": GITHUB_RAW_BASE + "amino-acid.jpg",
        "options": ["ก. Amino Acid", "ข. Hexoses", "ค. Lipids", "ง. Carbohydrates"],
        "answer": "ก. Amino Acid",
        "hint": "ไม่มี"
    }
]

# Init session states
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

# Callback เมื่อผู้เล่นกดเลือกคำตอบ
def handle_answer(choice, correct_answer):
    if not st.session_state.answered:
        st.session_state.answered = True
        st.session_state.selected_option = choice
        if choice == correct_answer:
            st.session_state.score += 1

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

st.title("🧬 เกมทายโครงสร้างสารชีวโมเลกุล")

is_game_finished = (st.session_state.current_question >= len(QUIZ_DATA)) or st.session_state.game_over_by_time

if not is_game_finished:
    q_idx = st.session_state.current_question
    q_data = QUIZ_DATA[q_idx]

    col_info, col_timer = st.columns([2, 1])
    with col_info:
        st.caption(f"ข้อที่ {q_idx + 1} / {len(QUIZ_DATA)}  |  คะแนนสะสม: {st.session_state.score}")
    with col_timer:
        st.markdown(f"⏱️ **เวลาที่เหลือ: {remaining_time} วินาที**")
    
    st.image(q_data["image"], caption="ภาพโครงสร้างโมเลกุล", use_container_width=True)
    st.markdown("### **เดาข้อที่คิดว่าใช่:**")

    # ปุ่มกด 4 ตัวเลือกโดยใช้ on_click callback เพื่อป้องกัน State ค้าง
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            q_data["options"][0], 
            use_container_width=True, 
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(q_data["options"][0], q_data["answer"])
        )
        st.button(
            q_data["options"][2], 
            use_container_width=True, 
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(q_data["options"][2], q_data["answer"])
        )
        
    with col2:
        st.button(
            q_data["options"][1], 
            use_container_width=True, 
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(q_data["options"][1], q_data["answer"])
        )
        st.button(
            q_data["options"][3], 
            use_container_width=True, 
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(q_data["options"][3], q_data["answer"])
        )

    # แสดงผลลัพธ์หลังเลือกคำตอบ
    if st.session_state.answered:
        if st.session_state.selected_option == q_data["answer"]:
            st.success(f"✅ **ถูกได้ไงวะ ใช่ AI หรอ!** {q_data['hint']}")
        else:
            st.error(f"❌ **ผิดไอ่โง่ ง่ายชิบหาย!** ข้อถูกคือ **{q_data['answer']}**")
        
        st.button("ข้อถัดไป ➔", on_click=next_question, type="primary")

    # Real-time Timer Loop
    if not st.session_state.answered and remaining_time > 0:
        time.sleep(1)
        st.rerun()

else:
    if st.session_state.game_over_by_time:
        st.error("⏰ **หมดเวลา 120 วินาทีแล้ว!**")
    else:
        st.balloons()
        st.success("🎉 **คุณทำครบทุกข้อแล้ว!**")
        
    st.header("🏆 สรุปผลการเล่น")
    st.subheader(f"คุณทำได้ **{st.session_state.score}** จาก **{len(QUIZ_DATA)}** คะแนน")
    st.button("🔄 ลองอีกครั้ง", on_click=restart_game, type="primary")
