import os


class LogObj:
    def __init__(self, path):
        self.path = path
        self.successful = None
        self.command_type = None
        self.read_file()

    def read_file(self):
        with open(self.path) as file:
            if os.stat(self.path).st_size == 0:
                self.command_type = 'error'
                self.successful = 'error'
            else:
                first_line = file.readline().rstrip()
                if 'sort' in first_line:
                    self.command_type = 'sort'
                elif 'clean' in first_line:
                    self.command_type = 'clean'
                elif 'stat' in first_line:
                    self.command_type = 'stat'
                else:
                    self.command_type = 'error'

                for line in file.readlines():
                    pass
                if self.path == "D:\Yonatan\Projects\CST_home_assignment\log\log_09_04_2022_20_56_08.log":
                    print("HI")
                print(self.path)
                last_line = line
                if 'Failure' in last_line:
                    self.successful = False
                elif 'Success' in last_line:
                    self.successful = True
                else:
                    self.successful = 'error'
