import streamlit as st
import requests
import json

st.set_page_config(
    page_title="JusticeFacile — Assistant Juridique IA",
    layout="centered"
)

st.markdown("""
<style>
    .main { background-color: #FDFAF3; }
    h1 { color: #1A2E4A; font-family: Georgia, serif; }
    .subtitle { color: #C9920A; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚖️ JusticeFacile")
st.markdown('<p class="subtitle">Assistant Juridique IA — Contexte Camerounais</p>',
            unsafe_allow_html=True)
st.markdown("---")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """Tu es JusticeFacile-IA, l'assistant juridique intelligent de la plateforme 
JusticeFacile, spécialisé dans le droit camerounais. Tu aides les citoyens camerounais 
à comprendre leurs droits et tu offres un soutien spécial aux victimes de VBG.

Règles :
- Réponds toujours en français sauf si l'utilisateur parle anglais
- Bases tes réponses sur le droit camerounais (Code pénal 2016/007, Code civil, Code du travail 92/007)
- Sois empathique, clair et accessible pour tout niveau d'éducation
- Pour les urgences VBG rappelle le 117 (Police) et le 116 (VBG Cameroun)
- Précise que tu es un assistant de premier niveau et qu'un juriste certifié doit être consulté
- Ne donne jamais de conseils médicaux"""

BIENVENUE = """Bonjour ! Je suis **JusticeFacile-IA**, votre assistant juridique.

Je peux vous aider avec :
- ⚖️ Vos droits en cas de licenciement, litige foncier, conflit civil
-  Soutien et orientation pour les victimes de violences (VBG)
-  Explication des lois camerounaises en langage simple

**Comment puis-je vous aider aujourd'hui ?**"""

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.chat_message("assistant"):
    st.markdown(BIENVENUE)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Posez votre question juridique..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("JusticeFacile-IA analyse votre question..."):

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            messages_api = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages_api += st.session_state.messages

            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": messages_api,
                "max_tokens": 1024,
                "temperature": 0.7
            }

            try:
                response = requests.post(
                    GROQ_URL,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                reponse_text = data["choices"][0]["message"]["content"]
                st.markdown(reponse_text)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reponse_text
                })

            except requests.exceptions.Timeout:
                st.error("La réponse prend trop de temps. Réessayez.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion : {str(e)}")
            except Exception as e:
                st.error(f"Erreur : {str(e)}")

with st.sidebar:
    st.markdown("### ⚖️ JusticeFacile")
    st.markdown("**Assistant Juridique IA**")
    st.markdown("---")
    st.markdown("🇨🇲 Spécialisé droit camerounais")
    st.markdown("🛡️ Soutien victimes VBG")
    st.markdown("---")
    st.markdown("**🚨 Urgences :**")
    st.markdown("Police : **117**")
    st.markdown("VBG : **116**")
    st.markdown("SAMU : **115**")
    st.markdown("---")
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("*Pour les cas complexes, consultez un juriste certifié.*")