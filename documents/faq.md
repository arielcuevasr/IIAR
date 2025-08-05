# Preguntas Frecuentes (FAQ)

## ¿Qué es este sistema RAG?
Es un sistema de Recuperación Aumentada por Generación (RAG) que utiliza modelos de IA de Google Gemini para responder preguntas basándose en documentos cargados.

## ¿Cómo añado nuevos documentos?
Puedes colocar archivos PDF, TXT, MD o DOCX en la carpeta `documents/` y ejecutar el script principal.

## ¿Qué modelos de Gemini se utilizan?
Por defecto, se usa Gemini 1.5 Flash para generación y un modelo de Sentence Transformers para embeddings. Puedes configurar esto en el archivo `.env`.

## ¿Dónde se guarda la base de datos?
La base de datos vectorial (ChromaDB) se guarda persistentemente en la carpeta `chroma_db/`.

## ¿Es seguro mi API Key?
Tu API Key se carga desde el archivo `.env` y no debe ser compartida ni subida a repositorios públicos.