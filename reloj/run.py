import sys
import os

# Agregar la carpeta src al path para que se puedan importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
