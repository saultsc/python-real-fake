#!/usr/bin/env python3
"""
🧪 Script de Prueba para el Modelo Mejorado
Prueba las mejoras de afinidad implementadas en el detector de verdad
"""

import sys
import os
import time
import pandas as pd
from truth_detector_server import TruthDetector

def test_model_improvements():
    """Prueba las mejoras del modelo mejorado"""
    print("🚀 Probando Modelo Mejorado de Detección de Verdad")
    print("=" * 60)
    
    # Inicializar detector
    detector = TruthDetector()
    
    # Cargar dataset
    print("📊 Cargando dataset...")
    if not detector.load_dataset():
        print("❌ Error cargando dataset")
        return
    
    print(f"✅ Dataset cargado: {detector.total_statements} afirmaciones")
    print(f"📈 Verdaderas: {detector.truth_count}, Falsas: {detector.false_count}")
    print(f"🏷️ Categorías: {', '.join(sorted(detector.categories))}")
    print(f"⚖️ Pesos por categoría: {detector.category_weights}")
    print()
    
    # Entrenar modelo
    print("🧠 Entrenando modelo mejorado...")
    start_time = time.time()
    detector.train()
    training_time = time.time() - start_time
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    print()
    
    # Casos de prueba por categoría
    test_cases = {
        "matematicas": [
            "2 + 2 = 4",
            "15 × 7 = 105",
            "√144 = 12",
            "50 ÷ 10 = 5",
            "3² = 9",
            "100 - 25 = 75"
        ],
        "ciencia": [
            "El agua hierve a 100°C",
            "La gravedad es 9.81 m/s²",
            "Los humanos tienen 206 huesos",
            "La temperatura corporal normal es 37°C",
            "El oxígeno es necesario para respirar",
            "Las plantas realizan fotosíntesis"
        ],
        "geografia": [
            "Madrid es la capital de España",
            "París es la capital de Francia",
            "Tokio es la capital de Japón",
            "Brasilia es la capital de Brasil",
            "Canberra es la capital de Australia",
            "Ottawa es la capital de Canadá"
        ],
        "tecnologia": [
            "Python es un lenguaje de programación",
            "Linux es un sistema operativo de código abierto",
            "HTML es un lenguaje de marcado",
            "JavaScript es un lenguaje de programación",
            "HTTP es un protocolo de comunicación",
            "Git es un sistema de control de versiones"
        ],
        "astronomia": [
            "La Tierra orbita alrededor del Sol",
            "La Luna orbita alrededor de la Tierra",
            "Marte es el cuarto planeta del sistema solar",
            "El Sol es una estrella",
            "La Vía Láctea es una galaxia",
            "Júpiter es el planeta más grande del sistema solar"
        ]
    }
    
    print("🧪 Probando casos por categoría...")
    print("=" * 60)
    
    total_correct = 0
    total_tests = 0
    
    for category, statements in test_cases.items():
        print(f"\n🏷️ Categoría: {category.upper()}")
        print("-" * 40)
        
        category_correct = 0
        category_tests = len(statements)
        
        for i, statement in enumerate(statements, 1):
            print(f"\n{i}. Afirmación: {statement}")
            
            # Predecir
            result = detector.predict(statement)
            
            # Mostrar resultado
            prediction = result["prediction"]
            confidence = result["confidence"]
            confidence_level = result["confidence_level"]
            detected_category = result["detected_category"]
            category_weight = result["category_weight"]
            
            print(f"   📊 Predicción: {prediction.upper()}")
            print(f"   🎯 Confianza: {confidence:.2%} ({confidence_level})")
            print(f"   🏷️ Categoría detectada: {detected_category}")
            print(f"   ⚖️ Peso de categoría: {category_weight}")
            
            # Verificar si la predicción es correcta (estas son afirmaciones verdaderas)
            if prediction == "verdadero":
                category_correct += 1
                total_correct += 1
                print("   ✅ CORRECTO")
            else:
                print("   ❌ INCORRECTO")
            
            total_tests += 1
            
            # Mostrar métricas adicionales si están disponibles
            if "max_true_similarity" in result:
                print(f"   📈 Max similaridad verdadera: {result['max_true_similarity']:.3f}")
                print(f"   📉 Max similaridad falsa: {result['max_false_similarity']:.3f}")
                print(f"   📊 Promedio verdadero: {result['avg_true_similarity']:.3f}")
                print(f"   📊 Promedio falso: {result['avg_false_similarity']:.3f}")
        
        # Estadísticas de la categoría
        category_accuracy = (category_correct / category_tests) * 100
        print(f"\n📊 Precisión en {category}: {category_accuracy:.1f}% ({category_correct}/{category_tests})")
    
    # Estadísticas generales
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS GENERALES")
    print("=" * 60)
    
    overall_accuracy = (total_correct / total_tests) * 100
    print(f"🎯 Precisión general: {overall_accuracy:.1f}% ({total_correct}/{total_tests})")
    
    # Información del modelo
    stats = detector.get_statistics()
    print(f"🤖 Modelo: {stats['model_name']}")
    print(f"🔧 Features: {stats['features']}")
    print(f"📝 N-gramas: {stats['ngram_range']}")
    print(f"📊 Total de datos de entrenamiento: {stats['total_statements']}")
    
    # Guardar modelo mejorado
    print("\n💾 Guardando modelo mejorado...")
    detector.save_model("truth_detector_improved.pkl")
    print("✅ Modelo guardado como 'truth_detector_improved.pkl'")
    
    return overall_accuracy

def test_edge_cases():
    """Prueba casos límite y difíciles"""
    print("\n🔍 Probando casos límite...")
    print("=" * 60)
    
    detector = TruthDetector()
    
    # Cargar modelo si existe
    if not detector.load_model("truth_detector_improved.pkl"):
        print("⚠️ No se encontró modelo mejorado, entrenando uno nuevo...")
        detector.load_dataset()
        detector.train()
    
    edge_cases = [
        "La suma de los ángulos internos de un triángulo es 180 grados",
        "El punto de ebullición del agua a nivel del mar es 100°C",
        "La velocidad de la luz en el vacío es aproximadamente 299,792,458 m/s",
        "La población de China es mayor a 1.4 mil millones de personas",
        "El sistema solar tiene 8 planetas",
        "La fórmula química del agua es H2O",
        "El ADN es la molécula que contiene la información genética",
        "La Tierra tarda 365.25 días en orbitar alrededor del Sol"
    ]
    
    print("🧪 Casos límite (afirmaciones complejas):")
    for i, statement in enumerate(edge_cases, 1):
        print(f"\n{i}. {statement}")
        
        result = detector.predict(statement)
        
        print(f"   📊 Predicción: {result['prediction'].upper()}")
        print(f"   🎯 Confianza: {result['confidence']:.2%} ({result['confidence_level']})")
        print(f"   🏷️ Categoría: {result['detected_category']}")
        
        if result['confidence'] < 0.3:
            print("   ⚠️ BAJA CONFIANZA - Caso difícil detectado")

if __name__ == "__main__":
    try:
        # Probar mejoras principales
        accuracy = test_model_improvements()
        
        # Probar casos límite
        test_edge_cases()
        
        print(f"\n🎉 ¡Pruebas completadas! Precisión general: {accuracy:.1f}%")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
