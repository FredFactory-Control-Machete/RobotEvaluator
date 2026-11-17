import pandas as pd


# main: Va a llamar a las funciones para calcular y va a leer el csv
def main():
    matrix = pd.read_csv("/Users//Desktop/Pruebas/robots_imaginarios.csv")
    vikor(matrix)

def vikor(matrix,minmax):
    criterios = matrix.drop(columns="Robot")
    valores = minmax.set_index("Criterio")
    #Copia para guardar los resultados, convierte los valores a float

    # Filters out all values above the max cost, can inlcude other cost criteria
    for i in criterios.columns:
        if not valores.loc[i, "Filter"]:
            continue
        if i == "Costo_USD":
            criterios = criterios.loc[criterios[i] <= valores.loc[i, "Max"]]
        else:
            criterios = criterios.loc[
                criterios[i].between(
                    valores.loc[i, "Min"],
                    valores.loc[i, "Max"],
                    inclusive="both")]
    if criterios.empty:
        raise ValueError("No robots meet the enabled filters.")

    normalizada = criterios.astype(float).copy()

    #find the absolute biggest diference, etween the parameters
    for i in criterios.columns:
        if i != "Costo_USD":
            normalizada[i] = (criterios[i] - valores.loc[i, "Ideal"]).abs()
    for j in range(normalizada.shape[1]):
        min = normalizada.iloc[:, j].min()
        max = normalizada.iloc[:, j].max()
        #Replace the value in the matrix for the converted value
        normalizada.iloc[:, j] = convertvalues(j, min, max, normalizada)
    #ponderada ya fue multiplicado por los pesos
    ponderada= calculoconepsos(valores["Weight"], normalizada)
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
    #Less is best always since it calcualtes for the middle value
    return (columna - min) / (max - min)

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
    for i in resultados.index:
        Ri = resultados.loc[i, "Ri"]
        Si = resultados.loc[i, "Si"]
        #calculo del score
        parteS = ( 0.0 if minSi == maxSi
                   else (Si - minSi) / (maxSi - minSi))
        parteR = (
            0.0 if maxRi == minRi
            else (Ri - minRi) / (maxRi - minRi)
        )
        resultados.loc[i, "Qi"] = v * parteS + (1 - v) * parteR

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
