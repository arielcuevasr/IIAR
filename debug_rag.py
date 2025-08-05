#!/usr/bin/env python3
"""
Script de debug para identificar por qué falla la inicialización en Streamlit
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

st.set_page_config(page_title="Debug RAG", page_icon="🔍")

st.title("🔍 Debug del Sistema RAG")

# Mostrar información del entorno
st.subheader("1. Variables de entorno")
api_key = os.getenv("GOOGLE_API_KEY")
st.write(f"- GOOGLE_API_KEY existe: {'✅' if api_key else '❌'}")
if api_key:
    st.write(f"- Longitud de API key: {len(api_key)}")

# Test de config
st.subheader("2. Módulo config")
try:
    from config import validate_environment, get_environment_config
    valid, errors = validate_environment()
    env_config = get_environment_config()
    
    st.write(f"- Validación: {'✅' if valid else '❌'}")
    if errors:
        st.write(f"- Errores: {errors}")
    st.write(f"- API key en config: {'✅' if env_config.get('google_api_key') else '❌'}")
except Exception as e:
    st.error(f"Error importando config: {e}")

# Test de RAGSystem
st.subheader("3. RAGSystem")
try:
    from rag_system import RAGSystem
    st.write("✅ RAGSystem importado correctamente")
    
    if st.button("Crear instancia de RAGSystem"):
        with st.spinner("Creando RAGSystem..."):
            try:
                rag = RAGSystem()
                st.success("✅ RAGSystem creado exitosamente!")
                
                # Mostrar estadísticas
                stats = rag.get_database_stats()
                st.json(stats)
                
            except Exception as e:
                st.error(f"❌ Error creando RAGSystem: {e}")
                st.exception(e)
                
except Exception as e:
    st.error(f"Error importando RAGSystem: {e}")
    st.exception(e)

# Test de funciones de la app principal
st.subheader("4. Funciones de app.py")
try:
    # Simular las funciones cacheadas
    @st.cache_resource
    def test_create_rag_system():
        try:
            from rag_system import RAGSystem
            return RAGSystem()
        except Exception as e:
            st.error(f"Error en función cacheada: {e}")
            return None
    
    if st.button("Test función cacheada"):
        with st.spinner("Probando función cacheada..."):
            rag = test_create_rag_system()
            if rag:
                st.success("✅ Función cacheada funciona!")
            else:
                st.error("❌ Función cacheada falló")
                
except Exception as e:
    st.error(f"Error en test de función cacheada: {e}")
    st.exception(e)