import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json
# from utils import get_chat_statistics, format_timestamp
from rag_system import RAGSystem

st.set_page_config(
    page_title="Analytics - Sistema RAG",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Análisis y Estadísticas")

# Verificar si hay datos
if 'chat_history' not in st.session_state or not st.session_state.chat_history:
    st.warning("No hay datos de conversaciones para analizar. Primero usa el sistema de chat.")
    st.stop()

# Función para obtener estadísticas
def get_chat_statistics(chat_history):
    if not chat_history:
        return {}
    
    total_conversations = len(chat_history)
    total_response_length = sum(len(chat['answer']) for chat in chat_history)
    avg_response_length = int(total_response_length / total_conversations) if total_conversations > 0 else 0
    
    # Calcular hora más común
    hours = []
    for chat in chat_history:
        if 'timestamp' in chat:
            try:
                dt = datetime.fromisoformat(chat['timestamp'].replace('Z', '+00:00'))
                hours.append(dt.hour)
            except:
                hours.append(datetime.now().hour)
    
    most_common_hour = max(set(hours), key=hours.count) if hours else 0
    
    # Contar fuentes únicas
    all_sources = set()
    for chat in chat_history:
        if 'sources' in chat:
            all_sources.update(chat['sources'])
    
    return {
        'total_conversations': total_conversations,
        'avg_response_length': avg_response_length,
        'most_common_hour': f'{most_common_hour:02d}:00',
        'total_sources_used': len(all_sources)
    }

# Obtener estadísticas
stats = get_chat_statistics(st.session_state.chat_history)

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Conversaciones",
        value=stats["total_conversations"]
    )

with col2:
    st.metric(
        label="Longitud Promedio Respuesta", 
        value=f"{stats['avg_response_length']} chars"
    )

with col3:
    st.metric(
        label="Hora Más Activa",
        value=stats["most_common_hour"]
    )

with col4:
    st.metric(
        label="Fuentes Utilizadas",
        value=stats["total_sources_used"]
    )

st.divider()

# Análisis temporal
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Actividad por Día")
    
    # Preparar datos temporales
    if st.session_state.chat_history:
        dates = []
        for chat in st.session_state.chat_history:
            if 'timestamp' in chat:
                try:
                    dt = datetime.fromisoformat(chat['timestamp'].replace('Z', '+00:00'))
                    dates.append(dt.date())
                except:
                    dates.append(datetime.now().date())
            else:
                dates.append(datetime.now().date())
        
        # Contar conversaciones por día
        date_counts = pd.Series(dates).value_counts().sort_index()
        
        if not date_counts.empty:
            fig = px.line(
                x=date_counts.index,
                y=date_counts.values,
                title="Conversaciones por Día",
                labels={'x': 'Fecha', 'y': 'Número de Conversaciones'}
            )
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos temporales suficientes")

with col2:
    st.subheader("🕐 Distribución por Hora")
    
    # Análisis por horas
    hours = []
    for chat in st.session_state.chat_history:
        if 'timestamp' in chat:
            try:
                dt = datetime.fromisoformat(chat['timestamp'].replace('Z', '+00:00'))
                hours.append(dt.hour)
            except:
                hours.append(datetime.now().hour)
        else:
            hours.append(datetime.now().hour)
    
    if hours:
        hour_counts = pd.Series(hours).value_counts().sort_index()
        
        fig = px.bar(
            x=hour_counts.index,
            y=hour_counts.values,
            title="Actividad por Hora del Día",
            labels={'x': 'Hora', 'y': 'Número de Conversaciones'}
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# Análisis de contenido
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Longitud de Respuestas")
    
    response_lengths = [len(chat['answer']) for chat in st.session_state.chat_history]
    
    fig = px.histogram(
        x=response_lengths,
        nbins=20,
        title="Distribución de Longitud de Respuestas",
        labels={'x': 'Longitud (caracteres)', 'y': 'Frecuencia'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔍 Fuentes Más Utilizadas")
    
    # Contar fuentes
    source_counts = {}
    for chat in st.session_state.chat_history:
        if 'sources' in chat:
            for source in chat['sources']:
                source_counts[source] = source_counts.get(source, 0) + 1
    
    if source_counts:
        # Tomar top 10
        top_sources = dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        fig = px.bar(
            x=list(top_sources.values()),
            y=list(top_sources.keys()),
            orientation='h',
            title="Top 10 Fuentes Más Utilizadas",
            labels={'x': 'Número de Usos', 'y': 'Fuente'}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de fuentes")

st.divider()

# Análisis de rendimiento
st.subheader("⚡ Análisis de Rendimiento del Sistema")

# Simular datos de rendimiento (en una implementación real, estos datos vendrían del sistema)
col1, col2, col3 = st.columns(3)

with col1:
    # Tiempo de respuesta promedio (simulado)
    avg_response_time = 2.3  # segundos
    st.metric(
        label="Tiempo Promedio de Respuesta",
        value=f"{avg_response_time}s",
        delta="-0.2s",
        delta_color="inverse"
    )

with col2:
    # Precisión estimada
    accuracy = 92.5  # porcentaje
    st.metric(
        label="Precisión Estimada",
        value=f"{accuracy}%",
        delta="2.1%"
    )

with col3:
    # Satisfacción del usuario (simulada)
    satisfaction = 4.7  # de 5
    st.metric(
        label="Satisfacción (1-5)",
        value=f"{satisfaction}/5",
        delta="0.3"
    )

# Historial detallado
st.divider()
st.subheader("📋 Historial Detallado")

# Crear DataFrame del historial
chat_data = []
for i, chat in enumerate(st.session_state.chat_history):
    chat_data.append({
        'ID': i + 1,
        'Pregunta': chat['question'][:100] + "..." if len(chat['question']) > 100 else chat['question'],
        'Longitud Respuesta': len(chat['answer']),
        'Fuentes': len(chat.get('sources', [])),
        'Timestamp': chat.get('timestamp', 'N/A')
    })

df = pd.DataFrame(chat_data)

# Mostrar tabla interactiva
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# Exportar datos de análisis
st.divider()
st.subheader("💾 Exportar Análisis")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Exportar Estadísticas CSV"):
        analytics_data = {
            'Métrica': [
                'Total Conversaciones',
                'Longitud Promedio Respuesta',
                'Hora Más Activa',
                'Fuentes Utilizadas',
                'Tiempo Promedio Respuesta',
                'Precisión Estimada'
            ],
            'Valor': [
                stats["total_conversations"],
                stats["avg_response_length"],
                stats["most_common_hour"],
                stats["total_sources_used"],
                f"{avg_response_time}s",
                f"{accuracy}%"
            ]
        }
        
        analytics_df = pd.DataFrame(analytics_data)
        csv = analytics_df.to_csv(index=False)
        
        st.download_button(
            label="⬇️ Descargar CSV",
            data=csv,
            file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📈 Exportar Datos Completos JSON"):
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "performance": {
                "avg_response_time": avg_response_time,
                "accuracy": accuracy,
                "satisfaction": satisfaction
            },
            "chat_history": st.session_state.chat_history
        }
        
        json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="⬇️ Descargar JSON",
            data=json_data,
            file_name=f"full_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )