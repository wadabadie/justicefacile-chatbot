import streamlit as st
from google import genai

# Configuration page
st.set_page_config(
    page_title="JusticeFacile — Assistant Juridique IA",
    layout="centered"
)

# Style CSS
st.markdown("""
<style>
    .main { background-color: #FDFAF3; }
    h1 { color: #1A2E4A; font-family: Georgia, serif; }
    .subtitle { color: #C9920A; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("#  JusticeFacile")
st.markdown('<p class="subtitle">Assistant Juridique IA — Contexte Camerounais</p>',
            unsafe_allow_html=True)
st.markdown("---")

# Configuration client Gemini
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Prompt système
SYSTEM_PROMPT = """Tu es JusticeFacile-IA, l'assistant juridique intelligent de la plateforme 
JusticeFacile, spécialisé dans le droit camerounais. Tu aides les citoyens camerounais 
à comprendre leurs droits et tu offres un soutien spécial aux victimes de VBG.

Règles :
- Réponds toujours en français
- Bases tes réponses sur le droit camerounais (Code pénal 2016/007, Code civil, Code du travail 92/007)
- Sois empathique, clair et accessible
- Pour les urgences VBG : rappelle le 117 (Police) et le 116 (VBG Cameroun)
- Précise que tu es un assistant de premier niveau et qu'un juriste certifié doit être consulté pour les cas complexes"""

# Initialisation historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Message de bienvenue
if not st.session_state.messages:
    with st.chat_message("assistant"):
        welcome = """Bonjour ! Je suis **JusticeFacile-IA**, votre assistant juridique.

Je peux vous aider avec :
-  Vos droits en cas de licenciement, litige foncier, conflit civil
-  Soutien et orientation pour les victimes de violences (VBG)
-  Explication des lois camerounaises en langage simple

**Comment puis-je vous aider aujourd'hui ?**"""
        st.markdown(welcome)
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome
    })

# Input utilisateur
if prompt := st.chat_input("Posez votre question juridique..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("JusticeFacile-IA analyse votre question..."):
            # Construire l'historique pour le contexte
            historique = ""
            for msg in st.session_state.messages[:-1]:
                role = "Utilisateur" if msg["role"] == "user" else "Assistant"
                historique += f"{role}: {msg['content']}\n"

            full_prompt = f"{SYSTEM_PROMPT}\n\n{historique}Utilisateur: {prompt}"

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt
            )
            reponse_text = response.text
            st.markdown(reponse_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reponse_text
    })

# Sidebar
with st.sidebar:
    st.markdown("###  JusticeFacile")
    st.markdown("**Assistant Juridique IA**")
    st.markdown("---")
    st.markdown(" Spécialisé droit camerounais")
    st.markdown(" Soutien victimes VBG")
    st.markdown("---")
    st.markdown("** Urgences :**")
    st.markdown("Police : **117**")
    st.markdown("VBG : **116**")
    st.markdown("SAMU : **115**")
    st.markdown("---")
    if st.button(" Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("*Pour les cas complexes, consultez un juriste certifié.*")