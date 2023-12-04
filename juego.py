import tkinter as tk
from tkinter import messagebox
import random

class Buscaminas:
    def __init__(self, master, rows, cols, bombas):
        # Inicializa la clase Buscaminas con parámetros iniciales
        self.master = master
        self.rows = rows
        self.cols = cols
        self.bombas = bombas
        self.tablero = [[0] * cols for _ in range(rows)]
        self.botones = [[None] * cols for _ in range(rows)]

        # Inicializa el tablero y coloca las bombas
        self.inicializar_tablero()
        self.colocar_bombas()

        # Crea la interfaz gráfica del juego
        self.crear_interfaz()

    def inicializar_tablero(self):
        # Inicializa el tablero con ceros
        for i in range(self.rows):
            for j in range(self.cols):
                self.tablero[i][j] = 0

    def colocar_bombas(self):
        # Coloca las bombas aleatorias en el tablero
        bombas_colocadas = 0
        while bombas_colocadas < self.bombas:
            fila = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.tablero[fila][col] != -1:
                self.tablero[fila][col] = -1
                bombas_colocadas += 1

        # Calcula el número de bombas alrededor de cada casilla sin bomba
        for i in range(self.rows):
            for j in range(self.cols):
                if self.tablero[i][j] != -1:
                    self.tablero[i][j] = self.contar_bombas_alrededor(i, j)

    def contar_bombas_alrededor(self, fila, col):
        # Cuenta el número de bombas alrededor de una casilla
        count = 0
        for i in range(max(0, fila - 1), min(self.rows, fila + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.tablero[i][j] == -1:
                    count += 1
        return count

    def crear_interfaz(self):
        # Crea los botones para cada casilla en la interfaz gráfica
        for i in range(self.rows):
            for j in range(self.cols):
                self.botones[i][j] = tk.Button(self.master, text='', width=3, height=2,
                                               command=lambda i=i, j=j: self.revelar_casilla(i, j))
                self.botones[i][j].grid(row=i, column=j)

    def revelar_casilla(self, fila, col):
        # Función llamada al hacer clic en una casilla
        if self.tablero[fila][col] == -1:
            # Si la casilla contiene una bomba, muestra un mensaje de "Fin del juego" y revela todas las bombas
            self.mostrar_bombas()
            messagebox.showinfo("Fin del juego", "¡Perdiste!")
            self.master.destroy()
        else:
            # Si la casilla no contiene una bomba, muestra el número y revela las casillas vacías cercanas
            self.mostrar_numero(fila, col)
            if self.tablero[fila][col] == 0:
                self.revelar_casillas_vacias(fila, col)

    def mostrar_numero(self, fila, col):
        # Muestra el número en la casilla y la deshabilita
        numero = self.tablero[fila][col]
        self.botones[fila][col].config(text=str(numero), state='disabled')

    def revelar_casillas_vacias(self, fila, col):
        # Revela las casillas vacías cercanas
        for i in range(max(0, fila - 1), min(self.rows, fila + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.tablero[i][j] != -1 and self.botones[i][j]['state'] == 'normal':
                    self.mostrar_numero(i, j)
                    if self.tablero[i][j] == 0:
                        self.revelar_casillas_vacias(i, j)

    def mostrar_bombas(self):
        # Muestra todas las bombas al final del juego
        for i in range(self.rows):
            for j in range(self.cols):
                if self.tablero[i][j] == -1:
                    self.botones[i][j].config(text="*", state='disabled')

def main():
    # Es la función principal para crear la interfaz y comenzar el juego
    root = tk.Tk()
    root.title("Buscaminas")
    root.iconbitmap("buscaminas.ico")
    filas = 8
    columnas = 8
    bombas = 10
    buscaminas = Buscaminas(root, filas, columnas, bombas)
    root.mainloop()

if __name__ == "__main__":
    # Inicia el juego si el script se ejecuta directamente
    main()
