from cli_command import CLICommand
import logging
import os


class SortCommand(CLICommand):
    def __init__(self, path, folder):
        super().__init__('sort', path, folder)
        self.main_path = path

    def sort_dir(self):
        # Performs the sort command in the object's directory
        logging.info('Performing sort command')
        file_type_dict = {}

        for file in self.file_list:
            name, extension = os.path.splitext(file)
            extension = extension[1:]
            if not extension:
                continue
            if extension in file_type_dict:
                file_type_dict[extension] += 1
                self.write_to_log('info',
                                  'Found an additional file of type {extension}, {file_num} have been found so far'
                                  .format(extension=extension, file_num=file_type_dict[extension]))
            else:
                file_type_dict[extension] = 1
                self.write_to_log('info', 'Found a new file type {extension}'.format(extension=extension))
                try:
                    self.write_to_log('info',
                                      'Trying to create folder for type {extension}'.format(extension=extension))
                    os.mkdir(os.path.join(self.path, extension))
                except FileExistsError:
                    self.write_to_log('warning', 'Folder type {extension} already exists - continuing sorting')
            self.write_to_log('info',
                              'Moving file {name}.{extension} to its new folder'.format(name=name, extension=extension))
            os.replace(os.path.join(self.path, file), os.path.join(self.path, extension, file))
        if not file_type_dict:  # No files have been found in the directory
            self.end_message = 'Directory was empty or only contained folders'
            self.success_flag = False
        self.write_to_log('info', file_type_dict)
        self.check_failure()
        return file_type_dict
