import streamlit as st
from googletrans import Translator, LANGUAGES
import time
import hashlib

# Page configuration
st.set_page_config(
    page_title="Google Translate",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Password configuration - CHANGE THESE!
VALID_USERS = {
    "admin": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
    "user1": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # "secret123"
    "team": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4",   # "hello"
}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    .translation-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username: str, password: str) -> bool:
    """Check if username and password are valid"""
    if username in VALID_USERS:
        return VALID_USERS[username] == hash_password(password)
    return False

def login_form():
    """Display login form"""
    st.markdown('<h1 class="main-header">🔐 Login Required</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.markdown("### Please enter your credentials:")
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            login_button = st.button("🔑 Login", type="primary", use_container_width=True)
        
        if login_button:
            if username and password:
                if check_credentials(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.warning("⚠️ Please enter both username and password")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demo credentials info (remove in production!)
        st.markdown("---")
        st.markdown("**Demo Credentials (remove this section in production!):**")
        st.code("""
Username: admin    | Password: password
Username: user1    | Password: secret123  
Username: team     | Password: hello
        """)

def logout_button():
    """Display logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"👤 Logged in as: **{st.session_state.username}**")
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'translator' not in st.session_state:
    st.session_state.translator = Translator()

# Authentication check
if not st.session_state.authenticated:
    login_form()
    st.stop()

# Add logout button to sidebar
logout_button()

def translate_text(text: str, src_lang: str, dest_lang: str) -> tuple:
    """Translate text using Google Translate"""
    try:
        translator = st.session_state.translator
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text, result.src
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return "", ""

def main():
    # Header
    st.markdown('<h1 class="main-header">🌐 Google Translate</h1>', unsafe_allow_html=True)
    st.markdown("**Powered by Google Translate API - Protected Access**")
    
    # Language selection
    st.subheader("🔤 Select Languages")
    
    # Get language options
    lang_options = list(LANGUAGES.items())
    lang_dict = dict(LANGUAGES)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**From Language:**")
        source_langs = [('auto', 'Auto-detect')] + [(code, name.title()) for code, name in lang_options]
        source_options = [f"{name} ({code})" for code, name in source_langs]
        
        selected_src_idx = st.selectbox(
            "Source language:",
            range(len(source_options)),
            format_func=lambda x: source_options[x],
            key="src_lang",
            index=0  # Default to auto-detect
        )
        selected_src_code = source_langs[selected_src_idx][0]
    
    with col2:
        st.markdown("**To Language:**")
        target_langs = [(code, name.title()) for code, name in lang_options]
        target_options = [f"{name} ({code})" for code, name in target_langs]
        
        # Default to English
        default_target = next((i for i, (code, name) in enumerate(target_langs) if code == 'en'), 0)
        
        selected_dest_idx = st.selectbox(
            "Target language:",
            range(len(target_options)),
            format_func=lambda x: target_options[x],
            key="dest_lang",
            index=default_target
        )
        selected_dest_code = target_langs[selected_dest_idx][0]
    
    # Translation interface
    st.subheader("✍️ Translation")
    
    # Input text
    input_text = st.text_area(
        "Enter text to translate:",
        height=150,
        placeholder="Type your text here...",
        key="input_text"
    )
    
    # Translation controls
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        translate_button = st.button("🚀 Translate", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.input_text = ""
        st.rerun()
    
    # Perform translation
    if translate_button and input_text.strip():
        with st.spinner("Translating..."):
            translated_text, detected_lang = translate_text(input_text, selected_src_code, selected_dest_code)
            
            if translated_text:
                # Display translation
                st.subheader("📝 Translation Result")
                
                # Show detected language if auto-detect was used
                if selected_src_code == 'auto' and detected_lang:
                    detected_name = lang_dict.get(detected_lang, detected_lang).title()
                    st.info(f"🔍 Detected language: **{detected_name}** ({detected_lang})")
                
                st.markdown(f'<div class="translation-box"><h4>🎯 {target_langs[selected_dest_idx][1]}:</h4><p style="font-size: 1.1em; line-height: 1.5;">{translated_text}</p></div>', unsafe_allow_html=True)
                
                # Add to history
                translation_record = {
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'from_lang': detected_name if selected_src_code == 'auto' else source_langs[selected_src_idx][1],
                    'to_lang': target_langs[selected_dest_idx][1],
                    'original': input_text,
                    'translated': translated_text
                }
                st.session_state.translation_history.insert(0, translation_record)
                
                # Keep only last 10 translations
                st.session_state.translation_history = st.session_state.translation_history[:10]
                
                # Copy button
                st.code(translated_text, language=None)
    
    elif translate_button and not input_text.strip():
        st.error("Please enter some text to translate.")
    
    # Translation history
    if st.session_state.translation_history:
        st.subheader("📚 Recent Translations")
        
        for i, record in enumerate(st.session_state.translation_history[:5]):
            with st.expander(f"{record['from_lang']} → {record['to_lang']} ({record['timestamp']})"):
                st.markdown(f"**Original ({record['from_lang']}):**")
                st.write(record['original'])
                st.markdown(f"**Translation ({record['to_lang']}):**")
                st.write(record['translated'])
    
    # Sidebar info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("**Google Translate Integration**")
        st.markdown("- 100+ languages supported")
        st.markdown("- Auto-language detection")
        st.markdown("- Real-time translation")
        st.markdown("- Translation history")
        
        st.markdown("---")
        st.markdown("**Usage:**")
        st.markdown("1. Select source and target languages")
        st.markdown("2. Enter your text")
        st.markdown("3. Click Translate")
        st.markdown("4. Copy the result")
    
    # Footer
    st.markdown("---")
    st.markdown("**Powered by Google Translate API**")

if __name__ == "__main__":
    main()
