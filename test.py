import tkinter as tk
#######
# GUI #
#######
def draw_circles(canvas, rect_width, rect_height, circle_radius=30):
    for i in range(8):
        for j in range(3):
            if not ((i > 3 and i < 6) and (j != 1)):
                x1 = j * rect_width
                y1 = i * rect_height
                circle_x = x1 + rect_width // 2
                circle_y = y1 + rect_height // 2
                canvas.create_oval(circle_x - circle_radius, circle_y - circle_radius,
                                   circle_x + circle_radius, circle_y + circle_radius,
                                   fill="black")

###################################################################
def get_move_ui():
    text = entry_field.get()
    print(text)
    display_field.config(state=tk.NORMAL)  
    display_field.delete(1.0, tk.END)  
    display_field.insert(tk.END, text)  
    draw_circles(canvas, rect_width, rect_height)
###################################################################

window = tk.Tk()
window.title("Royal Game of Ur")
rect_width = 100
rect_height = 100
display_field = tk.Text(window, height=1, width=40, state=tk.DISABLED)
display_field.pack()
canvas = tk.Canvas(window, width=rect_width*3, height=rect_height*8)
canvas.pack()
for i in range(8):
    for j in range(3):
        if not ((i > 3 and i < 6) and (j != 1)):
            x1 = j * rect_width
            y1 = i * rect_height
            x2 = x1 + rect_width
            y2 = y1 + rect_height
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

entry_field = tk.Entry(window)
entry_field.pack()
submit_button = tk.Button(window, text="Make Move", command=get_move_ui)
submit_button.pack()
window.mainloop()

#######
