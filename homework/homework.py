import pandas as pd
import os
import glob
import zipfile

def open_data():
    # Ruta hacia input
    path = 'files/input'

    # Se abren todos los .zip con glob
    zip_files = glob.glob(f'{path}/*.zip')

    # Se itera sobre cada archivo .zip para abrir sus csv
    for zfile in zip_files:
        # Se abre el archivo .zip
        with zipfile.ZipFile(zfile, 'r') as handler:
            # Se toman solo los archivos .csv
            csv_files = [file for file in handler.namelist() if file.endswith('.csv')]

            # Se itera sobre cada archivo .csv dentro del .zip
            for csv_file in csv_files:
                with handler.open(csv_file) as file:
                    df = pd.read_csv(file)
                    # Se limpian los datos de cada archivo
                    update_client(df)
                    update_campaign(df)
                    update_economics(df)

def update_client(df):
    # Limpieza y selección de columnas
    columnas = ['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']
    df = df[columnas]

    # Limpieza de las columnas 'job' y 'education'
    df['job'] = df['job'].str.replace('.', '').str.replace('-', '_')
    df['education'] = df['education'].str.replace('.', '_').replace('unknown', pd.NA)

    # Limpieza de las columnas 'credit_default' y 'mortgage'
    df['credit_default'] = df['credit_default'].replace({'yes': 1, 'no': 0, 'unknown': 0})
    df['mortgage'] = df['mortgage'].replace({'yes': 1, 'no': 0, 'unknown': 0})

    # Guardado de los datos
    save_data(df, 'client.csv')

def update_campaign(df):
    # Limpieza y selección de columnas
    columnas = ['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 
                'previous_outcome', 'campaign_outcome', 'last_contact_date']
    
    # Limpieza de las columnas 'previous_outcome' y 'campaign_outcome'
    df['previous_outcome'] = df['previous_outcome'].replace({'success': 1, 'failure': 0, 'nonexistent': 0})
    df['campaign_outcome'] = df['campaign_outcome'].replace({'yes': 1, 'no': 0})

    # Creación de la columna 'last_contact_date' combinando 'day' y 'month'
    df['last_contact_date'] = pd.to_datetime('2022-' + df['month'].astype(str) + '-' + df['day'].astype(str))

    # Selección de columnas relevantes
    df = df[columnas]

    # Guardado de los datos
    save_data(df, 'campaign.csv')

def update_economics(df):
    # Limpieza y selección de columnas
    columnas = ['client_id', 'cons_price_idx', 'euribor_three_months']
    df = df[columnas]

    # Guardado de los datos
    save_data(df, 'economics.csv')

def save_data(df, filename):
    # Crear la carpeta 'output' si no existe
    output_dir = 'files/output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ruta de guardado
    ruta = os.path.join(output_dir, filename)

    # Verificar si el archivo ya existe para decidir si incluir encabezado o no
    file_exists = os.path.exists(ruta)
    
    # Guardar el archivo CSV (modo 'a' para append)
    df.to_csv(ruta, mode='a', index=False, header=not file_exists)

def clean_campaign_data():
    # Limpiar archivos previos
    output_dir = 'files/output'
    if os.path.exists(output_dir):
        archivos = glob.glob(f'{output_dir}/*.csv')
        for archivo in archivos:
            os.remove(archivo)

        os.rmdir(output_dir)

    # Procesar los datos
    open_data()

if __name__ == "__main__":
     clean_campaign_data()
