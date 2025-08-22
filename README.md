# 🚀 Detector de Verdad con IA - Sistema Optimizado

Un sistema avanzado de detección de verdad/falsedad usando Inteligencia Artificial, con API REST y WebSocket en tiempo real, entrenado con un dataset masivo de **3,811 afirmaciones**.

## ✨ Características Principales

- **🤖 IA Avanzada**: Modelo basado en embeddings de SentenceTransformer
- **📊 Dataset Masivo**: 3,811 afirmaciones de múltiples categorías
- **🌐 API REST**: Endpoints HTTP para predicciones individuales y por lotes
- **🔌 WebSocket**: Comunicación en tiempo real
- **📈 Estadísticas**: Monitoreo completo del modelo y dataset
- **🏷️ Categorización**: Detección automática de categorías
- **🎯 Alta Precisión**: Niveles de confianza detallados

## 📊 Dataset y Categorías

El sistema incluye afirmaciones en las siguientes categorías:

- **🧮 Matemáticas**: Operaciones, fórmulas, propiedades
- **🔬 Ciencia**: Física, química, biología, constantes
- **🗺️ Geografía**: Países, capitales, ciudades, montañas, ríos
- **📚 Historia**: Eventos históricos, fechas, personajes
- **💻 Tecnología**: Lenguajes, protocolos, frameworks
- **🌌 Astronomía**: Planetas, asteroides, distancias

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

```bash
# Python 3.8+
# pip
# Virtual environment (recomendado)
```

### 2. Clonar y Configurar

```bash
git clone <tu-repositorio>
cd python-real-fake-ia

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Verificar Dataset

El sistema requiere el archivo `super_dataset.csv` con 3,811 afirmaciones. Si no lo tienes, ejecuta:

```bash
python super_data_generator.py
```

## 🎯 Uso del Sistema

### 1. Iniciar el Servidor

```bash
# Opción 1: Servidor completo
python api.py

# Opción 2: Servidor simple
python run_server.py
```

El servidor estará disponible en:
- 🌐 **API**: http://localhost:8000
- 📖 **Documentación**: http://localhost:8000/docs
- 🔌 **WebSocket**: ws://localhost:8000/ws

### 2. Probar el Sistema

```bash
# Ejecutar pruebas automáticas
python test_system.py

# Cliente WebSocket interactivo
python websocket_client.py
```

### 3. Usar la API

#### Predicción Individual (HTTP)

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"statement": "El cielo es azul"}'
```

#### Predicción por Lotes (HTTP)

```bash
curl -X POST "http://localhost:8000/predict/batch" \
     -H "Content-Type: application/json" \
     -d '{"statements": ["2 + 2 = 4", "La Tierra es plana"]}'
```

#### Estadísticas del Modelo

```bash
curl "http://localhost:8000/statistics"
```

### 4. Usar WebSocket

#### Conectar y Predecir

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
    // Enviar afirmación para analizar
    ws.send(JSON.stringify({
        type: 'predict',
        statement: 'El agua hierve a 100°C'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Resultado:', data);
};
```

#### Comandos WebSocket Disponibles

- `{"type": "predict", "statement": "tu afirmación"}` - Predicción individual
- `{"type": "predict_batch", "statements": ["af1", "af2"]}` - Predicción por lotes
- `{"type": "get_statistics"}` - Obtener estadísticas
- `{"type": "ping"}` - Verificar conexión

## 🔧 Estructura del Proyecto

```
python-real-fake-ia/
├── 📊 super_dataset.csv          # Dataset masivo (3,811 afirmaciones)
├── 🤖 truth_detector.py          # Motor de IA optimizado
├── 🌐 api.py                     # API FastAPI con WebSocket
├── 🚀 run_server.py              # Script de inicio del servidor
├── 🧪 test_system.py             # Pruebas del sistema
├── 🔌 websocket_client.py        # Cliente de prueba WebSocket
├── 📈 data_generator.py          # Generador de datos masivos
├── 🚀 super_data_generator.py    # Generador súper combinado
├── 🌐 web_data_scraper.py        # Scraper web optimizado
├── 📋 requirements.txt            # Dependencias
└── 📖 README.md                  # Este archivo
```

## 🎯 Funcionalidades de la IA

### Predicción Inteligente

- **Embeddings Avanzados**: Usa SentenceTransformer para comprensión semántica
- **Similaridad Coseno**: Compara con afirmaciones conocidas
- **Niveles de Confianza**: Muy alta, alta, moderada, baja
- **Explicaciones**: Justifica cada predicción
- **Afirmaciones Similares**: Muestra ejemplos relacionados

### Categorización Automática

- **Detección Inteligente**: Identifica categorías basándose en palabras clave
- **Filtrado por Categoría**: Mejora precisión en dominios específicos
- **Múltiples Fuentes**: Combina datos de diferentes orígenes

## 📈 Rendimiento y Escalabilidad

- **Dataset Masivo**: 3,811 afirmaciones para entrenamiento
- **Entrenamiento Rápido**: Modelo optimizado para velocidad
- **Memoria Eficiente**: Gestión inteligente de embeddings
- **Persistencia**: Guarda y carga modelos entrenados
- **Logging**: Monitoreo completo del sistema

## 🔍 Ejemplos de Uso

### Predicción de Matemáticas

```python
# Input: "2 + 2 = 4"
# Output: 
{
    "prediction": "verdadero",
    "confidence": 0.95,
    "confidence_level": "muy alta",
    "explanation": "La afirmación tiene 95% de similaridad con afirmaciones verdaderas conocidas",
    "most_similar_statement": "2 + 2 = 4",
    "category": "matematicas"
}
```

### Predicción de Ciencia

```python
# Input: "El agua hierve a 100°C"
# Output:
{
    "prediction": "verdadero",
    "confidence": 0.92,
    "confidence_level": "muy alta",
    "explanation": "La afirmación tiene 92% de similaridad con afirmaciones verdaderas conocidas",
    "most_similar_statement": "El agua hierve a 100°C",
    "category": "ciencia"
}
```

## 🚀 Casos de Uso

- **🧠 Educación**: Verificación de hechos en tiempo real
- **📰 Periodismo**: Fact-checking de noticias
- **🔬 Investigación**: Validación de afirmaciones científicas
- **💻 Aplicaciones**: Integración en chatbots y asistentes
- **📊 Análisis**: Procesamiento por lotes de grandes volúmenes

## 🛠️ Desarrollo y Contribución

### Agregar Nuevas Afirmaciones

1. Edita `super_dataset.csv` o usa los generadores
2. Ejecuta `python super_data_generator.py` para regenerar
3. Reinicia el servidor para cargar nuevos datos

### Personalizar el Modelo

- Modifica `truth_detector.py` para cambiar algoritmos
- Ajusta parámetros de embeddings en la clase `TruthDetector`
- Agrega nuevas categorías en `_detect_category()`

### Extender la API

- Agrega nuevos endpoints en `api.py`
- Implementa nuevas funcionalidades WebSocket
- Crea nuevos modelos de datos con Pydantic

## 📊 Monitoreo y Logs

El sistema incluye logging completo:

- **Inicio**: Carga de dataset y entrenamiento
- **Predicciones**: Cada análisis con métricas
- **WebSocket**: Conexiones y desconexiones
- **Errores**: Manejo robusto de excepciones

## 🔒 Seguridad y Producción

### Configuración de Producción

```python
# En api.py, cambiar:
allow_origins=["*"]  # Solo dominios específicos
host="0.0.0.0"       # Solo localhost si es necesario
```

### Rate Limiting

Considera implementar rate limiting para endpoints públicos:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## 🎉 Estado del Proyecto

- ✅ **Dataset Masivo**: 3,811 afirmaciones
- ✅ **IA Optimizada**: Modelo entrenado y funcional
- ✅ **API REST**: Endpoints HTTP completos
- ✅ **WebSocket**: Comunicación en tiempo real
- ✅ **Cliente de Prueba**: Herramientas de testing
- ✅ **Documentación**: Guía completa de uso

## 🤝 Soporte y Contacto

Para problemas, preguntas o contribuciones:

1. Revisa los logs del servidor
2. Ejecuta `python test_system.py` para diagnóstico
3. Verifica que el dataset esté disponible
4. Comprueba que todas las dependencias estén instaladas

## 📚 Recursos Adicionales

- **FastAPI**: https://fastapi.tiangolo.com/
- **SentenceTransformers**: https://www.sbert.net/
- **WebSockets**: https://websockets.readthedocs.io/
- **Pandas**: https://pandas.pydata.org/

---

**🚀 ¡Tu sistema de detección de verdad con IA está listo para usar!**
# python-real-fake
