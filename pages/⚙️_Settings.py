import streamlit as st
import json
import os
from config import RAGConfig, AppConfig, get_environment_config, validate_environment
from rag_system import RAGSystem

st.set_page_config(
    page_title="Configuración - Sistema RAG",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Configuración del Sistema")

# Inicializar configuración si no existe
if 'rag_config' not in st.session_state:
    st.session_state.rag_config = RAGConfig()

# Tabs para diferentes secciones
tab1, tab2, tab3, tab4 = st.tabs(["🤖 Sistema RAG", "🎨 Interfaz", "📁 Archivos", "🔧 Avanzado"])

# Tab 1: Configuración del Sistema RAG
with tab1:
    st.header("Configuración del Sistema RAG")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Embeddings y Chunks")
        
        # Configuración de chunk size
        chunk_size = st.slider(
            "Tamaño de Chunk",
            min_value=200,
            max_value=2000,
            value=st.session_state.rag_config.chunk_size,
            step=100,
            help="Tamaño de los fragmentos de texto para procesamiento"
        )
        
        # Configuración de chunk overlap
        chunk_overlap = st.slider(
            "Superposición de Chunks",
            min_value=0,
            max_value=500,
            value=st.session_state.rag_config.chunk_overlap,
            step=50,
            help="Superposición entre chunks consecutivos"
        )
        
        # Modelo de embeddings
        embedding_model = st.selectbox(
            "Modelo de Embeddings",
            ["models/embedding-001"],
            index=0,
            help="Modelo para generar embeddings de texto"
        )
    
    with col2:
        st.subheader("🔍 Retrieval")
        
        # Número de documentos a recuperar
        k_docs = st.slider(
            "Documentos a Recuperar (k)",
            min_value=1,
            max_value=10,
            value=st.session_state.rag_config.k,
            help="Número de documentos similares a recuperar"
        )
        
        # Tipo de búsqueda
        search_type = st.selectbox(
            "Tipo de Búsqueda",
            ["similarity", "mmr"],
            index=0,
            help="Algoritmo de búsqueda de similitud"
        )
        
        # Umbral de puntuación
        score_threshold = st.slider(
            "Umbral de Puntuación",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.rag_config.score_threshold,
            step=0.1,
            help="Puntuación mínima para considerar un documento relevante"
        )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Modelo de Lenguaje")
        
        # Modelo LLM
        llm_model = st.selectbox(
            "Modelo LLM",
            ["gemini-1.5-pro", "gemini-1.5-flash"],
            index=0,
            help="Modelo de lenguaje para generar respuestas"
        )
        
        # Temperatura
        temperature = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.rag_config.temperature,
            step=0.1,
            help="Creatividad del modelo (0 = conservador, 1 = creativo)"
        )
    
    with col2:
        st.subheader("🎯 Tokens")
        
        # Máximo tokens
        max_tokens = st.slider(
            "Máximo Tokens",
            min_value=512,
            max_value=4096,
            value=st.session_state.rag_config.max_tokens,
            step=256,
            help="Número máximo de tokens en la respuesta"
        )
    
    # Botón para aplicar configuración
    if st.button("💾 Guardar Configuración RAG", type="primary"):
        try:
            # Actualizar configuración
            st.session_state.rag_config.chunk_size = chunk_size
            st.session_state.rag_config.chunk_overlap = chunk_overlap
            st.session_state.rag_config.embedding_model = embedding_model
            st.session_state.rag_config.k = k_docs
            st.session_state.rag_config.search_type = search_type
            st.session_state.rag_config.score_threshold = score_threshold
            st.session_state.rag_config.llm_model = llm_model
            st.session_state.rag_config.temperature = temperature
            st.session_state.rag_config.max_tokens = max_tokens
            
            st.success("✅ Configuración guardada exitosamente")
            
            # Actualizar sistema RAG si existe
            if 'rag_system' in st.session_state and st.session_state.rag_system:
                rag = st.session_state.rag_system
                
                # Actualizar configuraciones
                retrieval_config = {
                    "search_type": search_type,
                    "k": k_docs,
                    "score_threshold": score_threshold
                }
                
                llm_config = {
                    "model": llm_model,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                rag.update_config("retrieval", retrieval_config)
                rag.update_config("llm", llm_config)
                
                st.success("✅ Sistema RAG actualizado con nueva configuración")
                
        except Exception as e:
            st.error(f"❌ Error guardando configuración: {str(e)}")

# Tab 2: Configuración de Interfaz
with tab2:
    st.header("Configuración de Interfaz")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Tema Visual")
        
        # Selector de tema
        current_theme = st.session_state.get('current_theme', 'default')
        theme = st.selectbox(
            "Tema de Color",
            ["default", "dark", "blue"],
            index=["default", "dark", "blue"].index(current_theme),
            help="Esquema de colores de la interfaz"
        )
        
        # Vista previa del tema
        if theme == "default":
            st.markdown("**Vista previa:** Tema clásico azul y morado")
        elif theme == "dark":
            st.markdown("**Vista previa:** Tema oscuro")
        elif theme == "blue":
            st.markdown("**Vista previa:** Tema azul profesional")
    
    with col2:
        st.subheader("📱 Configuración de Chat")
        
        # Máximo historial
        max_history = st.slider(
            "Máximo Historial de Chat",
            min_value=10,
            max_value=500,
            value=st.session_state.get('max_chat_history', 100),
            step=10,
            help="Número máximo de conversaciones a mantener"
        )
        
        # Auto-scroll
        auto_scroll = st.checkbox(
            "Auto-scroll en Chat",
            value=True,
            help="Desplazarse automáticamente a nuevos mensajes"
        )
    
    # Botón para aplicar tema
    if st.button("🎨 Aplicar Configuración de Interfaz", type="primary"):
        st.session_state.current_theme = theme
        st.session_state.max_chat_history = max_history
        st.session_state.auto_scroll = auto_scroll
        
        st.success("✅ Configuración de interfaz actualizada")
        st.rerun()

# Tab 3: Gestión de Archivos
with tab3:
    st.header("Gestión de Archivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Directorios")
        
        # Mostrar directorios actuales
        st.info(f"**Directorio de BD:** {st.session_state.rag_config.persist_directory}")
        st.info(f"**Directorio Temporal:** {st.session_state.rag_config.temp_directory}")
        
        # Configuración de límites
        max_file_size = st.slider(
            "Tamaño Máximo de Archivo (MB)",
            min_value=1,
            max_value=100,
            value=50,
            help="Tamaño máximo permitido por archivo"
        )
        
        max_files = st.slider(
            "Máximo Archivos por Carga",
            min_value=1,
            max_value=50,
            value=10,
            help="Número máximo de archivos por carga"
        )
    
    with col2:
        st.subheader("🧹 Limpieza")
        
        # Limpieza automática
        auto_cleanup = st.checkbox(
            "Limpieza Automática",
            value=True,
            help="Eliminar archivos temporales automáticamente"
        )
        
        # Tiempo de retención
        retention_hours = st.slider(
            "Retención de Archivos Temporales (horas)",
            min_value=1,
            max_value=168,
            value=24,
            help="Tiempo antes de eliminar archivos temporales"
        )
        
        # Botón de limpieza manual
        if st.button("🗑️ Limpiar Archivos Temporales Ahora"):
            try:
                temp_dir = st.session_state.rag_config.temp_directory
                if os.path.exists(temp_dir):
                    import shutil
                    shutil.rmtree(temp_dir)
                    os.makedirs(temp_dir, exist_ok=True)
                    st.success("✅ Limpieza de archivos temporales completada")
                else:
                    st.info("ℹ️ No hay archivos temporales para limpiar")
            except Exception as e:
                st.error(f"❌ Error en limpieza: {str(e)}")

# Tab 4: Configuración Avanzada
with tab4:
    st.header("Configuración Avanzada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 API y Seguridad")
        
        # Estado de API Key
        env_config = get_environment_config()
        api_key_status = "✅ Configurada" if env_config.get("google_api_key") else "❌ No configurada"
        st.info(f"**Google API Key:** {api_key_status}")
        
        if not env_config.get("google_api_key"):
            st.warning("⚠️ Configure su Google API Key en el archivo .env")
            st.code("GOOGLE_API_KEY=su_api_key_aqui", language="bash")
        
        # Debug mode
        debug_mode = st.checkbox(
            "Modo Debug",
            value=False,
            help="Mostrar información detallada de debug"
        )
        
        # Logging level
        log_level = st.selectbox(
            "Nivel de Log",
            ["INFO", "DEBUG", "WARNING", "ERROR"],
            index=0,
            help="Nivel de detalle en los logs"
        )
    
    with col2:
        st.subheader("📊 Monitoreo")
        
        # Estadísticas del sistema
        if st.button("🔍 Mostrar Estadísticas del Sistema"):
            try:
                if 'rag_system' in st.session_state and st.session_state.rag_system:
                    rag = st.session_state.rag_system
                    stats = rag.get_database_stats()
                    
                    st.json(stats)
                else:
                    st.warning("Sistema RAG no inicializado")
            except Exception as e:
                st.error(f"❌ Error obteniendo estadísticas: {str(e)}")
    
    st.divider()
    
    # Configuración de respaldo
    st.subheader("💾 Respaldo y Restauración")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Exportar Configuración"):
            config_data = {
                "rag_config": {
                    "chunk_size": st.session_state.rag_config.chunk_size,
                    "chunk_overlap": st.session_state.rag_config.chunk_overlap,
                    "embedding_model": st.session_state.rag_config.embedding_model,
                    "k": st.session_state.rag_config.k,
                    "search_type": st.session_state.rag_config.search_type,
                    "score_threshold": st.session_state.rag_config.score_threshold,
                    "llm_model": st.session_state.rag_config.llm_model,
                    "temperature": st.session_state.rag_config.temperature,
                    "max_tokens": st.session_state.rag_config.max_tokens
                },
                "ui_config": {
                    "theme": st.session_state.get('current_theme', 'default'),
                    "max_chat_history": st.session_state.get('max_chat_history', 100)
                }
            }
            
            config_json = json.dumps(config_data, indent=2)
            
            st.download_button(
                label="⬇️ Descargar Configuración",
                data=config_json,
                file_name="rag_config.json",
                mime="application/json"
            )
    
    with col2:
        # Importar configuración
        uploaded_config = st.file_uploader(
            "📥 Importar Configuración",
            type=["json"],
            help="Cargar archivo de configuración previamente exportado"
        )
        
        if uploaded_config:
            try:
                config_data = json.load(uploaded_config)
                
                # Aplicar configuración RAG
                if "rag_config" in config_data:
                    rag_conf = config_data["rag_config"]
                    for key, value in rag_conf.items():
                        if hasattr(st.session_state.rag_config, key):
                            setattr(st.session_state.rag_config, key, value)
                
                # Aplicar configuración UI
                if "ui_config" in config_data:
                    ui_conf = config_data["ui_config"]
                    st.session_state.current_theme = ui_conf.get('theme', 'default')
                    st.session_state.max_chat_history = ui_conf.get('max_chat_history', 100)
                
                st.success("✅ Configuración importada exitosamente")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error importando configuración: {str(e)}")
    
    with col3:
        if st.button("🔄 Restablecer por Defecto"):
            st.session_state.rag_config = RAGConfig()
            st.session_state.current_theme = 'default'
            st.session_state.max_chat_history = 100
            
            st.success("✅ Configuración restablecida a valores por defecto")
            st.rerun()

# Footer con información del sistema
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    ⚙️ Panel de Configuración | Sistema RAG Inteligente v2.0
</div>
""", unsafe_allow_html=True)