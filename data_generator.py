#!/usr/bin/env python3
"""
Generador masivo de datos para entrenamiento de IA
Genera miles de afirmaciones verdaderas y falsas
"""

import csv
import random
import json
from typing import List, Dict, Tuple


class MassiveDataGenerator:
    def __init__(self):
        self.dataset = []

    def generate_math_facts(self, count=500):
        """Genera hechos matemáticos masivamente"""
        print(f"🧮 Generando {count} hechos matemáticos...")

        operations = [
            ("+", lambda x, y: x + y),
            ("-", lambda x, y: x - y),
            ("×", lambda x, y: x * y),
            ("÷", lambda x, y: x // y if y != 0 else 0),
        ]

        facts_added = 0

        for i in range(count):
            # Generar números aleatorios
            a = random.randint(1, 100)
            b = random.randint(1, 50)

            # Seleccionar operación aleatoria
            op_symbol, op_func = random.choice(operations)

            # Calcular resultado correcto
            if op_symbol == "÷" and b == 0:
                b = 1  # Evitar división por cero

            result = op_func(a, b)

            # Crear afirmación verdadera
            true_statement = f"{a} {op_symbol} {b} = {result}"
            self.dataset.append(
                {
                    "statement": true_statement,
                    "truth_value": "verdadero",
                    "category": "matematicas",
                    "source": "generador_masivo",
                }
            )

            # Crear afirmación falsa (resultado incorrecto)
            false_result = result + random.randint(1, 10)
            false_statement = f"{a} {op_symbol} {b} = {false_result}"
            self.dataset.append(
                {
                    "statement": false_statement,
                    "truth_value": "falso",
                    "category": "matematicas",
                    "source": "generador_masivo",
                }
            )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos matemáticos")
        return facts_added

    def generate_science_facts(self, count=300):
        """Genera hechos científicos masivamente"""
        print(f"🔬 Generando {count} hechos científicos...")

        # Datos científicos base
        temperatures = {
            "agua": {"ebullicion": 100, "congelacion": 0},
            "nitrogeno": {"ebullicion": -196, "congelacion": -210},
            "oxigeno": {"ebullicion": -183, "congelacion": -218},
            "hierro": {"ebullicion": 2862, "congelacion": 1538},
            "mercurio": {"ebullicion": 357, "congelacion": -39},
        }

        constants = {
            "velocidad_luz": 299792458,
            "gravedad_tierra": 9.81,
            "velocidad_sonido": 343,
            "numero_avogadro": 6.022e23,
            "constante_planck": 6.626e-34,
        }

        facts_added = 0

        # Generar hechos de temperatura
        for substance, temps in temperatures.items():
            for temp_type, temp_value in temps.items():
                # Afirmación verdadera
                true_statement = f"El {substance} {temp_type} a {temp_value}°C"
                self.dataset.append(
                    {
                        "statement": true_statement,
                        "truth_value": "verdadero",
                        "category": "ciencia",
                        "source": "generador_masivo",
                    }
                )

                # Afirmación falsa
                false_temp = temp_value + random.randint(5, 20)
                false_statement = f"El {substance} {temp_type} a {false_temp}°C"
                self.dataset.append(
                    {
                        "statement": false_statement,
                        "truth_value": "falso",
                        "category": "ciencia",
                        "source": "generador_masivo",
                    }
                )

                facts_added += 2

        # Generar hechos de constantes
        for constant, value in constants.items():
            # Afirmación verdadera
            true_statement = f"La {constant.replace('_', ' ')} es {value}"
            self.dataset.append(
                {
                    "statement": true_statement,
                    "truth_value": "verdadero",
                    "category": "ciencia",
                    "source": "generador_masivo",
                }
            )

            # Afirmación falsa
            false_value = value * random.uniform(0.8, 1.2)
            false_statement = f"La {constant.replace('_', ' ')} es {false_value:.2e}"
            self.dataset.append(
                {
                    "statement": false_statement,
                    "truth_value": "falso",
                    "category": "ciencia",
                    "source": "generador_masivo",
                }
            )

            facts_added += 2

        # Generar hechos adicionales aleatorios
        remaining_count = count - facts_added
        for i in range(remaining_count // 2):
            # Hechos verdaderos sobre el cuerpo humano
            body_facts = [
                ("El corazón humano late 60-100 veces por minuto", True),
                ("Los humanos tienen 206 huesos", True),
                ("El cerebro humano pesa aproximadamente 1.4 kg", True),
                ("La temperatura corporal normal es 37°C", True),
                ("Los humanos tienen 5 sentidos", True),
            ]

            fact, is_true = random.choice(body_facts)
            self.dataset.append(
                {
                    "statement": fact,
                    "truth_value": "verdadero" if is_true else "falso",
                    "category": "ciencia",
                    "source": "generador_masivo",
                }
            )

            # Crear falsedad
            false_fact = fact.replace("es", "no es").replace("tiene", "no tiene")
            self.dataset.append(
                {
                    "statement": false_fact,
                    "truth_value": "falso",
                    "category": "ciencia",
                    "source": "generador_masivo",
                }
            )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos científicos")
        return facts_added

    def generate_geography_facts(self, count=400):
        """Genera hechos geográficos masivamente"""
        print(f"🗺️ Generando {count} hechos geográficos...")

        # Datos de países y capitales
        countries_data = [
            ("España", "Madrid", "Europa", 46736728),
            ("Francia", "París", "Europa", 67391582),
            ("Alemania", "Berlín", "Europa", 83190556),
            ("Italia", "Roma", "Europa", 60461826),
            ("Reino Unido", "Londres", "Europa", 67886011),
            ("Japón", "Tokio", "Asia", 125836021),
            ("China", "Pekín", "Asia", 1439323776),
            ("India", "Nueva Delhi", "Asia", 1380004385),
            ("Brasil", "Brasilia", "América del Sur", 212559417),
            ("México", "Ciudad de México", "América del Norte", 128932753),
            ("Canadá", "Ottawa", "América del Norte", 37742154),
            ("Australia", "Canberra", "Oceanía", 25499884),
            ("Rusia", "Moscú", "Europa/Asia", 144104080),
            ("Sudáfrica", "Pretoria", "África", 59308690),
            ("Egipto", "El Cairo", "África", 102334404),
        ]

        facts_added = 0

        for country, capital, region, population in countries_data:
            # Hechos verdaderos
            self.dataset.append(
                {
                    "statement": f"{capital} es la capital de {country}",
                    "truth_value": "verdadero",
                    "category": "geografia",
                    "source": "generador_masivo",
                }
            )

            self.dataset.append(
                {
                    "statement": f"{country} está en {region}",
                    "truth_value": "verdadero",
                    "category": "geografia",
                    "source": "generador_masivo",
                }
            )

            self.dataset.append(
                {
                    "statement": f"{country} tiene una población de {population:,} habitantes",
                    "truth_value": "verdadero",
                    "category": "geografia",
                    "source": "generador_masivo",
                }
            )

            # Hechos falsos
            self.dataset.append(
                {
                    "statement": f"{capital} no es la capital de {country}",
                    "truth_value": "falso",
                    "category": "geografia",
                    "source": "generador_masivo",
                }
            )

            false_population = population + random.randint(1000000, 10000000)
            self.dataset.append(
                {
                    "statement": f"{country} tiene una población de {false_population:,} habitantes",
                    "truth_value": "falso",
                    "category": "geografia",
                    "source": "generador_masivo",
                }
            )

            facts_added += 5

        # Generar hechos adicionales sobre ciudades
        cities = [
            ("Nueva York", "Estados Unidos", 8336817),
            ("Los Ángeles", "Estados Unidos", 3979576),
            ("Chicago", "Estados Unidos", 2693976),
            ("Toronto", "Canadá", 2930000),
            ("Sídney", "Australia", 5312163),
            ("Melbourne", "Australia", 5078196),
            ("São Paulo", "Brasil", 12252023),
            ("Río de Janeiro", "Brasil", 6747815),
            ("Buenos Aires", "Argentina", 3075646),
            ("Lima", "Perú", 9562280),
        ]

        for city, country, population in cities:
            # Hecho verdadero
            self.dataset.append(
                {
                    "statement": f"{city} es una ciudad de {country}",
                    "truth_value": "verdadero",
                    "category": "geografia",
                    "source": "generador_masivo",
                }
            )

            # Hecho falso
            false_country = random.choice([c[1] for c in cities if c[1] != country])
            self.dataset.append(
                {
                    "statement": f"{city} es una ciudad de {false_country}",
                    "truth_value": "falso",
                    "category": "geografia",
                    "source": "generador_masivo",
                }
            )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos geográficos")
        return facts_added

    def generate_history_facts(self, count=300):
        """Genera hechos históricos masivamente"""
        print(f"📚 Generando {count} hechos históricos...")

        # Datos históricos
        historical_events = [
            ("Colón", "descubrió", "América", 1492),
            ("Napoleón", "fue", "emperador de Francia", 1804),
            ("Hitler", "llegó al poder en", "Alemania", 1933),
            ("Kennedy", "fue asesinado en", "1963", 1963),
            ("Gandhi", "lideró la independencia de", "India", 1947),
            ("Einstein", "publicó la teoría de la", "relatividad", 1905),
            ("Mozart", "nació en", "1756", 1756),
            ("Shakespeare", "escribió", "Romeo y Julieta", 1597),
            ("Da Vinci", "pintó la", "Mona Lisa", 1503),
            ("Newton", "descubrió la", "gravedad", 1687),
        ]

        facts_added = 0

        for person, action, what, year in historical_events:
            # Hecho verdadero
            self.dataset.append(
                {
                    "statement": f"{person} {action} {what} en {year}",
                    "truth_value": "verdadero",
                    "category": "historia",
                    "source": "generador_masivo",
                }
            )

            # Hecho falso (año incorrecto)
            false_year = year + random.randint(10, 100)
            self.dataset.append(
                {
                    "statement": f"{person} {action} {what} en {false_year}",
                    "truth_value": "falso",
                    "category": "historia",
                    "source": "generador_masivo",
                }
            )

            facts_added += 2

        # Generar hechos sobre guerras
        wars = [
            ("Primera Guerra Mundial", 1914, 1918),
            ("Segunda Guerra Mundial", 1939, 1945),
            ("Guerra Fría", 1947, 1991),
            ("Guerra de Vietnam", 1955, 1975),
            ("Guerra de Corea", 1950, 1953),
        ]

        for war, start, end in wars:
            # Hecho verdadero
            self.dataset.append(
                {
                    "statement": f"La {war} duró de {start} a {end}",
                    "truth_value": "verdadero",
                    "category": "historia",
                    "source": "generador_masivo",
                }
            )

            # Hecho falso
            false_duration = (
                f"{start + random.randint(1, 5)} a {end + random.randint(1, 5)}"
            )
            self.dataset.append(
                {
                    "statement": f"La {war} duró de {false_duration}",
                    "truth_value": "falso",
                    "category": "historia",
                    "source": "generador_masivo",
                }
            )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos históricos")
        return facts_added

    def generate_technology_facts(self, count=300):
        """Genera hechos tecnológicos masivamente"""
        print(f"💻 Generando {count} hechos tecnológicos...")

        # Datos tecnológicos
        tech_concepts = [
            ("HTML", "es un lenguaje de marcado", "web"),
            ("CSS", "se usa para estilos", "web"),
            ("JavaScript", "es un lenguaje de programación", "web"),
            ("Python", "es un lenguaje interpretado", "programacion"),
            ("Java", "es un lenguaje compilado", "programacion"),
            ("C++", "es un lenguaje de bajo nivel", "programacion"),
            ("SQL", "es un lenguaje de bases de datos", "databases"),
            ("MongoDB", "es una base de datos NoSQL", "databases"),
            ("Docker", "permite contenerización", "devops"),
            ("Kubernetes", "orquesta contenedores", "devops"),
        ]

        facts_added = 0

        for tech, description, category in tech_concepts:
            # Hecho verdadero
            self.dataset.append(
                {
                    "statement": f"{tech} {description}",
                    "truth_value": "verdadero",
                    "category": "tecnologia",
                    "source": "generador_masivo",
                }
            )

            # Hecho falso
            false_description = description.replace("es", "no es").replace(
                "se usa", "no se usa"
            )
            self.dataset.append(
                {
                    "statement": f"{tech} {false_description}",
                    "truth_value": "falso",
                    "category": "tecnologia",
                    "source": "generador_masivo",
                }
            )

            facts_added += 2

        # Generar hechos sobre protocolos
        protocols = [
            ("HTTP", "HyperText Transfer Protocol"),
            ("HTTPS", "HTTP Secure"),
            ("FTP", "File Transfer Protocol"),
            ("SSH", "Secure Shell"),
            ("SMTP", "Simple Mail Transfer Protocol"),
        ]

        for protocol, full_name in protocols:
            # Hecho verdadero
            self.dataset.append(
                {
                    "statement": f"{protocol} significa {full_name}",
                    "truth_value": "verdadero",
                    "category": "tecnologia",
                    "source": "generador_masivo",
                }
            )

            # Hecho falso
            false_name = full_name.replace("Transfer", "Transport").replace(
                "Secure", "Safe"
            )
            self.dataset.append(
                {
                    "statement": f"{protocol} significa {false_name}",
                    "truth_value": "falso",
                    "category": "tecnologia",
                    "source": "generador_masivo",
                }
            )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos tecnológicos")
        return facts_added

    def save_to_csv(self, filename="massive_dataset.csv"):
        """Guarda el dataset masivo en CSV"""
        # Mezclar el dataset
        random.shuffle(self.dataset)

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["statement", "truth_value", "category", "source"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.dataset:
                writer.writerow(row)

        print(f"\n💾 Dataset masivo guardado en '{filename}'")
        print(f"📊 Total de afirmaciones: {len(self.dataset)}")

        # Estadísticas
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

    def generate_all_data(self):
        """Genera todos los tipos de datos"""
        print("🚀 Iniciando generación masiva de datos...")
        print("=" * 60)

        # Generar datos de todas las categorías
        self.generate_math_facts(500)
        self.generate_science_facts(300)
        self.generate_geography_facts(400)
        self.generate_history_facts(300)
        self.generate_technology_facts(300)

        # Guardar en CSV
        print("\n💾 Guardando dataset masivo...")
        self.save_to_csv()

        print("\n" + "=" * 60)
        print("🎉 ¡Generación masiva completada!")
        print(f"📊 Total de afirmaciones generadas: {len(self.dataset)}")


def main():
    """Función principal"""
    generator = MassiveDataGenerator()
    generator.generate_all_data()


if __name__ == "__main__":
    main()
