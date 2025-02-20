import pandas as pd
import folium
import os



# Mapa
mapa = folium.Map(location=[37, 0], zoom_start=2)


# CSV
file_path = "C:/Users/matheus.dinis_uello/Documents/Programação/Calor/base_uello.csv"

# Carregar os dados
df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)

# Remover linhas onde a coluna "Coordenadas" está vazia
df = df.dropna(subset=["Coordenadas"])

# Separar a coluna "Coordenadas" em "latitude" e "longitude"
df[["latitude", "longitude"]] = df["Coordenadas"].str.split(",", expand=True)

# Converter para tipo numérico
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

# Criar um mapa centralizado na média das coordenadas
mapa = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=12)

# Definir a chave da API corretamente
api_key = '20eac58f4f30435fa113c9fefdd58e88'

# Adicionar o TileLayer com a chave da API
folium.TileLayer(
    tiles=f'https://{{s}}.tile.thunderforest.com/mobile-atlas/{{z}}/{{x}}/{{y}}.png?apikey={api_key}',
    attr='&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    name="Thunderforest.MobileAtlas"
).add_to(mapa)

# Adicionar controle de camadas
folium.LayerControl().add_to(mapa)

# Adicionar marcadores ao mapa
# Adicionar marcadores ao mapa
for _, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['Cidade']} - {row['Micro Setor']}", # Usando a notação de colchetes para acessar a coluna com espaço
        icon = folium.Icon(icon = "glyphicon glyphicon-home", color = "black", icon_color = "white", prefix = "glyphicon"
        )
    ).add_to(mapa)

# Salvar o mapa
mapa_destino = r"C:/Users/matheus.dinis_uello/Documents/Programação/Calor/"
mapa.save(mapa_destino + "mapa.html")

print("Mapa criado! Abra o arquivo 'mapa.html' para visualizar.")