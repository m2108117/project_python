import numpy as np
from scipy.spatial.distance import cdist

# Считываем координаты из файла
with open('D:\\WORK\\kod\\POSCAR', 'r') as f:
    lines = f.readlines()
    coordinates = []
    atom_numbers = []
    for i, line in enumerate(lines[8:]):
        x, y, z = line.split()
        coordinates.append([float(x), float(y), float(z)])
        atom_numbers.append(i)
    coordinates = np.array(coordinates)
    atom_numbers = np.array(atom_numbers)
# Извлечение координат атомов из файла POSCAR
coordinatess = []
for line in lines[8:]:
    coordinatess.append(list(map(float, line.split()[:3])))


# Индекс Атома, к которому мы хотим найти ближайшие атомы сделать минус 1 потому что в питоне с нуля!!
ATOM_index = int(input("Введите номер атома: ")) - 1

arr = [[0, 0, 0]] # для сравнения на уникальность

for k in range(10000): #КОЛ-ВО СОЗДАВАЕМЫХ ФАЙЛОВ
    Test = False
    while( Test == False):
        # Вычисляем расстояния между всеми парами атомов
        distances = cdist([coordinates[ATOM_index]], coordinates)[0]

        # Сортируем индексы атомов по возрастанию расстояния
        indices = np.argsort(distances)

        # Создаем пустой список для соседей
        neighbors = []

        # Добавляем ближайших соседей в список=====================
        for i in range(1, 13):
            neighbors.append(atom_numbers[indices[i]])

        # Выбираем случайного соседа из списка
        print(neighbors)

        random_neighbor = np.random.choice(neighbors)
        # Выводим номер случайного соседа
        print(f"Случайный сосед атома {ATOM_index + 1}: {random_neighbor + 1}")

        # Вычисляем расстояния между всеми парами атомов
        distances = cdist([coordinates[random_neighbor]], coordinates)[0]

        # Сортируем индексы атомов по возрастанию расстояния
        indices = np.argsort(distances)

        # Добавляем ближайших соседей в список===========================
        for i in range(1, 13):
            neighbors.append(atom_numbers[indices[i]])


        # Удаляем повторяющиеся элементы из массива соседей
        neighbors.remove(random_neighbor)

        neighbors = list(set(neighbors))



        # Удаляем повторяющиеся элементы из массива соседей
        neighbors = list(set(neighbors))
        neighbors.remove(ATOM_index)
        if random_neighbor in neighbors:
            neighbors.remove(random_neighbor)

        if ATOM_index in neighbors:
            neighbors.remove(ATOM_index)

        # Выбираем случайного соседа из списка
        print(neighbors)
        random_neighbor_2 = np.random.choice(neighbors)
        qw = random_neighbor_2

        # Выводим номер случайного соседа
        print(f"Случайный сосед атома {random_neighbor + 1}: {random_neighbor_2 + 1}")

        #=========================================================================
        # Вычисляем расстояния между всеми парами атомов
        distances = cdist([coordinates[random_neighbor_2]], coordinates)[0]

        # Сортируем индексы атомов по возрастанию расстояния
        indices = np.argsort(distances)

        # Добавляем ближайших соседей в список===========================
        for i in range(1, 13):
             neighbors.append(atom_numbers[indices[i]])


        # Удаляем повторяющиеся элементы из массива соседей
        neighbors.remove(random_neighbor_2)

        neighbors = list(set(neighbors))

         # Выбираем случайного соседа из списка

        # Удаляем повторяющиеся элементы из массива соседей
        if random_neighbor_2 in neighbors:
            neighbors.remove(random_neighbor_2)

        if random_neighbor in neighbors:
            neighbors.remove(random_neighbor)

        if ATOM_index in neighbors:
            neighbors.remove(ATOM_index)


        neighbors = list(set(neighbors))
        print(neighbors)

        random_neighbor_3 = np.random.choice(neighbors)
        ww = random_neighbor_3


        # Выводим номер случайного соседа
        print(f"Случайный сосед атома {random_neighbor_2 + 1}: {random_neighbor_3 + 1}")





        # Вычисляем расстояния между всеми парами атомов
        distances = cdist([coordinates[random_neighbor_3]], coordinates)[0]

        # Сортируем индексы атомов по возрастанию расстояния
        indices = np.argsort(distances)

        # Добавляем ближайших соседей в список===========================
        for i in range(1, 13):
            neighbors.append(atom_numbers[indices[i]])


        # Удаляем повторяющиеся элементы из массива соседей
        neighbors.remove(random_neighbor_3)

        neighbors = list(set(neighbors))


        if random_neighbor_2 in neighbors:
            neighbors.remove(random_neighbor_2)

        if random_neighbor in neighbors:
            neighbors.remove(random_neighbor)

        if ATOM_index in neighbors:
            neighbors.remove(ATOM_index)


        if random_neighbor_3 in neighbors:
            neighbors.remove(random_neighbor_3)


        # Удаляем повторяющиеся элементы из массива соседей
        neighbors = list(set(neighbors))
        print(neighbors)

        random_neighbor_4 = np.random.choice(neighbors)
        qq = random_neighbor_4


        # Выводим номер случайного соседа
        print(f"Случайный сосед атома {random_neighbor_3 + 1}: {random_neighbor_4 + 1}")

        neighbors.remove(random_neighbor_4)
        if np.any(np.where(neighbors == ATOM_index)[0]):
            print("Введенный НАЧАЛЬНЫЙ присутствует в массиве соседей.")
            neighbors.remove(ATOM_index)



        new_neighbors = []
        for n in neighbors:
            new_neighbors.append(n + 1)
        print(new_neighbors)


        # Вычисление вектора для добавления атома кислорода
        #vector = np.array([0, 0, 1.5])  # вектор направлен вдоль оси z
        vector = np.array([0, 0, 1.5]) #ДОБАВЛЕНИЕ МАЛЕНЬКОГО РАЗБРОСА ПО X Y
        #random_numbersss = np.random.uniform(-0.05, 0.05, 2)
        #vector[:2] = random_numbersss

        oxygen_coords = []

        oxygen_coords.append(list(np.array(coordinatess[ATOM_index]) + vector))
        oxygen_coords.append(list(np.array(coordinatess[random_neighbor]) + vector))
        oxygen_coords.append(list(np.array(coordinates[random_neighbor_2]) + vector))
        oxygen_coords.append(list(np.array(coordinatess[random_neighbor_3]) + vector))
        oxygen_coords.append(list(np.array(coordinates[random_neighbor_4]) + vector))

        #new = [ATOM_index + 1, random_neighbor + 1, random_neighbor_2 + 1]
        new = [ATOM_index + 1, random_neighbor + 1, random_neighbor_2 + 1, random_neighbor_3 + 1, random_neighbor_4 + 1]

        new.sort()
        if new not in arr:

            arr.append([ATOM_index + 1, random_neighbor + 1, random_neighbor_2 + 1, random_neighbor_3 + 1, random_neighbor_4 + 1])

            # Сортировка каждого подмассива
            for sub_arr in arr:
                sub_arr.sort()
                Test = True
        else:
            print("RESTART")
            Test = False
        if Test == True:
            # Вывод отсортированного массива
            print(arr)

            # Объединение координат всех атомов в один список
            all_coords = coordinatess + oxygen_coords

            # Создание нового файла с добавленными атомами кислорода
            filename = f'D:\\WORK\\kod\\random_OH\\POSCAR_O_{k+1}'
            with open(filename, 'w') as f:
                f.write(lines[0])  # Записываем первую строку без изменений
                f.write(lines[1])  # Записываем масштабный коэффициент без изменений
                for i in range(2, 5):  # Записываем сетку решетки без изменений
                    f.write(lines[i])
                f.write('B N O\n')  # Добавляем названия атомов в пятую строку

                # Записываем количество атомов каждого типа вместе с количеством добавленных атомов кислорода
                #atom_counts = list(map(int, lines[6].split()))
                #atom_counts.append(3)
                f.write('56' + ' ' + '56' + ' ' +  '5' +  '\n')
                f.write('Cartesian\n')  # Записываем тип координат
                for coord in all_coords:
                    f.write(f'{coord[0]:.8f} {coord[1]:.8f} {coord[2]:.8f}\n')  # Записываем координаты атомов

            print(f'Файл {filename} успешно создан.')

            # Обновление координат для следующей итерации цикла
            #coordinates = all_coords[:-3]
            coordinates = all_coords[:-5]









