import streamlit as st
import os
import json
import time
from datetime import datetime
from typing import List, Dict
from rag_system import RAGSystem
import pandas as pd
from config import validate_environment, get_environment_config

# Configuración de la página
st.set_page_config(
    page_title="Sistema RAG Inteligente",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para una interfaz moderna
st.markdown("""
<style>
    /* Variables CSS para temas */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #4CAF50;
        --error-color: #f44336;
        --warning-color: #ff9800;
        --bg-color: #ffffff;
        --surface-color: #f8f9fa;
        --text-color: #333333;
        --border-color: #e0e0e0;
    }
    
    [data-theme="dark"] {
        --primary-color: #4a5568;
        --secondary-color: #2d3748;
        --accent-color: #68d391;
        --error-color: #fc8181;
        --warning-color: #f6ad55;
        --bg-color: #1a202c;
        --surface-color: #2d3748;
        --text-color: #e2e8f0;
        --border-color: #4a5568;
    }
    
    .main-header {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease;
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
    }
    
    .user-message {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        margin-left: 2rem;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .bot-message {
        background: rgba(248, 249, 250, 0.95);
        border-left: 4px solid var(--primary-color);
        margin-right: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .document-card {
        border: 2px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: var(--surface-color);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .document-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    .status-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    
    .success-card {
        background: rgba(212, 237, 218, 0.9);
        border-color: var(--accent-color);
        color: #155724;
    }
    
    .error-card {
        background: rgba(248, 215, 218, 0.9);
        border-color: var(--error-color);
        color: #721c24;
    }
    
    .warning-card {
        background: rgba(255, 243, 205, 0.9);
        border-color: var(--warning-color);
        color: #856404;
    }
    
    .info-card {
        background: rgba(209, 236, 241, 0.9);
        border-color: #17a2b8;
        color: #0c5460;
    }
    
    .glassmorphism {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 15px;
    }
    
    .floating-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .floating-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .theme-toggle {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .loading-spinner {
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 3px solid white;
        width: 20px;
        height: 20px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Mejoras para dispositivos móviles */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 0.5rem;
            margin-bottom: 1rem;
        }
        
        .chat-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            padding: 1rem;
        }
        
        .user-message {
            margin-left: 0;
        }
        
        .bot-message {
            margin-right: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Inicializar variables de sesión PRIMERO
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processed_documents' not in st.session_state:
    st.session_state.processed_documents = []
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'total_docs' not in st.session_state:
    st.session_state.total_docs = 0
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'rag_system_ready' not in st.session_state:
    st.session_state.rag_system_ready = False

# Validar configuración del entorno
env_valid, env_errors = validate_environment()
if not env_valid:
    st.error("⚠️ **Configuración incompleta:**")
    for error in env_errors:
        st.error(f"• {error}")
    st.info("💡 **Solución:** Configura tu API key de Google en el archivo .env")
    st.code("GOOGLE_API_KEY=tu_api_key_aqui", language="bash")
    st.stop()
# Inicializar RAGSystem con manejo de errores mejorado
@st.cache_resource
def create_rag_system():
    """Crea una instancia del sistema RAG (sin modificar session_state)"""
    try:
        return RAGSystem()
    except Exception as e:
        st.error(f"❌ Error inicializando el sistema RAG: {str(e)}")
        return None

def get_rag_system():
    """Obtiene el sistema RAG y actualiza el estado"""
    rag = create_rag_system()
    if rag:
        st.session_state.rag_system_ready = True
        return rag
    else:
        st.session_state.rag_system_ready = False
        return None

# Intentar inicializar el sistema RAG al inicio (con manejo seguro)
try:
    if not st.session_state.rag_system_ready:
        test_rag = create_rag_system()
        if test_rag:
            st.session_state.rag_system_ready = True
        else:
            st.session_state.rag_system_ready = False
except Exception as e:
    st.session_state.rag_system_ready = False
    st.error(f"Error al inicializar el sistema: {str(e)}")

# Header principal con indicador de estado
status_indicator = "🟢" if st.session_state.rag_system_ready else "🔴"
status_text = "Sistema Listo" if st.session_state.rag_system_ready else "Sistema No Disponible"

st.markdown(f"""
<div class="main-header">
    <h1>🧠 Sistema RAG Inteligente</h1>
    <p>Pregunta sobre tus documentos con IA avanzada</p>
    <div style="position: absolute; top: 1rem; left: 1rem; background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
        {status_indicator} {status_text}
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Panel de Control")
    
    # Métricas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📁 {st.session_state.total_docs}</h3>
            <p>Documentos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>❓ {st.session_state.total_questions}</h3>
            <p>Preguntas</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Estado del sistema
    system_status = "Activo 🟢" if st.session_state.rag_system_ready else "Inactivo 🔴"
    st.markdown(f"""
    <div class="info-card status-card">
        <strong>🔍 Estado del Sistema:</strong> {system_status}
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Gestión de documentos
    st.subheader("📁 Gestión de Documentos")
    
    # Cargar documentos
    uploaded_files = st.file_uploader(
        "Subir documentos",
        type=["txt", "pdf", "md"],
        accept_multiple_files=True,
        help="Formatos soportados: TXT, PDF, MD"
    )
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} archivo(s) seleccionado(s):**")
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({file.size} bytes)")
        
        if st.button("🔄 Procesar Documentos", type="primary", use_container_width=True):
            if not st.session_state.rag_system_ready:
                st.error("❌ Sistema RAG no está disponible. Revisa la configuración.")
            else:
                with st.spinner("🔄 Procesando documentos..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        rag = get_rag_system()
                        if not rag:
                            st.error("❌ Error: No se pudo inicializar el sistema RAG")
                        else:
                            temp_dir = "./temp_docs"
                            os.makedirs(temp_dir, exist_ok=True)
                            file_paths = []
                            
                            # Guardar archivos
                            status_text.text("📋 Guardando archivos...")
                            progress_bar.progress(20)
                            
                            for uploaded_file in uploaded_files:
                                file_path = os.path.join(temp_dir, uploaded_file.name)
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                file_paths.append(file_path)
                            
                            # Cargar documentos
                            status_text.text("📄 Cargando documentos...")
                            progress_bar.progress(50)
                            
                            documents = rag.load_documents(file_paths)
                            if documents:
                                # Procesar documentos
                                status_text.text("⚙️ Procesando y creando embeddings...")
                                progress_bar.progress(80)
                                
                                if rag.process_documents(documents):
                                    st.session_state.processed_documents.extend([f.name for f in uploaded_files])
                                    st.session_state.total_docs = len(st.session_state.processed_documents)
                                    
                                    progress_bar.progress(100)
                                    status_text.text("✅ ¡Completado!")
                                    
                                    st.markdown("""
                                    <div class="success-card status-card">
                                        <strong>✅ ¡Documentos procesados exitosamente!</strong><br>
                                        Ya puedes hacer preguntas sobre el contenido.
                                    </div>
                                    """, unsafe_allow_html=True)
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.markdown("""
                                    <div class="error-card status-card">
                                        <strong>❌ Error procesando documentos</strong><br>
                                        Verifica que los archivos sean válidos.
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="warning-card status-card">
                                    <strong>⚠️ No se pudieron cargar los documentos</strong><br>
                                    Verifica el formato de los archivos.
                                </div>
                                """, unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.markdown(f"""
                        <div class="error-card status-card">
                            <strong>❌ Error inesperado:</strong><br>
                            {str(e)}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    finally:
                        progress_bar.empty()
                        status_text.empty()
    
    # Cargar BD existente
    if st.button("📂 Cargar BD Existente", use_container_width=True):
        if not st.session_state.rag_system_ready:
            st.error("❌ Sistema RAG no disponible")
        else:
            with st.spinner("🔍 Cargando base de datos..."):
                try:
                    rag = get_rag_system()
                    if rag and rag.load_existing_vectorstore():
                        # Obtener estadísticas de la BD
                        stats = rag.get_database_stats()
                        
                        st.markdown("""
                        <div class="success-card status-card">
                            <strong>✅ Base de datos cargada exitosamente</strong><br>
                            Sistema listo para responder preguntas.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Mostrar estadísticas
                        with st.expander("📊 Ver estadísticas de la BD"):
                            st.json(stats)
                    else:
                        st.markdown("""
                        <div class="warning-card status-card">
                            <strong>⚠️ No se encontró base de datos existente</strong><br>
                            Procesa algunos documentos primero.
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-card status-card">
                        <strong>❌ Error cargando base de datos:</strong><br>
                        {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Documentos procesados
    if st.session_state.processed_documents:
        st.subheader("📚 Documentos Cargados")
        for i, doc in enumerate(st.session_state.processed_documents):
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📄 {doc}")
                with col2:
                    if st.button("🗑️", key=f"del_{i}", help="Eliminar"):
                        st.session_state.processed_documents.pop(i)
                        st.session_state.total_docs = len(st.session_state.processed_documents)
                        st.rerun()
    
    st.divider()
    
    # Exportar historial
    if st.session_state.chat_history:
        if st.button("📤 Exportar Chat", use_container_width=True):
            chat_data = {
                "timestamp": datetime.now().isoformat(),
                "chat_history": st.session_state.chat_history
            }
            st.download_button(
                label="💾 Descargar JSON",
                data=json.dumps(chat_data, indent=2, ensure_ascii=False),
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Limpiar historial
    if st.button("🗑️ Limpiar Historial", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.total_questions = 0
        st.rerun()

# Área principal - Chat
st.header("💬 Chat con tus Documentos")

# Mostrar historial de chat
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        # Pregunta del usuario
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 Tú:</strong><br>
            {chat['question']}
            <small style="opacity: 0.7; display: block; margin-top: 0.5rem;">
                {chat['timestamp']}
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        # Respuesta del bot
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Asistente:</strong><br>
            {chat['answer']}
        </div>
        """, unsafe_allow_html=True)
        
        # Fuentes si existen
        if chat.get('sources'):
            with st.expander("📚 Ver fuentes"):
                for i, source in enumerate(chat['sources'], 1):
                    st.markdown(f"**Fuente {i}:** {source}")

# Input para nueva pregunta
question = st.text_input(
    "💭 Escribe tu pregunta aquí:",
    placeholder="¿Qué quieres saber sobre tus documentos?",
    key="question_input"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ask_button = st.button("🚀 Obtener Respuesta", type="primary", use_container_width=True)

if ask_button and question:
    if not st.session_state.rag_system_ready:
        st.markdown("""
        <div class="error-card status-card">
            <strong>❌ Sistema no disponible</strong><br>
            Revisa la configuración de la API key.
        </div>
        """, unsafe_allow_html=True)
    else:
        try:
            rag = get_rag_system()
            
            if not rag or rag.vectorstore is None:
                st.markdown("""
                <div class="warning-card status-card">
                    <strong>⚠️ Base de datos vacía</strong><br>
                    Primero procesa algunos documentos o carga una BD existente.
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("🤔 Analizando tu pregunta..."):
                    # Configurar cadena QA
                    if rag.setup_qa_chain():
                        # Mostrar indicador de procesamiento
                        processing_container = st.empty()
                        processing_container.markdown("""
                        <div class="info-card status-card">
                            <div class="loading-spinner"></div>
                            <strong>🔍 Buscando en tus documentos...</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        response = rag.ask_question(question)
                        processing_container.empty()
                        
                        if response.get('error'):
                            st.markdown(f"""
                            <div class="error-card status-card">
                                <strong>❌ Error procesando pregunta:</strong><br>
                                {response['answer']}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Agregar al historial
                            chat_entry = {
                                'question': question,
                                'answer': response["answer"],
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'sources': [doc.metadata.get('source', 'Desconocido') for doc in response["source_documents"]],
                                'confidence': len(response["source_documents"])
                            }
                            
                            st.session_state.chat_history.append(chat_entry)
                            st.session_state.total_questions += 1
                            
                            # Mostrar respuesta inmediata
                            st.markdown("""
                            <div class="success-card status-card">
                                <strong>✅ Respuesta generada exitosamente</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Limpiar input y actualizar
                            time.sleep(0.5)
                            st.rerun()
                    else:
                        st.markdown("""
                        <div class="error-card status-card">
                            <strong>❌ Error configurando el sistema</strong><br>
                            Intenta recargar la aplicación.
                        </div>
                        """, unsafe_allow_html=True)
                        
        except Exception as e:
            st.markdown(f"""
            <div class="error-card status-card">
                <strong>❌ Error inesperado:</strong><br>
                {str(e)}
            </div>
            """, unsafe_allow_html=True)

# Footer mejorado
st.divider()
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 2rem;">
    <div style="margin-bottom: 1rem;">
        <span style="font-size: 1.5rem;">🧠</span>
        <strong style="color: #333; margin-left: 0.5rem;">Sistema RAG Inteligente</strong>
    </div>
    <div style="color: #666; font-size: 0.9rem; line-height: 1.5;">
        🚀 Powered by <strong>Gemini AI</strong> & <strong>LangChain</strong><br>
        📚 Análisis inteligente de documentos con IA
    </div>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #dee2e6; color: #999; font-size: 0.8rem;">
        © 2024 | Desarrollado con ❤️ y tecnología de vanguardia
    </div>
</div>
""", unsafe_allow_html=True)

# Botón flotante para scroll hacia arriba
st.markdown("""
<div class="floating-button" onclick="window.scrollTo({top: 0, behavior: 'smooth'});" title="Volver arriba">
    ↑
</div>
""", unsafe_allow_html=True)
