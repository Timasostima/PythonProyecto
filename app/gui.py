"""
Autor: Tymur Kulivar Shymanskyi
Clase: Diseño de interfaces
"""

import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
from utils import reload_recipes


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Busca Recetas")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.configure(bg="#333333")

        # Configuración del estilo de la interfaz
        style = ttk.Style(self)
        style.theme_use('clam')

        # Configuración de estilos para diferentes widgets
        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='white')
        style.configure('TButton', background='#4CAF50', foreground='white', font=("Arial", 12, "bold"))
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TCombobox', background='#333333', foreground='white', fieldbackground='#333333',
                        selectbackground='#555555', selectforeground='white', font=("Arial", 12, "bold"))
        style.map('TCombobox', fieldbackground=[('readonly', '#333333')], selectbackground=[('readonly', '#555555')],
                  selectforeground=[('readonly', 'white')])
        style.configure('TEntry', background='#333333', foreground='white', fieldbackground='#333333')
        style.configure('TScrollbar', background='#333333', troughcolor='#333333', arrowcolor='white')
        style.map('TScrollbar', background=[('active', '#555555'), ('pressed', '#777777')],
                  troughcolor=[('active', '#444444'), ('pressed', '#666666')],
                  arrowcolor=[('active', 'white'), ('pressed', 'white')])

        # Creación del marco principal
        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Creación del canvas y el scrollbar
        canvas = tk.Canvas(main_frame, bg="#333333")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style='TScrollbar')
        self.scrollable_frame = ttk.Frame(canvas)

        # Configuración de scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 1))

        # Creación de los frames principales
        Sidebar(main_frame, self.scrollable_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Recarga de receta
        reload_recipes(self.scrollable_frame, [])
