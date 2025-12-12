import customtkinter as ctk


class TimerView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Spacer top
        self.grid_rowconfigure(4, weight=1)  # Spacer bottom

        # Time Display
        self.time_label = ctk.CTkLabel(
            self, text="00:00:00", font=("Arial", 60, "bold")
        )
        self.time_label.grid(row=1, column=0, columnspan=3, pady=(20, 20))

        # Inputs Frame
        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.hour_entry = ctk.CTkEntry(
            self.entry_frame, width=60, placeholder_text="HH", justify="center"
        )
        self.hour_entry.pack(side="left", padx=5)

        self.label_sep1 = ctk.CTkLabel(self.entry_frame, text=":", font=("Arial", 20))
        self.label_sep1.pack(side="left")

        self.min_entry = ctk.CTkEntry(
            self.entry_frame, width=60, placeholder_text="MM", justify="center"
        )
        self.min_entry.pack(side="left", padx=5)

        self.label_sep2 = ctk.CTkLabel(self.entry_frame, text=":", font=("Arial", 20))
        self.label_sep2.pack(side="left")

        self.sec_entry = ctk.CTkEntry(
            self.entry_frame, width=60, placeholder_text="SS", justify="center"
        )
        self.sec_entry.pack(side="left", padx=5)

        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, columnspan=3, pady=20)

        self.start_button = ctk.CTkButton(
            self.buttons_frame,
            text="Iniciar",
            command=self.start_timer,
            fg_color="green",
            width=80,
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = ctk.CTkButton(
            self.buttons_frame,
            text="Pausar",
            command=self.toggle_pause,
            fg_color="orange",
            state="disabled",
            width=80,
        )
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = ctk.CTkButton(
            self.buttons_frame,
            text="Reiniciar",
            command=self.reset_timer,
            fg_color="red",
            width=80,
        )
        self.reset_button.grid(row=0, column=2, padx=10)

        self.running = False
        self.paused = False
        self.total_seconds = 0
        self.timer_id = None

    def start_timer(self):
        if not self.running and not self.paused:
            try:
                h_str = self.hour_entry.get()
                m_str = self.min_entry.get()
                s_str = self.sec_entry.get()

                h = int(h_str) if h_str else 0
                m = int(m_str) if m_str else 0
                s = int(s_str) if s_str else 0

                self.total_seconds = h * 3600 + m * 60 + s

                if self.total_seconds > 0:
                    self.running = True
                    self.entry_frame.grid_remove()  # Hide inputs
                    self.start_button.configure(state="disabled")
                    self.pause_button.configure(state="normal")
                    self.countdown()
            except ValueError:
                pass  # Ignore invalid input

    def toggle_pause(self):
        if self.running:
            # Pausar
            self.running = False
            self.paused = True
            self.pause_button.configure(text="Reanudar", fg_color="green")
            if self.timer_id:
                self.after_cancel(self.timer_id)
        elif self.paused:
            # Reanudar
            self.running = True
            self.paused = False
            self.pause_button.configure(text="Pausar", fg_color="orange")
            self.countdown()

    def reset_timer(self):
        self.running = False
        self.paused = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.total_seconds = 0
        self.time_label.configure(text="00:00:00")
        self.entry_frame.grid()  # Show inputs
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled", text="Pausar", fg_color="orange")

    def countdown(self):
        if self.running and self.total_seconds >= 0:
            m, s = divmod(self.total_seconds, 60)
            h, m = divmod(m, 60)
            self.time_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")

            if self.total_seconds == 0:
                self.running = False
                self.start_button.configure(state="normal")
                self.pause_button.configure(state="disabled")
                self.entry_frame.grid()
                # Optional: Play sound or show alert
            else:
                self.total_seconds -= 1
                self.timer_id = self.after(1000, self.countdown)
