"""
Configuraciones y utilidades para el sistema RAG
"""

import os
from dataclasses import dataclass
from typing import Dict, Any, List
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

@dataclass
class RAGConfig:
    """Configuración del sistema RAG"""
    
    # Configuración de embeddings
    embedding_model: str = "models/embedding-001"
    
    # Configuración del text splitter
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Configuración del retriever
    search_type: str = "similarity"
    k: int = 4
    score_threshold: float = 0.5
    
    # Configuración del LLM
    llm_model: str = "gemini-1.5-pro"
    temperature: float = 0.1
    max_tokens: int = 2048
    
    # Directorios
    persist_directory: str = "./chroma_db"
    temp_directory: str = "./temp_docs"
    
    # Formatos soportados
    supported_formats: List[str] = None
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ['.pdf', '.txt', '.md']

class AppConfig:
    """Configuración de la aplicación Streamlit"""
    
    # Configuración de página
    PAGE_TITLE = "Sistema RAG Inteligente"
    PAGE_ICON = "🧠"
    LAYOUT = "wide"
    
    # Temas de colores
    THEMES = {
        "default": {
            "primary_color": "#667eea",
            "secondary_color": "#764ba2",
            "background_color": "#ffffff",
            "text_color": "#000000"
        },
        "dark": {
            "primary_color": "#4a5568",
            "secondary_color": "#2d3748",
            "background_color": "#1a202c",
            "text_color": "#ffffff"
        },
        "blue": {
            "primary_color": "#3182ce",
            "secondary_color": "#2c5282",
            "background_color": "#ebf8ff",
            "text_color": "#1a365d"
        }
    }
    
    # Límites de archivos
    MAX_FILE_SIZE_MB = 50
    MAX_FILES_PER_UPLOAD = 10
    
    # Configuración de chat
    MAX_CHAT_HISTORY = 100
    CHAT_EXPORT_FORMATS = ["json", "txt", "csv"]

def get_environment_config() -> Dict[str, Any]:
    """
    Obtiene configuración desde variables de entorno
    """
    return {
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }

def validate_environment() -> tuple[bool, List[str]]:
    """
    Valida que las variables de entorno necesarias estén configuradas
    Returns:
        Tuple con (es_válido, lista_de_errores)
    """
    errors = []
    
    if not os.getenv("GOOGLE_API_KEY"):
        errors.append("GOOGLE_API_KEY no está configurada")
    
    return len(errors) == 0, errors

# Instancia global de configuración
rag_config = RAGConfig()
app_config = AppConfig()