import turtle as tu
import re
import docx
import time

# Load the document
source = "tulips"
data = docx.Document(f"{source}.docx")

coordinates = []
colours = []

for paragraph in data.paragraphs:
    try:
        # Find coordinate tuples (x, y)
        coord_matches = re.findall(r'\([-+]?\d*\.\d*, ?[-+]?\d*\.\d*\)', paragraph.text)
        coord_tuples = [tuple(map(float, re.findall(r'[-+]?\d*\.\d*', match))) for match in coord_matches]
        
        # Find color tuples (r, g, b)
        colour_matches = re.findall(r'\([-+]?\d*\.\d*, ?[-+]?\d*\.\d*, ?[-+]?\d*\.\d*\)', paragraph.text)
        if colour_matches:
            colour_tuple = tuple(map(float, re.findall(r'[-+]?\d*\.\d*', colour_matches[0])))
            colours.append(colour_tuple)
        else:
            colours.append((0, 0, 0))  # Default to black if no color is found

        coordinates.append(coord_tuples)
    
    except Exception as e:
        print(f"Error processing paragraph: {e}")

# Initialize turtle
pen = tu.Turtle()
screen = tu.Screen()
tu.tracer(0)  # Disable auto-update for smoother control
pen.speed(0)  # Slower speed
tu.delay(10)  # Add delay in milliseconds (adjust as needed)

screen.getcanvas().winfo_toplevel().attributes("-fullscreen", True)

# Draw shapes
for i, path in enumerate(coordinates):
    if not path:
        continue  # Skip empty coordinate lists
    
    col = colours[i]
    pen.color(col)
    pen.begin_fill()
    
    first = True
    for x, y in path:
        y = -y  # Flip y-axis for correct drawing
        if first:
            pen.up()
            pen.goto(x, y)
            pen.down()
            first = False
        else:
            pen.goto(x, y)
        
        tu.update()  # Update after each step
        time.sleep(0)  # Small pause to slow down movement

    pen.end_fill()

# Update screen once everything is drawn
tu.update()
screen.mainloop()
