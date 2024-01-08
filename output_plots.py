import matplotlib.pyplot as plt

data = {}

with open('output/avarage_128_100_3.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(': ') 
        data[int(key)] = eval(value)

tiles_value = []
for _ in range(14):
    tiles_value.append([])

for i in range(len(data)):
    for j in range(14):
        tiles_value[j].append(data[i][4][j])
        
colors = ["black", "blue", "red", "yellow", "pink", "green", "orange", "grey", "lime", "cyan", "brown", "purple", "deeppink", "navy"]
for i in range (14):
    plt.plot(tiles_value[i], color = colors[i], label = f"Tile {i+1}")
    
plt.xlabel("Generation")
plt.ylabel("Value")
plt.title("Population = 128, Generatios = 100, Depth = 3")
plt.legend()
plt.show()