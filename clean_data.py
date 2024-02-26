"""Taller evaluable presencial"""

import pandas as pd


def load_data(input_file):
    """Lea el archivo usando pandas y devuelva un DataFrame"""
    data = pd.read_csv(input_file, sep="\t")
    return data

def create_key(df, n):
    """Cree una nueva columna en el DataFrame que contenga el key de la columna 'text'"""

    df = df.copy()
    df["key"] = df["text"]
    df["key"] = df["key"].str.strip().str.lower().str.replace("-","").str.translate(
           str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
        )
    df["key"] = df["key"].str.split().str.join("").apply(lambda x:[x[i:i+n] for i in range(len(x)-n+1)])
    df["key"] = df["key"].apply(lambda x: sorted(set(x))).str.join("")
    
    return df


def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame"""

    df = df.copy()
    df = df.sort_values(by=["key","text"])
    key = df.groupby("key").first().reset_index()
    key = key.set_index("key")["text"].to_dict()
    df["cleaned"] = df["key"].map(key)

    # Ordene el dataframe por 'key' y 'text'
    # Seleccione la primera fila de cada grupo de 'key'
    # Cree un diccionario con 'key' como clave y 'text' como valor
    # Cree la columna 'cleaned' usando el diccionario

    return df


def save_data(df, output_file):
    """Guarda el DataFrame en un archivo"""

    df = df.copy()
    df = df[["cleaned"]]
    df = df.rename(columns={"cleaned": "text"})
    df.to_csv(output_file, index=False)

data = load_data("input.txt")
print(data)
def main(input_file, output_file, n=2):
    """Ejecuta la limpieza de datos"""

    df = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv("test.csv", index=False)
    save_data(df, output_file)


if __name__ == "__main__":
    main(
        input_file="input.txt",
        output_file="output.txt",
    )
