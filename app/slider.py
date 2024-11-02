import tkinter as tk
from RangeSlider import RangeSliderH


class Slider(RangeSliderH):
    def __init__(self, frame, max_val):
        self.left = tk.DoubleVar()
        self.right = tk.DoubleVar(value=max_val)
        super().__init__(
            frame,
            [self.left, self.right],
            Width=350,
            Height=39,
            padX=11,
            min_val=0,
            max_val=max_val,
            show_value=True,
            font_size=7,
            line_color="white",
            line_s_color="lightblue",
            bgColor="#333333",
            step_size=1,
            font_color="white",
            bar_color_inner="#555555",
            bar_color_outer="#777777",
        )

    def get_value(self):
        left_value = self.left.get()
        right_value = self.right.get()

        return (
            (int(left_value) if left_value else None),
            (int(right_value) if right_value else None)
        )
