import os
import math


def remove_duplicates():
    files_data = []
    duplicates = []
    for filename in os.listdir('D:\\WORK\\kod\\TEST'):
        with open(os.path.join('D:\\WORK\\kod\\TEST', filename)) as f:
            # Получить последние 5 строк файла с помощью функции tail
            lines = list(f)  # преобразовать итератор file в список
            oxygen_atoms = lines[-5:]

            # Получить координаты каждого атома кислорода и округлить их до 2 знаков после запятой
            coordinates = [tuple(round(float(coord), 2) for coord in atom.split()[:3]) for atom in oxygen_atoms]

            # Найти модули координат векторов между каждой парой атомов кислорода
            vector_modules = []
            for i in range(len(coordinates)):
                for j in range(i+1, len(coordinates)):
                    vector = tuple(abs(round(coordinates[i][k] - coordinates[j][k], 2)) for k in range(3))
                    coord_module = round(math.sqrt(sum([x**2 for x in vector])), 2)
                    vector_modules.append(coord_module)

            # Сортировать модули векторов по возрастанию
            sorted_vector_modules = sorted(vector_modules)

            # Добавить данные в массив files_data
            data = {"filename": filename, "vector_modules": sorted_vector_modules}
            duplicate_found = False
            for existing_data in files_data:
                if len(existing_data["vector_modules"]) == len(sorted_vector_modules):
                    close_enough = True
                    for i in range(len(existing_data["vector_modules"])):
                        if not math.isclose(existing_data["vector_modules"][i], sorted_vector_modules[i], rel_tol=0.02, abs_tol=0.02):
                            close_enough = False
                            break
                    if close_enough:
                        duplicate_found = True
                        print(f"Файл {filename} совпал с файлом {existing_data['filename']}")
                        duplicates.append(filename)
                        os.remove(os.path.join('D:\\WORK_laba\\kod\\TEST_2', filename))  # удалить файл
                        break

            if not duplicate_found:
                files_data.append(data)

    if duplicates:
        print(f"Были удалены следующие файлы: {', '.join(duplicates)}")
    else:
        print("Дупликаты не найдены")

    # Вывести уникальные файлы и векторы для каждого из них
    unique_files = list(set([data["filename"] for data in files_data]))
    for file in unique_files:
        print(f"Файл {file} имеет следующие модули векторов:")
        file_data = next((data for data in files_data if data["filename"] == file), None)
        if file_data:
            vector_modules = file_data["vector_modules"]
            for i, module in enumerate(vector_modules, start=1):
                print(f"{i}. {module}")
                print()  # Печатать пустую строку между файлами для лучшей читаемости

                # Добавить информацию о модулях векторов в отдельный файл для каждого уникального файла
                output_filename = os.path.splitext(file)[0] + '_output.txt'
                with open(output_filename, 'w') as f:
                    f.write(f"Модули векторов для файла {file}:\n")
                    for module in vector_modules:
                        f.write(f"{module}\n")

            print("Данные успешно записаны в файлы output.txt")


if __name__ == '__main__':
    remove_duplicates()

    # Тут можно добавить другие функции или код для выполнения после вызова remove_duplicates()
