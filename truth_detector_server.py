#!/usr/bin/env python3
"""
🚀 Servidor Completo del Detector de Verdad con IA
Incluye: IA + API REST + WebSocket en un solo archivo
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import json
import csv
import pandas as pd
from typing import List, Dict, Tuple
import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# MODELOS DE DATOS
# ============================================================================


class StatementRequest(BaseModel):
    statement: str


class BatchRequest(BaseModel):
    statements: List[str]


# ============================================================================
# DETECTOR DE VERDAD CON IA
# ============================================================================


class TruthDetector:
    def __init__(self):
        # Vectorizador TF-IDF mejorado con más features y stop_words en español
        spanish_stop_words = [
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'las', 'una', 'también', 'pero', 'sus', 'me', 'hasta', 'hay', 'donde', 'han', 'quien', 'están', 'estado', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros'
        ]
        
        self.vectorizer = TfidfVectorizer(
            max_features=5000,  # Aumentado de 2000 a 5000
            stop_words=spanish_stop_words,  # Stop words en español
            ngram_range=(1, 3),  # Unigramas, bigramas y trigramas
            min_df=2,  # Frecuencia mínima de documento
            max_df=0.95,  # Frecuencia máxima de documento
            sublinear_tf=True,  # Aplicar log a frecuencias
            analyzer='word'
        )
        
        # Vectorizador adicional para categorías
        self.category_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=spanish_stop_words,
            ngram_range=(1, 2)
        )
        
        self.truth_embeddings = None
        self.false_embeddings = None
        self.truth_statements = []
        self.false_statements = []
        self.truth_categories = []
        self.false_categories = []
        self.is_trained = False
        self.dataset_path = "super_dataset.csv"

        # Estadísticas del modelo
        self.total_statements = 0
        self.truth_count = 0
        self.false_count = 0
        self.categories = set()
        
        # Pesos por categoría para mejorar afinidad
        self.category_weights = {
            'matematicas': 1.2,      # Matemáticas: alta precisión
            'ciencia': 1.1,           # Ciencia: buena precisión
            'geografia': 1.0,         # Geografía: precisión estándar
            'historia': 1.0,          # Historia: precisión estándar
            'tecnologia': 1.1,        # Tecnología: buena precisión
            'astronomia': 1.15        # Astronomía: muy buena precisión
        }

    def load_dataset(self):
        """Carga el dataset masivo desde CSV con mejor manejo de categorías"""
        try:
            if not os.path.exists(self.dataset_path):
                logger.error(f"No se encontró el dataset: {self.dataset_path}")
                return False

            logger.info("Cargando dataset masivo...")
            df = pd.read_csv(self.dataset_path)

            # Separar afirmaciones verdaderas y falsas con sus categorías
            truth_df = df[df["truth_value"] == "verdadero"]
            false_df = df[df["truth_value"] == "falso"]
            
            self.truth_statements = truth_df["statement"].tolist()
            self.false_statements = false_df["statement"].tolist()
            self.truth_categories = truth_df["category"].tolist()
            self.false_categories = false_df["category"].tolist()

            # Obtener estadísticas
            self.total_statements = len(df)
            self.truth_count = len(self.truth_statements)
            self.false_count = len(self.false_statements)
            self.categories = set(df["category"].unique())

            logger.info(
                f"Dataset cargado: {self.total_statements} afirmaciones totales"
            )
            logger.info(f"Verdaderas: {self.truth_count}, Falsas: {self.false_count}")
            logger.info(f"Categorías: {', '.join(sorted(self.categories))}")

            return True

        except Exception as e:
            logger.error(f"Error cargando dataset: {e}")
            return False

    def train(self):
        """Entrena el modelo usando el dataset masivo con técnicas mejoradas"""
        logger.info("Entrenando el modelo de detección de verdad mejorado...")

        # Cargar dataset si no está cargado
        if not self.truth_statements or not self.false_statements:
            if not self.load_dataset():
                logger.error("No se pudo cargar el dataset. Usando datos básicos.")
                self._load_basic_knowledge()

        # Combinar todas las afirmaciones para entrenar el vectorizer
        all_statements = self.truth_statements + self.false_statements

        # Entrenar el vectorizer TF-IDF principal
        logger.info("Entrenando vectorizer TF-IDF mejorado...")
        self.vectorizer.fit(all_statements)

        # Entrenar vectorizer de categorías
        logger.info("Entrenando vectorizer de categorías...")
        all_categories = self.truth_categories + self.false_categories
        self.category_vectorizer.fit(all_categories)

        # Generar embeddings TF-IDF para afirmaciones verdaderas
        logger.info("Generando embeddings para afirmaciones verdaderas...")
        self.truth_embeddings = self.vectorizer.transform(self.truth_statements)

        # Generar embeddings TF-IDF para afirmaciones falsas
        logger.info("Generando embeddings para afirmaciones falsas...")
        self.false_embeddings = self.vectorizer.transform(self.false_statements)

        self.is_trained = True
        logger.info("Modelo mejorado entrenado exitosamente!")

        # Guardar el modelo
        self.save_model()

    def predict(self, statement: str) -> Dict:
        """Predice si una afirmación es verdadera o falsa con afinidad mejorada"""
        if not self.is_trained:
            logger.warning("El modelo no está entrenado. Entrenando...")
            self.train()

        # Generar embedding TF-IDF de la nueva afirmación
        statement_embedding = self.vectorizer.transform([statement])
        
        # Detectar categoría de la afirmación
        detected_category = self._detect_category(statement)
        category_weight = self.category_weights.get(detected_category, 1.0)

        # Calcular similaridad con afirmaciones verdaderas y falsas
        true_similarities = cosine_similarity(
            statement_embedding, self.truth_embeddings
        )
        false_similarities = cosine_similarity(
            statement_embedding, self.false_embeddings
        )

        # Aplicar pesos por categoría para mejorar afinidad
        true_similarities = self._apply_category_weights(
            true_similarities, self.truth_categories, category_weight
        )
        false_similarities = self._apply_category_weights(
            false_similarities, self.false_categories, category_weight
        )

        # Calcular métricas mejoradas de similaridad
        max_true_sim = np.max(true_similarities)
        max_false_sim = np.max(false_similarities)
        
        # Usar promedio ponderado para mayor estabilidad
        avg_true_sim = np.mean(true_similarities)
        avg_false_sim = np.mean(false_similarities)
        
        # Combinar métricas para mejor afinidad
        combined_true_score = (max_true_sim * 0.7) + (avg_true_sim * 0.3)
        combined_false_score = (max_false_sim * 0.7) + (avg_false_sim * 0.3)

        # Calcular confianza y decisión con umbral adaptativo
        confidence_threshold = 0.1  # Umbral mínimo para evitar predicciones muy inciertas
        
        if combined_true_score > combined_false_score and combined_true_score > confidence_threshold:
            confidence = float(combined_true_score)
            prediction = "verdadero"
            explanation = f"La afirmación tiene {confidence:.2%} de similaridad con afirmaciones verdaderas conocidas"
            similarities = true_similarities
            statements = self.truth_statements
        elif combined_false_score > combined_true_score and combined_false_score > confidence_threshold:
            confidence = float(combined_false_score)
            prediction = "falso"
            explanation = f"La afirmación tiene {confidence:.2%} de similaridad con afirmaciones falsas conocidas"
            similarities = false_similarities
            statements = self.false_statements
        else:
            # Caso de baja confianza - usar la más alta pero marcar como incierta
            if combined_true_score > combined_false_score:
                confidence = float(combined_true_score)
                prediction = "verdadero"
                explanation = f"La afirmación tiene {confidence:.2%} de similaridad con afirmaciones verdaderas conocidas (BAJA CONFIANZA)"
            else:
                confidence = float(combined_false_score)
                prediction = "falso"
                explanation = f"La afirmación tiene {confidence:.2%} de similaridad con afirmaciones falsas conocidas (BAJA CONFIANZA)"
            
            similarities = true_similarities if prediction == "verdadero" else false_similarities
            statements = self.truth_statements if prediction == "verdadero" else self.false_statements

        # Encontrar afirmaciones más similares para explicación
        most_similar_idx = np.argmax(similarities)
        most_similar = statements[most_similar_idx]
        similarity_score = similarities[0][most_similar_idx]

        # Determinar nivel de confianza mejorado
        if confidence > 0.8:
            confidence_level = "muy alta"
        elif confidence > 0.6:
            confidence_level = "alta"
        elif confidence > 0.4:
            confidence_level = "moderada"
        elif confidence > 0.2:
            confidence_level = "baja"
        else:
            confidence_level = "muy baja"

        return {
            "prediction": prediction,
            "confidence": confidence,
            "confidence_level": confidence_level,
            "explanation": explanation,
            "most_similar_statement": most_similar,
            "similarity_score": float(similarity_score),
            "detected_category": detected_category,
            "category_weight": category_weight,
            "max_true_similarity": float(max_true_sim),
            "max_false_similarity": float(max_false_sim),
            "avg_true_similarity": float(avg_true_sim),
            "avg_false_similarity": float(avg_false_sim),
            "total_training_data": self.total_statements,
            "model_status": "entrenado" if self.is_trained else "no entrenado",
        }

    def _detect_category(self, statement: str) -> str:
        """Detecta la categoría de una afirmación usando palabras clave"""
        statement_lower = statement.lower()
        
        # Palabras clave por categoría
        category_keywords = {
            'matematicas': ['+', '-', '×', '÷', '=', '²', '³', '√', 'suma', 'resta', 'multiplicación', 'división', 'cuadrado', 'raíz', 'ángulo', 'grados', 'porcentaje'],
            'ciencia': ['temperatura', 'grados', 'celsius', 'fahrenheit', 'peso', 'kg', 'gramos', 'litros', 'mililitros', 'presión', 'atmósfera', 'gravedad', 'velocidad', 'km/s', 'm/s', 'energía', 'calorías', 'proteínas', 'vitaminas', 'células', 'órganos', 'sistema', 'respiración', 'fotosíntesis'],
            'geografia': ['país', 'países', 'capital', 'ciudad', 'población', 'habitantes', 'continente', 'océano', 'mar', 'río', 'montaña', 'cordillera', 'desierto', 'bosque', 'clima', 'temperatura', 'lluvia', 'seco', 'húmedo'],
            'historia': ['año', 'siglo', 'década', 'fecha', 'guerra', 'batalla', 'rey', 'reina', 'emperador', 'presidente', 'revolución', 'independencia', 'colonización', 'imperio', 'dinastía'],
            'tecnologia': ['javascript', 'python', 'java', 'html', 'css', 'sql', 'api', 'http', 'https', 'ssl', 'tls', 'protocolo', 'framework', 'biblioteca', 'sistema operativo', 'linux', 'windows', 'mac', 'código abierto', 'software'],
            'astronomia': ['planeta', 'sol', 'luna', 'estrella', 'galaxia', 'asteroide', 'cometa', 'órbita', 'diámetro', 'km', 'años luz', 'constelación', 'nebulosa', 'agujero negro', 'nasa', 'espacial']
        }
        
        # Contar coincidencias por categoría
        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in statement_lower)
            category_scores[category] = score
        
        # Retornar la categoría con más coincidencias
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return 'general'

    def _apply_category_weights(self, similarities, categories, target_weight):
        """Aplica pesos por categoría a las similaridades"""
        weighted_similarities = similarities.copy()
        
        for i, category in enumerate(categories):
            if category in self.category_weights:
                weight = self.category_weights[category]
                # Aplicar peso solo si la similaridad es alta (> 0.3)
                if similarities[0][i] > 0.3:
                    weighted_similarities[0][i] *= weight
        
        return weighted_similarities

    def get_statistics(self) -> Dict:
        """Obtiene estadísticas del modelo y dataset"""
        return {
            "total_statements": self.total_statements,
            "truth_count": self.truth_count,
            "false_count": self.false_count,
            "categories": list(self.categories),
            "is_trained": self.is_trained,
            "model_name": "TF-IDF-Vectorizer-Mejorado",
            "category_weights": self.category_weights,
            "features": self.vectorizer.max_features,
            "ngram_range": self.vectorizer.ngram_range,
        }

    def _load_basic_knowledge(self):
        """Carga conocimiento básico como fallback con categorías"""
        logger.info("Cargando conocimiento básico como fallback...")

        self.truth_statements = [
            "El cielo es azul",
            "El agua hierve a 100 grados Celsius",
            "La Tierra es redonda",
            "Los humanos necesitan oxígeno para vivir",
            "El sol sale por el este",
            "Paris es la capital de Francia",
            "2 + 2 = 4",
            "Los gatos son mamíferos",
            "El fuego es caliente",
            "La gravedad atrae los objetos hacia abajo",
        ]

        self.false_statements = [
            "El cielo es verde",
            "El agua hierve a 50 grados Celsius",
            "La Tierra es plana",
            "Los humanos pueden respirar bajo el agua sin equipo",
            "El sol sale por el oeste",
            "Londres es la capital de Francia",
            "2 + 2 = 5",
            "Los gatos son reptiles",
            "El fuego es frío",
            "La gravedad empuja los objetos hacia arriba",
        ]

        # Asignar categorías básicas
        self.truth_categories = ["ciencia", "ciencia", "ciencia", "ciencia", "ciencia", "geografia", "matematicas", "ciencia", "ciencia", "ciencia"]
        self.false_categories = ["ciencia", "ciencia", "ciencia", "ciencia", "ciencia", "geografia", "matematicas", "ciencia", "ciencia", "ciencia"]

        self.total_statements = len(self.truth_statements) + len(self.false_statements)
        self.truth_count = len(self.truth_statements)
        self.false_count = len(self.false_statements)
        self.categories = {"ciencia", "geografia", "matematicas"}

    def save_model(self, filepath="truth_detector_model.pkl"):
        """Guarda el modelo entrenado mejorado"""
        model_data = {
            "vectorizer": self.vectorizer,
            "category_vectorizer": self.category_vectorizer,
            "truth_embeddings": self.truth_embeddings,
            "false_embeddings": self.false_embeddings,
            "truth_statements": self.truth_statements,
            "false_statements": self.false_statements,
            "truth_categories": self.truth_categories,
            "false_categories": self.false_categories,
            "is_trained": self.is_trained,
            "total_statements": self.total_statements,
            "truth_count": self.truth_count,
            "false_count": self.false_count,
            "categories": list(self.categories),
            "category_weights": self.category_weights,
        }

        with open(filepath, "wb") as f:
            pickle.dump(model_data, f)

        logger.info(f"Modelo guardado en {filepath}")

    def load_model(self, filepath="truth_detector_model.pkl"):
        """Carga un modelo previamente entrenado mejorado"""
        if os.path.exists(filepath):
            try:
                with open(filepath, "rb") as f:
                    model_data = pickle.load(f)

                self.vectorizer = model_data["vectorizer"]
                self.category_vectorizer = model_data.get("category_vectorizer", self.category_vectorizer)
                self.truth_embeddings = model_data["truth_embeddings"]
                self.false_embeddings = model_data["false_embeddings"]
                self.truth_statements = model_data.get("truth_statements", [])
                self.false_statements = model_data.get("false_statements", [])
                self.truth_categories = model_data.get("truth_categories", [])
                self.false_categories = model_data.get("false_categories", [])
                self.is_trained = model_data["is_trained"]
                self.total_statements = model_data.get("total_statements", 0)
                self.truth_count = model_data.get("truth_count", 0)
                self.false_count = model_data.get("false_count", 0)
                self.categories = set(model_data.get("categories", []))
                self.category_weights = model_data.get("category_weights", self.category_weights)

                logger.info(f"Modelo mejorado cargado desde {filepath}")
                logger.info(
                    f"Estadísticas: {self.total_statements} afirmaciones, {self.truth_count} verdaderas, {self.false_count} falsas"
                )
                logger.info(f"Pesos por categoría: {self.category_weights}")
                return True

            except Exception as e:
                logger.error(f"Error cargando modelo: {e}")
                return False
        else:
            logger.info(f"No se encontró el archivo {filepath}")
            return False


# ============================================================================
# MANEJADOR DE CONEXIONES WEBSOCKET
# ============================================================================


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Nueva conexión WebSocket. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(
            f"Conexión WebSocket cerrada. Total: {len(self.active_connections)}"
        )

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remover conexiones muertas
                self.active_connections.remove(connection)


# ============================================================================
# MANEJADOR DE LIFESPAN (REEMPLAZA @app.on_event)
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Inicializando el detector de verdad completo...")

    # Mostrar estadísticas del dataset
    if truth_detector.load_dataset():
        stats = truth_detector.get_statistics()
        logger.info(f"📊 Dataset cargado: {stats['total_statements']} afirmaciones")
        logger.info(
            f"✅ Verdaderas: {stats['truth_count']}, ❌ Falsas: {stats['false_count']}"
        )
        logger.info(f"🏷️ Categorías: {', '.join(stats['categories'])}")

    if not truth_detector.load_model():
        logger.info("🔄 Entrenando nuevo modelo con dataset masivo...")
        # Usar asyncio.to_thread para entrenar en un hilo separado
        await asyncio.to_thread(truth_detector.train)
    else:
        logger.info("✅ Modelo pre-entrenado cargado exitosamente!")

    logger.info("🚀 API lista para recibir solicitudes!")

    yield

    # Shutdown (opcional)
    logger.info("🛑 Cerrando servidor...")


# ============================================================================
# APLICACIÓN FASTAPI
# ============================================================================

# Inicializar FastAPI con lifespan
app = FastAPI(
    title="Truth Detector API - Completo",
    description="API completa para detectar verdad/falsedad usando IA con WebSocket",
    version="3.0.0",
    lifespan=lifespan,
)

# Configurar CORS para React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica tu dominio de React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar el detector de verdad y el manager de conexiones
truth_detector = TruthDetector()
manager = ConnectionManager()

# ============================================================================
# ENDPOINTS HTTP
# ============================================================================


@app.get("/")
async def root():
    stats = truth_detector.get_statistics()
    return {
        "message": "Bienvenido a la API del Detector de Verdad - Versión Completa",
        "version": "3.0.0",
        "model_status": "entrenado" if truth_detector.is_trained else "no entrenado",
        "dataset_stats": {
            "total_statements": stats["total_statements"],
            "truth_count": stats["truth_count"],
            "false_count": stats["false_count"],
            "categories": stats["categories"],
        },
        "endpoints": {
            "websocket": "/ws",
            "http_predict": "/predict",
            "batch_predict": "/predict/batch",
            "statistics": "/statistics",
            "health": "/health",
        },
    }


@app.get("/health")
async def health_check():
    stats = truth_detector.get_statistics()
    return {
        "status": "healthy",
        "model_trained": truth_detector.is_trained,
        "active_connections": len(manager.active_connections),
        "dataset_loaded": stats["total_statements"] > 0,
        "total_statements": stats["total_statements"],
    }


@app.get("/statistics")
async def get_statistics():
    """Obtiene estadísticas del modelo y dataset"""
    return {
        "success": True,
        "model_statistics": truth_detector.get_statistics(),
        "active_connections": len(manager.active_connections),
    }


@app.post("/predict")
async def predict_statement(request: StatementRequest):
    """Endpoint HTTP para predecir si una afirmación es verdadera o falsa"""
    try:
        result = await asyncio.to_thread(truth_detector.predict, request.statement)

        return {
            "success": True,
            "statement": request.statement,
            "result": result,
            "model_info": {
                "total_training_data": result.get("total_training_data", 0),
                "model_status": result.get("model_status", "desconocido"),
            },
        }
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        return {"success": False, "error": str(e)}


@app.post("/predict/batch")
async def predict_batch_statements(request: BatchRequest):
    """Endpoint HTTP para predecir múltiples afirmaciones en lote"""
    try:
        results = []
        for statement in request.statements:
            result = await asyncio.to_thread(truth_detector.predict, statement)
            results.append({"statement": statement, "result": result})

        return {
            "success": True,
            "total_statements": len(request.statements),
            "results": results,
            "model_info": {
                "total_training_data": (
                    results[0]["result"].get("total_training_data", 0) if results else 0
                ),
                "model_status": (
                    results[0]["result"].get("model_status", "desconocido")
                    if results
                    else "desconocido"
                ),
            },
        }
    except Exception as e:
        logger.error(f"Error en predicción por lotes: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# WEBSOCKET
# ============================================================================


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para comunicación en tiempo real con React"""
    await manager.connect(websocket)

    # Obtener estadísticas del modelo
    stats = truth_detector.get_statistics()

    # Enviar mensaje de bienvenida con información del modelo
    welcome_message = {
        "type": "welcome",
        "message": "Conectado al Detector de Verdad - Listo para React",
        "model_info": {
            "status": "entrenado" if truth_detector.is_trained else "no entrenado",
            "total_statements": stats["total_statements"],
            "truth_count": stats["truth_count"],
            "false_count": stats["false_count"],
            "categories": list(stats["categories"]),
        },
        "instructions": "Formato: {'type': 'predict', 'statement': 'tu afirmación aquí'}",
        "features": [
            "Predicción individual",
            "Predicción por lotes",
            "Detección de categorías",
            "Niveles de confianza",
            "Afirmaciones similares",
        ],
    }
    await manager.send_personal_message(json.dumps(welcome_message), websocket)

    try:
        while True:
            # Recibir mensaje del cliente React
            data = await websocket.receive_text()

            try:
                # Parsear el mensaje JSON
                message = json.loads(data)

                if message.get("type") == "predict":
                    statement = message.get("statement", "").strip()

                    if not statement:
                        error_response = {
                            "type": "error",
                            "message": "La afirmación no puede estar vacía",
                        }
                        await manager.send_personal_message(
                            json.dumps(error_response), websocket
                        )
                        continue

                    # Enviar mensaje de procesamiento
                    processing_response = {
                        "type": "processing",
                        "message": f"Analizando: '{statement}'",
                        "model_status": (
                            "entrenado" if truth_detector.is_trained else "no entrenado"
                        ),
                    }
                    await manager.send_personal_message(
                        json.dumps(processing_response), websocket
                    )

                    # Realizar la predicción
                    result = await asyncio.to_thread(truth_detector.predict, statement)

                    # Enviar resultado
                    response = {
                        "type": "prediction",
                        "statement": statement,
                        "result": result,
                        "timestamp": asyncio.get_event_loop().time(),
                        "model_info": {
                            "total_training_data": result.get("total_training_data", 0),
                            "model_status": result.get("model_status", "desconocido"),
                        },
                    }
                    await manager.send_personal_message(json.dumps(response), websocket)

                elif message.get("type") == "predict_batch":
                    statements = message.get("statements", [])

                    if not statements:
                        error_response = {
                            "type": "error",
                            "message": "La lista de afirmaciones no puede estar vacía",
                        }
                        await manager.send_personal_message(
                            json.dumps(error_response), websocket
                        )
                        continue

                    # Enviar mensaje de procesamiento
                    processing_response = {
                        "type": "processing_batch",
                        "message": f"Analizando {len(statements)} afirmaciones en lote",
                        "total_statements": len(statements),
                    }
                    await manager.send_personal_message(
                        json.dumps(processing_response), websocket
                    )

                    # Procesar en lotes
                    batch_results = []
                    for statement in statements:
                        result = await asyncio.to_thread(
                            truth_detector.predict, statement
                        )
                        batch_results.append({"statement": statement, "result": result})

                    # Enviar resultados por lotes
                    batch_response = {
                        "type": "batch_prediction",
                        "total_statements": len(statements),
                        "results": batch_results,
                        "timestamp": asyncio.get_event_loop().time(),
                    }
                    await manager.send_personal_message(
                        json.dumps(batch_response), websocket
                    )

                elif message.get("type") == "get_statistics":
                    # Enviar estadísticas del modelo
                    stats_response = {
                        "type": "statistics",
                        "model_statistics": truth_detector.get_statistics(),
                        "active_connections": len(manager.active_connections),
                    }
                    await manager.send_personal_message(
                        json.dumps(stats_response), websocket
                    )

                elif message.get("type") == "ping":
                    # Responder a ping con pong
                    pong_response = {"type": "pong", "message": "Conexión activa"}
                    await manager.send_personal_message(
                        json.dumps(pong_response), websocket
                    )

                else:
                    # Tipo de mensaje no reconocido
                    error_response = {
                        "type": "error",
                        "message": f"Tipo de mensaje no reconocido: {message.get('type')}",
                        "supported_types": [
                            "predict",
                            "predict_batch",
                            "get_statistics",
                            "ping",
                        ],
                    }
                    await manager.send_personal_message(
                        json.dumps(error_response), websocket
                    )

            except json.JSONDecodeError:
                # Error al parsear JSON
                error_response = {
                    "type": "error",
                    "message": "Formato JSON inválido. Usa: {'type': 'predict', 'statement': 'tu afirmación'}",
                }
                await manager.send_personal_message(
                    json.dumps(error_response), websocket
                )

            except Exception as e:
                # Error general
                logger.error(f"Error en WebSocket: {e}")
                error_response = {
                    "type": "error",
                    "message": f"Error interno: {str(e)}",
                }
                await manager.send_personal_message(
                    json.dumps(error_response), websocket
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Cliente React desconectado")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("🚀 Iniciando Servidor Completo del Detector de Verdad...")
    print("=" * 70)
    print("🤖 IA: Modelo de detección de verdad optimizado (TF-IDF)")
    print("🌐 API: Endpoints HTTP REST completos")
    print("🔌 WebSocket: Comunicación en tiempo real para React")
    print("=" * 70)
    print("🌐 URL del servidor: http://localhost:8000")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("📊 Health check: http://localhost:8000/health")
    print("📈 Estadísticas: http://localhost:8000/statistics")
    print("📖 Documentación: http://localhost:8000/docs")
    print("=" * 70)
    print("🎯 Para conectar desde React:")
    print("   const ws = new WebSocket('ws://localhost:8000/ws');")
    print("   ws.send(JSON.stringify({type: 'predict', statement: 'tu afirmación'}));")
    print("=" * 70)
    print("🛑 Presiona Ctrl+C para detener el servidor")
    print()

    uvicorn.run(
        "truth_detector_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
