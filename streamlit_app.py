import streamlit as st
from translatepy import Translator
import time
import hashlib

# Page configuration
st.set_page_config(
    page_title="Secure Translator",
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
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 10px 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
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
    st.markdown('<h1 class="main-header">🔐 Secure Translator Login</h1>', unsafe_allow_html=True)
    
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
        st.markdown("**Demo Credentials:**")
        st.code("""
Username: admin    | Password: password
Username: user1    | Password: secret123  
Username: team     | Password: hello
        """)
        st.markdown("**(Remove this section in production!)**")

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

# Language options
LANGUAGES = {
    'auto': 'Auto Detect',
    'en': 'English',
    'es': 'Spanish', 
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'pl': 'Polish',
    'cs': 'Czech',
    'sk': 'Slovak',
    'hu': 'Hungarian',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'he': 'Hebrew',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'id': 'Indonesian',
    'ms': 'Malay',
    'fa': 'Persian',
    'ur': 'Urdu',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'gu': 'Gujarati',
    'pa': 'Punjabi',
    'ne': 'Nepali',
    'si': 'Sinhala',
    'my': 'Myanmar',
    'km': 'Khmer',
    'lo': 'Lao',
    'ka': 'Georgian',
    'am': 'Amharic',
    'sw': 'Swahili',
    'zu': 'Zulu',
    'af': 'Afrikaans',
    'is': 'Icelandic',
    'mt': 'Maltese',
    'cy': 'Welsh',
    'ga': 'Irish',
    'eu': 'Basque',
    'ca': 'Catalan',
    'gl': 'Galician',
    'eo': 'Esperanto'
}

def translate_text(text: str, src_lang: str, dest_lang: str) -> tuple:
    """Translate text using translatepy"""
    try:
        translator = st.session_state.translator
        
        if src_lang == 'auto':
            # Auto-detect source language
            result = translator.translate(text, dest_lang)
            detected = translator.language(text)
            return result.result, detected.result
        else:
            result = translator.translate(text, dest_lang, src_lang)
            return result.result, src_lang
            
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return "", ""

def translate_file_content(content: str, src_lang: str, dest_lang: str) -> str:
    """Translate the content of a file"""
    try:
        translator = st.session_state.translator
        
        # Split content into smaller chunks to avoid API limits
        chunks = [content[i:i+5000] for i in range(0, len(content), 5000)]
        translated_chunks = []
        
        for chunk in chunks:
            if chunk.strip():  # Only translate non-empty chunks
                if src_lang == 'auto':
                    result = translator.translate(chunk, dest_lang)
                else:
                    result = translator.translate(chunk, dest_lang, src_lang)
                translated_chunks.append(result.result)
            else:
                translated_chunks.append(chunk)  # Keep empty chunks as is
        
        return '\n'.join(translated_chunks)
        
    except Exception as e:
        st.error(f"Error translating file content: {str(e)}")
        return content  # Return original content if translation fails

def main():
    # Header
    st.markdown('<h1 class="main-header">🌐 Secure File Translator</h1>', unsafe_allow_html=True)
    st.markdown("**Multi-language translation with secure access control**")
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["📄 File Translation", "✍️ Text Translation"])
    
    with tab1:
        st.subheader("📁 Batch File Translation")
        
        # Language selection for files
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**From Language:**")
            source_options = list(LANGUAGES.keys())
            source_labels = [f"{LANGUAGES[code]} ({code})" for code in source_options]
            
            selected_src_idx_file = st.selectbox(
                "Source language:",
                range(len(source_options)),
                format_func=lambda x: source_labels[x],
                key="src_lang_file",
                index=0  # Default to auto-detect
            )
            selected_src_code_file = source_options[selected_src_idx_file]
        
        with col2:
            st.markdown("**To Language:**")
            target_options = [code for code in LANGUAGES.keys() if code != 'auto']
            target_labels = [f"{LANGUAGES[code]} ({code})" for code in target_options]
            
            # Default to English
            default_target = target_options.index('en') if 'en' in target_options else 0
            
            selected_dest_idx_file = st.selectbox(
                "Target language:",
                range(len(target_options)),
                format_func=lambda x: target_labels[x],
                key="dest_lang_file",
                index=default_target
            )
            selected_dest_code_file = target_options[selected_dest_idx_file]
        
        # File upload
        st.markdown("### 📎 Upload Files")
        uploaded_files = st.file_uploader(
            "Choose text files to translate",
            type=['txt', 'md', 'csv', 'py', 'js', 'html', 'xml', 'json'],
            accept_multiple_files=True,
            help="You can upload multiple files at once. Supported formats: .txt, .md, .csv, .py, .js, .html, .xml, .json"
        )
        
        if uploaded_files:
            st.success(f"📁 {len(uploaded_files)} file(s) uploaded successfully!")
            
            # Display file list
            with st.expander("📋 Uploaded Files", expanded=True):
                for file in uploaded_files:
                    file_size = len(file.getvalue()) / 1024  # Size in KB
                    st.markdown(f"• **{file.name}** ({file_size:.1f} KB)")
            
            # Translation button for files
            if st.button("🚀 Translate All Files", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                translated_files = []
                
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"Translating {uploaded_file.name}...")
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    
                    try:
                        # Read file content
                        if uploaded_file.type == "text/plain" or uploaded_file.name.endswith(('.txt', '.md', '.py', '.js', '.html', '.xml', '.json', '.csv')):
                            content = uploaded_file.getvalue().decode('utf-8')
                        else:
                            content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
                        
                        # Translate content
                        translated_content = translate_file_content(content, selected_src_code_file, selected_dest_code_file)
                        
                        # Create new filename
                        name_parts = uploaded_file.name.rsplit('.', 1)
                        if len(name_parts) == 2:
                            new_filename = f"{name_parts[0]}_translated_{selected_dest_code_file}.{name_parts[1]}"
                        else:
                            new_filename = f"{uploaded_file.name}_translated_{selected_dest_code_file}.txt"
                        
                        translated_files.append({
                            'original_name': uploaded_file.name,
                            'translated_name': new_filename,
                            'content': translated_content,
                            'original_content': content
                        })
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                status_text.text("✅ Translation completed!")
                
                # Display results
                if translated_files:
                    st.subheader("📥 Download Translated Files")
                    
                    # Create download buttons for each file
                    for file_info in translated_files:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.markdown(f"**{file_info['translated_name']}**")
                        
                        with col2:
                            st.download_button(
                                label="📥 Download",
                                data=file_info['content'],
                                file_name=file_info['translated_name'],
                                mime='text/plain',
                                key=f"download_{file_info['translated_name']}"
                            )
                        
                        with col3:
                            if st.button("👁️ Preview", key=f"preview_{file_info['translated_name']}"):
                                st.session_state[f"show_preview_{file_info['translated_name']}"] = True
                        
                        # Show preview if requested
                        if st.session_state.get(f"show_preview_{file_info['translated_name']}", False):
                            with st.expander(f"Preview: {file_info['translated_name']}", expanded=True):
                                col_orig, col_trans = st.columns(2)
                                
                                with col_orig:
                                    st.markdown("**Original:**")
                                    st.text_area(
                                        "Original content",
                                        value=file_info['original_content'][:1000] + ("..." if len(file_info['original_content']) > 1000 else ""),
                                        height=200,
                                        key=f"orig_{file_info['translated_name']}",
                                        disabled=True
                                    )
                                
                                with col_trans:
                                    st.markdown("**Translated:**")
                                    st.text_area(
                                        "Translated content",
                                        value=file_info['content'][:1000] + ("..." if len(file_info['content']) > 1000 else ""),
                                        height=200,
                                        key=f"trans_{file_info['translated_name']}",
                                        disabled=True
                                    )
                    
                    # Add to history
                    batch_record = {
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'type': 'batch_files',
                        'from_lang': LANGUAGES[selected_src_code_file],
                        'to_lang': LANGUAGES[selected_dest_code_file],
                        'file_count': len(translated_files),
                        'files': [f['original_name'] for f in translated_files],
                        'user': st.session_state.username
                    }
                    st.session_state.translation_history.insert(0, batch_record)
                    st.session_state.translation_history = st.session_state.translation_history[:20]
    
    with tab2:
        # Language selection for text
        st.subheader("🔤 Select Languages")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**From Language:**")
            source_options = list(LANGUAGES.keys())
            source_labels = [f"{LANGUAGES[code]} ({code})" for code in source_options]
            
            selected_src_idx = st.selectbox(
                "Source language:",
                range(len(source_options)),
                format_func=lambda x: source_labels[x],
                key="src_lang_text",
                index=0  # Default to auto-detect
            )
            selected_src_code = source_options[selected_src_idx]
        
        with col2:
            st.markdown("**To Language:**")
            target_options = [code for code in LANGUAGES.keys() if code != 'auto']
            target_labels = [f"{LANGUAGES[code]} ({code})" for code in target_options]
            
            # Default to English
            default_target = target_options.index('en') if 'en' in target_options else 0
            
            selected_dest_idx = st.selectbox(
                "Target language:",
                range(len(target_options)),
                format_func=lambda x: target_labels[x],
                key="dest_lang_text",
                index=default_target
            )
            selected_dest_code = target_options[selected_dest_idx]
        
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
                        detected_name = LANGUAGES.get(detected_lang, detected_lang)
                        st.info(f"🔍 Detected language: **{detected_name}** ({detected_lang})")
                    
                    st.markdown(f'<div class="translation-box"><h4>🎯 {LANGUAGES[selected_dest_code]}:</h4><p style="font-size: 1.1em; line-height: 1.5;">{translated_text}</p></div>', unsafe_allow_html=True)
                    
                    # Download as file option
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.download_button(
                            label="📥 Download as .txt",
                            data=translated_text,
                            file_name=f"translated_text_{selected_dest_code}.txt",
                            mime='text/plain'
                        )
                    
                    # Add to history
                    from_lang_name = LANGUAGES.get(detected_lang, detected_lang) if selected_src_code == 'auto' else LANGUAGES[selected_src_code]
                    translation_record = {
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'type': 'text',
                        'from_lang': from_lang_name,
                        'to_lang': LANGUAGES[selected_dest_code],
                        'original': input_text,
                        'translated': translated_text,
                        'user': st.session_state.username
                    }
                    st.session_state.translation_history.insert(0, translation_record)
                    
                    # Keep only last 20 translations
                    st.session_state.translation_history = st.session_state.translation_history[:20]
                    
                    # Copy button
                    st.code(translated_text, language=None)
                    
                    # Success message
                    st.markdown('<div class="success-message">✅ Translation completed successfully!</div>', unsafe_allow_html=True)
        
        elif translate_button and not input_text.strip():
            st.markdown('<div class="error-message">❌ Please enter some text to translate.</div>', unsafe_allow_html=True)
    
    # Translation history
    if st.session_state.translation_history:
        st.subheader("📚 Recent Activity")
        
        # Filter by current user or show all for admin
        user_history = st.session_state.translation_history
        if st.session_state.username != 'admin':
            user_history = [record for record in st.session_state.translation_history 
                          if record.get('user') == st.session_state.username]
        
        for i, record in enumerate(user_history[:5]):
            if record.get('type') == 'batch_files':
                with st.expander(f"📁 Batch: {record['file_count']} files | {record['from_lang']} → {record['to_lang']} ({record['timestamp']})"):
                    if st.session_state.username == 'admin':
                        st.markdown(f"**User:** {record.get('user', 'Unknown')}")
                    st.markdown(f"**Files translated:** {record['file_count']}")
                    st.markdown(f"**Languages:** {record['from_lang']} → {record['to_lang']}")
                    st.markdown("**Files:**")
                    for filename in record['files']:
                        st.markdown(f"• {filename}")
            else:
                with st.expander(f"✍️ Text: {record['from_lang']} → {record['to_lang']} ({record['timestamp']})"):
                    if st.session_state.username == 'admin':
                        st.markdown(f"**User:** {record.get('user', 'Unknown')}")
                    st.markdown(f"**Original ({record['from_lang']}):**")
                    st.write(record['original'])
                    st.markdown(f"**Translation ({record['to_lang']}):**")
                    st.write(record['translated'])
    
    # Sidebar info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("**Secure File Translation Service**")
        st.markdown("- 50+ languages supported")
        st.markdown("- Auto-language detection")
        st.markdown("- Batch file processing")
        st.markdown("- Individual file downloads")
        st.markdown("- Translation history")
        st.markdown("- User access control")
        
        st.markdown("---")
        st.markdown("**Supported File Types:**")
        st.markdown("• Text files (.txt)")
        st.markdown("• Markdown (.md)")
        st.markdown("• Code files (.py, .js, .html)")
        st.markdown("• Data files (.csv, .json, .xml)")
        
        st.markdown("---")
        st.markdown("**File Translation Process:**")
        st.markdown("1. Upload multiple files")
        st.markdown("2. Select languages")
        st.markdown("3. Click 'Translate All Files'")
        st.markdown("4. Download translated files")
        
        st.markdown("---")
        st.markdown("**Security Features:**")
        st.markdown("- Password protected access")
        st.markdown("- User session tracking")
        st.markdown("- Secure file processing")
        st.markdown("- Activity logging")
    
    # Footer
    st.markdown("---")
    st.markdown("**Powered by TranslatePy | Secure File Translation Service**")

if __name__ == "__main__":
    main()
