import os
import logging
from typing import List, Optional, Dict, Any
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import time

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Inicializa el sistema RAG mejorado
        Args:
            persist_directory: Directorio para persistir la base de datos vectorial
        """
        try:
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY no está configurada en las variables de entorno.")

            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001", 
                google_api_key=google_api_key
            )
            
            # Configuración mejorada del text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            self.persist_directory = persist_directory
            self.vectorstore = None
            self.qa_chain = None
            self.google_api_key = google_api_key
            
            # Configuraciones avanzadas
            self.retrieval_config = {
                "search_type": "similarity",
                "k": 4,
                "score_threshold": 0.5
            }
            
            self.llm_config = {
                "model": "gemini-1.5-pro",
                "temperature": 0.1,
                "max_tokens": 2048
            }
            
            logger.info("Sistema RAG inicializado correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando RAGSystem: {str(e)}")
            raise

    def load_documents(self, file_paths: List[str]) -> List[Document]:
        """
        Carga documentos desde archivos con manejo mejorado de errores
        Args:
            file_paths: Lista de rutas a los archivos
        Returns:
            Lista de documentos cargados
        """
        documents = []
        supported_formats = {'.pdf', '.txt', '.md'}
        
        for file_path in file_paths:
            try:
                file_extension = os.path.splitext(file_path)[1].lower()
                
                if file_extension not in supported_formats:
                    logger.warning(f"Formato no soportado: {file_path}")
                    continue
                
                # Verificar que el archivo existe
                if not os.path.exists(file_path):
                    logger.error(f"Archivo no encontrado: {file_path}")
                    continue
                
                # Cargar según el tipo de archivo
                if file_extension == '.pdf':
                    loader = PyPDFLoader(file_path)
                elif file_extension == '.txt':
                    loader = TextLoader(file_path, encoding='utf-8')
                elif file_extension == '.md':
                    loader = UnstructuredMarkdownLoader(file_path)
                
                docs = loader.load()
                
                # Agregar metadata adicional
                for doc in docs:
                    doc.metadata.update({
                        'file_path': file_path,
                        'file_name': os.path.basename(file_path),
                        'file_type': file_extension,
                        'load_time': time.time()
                    })
                
                documents.extend(docs)
                logger.info(f"Cargado exitosamente: {file_path} ({len(docs)} páginas)")
                
            except Exception as e:
                logger.error(f"Error cargando {file_path}: {str(e)}")
                continue
        
        logger.info(f"Total de documentos cargados: {len(documents)}")
        return documents

    def process_documents(self, documents: List[Document]) -> bool:
        """
        Procesa documentos: los divide en chunks y crea embeddings
        Args:
            documents: Lista de documentos a procesar
        Returns:
            True si el procesamiento fue exitoso
        """
        try:
            if not documents:
                logger.warning("No hay documentos para procesar")
                return False
            
            # Dividir documentos en chunks
            texts = self.text_splitter.split_documents(documents)
            logger.info(f"Documentos divididos en {len(texts)} chunks")
            
            if not texts:
                logger.warning("No se generaron chunks válidos")
                return False
            
            # Crear vector store
            self.vectorstore = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            logger.info("Base de datos vectorial creada y guardada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error procesando documentos: {str(e)}")
            return False

    def load_existing_vectorstore(self) -> bool:
        """
        Carga una base de datos vectorial existente
        Returns:
            True si la carga fue exitosa
        """
        try:
            if not os.path.exists(self.persist_directory):
                logger.warning(f"Directorio de persistencia no existe: {self.persist_directory}")
                return False
            
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            
            logger.info("Base de datos vectorial cargada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando base de datos: {str(e)}")
            return False

    def setup_qa_chain(self) -> bool:
        """
        Configura la cadena de pregunta-respuesta con prompt personalizado
        Returns:
            True si la configuración fue exitosa
        """
        try:
            if not self.vectorstore:
                raise ValueError("Primero debes procesar documentos o cargar una base de datos existente")
            
            # Crear retriever con configuración avanzada
            retriever = self.vectorstore.as_retriever(
                search_type=self.retrieval_config["search_type"],
                search_kwargs={"k": self.retrieval_config["k"]}
            )
            
            # Prompt personalizado en español
            custom_prompt = PromptTemplate(
                template="""Eres un asistente inteligente especializado en responder preguntas basándote en documentos específicos.

Contexto de los documentos:
{context}

Pregunta del usuario: {question}

Instrucciones:
1. Responde ÚNICAMENTE basándote en la información proporcionada en el contexto
2. Si la información no está en el contexto, indica claramente que no tienes esa información
3. Proporciona respuestas detalladas y bien estructuradas
4. Cita las fuentes cuando sea relevante
5. Usa un tono profesional pero amigable
6. Responde en español

Respuesta:""",
                input_variables=["context", "question"]
            )
            
            # Crear LLM con configuración optimizada
            llm = ChatGoogleGenerativeAI(
                model=self.llm_config["model"],
                temperature=self.llm_config["temperature"],
                max_tokens=self.llm_config["max_tokens"],
                google_api_key=self.google_api_key
            )
            
            # Crear cadena QA con prompt personalizado
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": custom_prompt}
            )
            
            logger.info("Cadena QA configurada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error configurando cadena QA: {str(e)}")
            return False

    def ask_question(self, question: str) -> Dict[str, Any]:
        """
        Hace una pregunta al sistema RAG con manejo mejorado de errores
        Args:
            question: La pregunta a realizar
        Returns:
            Diccionario con la respuesta y documentos fuente
        """
        try:
            if not self.qa_chain:
                raise ValueError("Primero debes configurar la cadena QA")
            
            if not question or question.strip() == "":
                raise ValueError("La pregunta no puede estar vacía")
            
            logger.info(f"Procesando pregunta: {question[:100]}...")
            
            result = self.qa_chain.invoke({"query": question})
            
            response = {
                "answer": result["result"], 
                "source_documents": result["source_documents"],
                "question": question,
                "timestamp": time.time()
            }
            
            logger.info("Pregunta procesada exitosamente")
            return response
            
        except Exception as e:
            logger.error(f"Error procesando pregunta: {str(e)}")
            return {
                "answer": f"Lo siento, ocurrió un error al procesar tu pregunta: {str(e)}",
                "source_documents": [],
                "question": question,
                "timestamp": time.time(),
                "error": True
            }

    def add_documents(self, file_paths: List[str]) -> bool:
        """
        Añade nuevos documentos a la base de datos existente
        Args:
            file_paths: Lista de rutas a los nuevos archivos
        Returns:
            True si la adición fue exitosa
        """
        try:
            documents = self.load_documents(file_paths)
            if not documents:
                logger.warning("No se cargaron documentos válidos")
                return False
            
            texts = self.text_splitter.split_documents(documents)
            
            if self.vectorstore:
                # Añadir a vectorstore existente
                self.vectorstore.add_documents(texts)
                logger.info(f"Añadidos {len(texts)} chunks nuevos a la base de datos existente")
            else:
                # Crear nuevo vectorstore
                success = self.process_documents(documents)
                if not success:
                    return False
                logger.info(f"Creada nueva base de datos con {len(texts)} chunks")
            
            return True
            
        except Exception as e:
            logger.error(f"Error añadiendo documentos: {str(e)}")
            return False

    def get_database_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la base de datos vectorial
        Returns:
            Diccionario con estadísticas
        """
        try:
            if not self.vectorstore:
                return {"status": "No hay base de datos cargada"}
            
            # Obtener información básica
            stats = {
                "status": "Base de datos activa",
                "persist_directory": self.persist_directory,
                "embedding_model": "models/embedding-001",
                "llm_model": self.llm_config["model"],
                "chunk_size": self.text_splitter._chunk_size,
                "chunk_overlap": self.text_splitter._chunk_overlap
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {str(e)}")
            return {"status": f"Error: {str(e)}"}

    def update_config(self, config_type: str, new_config: Dict[str, Any]) -> bool:
        """
        Actualiza la configuración del sistema
        Args:
            config_type: Tipo de configuración ('retrieval' o 'llm')
            new_config: Nueva configuración
        Returns:
            True si la actualización fue exitosa
        """
        try:
            if config_type == "retrieval":
                self.retrieval_config.update(new_config)
                logger.info("Configuración de retrieval actualizada")
            elif config_type == "llm":
                self.llm_config.update(new_config)
                logger.info("Configuración de LLM actualizada")
            else:
                logger.warning(f"Tipo de configuración no reconocido: {config_type}")
                return False
            
            # Re-configurar la cadena QA si existe
            if self.vectorstore:
                return self.setup_qa_chain()
            
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando configuración: {str(e)}")
            return False
