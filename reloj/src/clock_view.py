import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import math


class ClockView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configuración del Canvas
        self.centro_x = 150
        self.centro_y = 150
        self.radio = 100

        # IDs de las manecillas (para borrarlas y redibujarlas)
        self.id_sec = None
        self.id_min = None
        self.id_hora = None

        self.canvas = tk.Canvas(
            self,
            width=300,
            height=300,
            bg=self._apply_appearance_mode(
                ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
            ),
            highlightthickness=0,  # Elimina el borde por defecto del canvas
        )
        self.canvas.pack(expand=True)

        self.dibujar_caratula()
        self.actualizar_reloj_analogico()

    def dibujar_caratula(self):
        # 4.4. Dibujar el círculo del reloj
        self.canvas.create_oval(
            self.centro_x - self.radio,
            self.centro_y - self.radio,
            self.centro_x + self.radio,
            self.centro_y + self.radio,
            outline="gray",
            width=2,
        )

        # 4.4. Dibujar el punto central
        self.canvas.create_oval(
            self.centro_x - 5,
            self.centro_y - 5,
            self.centro_x + 5,
            self.centro_y + 5,
            fill="red",
        )

        for i, num in enumerate([12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]):
            # Posiciones para el número
            x, y = self.calcular_posicion(i, 12, self.radio + 20)
            # Posiciones para la marca (línea)
            x_marca_int, y_marca_int = self.calcular_posicion(i, 12, self.radio - 5)
            x_marca_ext, y_marca_ext = self.calcular_posicion(i, 12, self.radio)

            # Dibujar el número solo en las 4 principales
            if num % 3 == 0:
                self.canvas.create_text(
                    x, y, text=str(num), fill="white", font=("Arial", 12, "bold")
                )

            # Dibujar las marcas (pequeñas líneas en el borde)
            self.canvas.create_line(
                x_marca_int, y_marca_int, x_marca_ext, y_marca_ext, fill="gray", width=2
            )

    def calcular_posicion(self, unidad, factor, longitud):
        """Calcula las coordenadas (x, y) de la punta de la manecilla."""
        angulo = 360 * (unidad / factor) - 90

        """ Convierte el ángulo a radianes para las funciones trigonométricas """
        rad = math.radians(angulo)

        """ Calcula las coordenadas (x, y) de la punta de la manecilla """
        x = self.centro_x + longitud * math.cos(rad)
        y = self.centro_y + longitud * math.sin(rad)

        return x, y

    def dibujar_manecilla(self, id_anterior, unidad, factor, longitud, ancho, color):
        """Calcula la posición y dibuja/redibuja la manecilla."""

        # Calcula la nueva posición de la punta
        x_punta, y_punta = self.calcular_posicion(unidad, factor, longitud)

        # Si la manecilla ya existe, la borra
        if id_anterior:
            self.canvas.delete(id_anterior)

        # Dibuja una nueva línea (manecilla) desde el centro hasta la punta
        id_nuevo = self.canvas.create_line(
            self.centro_x,
            self.centro_y,
            x_punta,
            y_punta,
            width=ancho,
            fill=color,
            capstyle=tk.ROUND,
        )

        return id_nuevo

    def actualizar_reloj_analogico(self):
        """Obtiene la hora actual y actualiza la posición de las manecillas."""
        now = datetime.now().time()

        hora = now.hour % 12
        minuto = now.minute
        segundo = now.second

        self.id_sec = self.dibujar_manecilla(
            self.id_sec, segundo, 60, self.radio * 0.9, 2, "red"
        )

        minuto_total = minuto + segundo / 60

        self.id_min = self.dibujar_manecilla(
            self.id_min, minuto_total, 60, self.radio * 0.8, 3, "white"
        )

        hora_total = hora + minuto / 60

        self.id_hora = self.dibujar_manecilla(
            self.id_hora, hora_total, 12, self.radio * 0.6, 5, "white"
        )

        self.after(1000, self.actualizar_reloj_analogico)
