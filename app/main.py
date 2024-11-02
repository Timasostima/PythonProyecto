"""
Autor: Tymur Kulivar Shymanskyi
Clase: Diseño de interfaces
"""

from multiprocessing import Process
import time
from gui import GUI
from api.api import run

if __name__ == "__main__":
    # Ejecución de la API en un proceso separado
    flask_process = Process(target=run)
    flask_process.start()
    time.sleep(1)

    # Ejecución de la interfaz gráfica
    app = GUI()
    app.mainloop()

    # Finalización del proceso de la API
    flask_process.kill()
