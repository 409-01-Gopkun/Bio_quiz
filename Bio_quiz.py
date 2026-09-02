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

# ลิงก์ไฟล์เสียงเอฟเฟกต์ (สามารถเปลี่ยน URL เป็นไฟล์ .mp3 ที่ต้องการได้)
SOUND_CORRECT_URL = "https://raw.githubusercontent.com/409-01-Gopkun/Bio_quiz/main/Audio/correct.mp3"
SOUND_WRONG_URL = "https://raw.githubusercontent.com/409-01-Gopkun/Bio_quiz/main/Audio/wrong.mp3"

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

# ฟังก์ชันเล่นเสียงเอฟเฟกต์
def play_sound(sound_url):
    st.html(f"""
        <audio autoplay hidden>
            <source src="{sound_url}" type="audio/mp3">
        </audio>
    """)

# Callbacks
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

# ฟังก์ชันแสดงเวลาแบบ Real-time โดยไม่ rerun ทั้งหน้ากระดาน
@st.fragment(run_every=1.0)
def render_timer():
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(TOTAL_TIME_LIMIT - elapsed_time))
    
    if remaining_time <= 0 and not st.session_state.game_over_by_time:
        st.session_state.game_over_by_time = True
        st.rerun()
        
    st.markdown(f"⏱️ **เวลาที่เหลือ: {remaining_time} วินาที**")

st.title("🧬 เกมทายโครงสร้างสารชีวโมเลกุล by NongGluay56")

is_game_finished = (st.session_state.current_question >= len(QUIZ_DATA)) or st.session_state.game_over_by_time

if not is_game_finished:
    q_idx = st.session_state.current_question
    q_data = QUIZ_DATA[q_idx]

    col_info, col_timer = st.columns([2, 1])
    with col_info:
        st.caption(f"ข้อที่ {q_idx + 1} / {len(QUIZ_DATA)}  |  คะแนนสะสม: {st.session_state.score}")
    with col_timer:
        render_timer()
    
    st.image(q_data["image"], caption="ภาพโครงสร้างโมเลกุล", use_container_width=True)
    st.markdown("### **เดาข้อที่คิดว่าใช่:**")

    # ใส่ key แยกตาม q_idx เพื่อไม่ให้ปุ่มจำ State ซ้ำข้อเดิม
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            q_data["options"][0], 
            key=f"btn_{q_idx}_0",
            use_container_width=True, 
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(q_data["options"][0], q_data["answer"])
        )
        st.button(
            q_data["options"][2], 
            key=f"btn_{q_idx}_2",
            use_container_width=True, 
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(q_data["options"][2], q_data["answer"])
        )
        
    with col2:
        st.button(
            q_data["options"][1], 
            key=f"btn_{q_idx}_1",
            use_container_width=True, 
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(q_data["options"][1], q_data["answer"])
        )
        st.button(
            q_data["options"][3], 
            key=f"btn_{q_idx}_3",
            use_container_width=True, 
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(q_data["options"][3], q_data["answer"])
        )

    # แสดงผลลัพธ์และเล่นเสียงหลังเลือกคำตอบ
    if st.session_state.answered:
        if st.session_state.selected_option == q_data["answer"]:
            play_sound(SOUND_CORRECT_URL)
            st.success(f"✅ **ถูกได้ไงวะ ใช้ AI หรอ!** {q_data['hint']}")
        else:
            play_sound(SOUND_WRONG_URL)
            st.error(f"❌ **ผิดไอ่สึ่งตึง ง่าวชิบหาย!** ข้อถูกคือ **{q_data['answer']}**")
        
        st.button("ข้อถัดไป ➔", on_click=next_question, type="primary", key=f"next_{q_idx}")

else:
    if st.session_state.game_over_by_time:
        st.error("⏰ **ช้าเกิน ไอ่น้อง!**")
    else:
        st.balloons()
        st.success("🎉 **ไวจัด เหมือนไอรีนเลย!**")
        
    st.header("🏆 สรุปผลการเล่น")
    st.subheader(f"คุณเดาถูก **{st.session_state.score}** จาก **{len(QUIZ_DATA)}** คะแนน")
    st.button("🔄 อีกสักรอบไหมไอ่น้อง", on_click=restart_game, type="primary", key="restart_btn")
