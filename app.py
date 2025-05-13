import streamlit as st
import openai
import base64
import json

# Konfiguracja
PASSWORD = st.secrets["APP_PASSWORD"]
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Funkcja do zamiany obrazu na base64
def image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Logowanie
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    pwd = st.text_input("Podaj hasło:", type="password")
    if pwd == PASSWORD:
        st.session_state.logged_in = True
    else:
        st.stop()

st.title("Asystent Opisywania i Tagowania Zdjęć z FAQ w Chmurze")

# FAQ
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
    image_b64 = image_to_base64(uploaded_file)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Co znajduje się na tym zdjęciu? Opisz je oraz zaproponuj 5 hashtagów."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        st.subheader("Wygenerowany opis i tagi:")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Błąd podczas analizy obrazu: {str(e)}")