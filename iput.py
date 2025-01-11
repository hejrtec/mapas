import gmplot
from geopy.geocoders import Nominatim
import http.server
import socketserver
import webbrowser
import os
import time

def create_map(locations):
    # Cria um objeto Nominatim com um User-Agent personalizado
    geolocator = Nominatim(user_agent="meu_aplicativo_geocoding")

    # Lista para armazenar as coordenadas
    latitudes = []
    longitudes = []

    # Obtém as coordenadas para cada local
    for location in locations:
        if isinstance(location, tuple) and len(location) == 2:
            # Se já for uma tupla de (latitude, longitude)
            lat, lon = location
        else:
            # Geocodifica o endereço
            try:
                location = geolocator.geocode(location)
                if location:
                    lat, lon = location.latitude, location.longitude
                else:
                    print(f"Endereço não encontrado: {location}")
                    continue
            except Exception as e:
                print(f"Erro ao geocodificar {location}: {e}")
                continue
        
        latitudes.append(lat)
        longitudes.append(lon)
        time.sleep(1)  # Espera 1 segundo entre as solicitações

    # Cria o mapa
    gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 10)  # Centro do mapa na primeira localização

    # Adiciona os pontos ao mapa
    gmap.scatter(latitudes, longitudes, color='red', size=40, marker=True)

    # Salva o mapa em um arquivo HTML
    gmap.draw("map.html")
    print("Mapa gerado: map.html")

    # Inicia um servidor HTTP para servir o arquivo HTML
    PORT = 8000
    os.chdir(os.path.dirname(os.path.abspath("map.html")))  # Muda o diretório para onde o map.html está
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Servidor HTTP iniciado na porta {PORT}")
        webbrowser.open(f"http://localhost:{PORT}/map.html")  # Abre o navegador automaticamente
        httpd.serve_forever()

# Solicita ao usuário que insira localizações
user_input = input("Digite as localizações desejadas (separadas por vírgula): ")
locations = [loc.strip() for loc in user_input.split(',')]  # Divide a entrada em uma lista

create_map(locations)