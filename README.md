# 🧠 Sistema RAG Inteligente

Un sistema de Retrieval-Augmented Generation (RAG) avanzado construido con Streamlit, LangChain y Google Gemini para consultar documentos de manera inteligente.

## ✨ Características

### 🔥 Funcionalidades Principales
- **Chat Inteligente**: Pregunta sobre tus documentos con IA avanzada
- **Soporte Multi-formato**: PDF, TXT, MD
- **Interfaz Moderna**: Diseño profesional y responsivo
- **Historial de Chat**: Guarda y exporta conversaciones
- **Analytics Avanzados**: Estadísticas y métricas de uso
- **Configuración Flexible**: Personaliza todos los parámetros

### 🎨 Interfaz Mejorada
- **Sidebar Inteligente**: Panel de control completo
- **Temas Personalizables**: 3 esquemas de color
- **Métricas en Tiempo Real**: Documentos procesados, preguntas realizadas
- **Gestión de Documentos**: Vista previa y eliminación
- **Exportación**: JSON, CSV, TXT

### 🔧 Sistema RAG Avanzado
- **Manejo de Errores Robusto**: Logging detallado y recuperación de errores
- **Configuración Dinámica**: Ajusta parámetros sin reiniciar
- **Prompt Personalizado**: Optimizado para español
- **Embeddings Optimizados**: Google Embedding-001
- **Chunking Inteligente**: Configuración avanzada de fragmentación

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+
- API Key de Google Gemini

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd mi_rag_project
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto:
```env
GOOGLE_API_KEY=tu_api_key_aqui
DEBUG_MODE=false
LOG_LEVEL=INFO
```

4. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

## 📁 Estructura del Proyecto

```
mi_rag_project/
├── app.py                    # Aplicación principal
├── rag_system.py            # Sistema RAG mejorado
├── config.py                # Configuraciones
├── utils.py                 # Utilidades
├── requirements.txt         # Dependencias
├── README.md               # Documentación
├── .env                    # Variables de entorno
├── pages/                  # Páginas adicionales
│   ├── 📊_Analytics.py     # Analytics y estadísticas
│   └── ⚙️_Settings.py      # Configuración del sistema
├── chroma_db/              # Base de datos vectorial
├── temp_docs/              # Documentos temporales
└── documents/              # Documentos de ejemplo
```

## 🎯 Uso

### 1. Cargar Documentos
- Usa el sidebar para subir archivos PDF, TXT o MD
- Haz clic en "🔄 Procesar Documentos"
- Ve el progreso en las métricas del panel

### 2. Hacer Preguntas
- Escribe tu pregunta en el chat principal
- Haz clic en "🚀 Obtener Respuesta"
- Ve la respuesta con fuentes incluidas

### 3. Analizar Datos
- Ve a "📊 Analytics" para ver estadísticas
- Exporta datos en CSV o JSON
- Analiza patrones de uso

### 4. Configurar Sistema
- Ve a "⚙️ Settings" para personalizar
- Ajusta parámetros del modelo
- Cambia temas visuales
- Gestiona archivos

## 🔧 Configuración Avanzada

### Parámetros del Sistema RAG

**Text Splitter:**
- `chunk_size`: Tamaño de fragmentos (500-2000)
- `chunk_overlap`: Superposición (0-500)

**Retrieval:**
- `k`: Documentos a recuperar (1-10)
- `search_type`: Tipo de búsqueda (similarity/mmr)
- `score_threshold`: Umbral de relevancia (0.0-1.0)

**LLM:**
- `model`: Modelo Gemini (1.5-pro/1.5-flash)
- `temperature`: Creatividad (0.0-1.0)
- `max_tokens`: Longitud respuesta (512-4096)

### Personalización de Temas

La aplicación soporta 3 temas:
- **Default**: Azul y morado clásico
- **Dark**: Modo oscuro profesional
- **Blue**: Azul corporativo

## 📊 Analytics

El sistema incluye analytics completos:

- **Métricas de Uso**: Conversaciones, respuestas, fuentes
- **Análisis Temporal**: Actividad por día/hora
- **Distribución de Contenido**: Longitud de respuestas
- **Fuentes Populares**: Documentos más consultados
- **Rendimiento**: Tiempos de respuesta estimados

## 🔒 Seguridad

- **API Keys**: Almacenadas de forma segura en variables de entorno
- **Validación de Archivos**: Verificación de formatos y tamaños
- **Limpieza Automática**: Eliminación de archivos temporales
- **Logging**: Registro detallado de actividades

## 🐛 Solución de Problemas

### Errores Comunes

1. **Error de API Key**
   - Verifica que `GOOGLE_API_KEY` esté configurada
   - Asegúrate de que la key sea válida

2. **Error al procesar documentos**
   - Verifica el formato del archivo (PDF, TXT, MD)
   - Asegúrate de que el archivo no esté corrupto

3. **Base de datos no carga**
   - Verifica que el directorio `chroma_db` existe
   - Intenta procesar documentos nuevamente

### Logs y Debug

Activa el modo debug en `.env`:
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

## 🔄 Actualizaciones

### v2.0 - Mejoras Principales
- ✅ Interfaz completamente rediseñada
- ✅ Sistema RAG mejorado con mejor manejo de errores
- ✅ Analytics y estadísticas avanzadas
- ✅ Configuración flexible y temas
- ✅ Gestión completa de documentos
- ✅ Exportación de datos y conversaciones

### Próximas Mejoras
- 📝 Soporte para más formatos (DOCX, XLSX)
- 🔍 Búsqueda semántica avanzada
- 👥 Soporte multi-usuario
- 🌐 API REST
- 🤖 Integración con más modelos LLM

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ve el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si tienes problemas o preguntas:
- Abre un issue en GitHub
- Revisa la documentación
- Verifica los logs de la aplicación

---

**🧠 Sistema RAG Inteligente** - Powered by Gemini AI & LangChain