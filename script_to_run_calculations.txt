import os
import paramiko
import time


class SSHConnections:
    def __init__(self, server, username, password, port=22):
        self.server = server
        self.username = username
        self.password = password
        self.port = port
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.server, username=self.username, password=self.password, port=self.port)

    def run_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8').strip()
        return output

    def get_folder_list(self, folder_path):
        command = f"ls -1 {folder_path}"
        folder_list = self.run_command(command).split('\n')
        return folder_list


    def move_folder(self, src_folder, dest_folder):
        sftp = self.ssh.open_sftp()
        try:
            sftp.rename(src_folder, dest_folder)
            return True
        except FileNotFoundError:
            return False

    def check_file_contains_word(self, folder_path, word):
        try:
            with self.ssh.open_sftp().open(f"{folder_path}/OUTCAR") as f:
                content = f.read().decode()
                if word in content:
                    return True
                else:
                    return False
        except IOError:
            # Если файл OUTCAR не найден, то пропускаем эту папку
            print('OUTCAR не найден')
            return False
 
    def check_file_contains_word_2(self, folder_path, word):
        try:
            with self.ssh.open_sftp() as sftp:
                file_list = sftp.listdir(folder_path)
                for filename in file_list:
                    if filename.startswith("slurm"):                        
                        file_path = folder_path + '/' + filename
                        with sftp.open(file_path, 'r') as file:
                            content = file.read().decode()
                            if word in content:
                                return True
                            else:
                                return False
        except IOError:
            # Если файлы slurm не найдены, то пропускаем эту папку
            print("slurm не найден")
            return False


    def close(self):
        self.ssh.close()


def start_task(ssh_conn, task_dir, in_process_dir):
    # get the first 5 folders in task_dir
    folder_list = ssh_conn.get_folder_list(task_dir)[:5]
    for folder in folder_list[:4]:
        # move the folder to in_process_dir
        success = ssh_conn.move_folder(f"{task_dir}/{folder}", f"{in_process_dir}/{folder}")
        if success:
            # run sbatch command in the folder
            new_remote_path = f"{in_process_dir}/{folder}"         
            ssh_conn.run_command(f"cd {new_remote_path} ; sbatch cherrystart") #starting task
            
            print(f"Folder {folder} moved to In_Process directory and sbatch command executed first beginning")
            time.sleep(10)  # Delay for sbatch command to start

def start_task_1(ssh_conn, task_dir, in_process_dir):
    folder_list = ssh_conn.get_folder_list(task_dir)
    for folder in folder_list[:1]:
        # move the folder to in_process_dir
        success = ssh_conn.move_folder(f"{task_dir}/{folder}", f"{in_process_dir}/{folder}")
        if success:
            # run sbatch command in the folder
            new_remote_path = f"{in_process_dir}/{folder}"
            
            ssh_conn.run_command(f"cd {new_remote_path} ; sbatch cherrystart") #starting task
 
            print(f"Folder {folder} moved to In_Process directory and sbatch command executed_second time")
            time.sleep(10)  # Delay for sbatch command to start


def main_loop(ssh_conn, task_dir, in_process_dir, done_dir):
    while True:
        # check if there are folders in task_dir to move to in_process_dir
        if len(ssh_conn.get_folder_list(task_dir)) == 0:
            print("All tasks completed.")
            break

        # wait for 10 minutes before checking the folders
        print("Waiting for 10 minutes...")
        time.sleep(600)
# check if any folder in in_process_dir is ready to move to done_dir
        folder_list = ssh_conn.get_folder_list(in_process_dir)
        found_folders = []
        for folder in folder_list:
            if ssh_conn.check_file_contains_word(f"{in_process_dir}/{folder}", 'General'):
                found_folders.append(folder)
                ssh_conn.move_folder(f"{in_process_dir}/{folder}", f"{done_dir}/Done_outcar/{folder}")
                print(f"Folder {folder} moved to Done_outcar directory.")

            elif ssh_conn.check_file_contains_word_2(f"{in_process_dir}/{folder}", 'DUE'):
                found_folders.append(folder)
                ssh_conn.move_folder(f"{in_process_dir}/{folder}", f"{done_dir}/Restart/{folder}")
                print(f"Folder {folder} moved to restart directory.")
        print(len(folder_list))
  
        checkout = ssh_conn.get_folder_list(in_process_dir)
        if len(checkout) <= 4:
            start_task_1(ssh_conn, task_dir, in_process_dir)

        #wait for 10 minutes before the next iteration
        print("Waiting for 10 minutes... before next iteration")
        time.sleep(600)


if __name__ == '__main__':
    # specify server credentials
    server = 'put your information here'
    username = 'put your information here'
    password = 'put your information here'

    # specify the directories
    task_dir = '/home/Work/Task'
    in_process_dir = '/home/Work/In_process'
    done_dir = '/home/Work/Done'

    # establish SSH connection
    ssh_conn = SSHConnections(server, username, password)

    # start new tasks
    start_task(ssh_conn, task_dir, in_process_dir) 

    # start the main loop
    main_loop(ssh_conn, task_dir, in_process_dir, done_dir)

    # close the SSH connection
    ssh_conn.close()