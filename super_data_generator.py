#!/usr/bin/env python3
"""
Súper Generador de Datos para Entrenamiento de IA
Combina scraping web y generación masiva para obtener miles de afirmaciones
"""

import csv
import random
import time
from typing import List, Dict, Tuple
from web_data_scraper import WebDataScraper
from data_generator import MassiveDataGenerator


class SuperDataGenerator:
    def __init__(self):
        self.dataset = []
        self.web_scraper = WebDataScraper()
        self.massive_generator = MassiveDataGenerator()

    def generate_web_data(self):
        """Obtiene datos del scraper web"""
        print("🌐 Obteniendo datos del scraper web...")

        # Usar el scraper web existente
        self.web_scraper.scrape_all_sources()

        # Copiar los datos al dataset principal
        self.dataset.extend(self.web_scraper.dataset)

        print(f"✅ Datos web agregados: {len(self.web_scraper.dataset)} afirmaciones")
        return len(self.web_scraper.dataset)

    def generate_massive_data(self):
        """Genera datos masivos localmente"""
        print("🚀 Generando datos masivos...")

        # Usar el generador masivo
        self.massive_generator.generate_all_data()

        # Copiar los datos al dataset principal
        self.dataset.extend(self.massive_generator.dataset)

        print(
            f"✅ Datos masivos agregados: {len(self.massive_generator.dataset)} afirmaciones"
        )
        return len(self.massive_generator.dataset)

    def generate_additional_math_variations(self, count=1000):
        """Genera variaciones matemáticas adicionales"""
        print(f"🧮 Generando {count} variaciones matemáticas adicionales...")

        facts_added = 0

        # Generar operaciones más complejas
        for i in range(count):
            # Operaciones básicas con más variaciones
            a = random.randint(1, 200)
            b = random.randint(1, 100)
            c = random.randint(1, 50)

            # Diferentes tipos de operaciones
            operations = [
                (f"{a} + {b} = {a + b}", "matematicas"),
                (f"{a} - {b} = {a - b}", "matematicas"),
                (f"{a} × {b} = {a * b}", "matematicas"),
                (
                    f"{a} ÷ {b} = {a // b}" if b != 0 else f"{a} ÷ 1 = {a}",
                    "matematicas",
                ),
                (f"{a}² = {a**2}", "matematicas"),
                (f"√{a**2} = {a}", "matematicas"),
                (f"{a} + {b} + {c} = {a + b + c}", "matematicas"),
                (f"({a} + {b}) × {c} = {(a + b) * c}", "matematicas"),
            ]

            # Seleccionar operación aleatoria
            statement, category = random.choice(operations)

            # Agregar afirmación verdadera
            self.dataset.append(
                {
                    "statement": statement,
                    "truth_value": "verdadero",
                    "category": category,
                    "source": "variaciones_matematicas",
                }
            )

            # Crear falsedad
            if "=" in statement:
                parts = statement.split("=")
                if len(parts) == 2:
                    # Cambiar el resultado
                    result = eval(parts[1].strip())
                    false_result = result + random.randint(1, 20)
                    false_statement = f"{parts[0]}= {false_result}"

                    self.dataset.append(
                        {
                            "statement": false_statement,
                            "truth_value": "falso",
                            "category": category,
                            "source": "variaciones_matematicas",
                        }
                    )

                    facts_added += 2

        print(f"✅ Agregadas {facts_added} variaciones matemáticas")
        return facts_added

    def generate_science_variations(self, count=500):
        """Genera variaciones científicas adicionales"""
        print(f"🔬 Generando {count} variaciones científicas...")

        facts_added = 0

        # Datos científicos adicionales
        science_data = [
            ("La densidad del oro es 19.32 g/cm³", "ciencia"),
            ("La densidad del plomo es 11.34 g/cm³", "ciencia"),
            ("La densidad del aluminio es 2.70 g/cm³", "ciencia"),
            ("La densidad del cobre es 8.96 g/cm³", "ciencia"),
            ("La densidad del zinc es 7.14 g/cm³", "ciencia"),
            ("El punto de ebullición del alcohol es 78.37°C", "ciencia"),
            ("El punto de ebullición del benceno es 80.1°C", "ciencia"),
            ("El punto de ebullición del tolueno es 110.6°C", "ciencia"),
            ("El punto de ebullición del xileno es 138.4°C", "ciencia"),
            ("El punto de ebullición del naftaleno es 218°C", "ciencia"),
        ]

        for statement, category in science_data:
            # Afirmación verdadera
            self.dataset.append(
                {
                    "statement": statement,
                    "truth_value": "verdadero",
                    "category": category,
                    "source": "variaciones_cientificas",
                }
            )

            # Crear falsedad
            if "es" in statement:
                false_statement = statement.replace("es", "no es")
            elif "del" in statement:
                false_statement = statement.replace("del", "no del")
            else:
                false_statement = f"No es cierto que {statement.lower()}"

            self.dataset.append(
                {
                    "statement": false_statement,
                    "truth_value": "falso",
                    "category": category,
                    "source": "variaciones_cientificas",
                }
            )

            facts_added += 2

        print(f"✅ Agregadas {facts_added} variaciones científicas")
        return facts_added

    def generate_geography_variations(self, count=600):
        """Genera variaciones geográficas adicionales"""
        print(f"🗺️ Generando {count} variaciones geográficas...")

        facts_added = 0

        # Datos geográficos adicionales
        geography_data = [
            ("El Monte Everest tiene 8,848 metros de altura", "geografia"),
            ("El Monte K2 tiene 8,611 metros de altura", "geografia"),
            ("El Monte Kangchenjunga tiene 8,586 metros de altura", "geografia"),
            ("El Monte Lhotse tiene 8,516 metros de altura", "geografia"),
            ("El Monte Makalu tiene 8,485 metros de altura", "geografia"),
            ("El río Nilo tiene 6,650 km de longitud", "geografia"),
            ("El río Amazonas tiene 6,400 km de longitud", "geografia"),
            ("El río Yangtsé tiene 6,300 km de longitud", "geografia"),
            ("El río Mississippi tiene 6,275 km de longitud", "geografia"),
            ("El río Yenisei tiene 5,539 km de longitud", "geografia"),
        ]

        for statement, category in geography_data:
            # Afirmación verdadera
            self.dataset.append(
                {
                    "statement": statement,
                    "truth_value": "verdadero",
                    "category": category,
                    "source": "variaciones_geograficas",
                }
            )

            # Crear falsedad
            if "tiene" in statement:
                false_statement = statement.replace("tiene", "no tiene")
            else:
                false_statement = f"No es cierto que {statement.lower()}"

            self.dataset.append(
                {
                    "statement": false_statement,
                    "truth_value": "falso",
                    "category": category,
                    "source": "variaciones_geograficas",
                }
            )

            facts_added += 2

        print(f"✅ Agregadas {facts_added} variaciones geográficas")
        return facts_added

    def generate_technology_variations(self, count=400):
        """Genera variaciones tecnológicas adicionales"""
        print(f"💻 Generando {count} variaciones tecnológicas...")

        facts_added = 0

        # Datos tecnológicos adicionales
        tech_data = [
            ("React es una biblioteca de JavaScript", "tecnologia"),
            ("Vue.js es un framework progresivo", "tecnologia"),
            ("Angular es un framework de Google", "tecnologia"),
            ("Node.js permite JavaScript en el servidor", "tecnologia"),
            ("Express.js es un framework web para Node.js", "tecnologia"),
            ("MongoDB es una base de datos NoSQL", "tecnologia"),
            ("PostgreSQL es una base de datos relacional", "tecnologia"),
            ("Redis es una base de datos en memoria", "tecnologia"),
            ("Elasticsearch es un motor de búsqueda", "tecnologia"),
            ("Kafka es una plataforma de streaming", "tecnologia"),
        ]

        for statement, category in tech_data:
            # Afirmación verdadera
            self.dataset.append(
                {
                    "statement": statement,
                    "truth_value": "verdadero",
                    "category": category,
                    "source": "variaciones_tecnologicas",
                }
            )

            # Crear falsedad
            if "es" in statement:
                false_statement = statement.replace("es", "no es")
            elif "permite" in statement:
                false_statement = statement.replace("permite", "no permite")
            else:
                false_statement = f"No es cierto que {statement.lower()}"

            self.dataset.append(
                {
                    "statement": false_statement,
                    "truth_value": "falso",
                    "category": category,
                    "source": "variaciones_tecnologicas",
                }
            )

            facts_added += 2

        print(f"✅ Agregadas {facts_added} variaciones tecnológicas")
        return facts_added

    def save_combined_dataset(self, filename="super_dataset.csv"):
        """Guarda el dataset combinado en CSV"""
        print(f"\n💾 Guardando dataset súper combinado...")

        # Mezclar todo el dataset
        random.shuffle(self.dataset)

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["statement", "truth_value", "category", "source"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.dataset:
                writer.writerow(row)

        print(f"💾 Dataset súper combinado guardado en '{filename}'")
        print(f"📊 Total de afirmaciones: {len(self.dataset)}")

        # Estadísticas completas
        sources = {}
        categories = {}
        truth_counts = {"verdadero": 0, "falso": 0}

        for row in self.dataset:
            source = row["source"]
            cat = row["category"]
            truth = row["truth_value"]

            if source not in sources:
                sources[source] = 0
            sources[source] += 1

            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1

            truth_counts[truth] += 1

        print(f"\n📈 Distribución por fuente:")
        for source, count in sorted(sources.items()):
            print(f"   {source}: {count}")

        print(f"\n📊 Distribución por categoría:")
        for cat, count in sorted(categories.items()):
            print(f"   {cat}: {count}")

        print(f"\n🎯 Distribución por veracidad:")
        print(f"   Verdaderas: {truth_counts['verdadero']}")
        print(f"   Falsas: {truth_counts['falso']}")

        print(f"\n🚀 ¡Dataset súper generado completado!")
        print(f"📊 Total final: {len(self.dataset)} afirmaciones")

    def generate_super_dataset(self):
        """Genera el dataset súper completo"""
        print("🚀 Iniciando generación del dataset súper completo...")
        print("=" * 80)

        # Paso 1: Datos del scraper web
        print("\n🌐 PASO 1: Obteniendo datos del scraper web...")
        web_count = self.generate_web_data()

        # Paso 2: Datos masivos generados localmente
        print("\n🚀 PASO 2: Generando datos masivos...")
        massive_count = self.generate_massive_data()

        # Paso 3: Variaciones adicionales
        print("\n✨ PASO 3: Generando variaciones adicionales...")
        math_vars = self.generate_additional_math_variations(1000)
        science_vars = self.generate_science_variations(500)
        geo_vars = self.generate_geography_variations(600)
        tech_vars = self.generate_technology_variations(400)

        # Paso 4: Guardar dataset combinado
        print("\n💾 PASO 4: Guardando dataset súper combinado...")
        self.save_combined_dataset()

        print("\n" + "=" * 80)
        print("🎉 ¡GENERACIÓN SÚPER COMPLETADA!")
        print(f"📊 Resumen final:")
        print(f"   🌐 Datos web: {web_count}")
        print(f"   🚀 Datos masivos: {massive_count}")
        print(f"   🧮 Variaciones matemáticas: {math_vars}")
        print(f"   🔬 Variaciones científicas: {science_vars}")
        print(f"   🗺️ Variaciones geográficas: {geo_vars}")
        print(f"   💻 Variaciones tecnológicas: {tech_vars}")
        print(f"   📊 TOTAL COMBINADO: {len(self.dataset)}")
        print("=" * 80)


def main():
    """Función principal"""
    super_generator = SuperDataGenerator()
    super_generator.generate_super_dataset()


if __name__ == "__main__":
    main()
