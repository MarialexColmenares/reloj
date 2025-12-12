import customtkinter as ctk
from clock_view import ClockView
from timer_view import TimerView
from stopwatch_view import StopwatchView
from alarm_view import AlarmView

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Reloj")
        self.geometry(
            "500x600"
        )  # Aumenté un poco la altura para acomodar mejor el reloj + alarmas

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Contenedor para las vistas
        self.views_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.views_frame.grid_columnconfigure(0, weight=1)
        self.views_frame.grid_rowconfigure(0, weight=1)

        # Inicializar vistas
        self.views = {}

        # Vista Reloj Mundial (ClockView)
        self.views["Reloj Mundial"] = ClockView(self.views_frame)
        self.views["Reloj Mundial"].grid(row=0, column=0, sticky="nsew")

        # Vista Temporizador (TimerView)
        self.views["Temporizador"] = TimerView(self.views_frame)
        self.views["Temporizador"].grid(row=0, column=0, sticky="nsew")

        # Vista Alarma (AlarmView)
        self.views["Alarma"] = AlarmView(self.views_frame)
        self.views["Alarma"].grid(row=0, column=0, sticky="nsew")

        # Vista Cronómetro (StopwatchView)
        self.views["Cronómetro"] = StopwatchView(self.views_frame)
        self.views["Cronómetro"].grid(row=0, column=0, sticky="nsew")

        self.main_label = ctk.CTkLabel(
            self, text="Reloj Mundial", font=("Arial", 14, "bold")
        )
        self.main_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self._crear_barra_navegacion()

        # Mostrar vista inicial
        self.cambiar_vista("Reloj Mundial")

    def _crear_barra_navegacion(self):
        """
        Crea el CTkFrame de la barra de navegación y coloca los 4 botones
        en la parte inferior de la interfaz.
        """
        # Creación del Frame Contenedor (Fila 1 de la ventana principal)
        self.navbar_frame = ctk.CTkFrame(self, height=50)
        self.navbar_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))

        # Configurar la cuadrícula del frame para distribuir 4 elementos uniformemente
        for i in range(4):
            self.navbar_frame.grid_columnconfigure(i, weight=1)

        # --- Creación y Posicionamiento de los Botones ---

        # Lista de tuplas: (Texto del Botón, Nombre de la Vista, Atributo del Botón)
        botones_data = [
            ("⏰ Alarma", "Alarma", "btn_alarma"),
            ("🌎 Reloj Mundial", "Reloj Mundial", "btn_reloj"),
            ("⏳ Temporizador", "Temporizador", "btn_temporizador"),
            ("⏱️ Cronómetro", "Cronómetro", "btn_cronometro"),
        ]

        for i, (texto, vista, atributo) in enumerate(botones_data):

            # Crear el botón
            btn = ctk.CTkButton(
                self.navbar_frame,
                text=texto,
                command=lambda v=vista: self.cambiar_vista(v),
            )

            # Asignar el botón al atributo de la instancia (e.g., self.btn_alarma)
            setattr(self, atributo, btn)

            # Posicionar el botón en la cuadrícula
            btn.grid(row=0, column=i, sticky="ew", padx=5, pady=5)

    def cambiar_vista(self, vista_nombre):
        """Actualiza la etiqueta de contenido principal y resalta el botón activo."""
        print(f"Vista seleccionada: {vista_nombre}")
        self.main_label.configure(text=f"Vista: {vista_nombre}")

        # Mostrar la vista seleccionada y ocultar las demás
        for nombre, frame in self.views.items():
            if nombre == vista_nombre:
                frame.tkraise()  # Traer al frente
            else:
                pass

        # Obtener la lista de todos los botones de navegación
        botones = [
            self.btn_alarma,
            self.btn_reloj,
            self.btn_temporizador,
            self.btn_cronometro,
        ]

        # Color de realce (activo)
        color_activo = ctk.ThemeManager.theme["CTkButton"]["hover_color"]
        # Color por defecto (inactivo)
        color_inactivo = ctk.ThemeManager.theme["CTkButton"]["fg_color"]

        # Iterar y actualizar colores
        for btn in botones:
            btn.configure(fg_color=color_inactivo)

        # Activar el botón seleccionado basándose en la vista
        if vista_nombre == "Alarma":
            self.btn_alarma.configure(fg_color=color_activo)
        elif vista_nombre == "Reloj Mundial":
            self.btn_reloj.configure(fg_color=color_activo)
        elif vista_nombre == "Temporizador":
            self.btn_temporizador.configure(fg_color=color_activo)
        elif vista_nombre == "Cronómetro":
            self.btn_cronometro.configure(fg_color=color_activo)


if __name__ == "__main__":
    app = App()
    app.mainloop()
