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

st.title("Asystent Opisu Obrazów i FAQ")

uploaded_file = st.file_uploader("Wgraj zdjęcie do analizy", type=["jpg", "png", "jpeg"])
faq_question = st.text_input("Zadaj pytanie (np. z FAQ)")

if uploaded_file:
    st.image(uploaded_file, use_container_width=True)

    # Symulowana analiza obrazu
    vision_tags = ["dog", "grass", "sunny", "outdoor"]
    vision_description = "A dog sitting on grass on a sunny day."

    prompt = f'''
    Na podstawie tego opisu: "{vision_description}" oraz tagów {vision_tags},
    wygeneruj ładny opis zdjęcia i zaproponuj 5 tagów (hashtagów).
    '''

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem AI."},
            {"role": "user", "content": prompt}
        ]
    )

    st.subheader("Wygenerowany opis i tagi:")
    st.write(response.choices[0].message.content)

if faq_question:
    with open("faq.json", "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    found = next((item["answer"] for item in faq_data if faq_question.lower() in item["question"].lower()), None)
    
    if found:
        st.subheader("Odpowiedź z FAQ:")
        st.write(found)
    else:
        fallback_prompt = f"Użytkownik zapytał: {faq_question}. Odpowiedz zgodnie z treścią FAQ."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Odpowiadasz na pytania na podstawie FAQ."},
                {"role": "user", "content": fallback_prompt}
            ]
        )
        st.subheader("Odpowiedź z modelu:")
        st.write(response.choices[0].message.content)