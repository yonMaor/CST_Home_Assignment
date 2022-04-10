import os
import logging
from datetime import datetime as dt


class CLICommand:
    def __init__(self, command_type, path, folder_name):
        # Constructs the CLICommand object
        # Args:
        #   str command_type: the type of command to be performed (sort, clean, or stat')
        #   str path: directory on which to perform the command
        self.main_path = path
        self.path = os.path.join(path, folder_name)
        self.logger = logging.getLogger("CLI_Logger")
        self.log_name = ('log_' + dt.now().strftime("%d_%m_%Y_%H_%M_%S") + '.log')
        self.set_logger_properties(self.log_name)
        self.success_flag = True
        self.command_type = command_type
        self.end_message = 'Command (' + self.command_type + ') was successfully run'
        self.file_list = None
        self.get_file_list()
        self.check_path_and_type()
        self.write_to_log('info',
                          'Creating CLICommand object of type {type} for path {path}'.format(type=command_type,
                                                                                             path=self.path))

    def check_path_and_type(self):
        # Checks the path and command strings
        if not self.path or not os.path.isdir(self.path):
            self.end_message = 'Bad path entered, please enter a correct path'
            self.write_to_log('error', 'Bad path entered, please enter a correct path')
        if not self.command_type == 'sort' and not self.command_type == 'clean' and not self.command_type == 'stat':
            self.end_message = 'Chosen command does not exist, please choose an existing command'
            self.write_to_log('error', 'Chosen command does not exist, please choose an existing command')

    def get_file_list(self):
        # Gets the list of files in self.path
        try:
            self.file_list = os.listdir(self.path)
        except OSError:
            failure_text = 'Folder does not exist (' + self.path + ')'
            self.write_to_log('error', failure_text)
            self.end_message = failure_text
            self.success_flag = False

    def write_to_log(self, log_type, log_text):
        # Handles writing to the log file
        print(log_text)
        if log_type == 'info':
            logging.info(log_text)
        elif log_type == 'error':
            logging.error(log_text)
        elif log_type == 'warning':
            logging.warning(log_text)

    def sort_files_by_date_time(self, file_list):
        # Sorts list of files in chronological order (oldest to newest)
        # Args:
        #   list file_list: list of files
        file_list.sort(key=lambda x: os.path.getmtime(os.path.join(self.path, x)))
        return file_list

    def check_failure(self):
        self.write_to_log('info', self.end_message)

    def set_logger_properties(self, log_name):
        # Sets initial logger properties
        logging.basicConfig(filename=os.path.join(self.main_path, 'log', log_name), filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S', level=logging.DEBUG)

    @staticmethod
    def raise_error(error_text):
        # Raises an exception
        raise Exception(error_text)
        logging.error(error_text)
