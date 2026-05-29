import pandas as pd
import random
from datetime import datetime

sectores = [
    "Piantini",
    "Naco",
    "Bella Vista",
    "Evaristo Morales",
    "Gazcue",
    "Serralles",
    "Los Prados"
]

tipos = [
    "Apartamento",
    "Penthouse",
    "Casa",
    "Studio"
]

propiedades = []

for i in range(1, 101):
    sector = random.choice(sectores)
    tipo = random.choice(tipos)

    habitaciones = random.randint(1, 5)
    banos = random.randint(1, 4)

    metros = random.randint(45, 350)

    precio = metros * random.randint(1200, 3200)

    propiedades.append({
        "id": i,
        "sector": sector,
        "tipo": tipo,
        "habitaciones": habitaciones,
        "banos": banos,
        "metros": metros,
        "precio_usd": precio,
        "fecha_extraccion": datetime.now()
    })

df = pd.DataFrame(propiedades)

df["precio_metro"] = (
    df["precio_usd"] / df["metros"]
).round(2)

df.to_csv(
    "data/raw/properties.csv",
    index=False
)

print("Dataset generado correctamente.")
print(df.head())