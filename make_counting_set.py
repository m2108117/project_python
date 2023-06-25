import os
import shutil

# задаем исходную папку и путь к новым папкам
source_dir = "D:\\WORK\\kod\\90\\RAN"
destination_dir = "D:\\WORK\\kod\\90\\RAN_2"

# получаем список файлов в исходной папке
file_list = os.listdir(source_dir)

# создаем новые папки в указанной директории
for i in range(len(file_list)):
    folder_name = f"Folder_{i+1}"
    os.makedirs(os.path.join(destination_dir, folder_name))

# скопировать каждый файл из исходной папки в созданные папки по порядку и переименовать в POSCAR
for i, filename in enumerate(file_list):

        folder_name = f"Folder_{i+1}"
        source_file_path = os.path.join(source_dir, filename)
        destination_file_path = os.path.join(destination_dir, folder_name, "POSCAR")
        shutil.copy(source_file_path, destination_file_path)
        print(f"Copied file {filename} to folder {folder_name} and renamed to POSCAR")