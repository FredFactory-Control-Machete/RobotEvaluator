import VIKOR as v
import TOPSIS as t
import CODAS as c
import MORA as m
import pandas as pd

def main():
    matrix = pd.read_csv("/Users/gabrielburbano/Desktop/Pruebas/robots_imaginarios.csv")
    matrizpesos = pesos(matrix)
    return v(matrix,matrizpesos)

def pesos(matrix):
    criterios = matrix.drop(columns="Robot")
    matrizpesos = pd.Series(
        0.0,
        index=criterios.columns)
    for i in range(criterios.shape[1]):
        #check the value is within 0-1
        while True:
            try:
                x = float(input(f"Peso de {criterios.columns[i]} (0-1): "))
                if  0 <= x <= 1:
                    matrizpesos.iloc[i] =  x
                    break
                else:
                    print("El valor debe estar en 0 y 1")
                    continue
            except ValueError:
                print("Entrada invalida, ingrese un numero.")
                continue
    return matrizpesos

if __name__ == '__main__':
    main()