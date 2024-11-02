from multiprocessing import Process
import time
from gui import GUI
from api.api import run

if __name__ == "__main__":
    flask_process = Process(target=run)
    flask_process.start()
    time.sleep(1)

    app = GUI()
    app.mainloop()

    flask_process.kill()
