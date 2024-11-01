class Recipe:
    def __init__(self, name=None, descripcion=None, tipo=None, minutos=None, calorias=None, dificultad=None,
                 ingredients=None, image_path=None):
        if ingredients is None:
            ingredients = []

        self.name = name
        self.descripcion = descripcion
        self.tipo = tipo
        self.minutos = minutos
        self.calorias = calorias
        self.dificultad = dificultad
        self.ingredients = ingredients
        self.image_path = image_path

    def __str__(self):
        st = ""
        if self.name is not None:
            st += f"nombre={self.name}, "
        if self.descripcion is not None:
            st += f"descripcion={self.descripcion}, "
        if self.tipo is not None:
            st += f"tipo={self.tipo}, "
        if self.minutos is not None:
            st += f"minutos={self.minutos}, "
        if self.calorias is not None:
            st += f"calorias={self.calorias}, "
        if self.dificultad is not None:
            st += f"dificultad={self.dificultad}, "
        if self.ingredients:
            st += f"ingredients={[ingr for ingr in self.ingredients]}, "
        if self.image_path is not None:
            st += f"image_path={self.image_path}, "
        return st[:-2]