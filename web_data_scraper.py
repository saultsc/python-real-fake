#!/usr/bin/env python3
"""
Scraper de datos web para obtener verdades irrefutables
Usa múltiples APIs y fuentes web gratuitas
"""

import requests
import csv
import time
from typing import List, Dict, Tuple
import random
import json


class WebDataScraper:
    def __init__(self):
        self.dataset = []
        self.api_keys = {
            "nasa": "DEMO_KEY",  # Gratis para uso básico
            "openweather": None,  # Requiere registro
            "wikidata": None,  # No requiere API key
            "dbpedia": None,  # No requiere API key
        }

    def get_wikidata_countries(self):
        """Obtiene países y capitales de Wikidata"""
        print("🌍 Obteniendo datos de Wikidata...")

        try:
            # Consulta SPARQL más simple y efectiva
            query = """
            SELECT ?country ?capital WHERE {
              ?country wdt:P31 wd:Q3624078 .
              ?country wdt:P36 ?capital .
              ?country wdt:P1448 ?name .
              ?capital wdt:P1448 ?capitalName .
            }
            LIMIT 200
            """

            url = "https://query.wikidata.org/sparql"
            response = requests.get(url, params={"query": query, "format": "json"})

            if response.status_code == 200:
                data = response.json()
                facts_added = 0

                for result in data["results"]["bindings"]:
                    try:
                        country = result["name"]["value"]
                        capital = result["capitalName"]["value"]

                        # Filtrar nombres válidos
                        if (
                            len(country) < 50
                            and len(capital) < 50
                            and not country.isdigit()
                            and not capital.isdigit()
                        ):

                            # Agregar hecho verdadero
                            self.dataset.append(
                                {
                                    "statement": f"{capital} es la capital de {country}",
                                    "truth_value": "verdadero",
                                    "category": "geografia",
                                    "source": "wikidata",
                                }
                            )

                            # Agregar falsedad
                            self.dataset.append(
                                {
                                    "statement": f"{capital} no es la capital de {country}",
                                    "truth_value": "falso",
                                    "category": "geografia",
                                    "source": "wikidata",
                                }
                            )

                            facts_added += 2

                    except Exception as e:
                        continue

                print(f"✅ Agregados {facts_added} hechos de Wikidata")
                return facts_added

        except Exception as e:
            print(f"⚠️ Error obteniendo datos de Wikidata: {e}")
            return 0

    def get_wikidata_elements(self):
        """Obtiene elementos químicos de Wikidata"""
        print("🔬 Obteniendo elementos químicos de Wikidata...")

        try:
            query = """
            SELECT ?element ?symbol ?number WHERE {
              ?element wdt:P31 wd:Q11344 .
              ?element wdt:P246 ?symbol .
              ?element wdt:P1086 ?number .
              ?element wdt:P1448 ?name .
              FILTER(?number <= 50)
            }
            ORDER BY ?number
            LIMIT 50
            """

            url = "https://query.wikidata.org/sparql"
            response = requests.get(url, params={"query": query, "format": "json"})

            if response.status_code == 200:
                data = response.json()
                facts_added = 0

                for result in data["results"]["bindings"]:
                    try:
                        element = result["name"]["value"]
                        symbol = result["symbol"]["value"]
                        number = result["number"]["value"]

                        if len(element) < 30:
                            # Agregar hecho verdadero
                            self.dataset.append(
                                {
                                    "statement": f"El {element} tiene símbolo químico {symbol}",
                                    "truth_value": "verdadero",
                                    "category": "quimica",
                                    "source": "wikidata",
                                }
                            )

                            self.dataset.append(
                                {
                                    "statement": f"El {element} tiene número atómico {number}",
                                    "truth_value": "verdadero",
                                    "category": "quimica",
                                    "source": "wikidata",
                                }
                            )

                            # Agregar falsedades
                            self.dataset.append(
                                {
                                    "statement": f"El {element} no tiene símbolo químico {symbol}",
                                    "truth_value": "falso",
                                    "category": "quimica",
                                    "source": "wikidata",
                                }
                            )

                            facts_added += 3

                    except Exception as e:
                        continue

                print(f"✅ Agregados {facts_added} hechos químicos de Wikidata")
                return facts_added

        except Exception as e:
            print(f"⚠️ Error obteniendo elementos químicos: {e}")
            return 0

    def get_nasa_asteroids(self):
        """Obtiene datos de asteroides de la NASA"""
        print("🚀 Obteniendo datos de asteroides de la NASA...")

        try:
            api_key = self.api_keys["nasa"]
            url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={api_key}&start_date=2024-01-01&end_date=2024-01-07"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                facts_added = 0

                for date, asteroids in data["near_earth_objects"].items():
                    for asteroid in asteroids[:20]:  # Aumentar a 20 por fecha
                        try:
                            name = asteroid["name"]
                            diameter = asteroid["estimated_diameter"]["kilometers"][
                                "estimated_diameter_max"
                            ]
                            distance = asteroid["close_approach_data"][0][
                                "miss_distance"
                            ]["kilometers"]

                            # Agregar hechos verdaderos
                            self.dataset.append(
                                {
                                    "statement": f"El asteroide {name} tiene un diámetro aproximado de {diameter:.2f} km",
                                    "truth_value": "verdadero",
                                    "category": "astronomia",
                                    "source": "nasa",
                                }
                            )

                            self.dataset.append(
                                {
                                    "statement": f"El asteroide {name} pasó a {distance:.0f} km de la Tierra",
                                    "truth_value": "verdadero",
                                    "category": "astronomia",
                                    "source": "nasa",
                                }
                            )

                            facts_added += 2

                        except Exception as e:
                            continue

                print(f"✅ Agregados {facts_added} hechos astronómicos de la NASA")
                return facts_added

        except Exception as e:
            print(f"⚠️ Error obteniendo datos de la NASA: {e}")
            return 0

    def get_basic_facts(self):
        """Genera hechos básicos pero útiles localmente"""
        print("📚 Generando hechos básicos...")

        basic_facts = [
            # Matemáticas básicas
            ("2 + 2 = 4", "matematicas"),
            ("5 × 5 = 25", "matematicas"),
            ("10 ÷ 2 = 5", "matematicas"),
            ("3² = 9", "matematicas"),
            ("√16 = 4", "matematicas"),
            ("7 × 8 = 56", "matematicas"),
            ("15 ÷ 3 = 5", "matematicas"),
            ("4³ = 64", "matematicas"),
            ("√25 = 5", "matematicas"),
            ("12 × 12 = 144", "matematicas"),
            # Ciencias básicas
            ("El agua hierve a 100°C", "ciencia"),
            ("El agua se congela a 0°C", "ciencia"),
            ("La Tierra gira alrededor del Sol", "ciencia"),
            ("Los humanos tienen 206 huesos", "ciencia"),
            ("El corazón humano late 60-100 veces por minuto", "ciencia"),
            ("La velocidad de la luz es 300,000 km/s", "ciencia"),
            ("El ADN es la molécula de la herencia", "ciencia"),
            ("Las plantas realizan fotosíntesis", "ciencia"),
            ("El oxígeno es necesario para la respiración", "ciencia"),
            ("La gravedad atrae los objetos hacia la Tierra", "ciencia"),
            # Geografía básica
            ("Madrid es la capital de España", "geografia"),
            ("París es la capital de Francia", "geografia"),
            ("Londres es la capital de Reino Unido", "geografia"),
            ("Roma es la capital de Italia", "geografia"),
            ("Berlín es la capital de Alemania", "geografia"),
            ("Tokio es la capital de Japón", "geografia"),
            ("Moscú es la capital de Rusia", "geografia"),
            ("Pekín es la capital de China", "geografia"),
            ("Nueva Delhi es la capital de India", "geografia"),
            ("Brasilia es la capital de Brasil", "geografia"),
            # Historia básica
            ("Colón descubrió América en 1492", "historia"),
            ("La Segunda Guerra Mundial terminó en 1945", "historia"),
            ("La Revolución Francesa comenzó en 1789", "historia"),
            ("La independencia de EE.UU. fue en 1776", "historia"),
            ("La caída del Muro de Berlín fue en 1989", "historia"),
            ("Napoleón fue emperador de Francia", "historia"),
            ("La Primera Guerra Mundial fue de 1914-1918", "historia"),
            ("La Revolución Industrial comenzó en el siglo XVIII", "historia"),
            ("La Edad Media duró del siglo V al XV", "historia"),
            ("La Antigua Roma existió antes de Cristo", "historia"),
            # Tecnología básica
            ("Un byte tiene 8 bits", "tecnologia"),
            ("HTML significa HyperText Markup Language", "tecnologia"),
            ("HTTP significa HyperText Transfer Protocol", "tecnologia"),
            ("Un kilobyte tiene 1024 bytes", "tecnologia"),
            ("Un megabyte tiene 1024 kilobytes", "tecnologia"),
            ("Python es un lenguaje de programación", "tecnologia"),
            ("JavaScript se ejecuta en el navegador", "tecnologia"),
            ("Linux es un sistema operativo de código abierto", "tecnologia"),
            ("WiFi permite conexión inalámbrica a internet", "tecnologia"),
            ("Bluetooth es una tecnología de comunicación inalámbrica", "tecnologia"),
        ]

        facts_added = 0

        for fact, category in basic_facts:
            # Agregar hecho verdadero
            self.dataset.append(
                {
                    "statement": fact,
                    "truth_value": "verdadero",
                    "category": category,
                    "source": "basico",
                }
            )

            # Crear falsedad
            if "=" in fact:
                # Para matemáticas, cambiar el resultado
                parts = fact.split("=")
                if len(parts) == 2:
                    false_fact = f"{parts[0]}= {int(parts[1].strip()) + 1}"
                    self.dataset.append(
                        {
                            "statement": false_fact,
                            "truth_value": "falso",
                            "category": category,
                            "source": "basico",
                        }
                    )
            else:
                # Para otros hechos, negar la afirmación
                false_fact = (
                    fact.replace("es", "no es")
                    .replace("tiene", "no tiene")
                    .replace("fue", "no fue")
                )
                self.dataset.append(
                    {
                        "statement": false_fact,
                        "truth_value": "falso",
                        "category": category,
                        "source": "basico",
                    }
                )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos básicos")
        return facts_added

    def get_geonames_data(self):
        """Obtiene datos geográficos de GeoNames (gratis)"""
        print("🗺️ Obteniendo datos de GeoNames...")

        try:
            # GeoNames permite consultas gratuitas sin API key
            # Límite: 20,000 consultas por día

            # Obtener ciudades principales
            url = "http://api.geonames.org/searchJSON"
            params = {
                "q": "city",
                "maxRows": 200,
                "startRow": 0,
                "username": "demo",  # Usuario demo para pruebas
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                facts_added = 0

                for city in data.get("geonames", []):
                    try:
                        city_name = city["name"]
                        country = city["countryName"]
                        population = city.get("population", 0)

                        if population > 100000:  # Solo ciudades grandes
                            # Agregar hecho verdadero
                            self.dataset.append(
                                {
                                    "statement": f"{city_name} es una ciudad de {country}",
                                    "truth_value": "verdadero",
                                    "category": "geografia",
                                    "source": "geonames",
                                }
                            )

                            self.dataset.append(
                                {
                                    "statement": f"{city_name} tiene una población de {population:,} habitantes",
                                    "truth_value": "verdadero",
                                    "category": "geografia",
                                    "source": "geonames",
                                }
                            )

                            facts_added += 2

                    except Exception as e:
                        continue

                print(f"✅ Agregados {facts_added} hechos geográficos de GeoNames")
                return facts_added

        except Exception as e:
            print(f"⚠️ Error obteniendo datos de GeoNames: {e}")
            return 0

    def get_restcountries_data(self):
        """Obtiene datos de países de REST Countries API (gratis)"""
        print("🏳️ Obteniendo datos de países...")

        try:
            url = "https://restcountries.com/v3.1/all"
            response = requests.get(url)

            if response.status_code == 200:
                countries = response.json()
                facts_added = 0

                for country in countries[:150]:  # Aumentar a 150 países
                    try:
                        name = country["name"]["common"]
                        capital = country.get("capital", ["N/A"])[0]
                        population = country.get("population", 0)
                        region = country.get("region", "N/A")
                        area = country.get("area", 0)

                        if capital != "N/A" and population > 0 and region != "N/A":
                            # Agregar hechos verdaderos
                            self.dataset.append(
                                {
                                    "statement": f"{capital} es la capital de {name}",
                                    "truth_value": "verdadero",
                                    "category": "geografia",
                                    "source": "restcountries",
                                }
                            )

                            self.dataset.append(
                                {
                                    "statement": f"{name} está en la región de {region}",
                                    "truth_value": "verdadero",
                                    "category": "geografia",
                                    "source": "restcountries",
                                }
                            )

                            self.dataset.append(
                                {
                                    "statement": f"{name} tiene una población de {population:,} habitantes",
                                    "truth_value": "verdadero",
                                    "category": "geografia",
                                    "source": "restcountries",
                                }
                            )

                            if area > 0:
                                self.dataset.append(
                                    {
                                        "statement": f"{name} tiene un área de {area:,.0f} km²",
                                        "truth_value": "verdadero",
                                        "category": "geografia",
                                        "source": "restcountries",
                                    }
                                )

                            # Agregar falsedades
                            self.dataset.append(
                                {
                                    "statement": f"{capital} no es la capital de {name}",
                                    "truth_value": "falso",
                                    "category": "geografia",
                                    "source": "restcountries",
                                }
                            )

                            facts_added += 5 if area > 0 else 4

                    except Exception as e:
                        continue

                print(f"✅ Agregados {facts_added} hechos de países de REST Countries")
                return facts_added

        except Exception as e:
            print(f"⚠️ Error obteniendo datos de países: {e}")
            return 0

    def get_additional_science_facts(self):
        """Genera hechos científicos adicionales"""
        print("🔬 Generando hechos científicos adicionales...")

        science_facts = [
            ("La temperatura corporal normal es 37°C", "ciencia"),
            ("El pH del agua pura es 7", "ciencia"),
            ("La velocidad del sonido es 343 m/s", "ciencia"),
            ("La masa de la Tierra es 5.97 × 10²⁴ kg", "ciencia"),
            ("La distancia Tierra-Luna es 384,400 km", "ciencia"),
            ("La velocidad de la luz es 299,792,458 m/s", "ciencia"),
            ("El número de Avogadro es 6.022 × 10²³", "ciencia"),
            ("La constante de Planck es 6.626 × 10⁻³⁴ J·s", "ciencia"),
            ("La gravedad en la Tierra es 9.81 m/s²", "ciencia"),
            ("La presión atmosférica es 101,325 Pa", "ciencia"),
            ("El punto de ebullición del nitrógeno es -196°C", "ciencia"),
            ("El punto de fusión del hierro es 1,538°C", "ciencia"),
            ("La densidad del agua es 1 g/cm³", "ciencia"),
            ("El radio de la Tierra es 6,371 km", "ciencia"),
            ("La edad del universo es 13.8 mil millones de años", "ciencia"),
        ]

        facts_added = 0

        for fact, category in science_facts:
            # Agregar hecho verdadero
            self.dataset.append(
                {
                    "statement": fact,
                    "truth_value": "verdadero",
                    "category": category,
                    "source": "ciencia_adicional",
                }
            )

            # Crear falsedad
            if "es" in fact:
                false_fact = fact.replace("es", "no es")
            elif "tiene" in fact:
                false_fact = fact.replace("tiene", "no tiene")
            else:
                false_fact = f"No es cierto que {fact.lower()}"

            self.dataset.append(
                {
                    "statement": false_fact,
                    "truth_value": "falso",
                    "category": category,
                    "source": "ciencia_adicional",
                }
            )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos científicos adicionales")
        return facts_added

    def get_math_facts(self):
        """Genera hechos matemáticos adicionales"""
        print("🧮 Generando hechos matemáticos adicionales...")

        math_facts = [
            ("π (pi) es aproximadamente 3.14159", "matematicas"),
            ("e (número de Euler) es aproximadamente 2.71828", "matematicas"),
            ("φ (número áureo) es aproximadamente 1.61803", "matematicas"),
            ("√2 es aproximadamente 1.41421", "matematicas"),
            ("√3 es aproximadamente 1.73205", "matematicas"),
            ("La suma de los ángulos de un triángulo es 180°", "matematicas"),
            ("La suma de los ángulos de un cuadrilátero es 360°", "matematicas"),
            ("Un círculo tiene 360 grados", "matematicas"),
            ("Un triángulo equilátero tiene 3 lados iguales", "matematicas"),
            ("Un cuadrado tiene 4 lados iguales", "matematicas"),
            ("Un pentágono tiene 5 lados", "matematicas"),
            ("Un hexágono tiene 6 lados", "matematicas"),
            ("La fórmula del área de un círculo es πr²", "matematicas"),
            ("La fórmula del área de un triángulo es (b×h)/2", "matematicas"),
            ("La fórmula del área de un cuadrado es l²", "matematicas"),
        ]

        facts_added = 0

        for fact, category in math_facts:
            # Agregar hecho verdadero
            self.dataset.append(
                {
                    "statement": fact,
                    "truth_value": "verdadero",
                    "category": category,
                    "source": "matematicas_adicional",
                }
            )

            # Crear falsedad
            if "es" in fact:
                false_fact = fact.replace("es", "no es")
            elif "tiene" in fact:
                false_fact = fact.replace("tiene", "no tiene")
            else:
                false_fact = f"No es cierto que {fact.lower()}"

            self.dataset.append(
                {
                    "statement": false_fact,
                    "truth_value": "falso",
                    "category": category,
                    "source": "matematicas_adicional",
                }
            )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos matemáticos adicionales")
        return facts_added

    def get_technology_facts(self):
        """Genera hechos tecnológicos adicionales"""
        print("💻 Generando hechos tecnológicos adicionales...")

        tech_facts = [
            ("TCP/IP es el protocolo de internet", "tecnologia"),
            ("DNS convierte nombres en direcciones IP", "tecnologia"),
            ("HTTP es un protocolo de transferencia", "tecnologia"),
            ("HTTPS es HTTP con cifrado SSL/TLS", "tecnologia"),
            ("FTP es un protocolo de transferencia de archivos", "tecnologia"),
            ("SSH permite conexiones seguras remotas", "tecnologia"),
            ("JSON es un formato de intercambio de datos", "tecnologia"),
            ("XML es un lenguaje de marcado extensible", "tecnologia"),
            ("SQL es un lenguaje de consulta de bases de datos", "tecnologia"),
            ("Git es un sistema de control de versiones", "tecnologia"),
            ("Docker permite contenerización de aplicaciones", "tecnologia"),
            ("Kubernetes orquesta contenedores", "tecnologia"),
            ("REST es un estilo de arquitectura web", "tecnologia"),
            ("GraphQL es un lenguaje de consulta para APIs", "tecnologia"),
            ("Microservicios dividen aplicaciones en servicios", "tecnologia"),
        ]

        facts_added = 0

        for fact, category in tech_facts:
            # Agregar hecho verdadero
            self.dataset.append(
                {
                    "statement": fact,
                    "truth_value": "verdadero",
                    "category": category,
                    "source": "tecnologia_adicional",
                }
            )

            # Crear falsedad
            if "es" in fact:
                false_fact = fact.replace("es", "no es")
            elif "permite" in fact:
                false_fact = fact.replace("permite", "no permite")
            else:
                false_fact = f"No es cierto que {fact.lower()}"

            self.dataset.append(
                {
                    "statement": false_fact,
                    "truth_value": "falso",
                    "category": category,
                    "source": "tecnologia_adicional",
                }
            )

            facts_added += 2

        print(f"✅ Agregados {facts_added} hechos tecnológicos adicionales")
        return facts_added

    def save_to_csv(self, filename="web_scraped_dataset.csv"):
        """Guarda el dataset en CSV"""
        # Mezclar el dataset
        random.shuffle(self.dataset)

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["statement", "truth_value", "category", "source"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.dataset:
                writer.writerow(row)

        print(f"\n💾 Dataset guardado en '{filename}'")
        print(f"📊 Total de afirmaciones: {len(self.dataset)}")

        # Estadísticas por fuente
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

    def scrape_all_sources(self):
        """Obtiene datos de todas las fuentes web"""
        print("🚀 Iniciando scraping de datos web...")
        print("=" * 60)

        # Obtener datos de todas las fuentes
        self.get_basic_facts()  # Hechos básicos garantizados

        self.get_wikidata_countries()
        time.sleep(1)  # Pausa para no sobrecargar las APIs

        self.get_wikidata_elements()
        time.sleep(1)

        self.get_nasa_asteroids()
        time.sleep(1)

        self.get_geonames_data()
        time.sleep(1)

        self.get_restcountries_data()
        time.sleep(1)

        # Agregar hechos adicionales generados localmente
        self.get_additional_science_facts()
        self.get_math_facts()
        self.get_technology_facts()

        # Guardar en CSV
        print("\n💾 Guardando dataset...")
        self.save_to_csv()

        print("\n" + "=" * 60)
        print("🎉 ¡Scraping web completado!")
        print(f"📊 Total de afirmaciones obtenidas: {len(self.dataset)}")
        print(
            f"🌐 Fuentes utilizadas: {len(set([row['source'] for row in self.dataset]))}"
        )


def main():
    """Función principal"""
    scraper = WebDataScraper()
    scraper.scrape_all_sources()


if __name__ == "__main__":
    main()
