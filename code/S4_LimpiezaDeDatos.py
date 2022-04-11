import os
import urllib3
import requests
import pandas as pd

# Variables globales
mainpath = "../datasets"
medals_url = "http://winterolympicsmedals.com/medals.csv"


# Función para carga de datos a través de la función read_csv
def read_data():
    filename = "titanic/titanic3.csv"
    fullpath = os.path.join(mainpath, filename)
    data_0 = pd.read_csv(fullpath)
    print("Primer datasets: \n{}".format(data_0))

    """ Parámetros de la función read_csv:
        dtype = cambia el formato de las columnas indicadas
        header = elige la fila que será la cabecera o nombre de las columnas
        names = cambia los nombres de las columnas por las indicadas
        skiprows = comienza el dataframe desde la fila siguiente a la que se indica
        index_col = elige la columna que será el index del dataframe
        skip_blank_lines = salta las líneas en blanco
        na_filter = si es False, cambia los valores NaN por vacios. Si es True, deja los valores como NaN o predeterminados 
    Ejemplo: 
        data = pd.read_csv(filepath_or_buffer="../datasets/titanic/titanic3.csv", sep=",", dtype={"ingresos": np.float64, "edad": np.int32}, header=0, names=["ingresos", "edad"], skiprows=12, index_col=None, skip_blank_lines=False, na_filter=False) """

    data_1 = pd.read_csv(filepath_or_buffer=fullpath, sep=",", skip_blank_lines=True, na_filter=False)
    print("\nSegundo datasets: \n{}".format(data_1))

    # Para cambiar la cabecera a partir de un fichero a parte del datasets
    data_2_cols = pd.read_csv("{}/customer-churn-model/Customer Churn Columns.csv".format(mainpath))
    data_2_col_list = data_2_cols["Column_Names"].to_list()
    data_2 = pd.read_csv("{}/customer-churn-model/Customer Churn Model.txt".format(mainpath), header=None, names=data_2_col_list, skiprows=1)
    print("\nTercer datasets: \n{}".format(data_2))


# Función para leer datos de forma manual (se suele utilizar cuando son ficheros muy grandes, 5G o más)
def read_data_manual():
    # Abre el fichero en modo read ('r'), si se desea escribir (se borra todo el contenido) se utiliza el modo write ('w'). Si por el contrario se desea agregar contenido sin borrar lo que ya existe se utiliza el modo append ('a')
    data_3 = open("{}/customer-churn-model/Customer Churn Model.txt".format(mainpath), "r")

    # Recorre la primera fila para obtener los nombres de la columnas y data_3 ya se ubica en la siguiente fila automaticamente
    cols = data_3.readline().strip().split(",")
    n_cols = len(cols)

    # Contador para las filas
    counter = 0
    main_dict = dict()

    # Inicializa el diccionario con las columnas = lista de las celdas asignadas por columnas
    for col in cols:
        main_dict[col] = list()

    # Almacena en el main_dict cada celda de las filas recorridas
    for line in data_3:
        values = line.strip().split(",")
        for i in range(len(cols)):
            main_dict[cols[i]].append(values[i])
        counter += 1

    print("El dataset tiene {0} filas y {1} columnas".format(counter, n_cols))

    # Convierte el diccionario en un dataframe
    df3 = pd.DataFrame(main_dict)
    print("\nDataset convertido a Dataframe con la libreria pandas: \n{}".format(df3))


# Función para lectura y escritura de fichero de forma manual separados por tabulador (\t)
def write_data_manual():
    infile = "{}/customer-churn-model/Customer Churn Model.txt".format(mainpath)
    outfile = "{}/customer-churn-model/Tab Customer Churn Model.txt".format(mainpath)

    with open(infile, 'r') as infile1:
        with open(outfile, 'w') as outfile1:
            for line in infile1:
                fields = line.strip().split(",")
                outfile1.write("\t".join(fields))
                outfile1.write("\n")

    df4 = pd.read_csv(outfile, sep="\t")
    print("\nDataset separado por \\t: \n{}".format(df4))


# Función para leer datos desde una URL
def read_url():
    # Almacenar los datos en dataframe utilizando la librería pandas
    medals_data = pd.read_csv(medals_url)
    print("\nDataset descargado de URL: \n{}".format(medals_data))


# Función para leer fichero xls y xlsx
def read_xls():
    filename_1 = "titanic/titanic3.xls"
    filename_2 = "titanic/titanic3.xlsx"
    fullpath_1 = os.path.join(mainpath, filename_1)
    fullpath_2 = os.path.join(mainpath, filename_2)
    titanic2 = pd.read_excel(fullpath_1, "titanic3")
    titanic3 = pd.read_excel(fullpath_2, "titanic3")

    print("\nDataset del fichero xls: \n{}".format(titanic2))
    print("\nDataset del fichero xlsx: \n{}".format(titanic3))

    titanic2.to_csv(mainpath + "/titanic/titanic_custom.csv")
    titanic3.to_excel(mainpath + "/titanic/titanic_custom.xls")
    titanic3.to_json(mainpath + "/titanic/titanic_custom.json")


# Función para leer los datos de una URL externa, procesarlos y convertirlos a un DataFrame para posteriormente guardarlos en un .csv, .json y .xlsx
def get_data_url():
    # Exportar la información con la librería urllib3
    http = urllib3.PoolManager()
    result_1 = http.request('GET', medals_url)
    data_1 = result_1.data

    # El objeto data_1 contiene un string binario, se descodifica a 'utf-8'
    data_1 = data_1.decode('utf-8')

    # Se divide el string en un array de filas
    row = data_1.split("\n")

    # Se extrae la 1ra línea ya que contiene la cabecera
    col_names = row[0].split(",")
    n_cols = len(col_names)

    # Contador para las filas
    counter = 0
    main_dict = dict()

    # Inicializa el diccionario con las columnas = lista de las celdas asignadas por columnas
    for col in col_names:
        main_dict[col] = list()

    # Almacena en el main_dict cada celda de las filas recorridas
    for line in row:
        # Se obvia la primera fila que contiene la cabecera
        if counter > 0:
            values = line.strip().split(",")
            # Se añade cada valor a su respectiva columna del diccionario
            for i in range(n_cols):
                main_dict[col_names[i]].append(values[i])
        counter += 1

    print("El dataset tiene {0} filas y {1} columnas".format(counter, n_cols))

    # Convierte el diccionario en un dataframe
    df_1 = pd.DataFrame(main_dict)
    print("\nDataset 1 convertido a Dataframe utilizando la librería urllib3: \n{}".format(df_1))

    # Exportar la información con la librería requests
    result_2 = requests.get(medals_url, verify=False, stream=True)
    data_2 = result_2.text
    df_2 = pd.DataFrame([row.split(',') for row in data_2.split('\n')[1:]], columns=[col for col in data_2.split('\n')[0].split(',')])
    print("\nDataset 2 convertido a Dataframe utilizando la librería requests: \n{}".format(df_2))

    # Se guarda la información en un .csv, .json y .xls
    filename = "athletes/downloaded_medals"
    fullpath = os.path.join(mainpath, filename)

    df_2.to_csv("{}.csv".format(fullpath), index=False)
    df_2.to_json("{}.json".format(fullpath), orient="records")
    df_2.to_excel("{}.xlsx".format(fullpath), index=False)
    print("Los ficheros se han guardado correctamente en {}".format(fullpath))

    return df_2


if __name__ == '__main__':
    # Función para carga de datos a través de la función read_csv
    read_data()

    # Función para leer datos de forma manual (se suele utilizar cuando son ficheros muy grandes, 5G o más)
    read_data_manual()

    # Funcion para lectura y escritura de fichero de forma manual separados por tabulador (\t)
    write_data_manual()

    # Función para leer datos desde una URL
    read_url()

    # Función para leer fichero xls y xlsx
    read_xls()

    # Función para leer los datos de una URL externa, procesarlos y convertirlos a un DataFrame para posteriormente guardarlos en un .csv, .json y .xlsx
    medals_df = get_data_url()