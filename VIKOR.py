import pandas as pd


# main: Va a llamar a las funciones para calcular y va a leer el csv
def main():
    matrix = pd.read_csv("/Users//Desktop/Pruebas/robots_imaginarios.csv")
    vikor(matrix)

def vikor(matrix,pesos):
    criterios = matrix.drop(columns="Robot")
    #Copia para guardar los resultados, convierte los valores a float
    normalizada = criterios.astype(float).copy()
    # find the minimums and max of each category
    for j in range(normalizada.shape[1]):
        min = normalizada.iloc[:, j].min()
        max = normalizada.iloc[:, j].max()
        #Replace the value in the matrix for the converted value
        normalizada.iloc[:, j] = convertvalues(j, min, max, normalizada)
    #ponderada ya fue multiplicado por los pesos
    ponderada= calculoconepsos(pesos, normalizada)
    resultados = calculoscore(ponderada)
    recomendaciones = recomendar_robots(matrix, resultados)
    print("Matriz con los criterios de 1 a 0:\n", normalizada)
    print(f"Matriz con los pesos ya multiplicados \n", ponderada)
    print(f"Matriz de pesos calculados \n", resultados)
    print("\nLas 3 primeras recomendaciones:")
    print(recomendaciones.to_string(index=False))

    return recomendaciones

#convert the values to dij
def convertvalues(j,min,max,criterios):
    columna = criterios.iloc[:, j]
    #in case all robot values are the same , which is unlikely
    if max == min:
        return columna*0
    #Cost criteria, less is best
    if criterios.columns[j] in {"Costo_USD", "Consumo_medio_W"}:
        return (columna-min)/(max-min)
    #Profit criteria, more is best
    return ((max-columna)/(max-min))

#Calcular la matriz con los pesos
def calculoconepsos(pesos, normalizada):
    ponderada = normalizada.mul(pesos, axis="columns")
    return ponderada

#calcula el score del robot
def calculoscore(ponderada):
    resultados = pd.DataFrame(index=ponderada.index)
    #Si es la suma de todos los valores de criterios
    resultados["Si"] = ponderada.sum(axis=1)
    #Ri es el valor de criterio mas alto
    resultados["Ri"] = ponderada.max(axis=1)
    #Q1 es el score del robot
    resultados["Qi"] = 0.0
    resultados = calculoQi(resultados)
    return resultados

#realiza el calculo de Qi
def calculoQi(resultados):
    v = 0.5  # hay que definir que v usar
    maxSi = resultados["Si"].max()
    minSi = resultados["Si"].min()
    maxRi = resultados["Ri"].max()
    minRi = resultados["Ri"].min()
    #Saca maximos y minimos necesarios para el calculo del score final de vikor
    for i in range(resultados.shape[0]):
        Ri = resultados.iloc[i, 1]
        Si = resultados.iloc[i, 0]
        #calculo del score
        resultados.loc[i,"Qi"] = v*((Si-minSi)/(maxSi-minSi))+(1-v)*((Ri-minRi)/(maxRi-minRi))
    return resultados

def recomendar_robots(matrix, resultados):
    tabla = resultados.copy()
    # Añadir el nombre correspondiente a cada robot.
    tabla.insert(0, "Robot", matrix["Robot"])
    # Elegir los tres valores más pequeños de Qi.
    recomendaciones = tabla.nsmallest(3, "Qi")
    return recomendaciones

if __name__ == "__main__":
    main()
