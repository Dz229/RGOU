import tkinter as tk

def print_text():
    text = entry_field.get()
    print(text)
    display_field.config(state=tk.NORMAL)  # Enable text modification
    display_field.delete(1.0, tk.END)  # Clear the current text
    display_field.insert(tk.END, text)  # Insert the new text
    display_field.config(state=tk.DISABLED) 

# Create a new Tkinter window
window = tk.Tk()
window.title("Royal Game of Ur")

# Set the size of each rectangle
rect_width = 100
rect_height = 100


# Create a text field for display above the canvas, which user can't modify
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
            
             # Draw circle in the center of the rectangle
            circle_x = x1 + rect_width // 2
            circle_y = y1 + rect_height // 2
            circle_radius = 30  # radius of the circle
            # canvas.create_oval(circle_x - circle_radius, circle_y - circle_radius,
            #                 circle_x + circle_radius, circle_y + circle_radius,
            #                 fill="red")    
            
            
# Create a text entry field below the canvas
entry_field = tk.Entry(window)
entry_field.pack()

# Create a button to submit the text
submit_button = tk.Button(window, text="Print Text", command=print_text)
submit_button.pack()

# Start the Tkinter event loop
window.mainloop()
