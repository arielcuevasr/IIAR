"""
Utilidades y funciones auxiliares para el sistema RAG
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st
import time

def format_file_size(size_bytes: int) -> str:
    """
    Convierte bytes a formato legible
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_timestamp(timestamp: float) -> str:
    """
    Convierte timestamp a formato legible
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def export_chat_history(chat_history: List[Dict], format_type: str = "json") -> str:
    """
    Exporta historial de chat en diferentes formatos
    """
    if format_type == "json":
        return json.dumps(chat_history, indent=2, ensure_ascii=False)
    
    elif format_type == "txt":
        output = []
        for i, chat in enumerate(chat_history, 1):
            output.append(f"=== Conversación {i} ===")
            output.append(f"Fecha: {chat.get('timestamp', 'N/A')}")
            output.append(f"Pregunta: {chat['question']}")
            output.append(f"Respuesta: {chat['answer']}")
            if chat.get('sources'):
                output.append("Fuentes:")
                for source in chat['sources']:
                    output.append(f"  - {source}")
            output.append("")
        return "\n".join(output)
    
    elif format_type == "csv":
        df = pd.DataFrame(chat_history)
        return df.to_csv(index=False)
    
    else:
        raise ValueError(f"Formato no soportado: {format_type}")

def clean_temp_files(temp_dir: str, max_age_hours: int = 24):
    """
    Limpia archivos temporales antiguos
    """
    if not os.path.exists(temp_dir):
        return
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                try:
                    os.remove(file_path)
                    st.info(f"Archivo temporal eliminado: {filename}")
                except Exception as e:
                    st.warning(f"No se pudo eliminar {filename}: {str(e)}")

def validate_file_upload(uploaded_file, max_size_mb: int = 50) -> tuple[bool, str]:
    """
    Valida un archivo subido
    Returns:
        Tuple con (es_válido, mensaje_error)
    """
    if uploaded_file.size > max_size_mb * 1024 * 1024:
        return False, f"El archivo es muy grande. Máximo: {max_size_mb}MB"
    
    allowed_extensions = {'.pdf', '.txt', '.md'}
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        return False, f"Formato no soportado. Permitidos: {', '.join(allowed_extensions)}"
    
    return True, ""

def create_download_link(data: str, filename: str, mime_type: str = "text/plain") -> str:
    """
    Crea un enlace de descarga para datos
    """
    import base64
    
    b64 = base64.b64encode(data.encode()).decode()
    return f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Descargar {filename}</a>'

def get_chat_statistics(chat_history: List[Dict]) -> Dict[str, Any]:
    """
    Calcula estadísticas del historial de chat
    """
    if not chat_history:
        return {
            "total_conversations": 0,
            "avg_response_length": 0,
            "most_common_hour": "N/A",
            "total_sources_used": 0
        }
    
    total_conversations = len(chat_history)
    
    # Longitud promedio de respuestas
    response_lengths = [len(chat['answer']) for chat in chat_history]
    avg_response_length = sum(response_lengths) / len(response_lengths) if response_lengths else 0
    
    # Hora más común (si hay timestamps)
    hours = []
    for chat in chat_history:
        if 'timestamp' in chat:
            try:
                dt = datetime.fromisoformat(chat['timestamp'].replace('Z', '+00:00'))
                hours.append(dt.hour)
            except:
                pass
    
    most_common_hour = max(set(hours), key=hours.count) if hours else "N/A"
    
    # Total de fuentes utilizadas
    total_sources = sum(len(chat.get('sources', [])) for chat in chat_history)
    
    return {
        "total_conversations": total_conversations,
        "avg_response_length": round(avg_response_length),
        "most_common_hour": f"{most_common_hour}:00" if most_common_hour != "N/A" else "N/A",
        "total_sources_used": total_sources
    }

def apply_custom_css(theme: str = "default") -> str:
    """
    Aplica CSS personalizado según el tema
    """
    themes = {
        "default": {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "background": "#ffffff",
            "text": "#000000"
        },
        "dark": {
            "primary": "#4a5568",
            "secondary": "#2d3748",
            "background": "#1a202c",
            "text": "#ffffff"
        },
        "blue": {
            "primary": "#3182ce",
            "secondary": "#2c5282",
            "background": "#ebf8ff",
            "text": "#1a365d"
        }
    }
    
    colors = themes.get(theme, themes["default"])
    
    return f"""
    <style>
        .main-header {{
            background: linear-gradient(90deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .chat-message {{
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .user-message {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white;
            margin-left: 2rem;
        }}
        
        .bot-message {{
            background: #f8f9fa;
            border-left: 4px solid {colors['primary']};
            margin-right: 2rem;
        }}
        
        .stButton > button {{
            background: linear-gradient(90deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }}
        
        .stButton > button:hover {{
            opacity: 0.8;
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }}
    </style>
    """

def show_success_message(message: str):
    """Muestra mensaje de éxito con estilo personalizado"""
    st.markdown(f"""
    <div style="
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    ">
        ✅ {message}
    </div>
    """, unsafe_allow_html=True)

def show_warning_message(message: str):
    """Muestra mensaje de advertencia con estilo personalizado"""
    st.markdown(f"""
    <div style="
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    ">
        ⚠️ {message}
    </div>
    """, unsafe_allow_html=True)

def show_error_message(message: str):
    """Muestra mensaje de error con estilo personalizado"""
    st.markdown(f"""
    <div style="
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    ">
        ❌ {message}
    </div>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Inicializa las variables de sesión de Streamlit"""
    default_values = {
        'chat_history': [],
        'processed_documents': [],
        'total_questions': 0,
        'total_docs': 0,
        'current_theme': 'default',
        'rag_system': None,
        'last_cleanup': time.time()
    }
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value