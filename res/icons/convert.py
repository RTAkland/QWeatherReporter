import os


file_list = []

for i in range(100, 10000):
    if os.path.exists(f'{i}.svg'):
        file_list.append(i)


for i in file_list:
    os.system(f'inkscape -z -e {i}.png -w 256 -h 256 {i}.svg')