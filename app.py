import streamlit as st
import openai
import json

# Konfiguracja (sekrety)
PASSWORD = st.secrets["APP_PASSWORD"]
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    pwd = st.text_input("Podaj hasło:", type="password")
    if pwd == PASSWORD:
        st.session_state.logged_in = True
    else:
        st.stop()

st.title("Asystent Opisywania i Tagowania Zdjęć z FAQ w Chmurze")

# Ładowanie FAQ
with open("faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

st.header("FAQ – Najczęściej zadawane pytania")

faq_question = st.text_input("Zadaj pytanie (np. 'Jak działa system?')")

matched = [
    item["answer"]
    for item in faq_data
    if faq_question.lower() in item["question"].lower()
]

st.subheader("Odpowiedź:")
if matched:
    st.write(matched[0])
elif faq_question:
    st.write("Niestety, nie mogę Ci pomóc.")

with st.expander("Pokaż pełną listę pytań z FAQ"):
    for item in faq_data:
        st.markdown(f"**Q:** {item['question']}")
        st.markdown(f"**A:** {item['answer']}")
        st.markdown("---")

st.header("Analiza zdjęcia")

uploaded_file = st.file_uploader("Wgraj zdjęcie do analizy", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, use_container_width=True)

    vision_tags = ["dog", "grass", "sunny", "outdoor"]
    vision_description = "A dog sitting on grass on a sunny day."

    prompt = f'''
    Na podstawie tego opisu: "{vision_description}" oraz tagów {vision_tags},
    wygeneruj ładny opis zdjęcia i zaproponuj 5 tagów (hashtagów).
    '''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem AI."},
            {"role": "user", "content": prompt}
        ]
    )

    st.subheader("Wygenerowany opis i tagi:")
    st.write(response.choices[0].message.content)