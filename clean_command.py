from cli_command import CLICommand
import logging
import os
import configuration


class CleanCommand(CLICommand):
    def __init__(self, path, folder):
        super().__init__('clean', path, folder)
        self.main_path = path
        self.window_size = configuration.WINDOW_SIZE
        self.deletion_threshold = configuration.DELETION_THRESHOLD

    def clean_dir(self):
        # Performs the clean command
        logging.info('Performing clean command')
        if len(self.file_list) == 0:
            self.success_flag = False
            self.end_message = 'No logs to erase (log folder is empty)'
        else:
            if len(self.file_list) > self.window_size:
                self.file_list = self.sort_files_by_date_time(self.file_list)
                iFile = 0
                if self.deletion_threshold > len(self.file_list):
                    self.write_to_log('warning', 'Tried to delete more logs than possible')
                    self.deletion_threshold = len(self.file_list)
                while iFile < self.deletion_threshold:
                    self.write_to_log('info', 'Deleting file {file}'.format(file=self.file_list[iFile]))
                    os.remove(os.path.join(self.path, self.file_list[iFile]))
                    iFile += 1
            else:
                self.success_flag = False
                self.end_message = 'File number was smaller than window size (no logs deleted)'

        self.check_failure()
