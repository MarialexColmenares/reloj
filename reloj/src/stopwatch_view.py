import customtkinter as ctk
import time


class StopwatchView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Time Display
        self.time_label = ctk.CTkLabel(
            self, text="00:00.00", font=("Arial", 60, "bold")
        )
        self.time_label.grid(row=0, column=0, columnspan=3, pady=(40, 20))

        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, columnspan=3, pady=20)

        self.start_button = ctk.CTkButton(
            self.buttons_frame,
            text="Iniciar",
            command=self.start,
            fg_color="green",
            width=80,
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = ctk.CTkButton(
            self.buttons_frame,
            text="Pausar",
            command=self.pause,
            fg_color="orange",
            state="disabled",
            width=80,
        )
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = ctk.CTkButton(
            self.buttons_frame,
            text="Reiniciar",
            command=self.reset,
            fg_color="red",
            width=80,
        )
        self.reset_button.grid(row=0, column=2, padx=10)

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.timer_id = None

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()
            self.start_button.configure(state="disabled")
            self.pause_button.configure(
                state="normal", text="Pausar", fg_color="orange"
            )

    def pause(self):
        if self.running:
            self.running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self.start_button.configure(state="normal", text="Reanudar")
            self.pause_button.configure(state="disabled")

    def reset(self):
        self.pause()
        self.elapsed_time = 0
        self.time_label.configure(text="00:00.00")
        self.start_button.configure(text="Iniciar")
        self.pause_button.configure(state="disabled", text="Pausar", fg_color="orange")

    def update_timer(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time

            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            milliseconds = int((self.elapsed_time * 100) % 100)

            self.time_label.configure(
                text=f"{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
            )
            self.timer_id = self.after(50, self.update_timer)  # Update every 50ms
