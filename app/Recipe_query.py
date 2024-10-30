class Recipe_query:
    def __init__(self, name=None, type=None, max_t=None, max_cal=None, min_cal=None, max_diff=None,
                 min_diff=None, ingredients=None):
        if ingredients is None:
            ingredients = []

        self.name = name
        self.type = type
        self.max_t = max_t
        self.max_cal = max_cal
        self.min_cal = min_cal
        self.max_diff = max_diff
        self.min_diff = min_diff
        self.ingredients = ingredients

    def __str__(self):
        st = ""
        if self.type is not None:
            st += f"tipo={self.type}, "
        if self.max_t is not None:
            st += f"max_t={self.max_t}, "
        if self.max_cal is not None:
            st += f"max_cal={self.max_cal}, "
        if self.min_cal is not None:
            st += f"min_cal={self.min_cal}, "
        if self.max_diff is not None:
            st += f"max_diff={self.max_diff}, "
        if self.min_diff is not None:
            st += f"min_diff={self.min_diff}, "
        if self.ingredients:
            st += f"ingr={[ingr for ingr in self.ingredients]}, "
        return st[:-2]
