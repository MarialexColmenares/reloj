import customtkinter as ctk
from clock_view import ClockView


class AlarmView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Reloj fijo
        self.grid_rowconfigure(1, weight=1)  # Lista de alarmas expandible

        # 1. Reloj Analógico en la parte superior
        self.clock = ClockView(self)
        self.clock.grid(row=0, column=0, pady=(10, 0))

        # 2. Frame para la lista de alarmas (Scrollable)
        self.alarms_scroll_frame = ctk.CTkScrollableFrame(
            self, label_text="Mis Alarmas"
        )
        self.alarms_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.alarms_scroll_frame.grid_columnconfigure(0, weight=1)

        # Botón para agregar alarma
        self.add_button = ctk.CTkButton(
            self, text="+ Agregar Alarma", command=self.open_add_alarm_dialog
        )
        self.add_button.grid(row=2, column=0, pady=10)

        # Agregar algunas alarmas de ejemplo
        self.add_alarm_row("07:00", True)
        self.add_alarm_row("08:30", False)

    def open_add_alarm_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Nueva Alarma")
        dialog.geometry("300x200")
        dialog.grab_set()  # Hace que la ventana sea modal

        ctk.CTkLabel(dialog, text="Configurar Hora", font=("Arial", 16, "bold")).pack(
            pady=10
        )

        frame_time = ctk.CTkFrame(dialog, fg_color="transparent")
        frame_time.pack(pady=10)

        entry_hour = ctk.CTkEntry(frame_time, width=50, placeholder_text="HH")
        entry_hour.pack(side="left", padx=5)

        ctk.CTkLabel(frame_time, text=":").pack(side="left")

        entry_min = ctk.CTkEntry(frame_time, width=50, placeholder_text="MM")
        entry_min.pack(side="left", padx=5)

        def save_alarm():
            h = entry_hour.get()
            m = entry_min.get()
            if h.isdigit() and m.isdigit():
                # Formato simple HH:MM
                time_text = f"{int(h):02d}:{int(m):02d}"
                self.add_alarm_row(time_text, True)
                dialog.destroy()

        ctk.CTkButton(dialog, text="Guardar", command=save_alarm).pack(pady=20)

    def add_alarm_row(self, time_text, is_on):
        row_frame = ctk.CTkFrame(self.alarms_scroll_frame)
        row_frame.pack(fill="x", pady=5, padx=5)

        # Etiqueta de la hora
        time_label = ctk.CTkLabel(row_frame, text=time_text, font=("Arial", 24, "bold"))
        time_label.pack(side="left", padx=20, pady=10)

        # Frame para controles (Switch + Eliminar)
        controls_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        controls_frame.pack(side="right", padx=10)

        # Función para actualizar texto del switch
        def toggle_switch():
            if switch.get():
                switch.configure(text="Activa")
            else:
                switch.configure(text="Desactivada")

        # Switch de encendido/apagado
        switch = ctk.CTkSwitch(
            controls_frame,
            text="Activa" if is_on else "Desactivada",
            command=toggle_switch,
        )
        if is_on:
            switch.select()
        else:
            switch.deselect()
        switch.pack(side="left", padx=10)

        # Botón Eliminar
        btn_delete = ctk.CTkButton(
            controls_frame,
            text="X",
            width=30,
            fg_color="red",
            hover_color="darkred",
            command=lambda: row_frame.destroy(),
        )
        btn_delete.pack(side="left", padx=5)
