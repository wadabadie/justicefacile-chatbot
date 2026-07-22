import streamlit as st
import google.generativeai as genai

# Configuration page
st.set_page_config(
    page_title="JusticeFacile — Assistant Juridique IA",
    layout="centered"
)

# Style CSS
st.markdown("""
<style>
    .main { background-color: #FDFAF3; }
    .stChatMessage { border-radius: 12px; }
    h1 { color: #1A2E4A; font-family: Georgia, serif; }
    .subtitle { color: #C9920A; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("# JusticeFacile")
st.markdown('<p class="subtitle">Assistant Juridique IA — Contexte Camerounais</p>',
            unsafe_allow_html=True)
st.markdown("---")

# Configuration Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

# Prompt système
SYSTEM_PROMPT = """Tu es JusticeFacile-IA, l'assistant juridique intelligent de la plateforme 
JusticeFacile, spécialisé dans le droit camerounais. Tu aides les citoyens camerounais 
à comprendre leurs droits, à naviguer dans les procédures juridiques, et tu offres un 
soutien spécial aux victimes de violences basées sur le genre (VBG).

Règles importantes :
- Tu réponds toujours en français (ou dans la langue de l'utilisateur)
- Tu bases tes réponses sur le droit camerounais (Code pénal 2016/007, Code civil, 
  Code du travail 92/007, lois sur les VBG)
- Tu es empathique, clair et accessible pour tout niveau d'éducation
- Pour les urgences VBG, tu rappelles toujours le numéro d'urgence et les ressources disponibles
- Tu précises toujours que tu es un assistant de premier niveau et que 
  pour les cas complexes, un juriste certifié doit être consulté
- Tu ne donnes jamais de conseils médicaux
- Si quelqu'un est en danger immédiat, tu lui demandes d'appeler le 117 (Police) 
  ou le 116 (numéro vert VBG au Cameroun)"""

# Initialisation historique
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Affichage historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Message de bienvenue
if not st.session_state.messages:
    with st.chat_message("assistant"):
        welcome = """Bonjour ! Je suis **Justicefacile-IA**, votre assistant juridique intelligent.

Je peux vous aider avec :
-  Vos droits en cas de licenciement, litige foncier, conflit civil
-  Soutien et orientation pour les victimes de violences (VBG)
-  Explication des lois camerounaises en langage simple
-  Orientation vers les démarches juridiques appropriées

**Comment puis-je vous aider aujourd'hui ?**"""
        st.markdown(welcome)
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome
    })

# Input utilisateur
if prompt := st.chat_input("Posez votre question juridique..."):
    # Afficher message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Générer réponse Gemini
    with st.chat_message("assistant"):
        with st.spinner("JusticeFacile-IA analyse votre question..."):
            full_prompt = f"{SYSTEM_PROMPT}\n\nQuestion : {prompt}"
            response = st.session_state.chat.send_message(full_prompt)
            st.markdown(response.text)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.text
    })

# Sidebar
with st.sidebar:
    st.markdown("###  JusticeFacile")
    st.markdown("**Assistant Juridique IA**")
    st.markdown("---")
    st.markdown(" Spécialisé droit camerounais")
    st.markdown(" Soutien victimes VBG")
    st.markdown(" Base légale mise à jour")
    st.markdown("---")
    st.markdown("** Urgences :**")
    st.markdown("Police : **117**")
    st.markdown("VBG : **116**")
    st.markdown("SAMU : **115**")
    st.markdown("---")
    if st.button(" Effacer la conversation"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()
    st.markdown("---")
    st.markdown("*Juris-IA est un assistant de premier niveau. "
                "Pour les cas complexes, consultez un juriste certifié.*")