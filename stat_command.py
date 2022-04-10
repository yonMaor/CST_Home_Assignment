from cli_command import CLICommand
import logging
import os
from log_obj import LogObj
import datetime
import csv


class StatCommand(CLICommand):
    def __init__(self, path, folder):
        super().__init__('stat', path, folder)
        self.main_path = path

    def dir_stat(self, time_stamp):
        # Performs the stat command
        # Args:
        #   str time_stamp: time_stamp at which stat counting starts
        time_stamp = self.check_convert_time_stamp(time_stamp)
        print(time_stamp)
        logging.info('Performing stat command')
        # Find all logs after time_stamp
        sorted_file_list = self.sort_files_by_date_time(self.file_list)
        use_dict = {'sort': 0, 'clean': 0, 'stat': 0}
        success_dict = {'sort': 0, 'clean': 0, 'stat': 0}
        failure_dict = {'sort': 0, 'clean': 0, 'stat': 0}
        for file in sorted_file_list:
            if time_stamp != 'failure':
                if self.compare_time_stamps(os.path.getmtime(os.path.join(self.path, file)),
                                            time_stamp):  # File is relevant
                    self.write_to_log('info', '{file} is relevant to stats'.format(file=file))
                    log_obj = LogObj(os.path.join(self.path, file))
                    if log_obj.command_type == 'error':
                        self.write_to_log('warning', file + ' has no clear command type')
                        continue
                    use_dict[log_obj.command_type] += 1
                    if log_obj.successful == True:
                        success_dict[log_obj.command_type] += 1
                    elif log_obj.successful == False:
                        failure_dict[log_obj.command_type] += 1
                    else:
                        self.write_to_log('warning', file + ' did not clearly succeed or fail')
                        continue
            else:
                break
        if time_stamp != 'failure':
            self.write_results_to_csv(use_dict, failure_dict)

        self.check_failure()

    def check_convert_time_stamp(self, time_stamp):
        if type(time_stamp) == datetime:
            return time_stamp
        elif type(time_stamp) == str:
            try:
                time_stamp = datetime.datetime.strptime(time_stamp, '%d/%m/%y %H:%M')
            except ValueError:
                self.end_message = 'User time is stamp not according to required format'
                self.success_flag = False
                time_stamp = 'failure'
        else:
            self.end_message = 'User time stamp is not according to required format'
            self.success_flag = False
            time_stamp = 'failure'
        return time_stamp

    def write_results_to_csv(self, use_dict, failure_dict):
        # Writes stat results to a csv file
        # Args:
        #   dict use_dict: Dictionary with the number of uses of each command
        #   dict failure_dict: Dictionary with the number of failures of each command
        with open(os.path.join(self.main_path, 'stat_results.csv'), 'w') as f:
            writer = csv.writer(f)
            rows = [['Number of Uses'],
                    ['Sort', use_dict['sort']],
                    ['Clean', use_dict['clean']],
                    ['Stat', use_dict['stat']]]
            for row in rows:
                writer.writerow(row)

            rows = [['Number of Failures'],
                    ['Sort', failure_dict['sort']],
                    ['Clean', failure_dict['clean']],
                    ['Stat', failure_dict['stat']]]
            for row in rows:
                writer.writerow(row)

            rows = [['Most Used Command', max(use_dict, key=lambda x: use_dict[x])],
                    ['Least Used Command', min(use_dict, key=lambda x: use_dict[x])],
                    ['Most Failed Command', max(failure_dict, key=lambda x: failure_dict[x])]]
            for row in rows:
                writer.writerow(row)

    @staticmethod
    def compare_time_stamps(file_time_stamp, user_time_stamp):
        # Compares two time stamps. Returns True if user_time_stamp is earlier and false if file_time_stamp is earlier
        # Args:
        #   float file_time_stamp: file last modification time in seconds since epoch
        #   datetime user_time_stamp: time entered by the user for the stat function
        user_time_stamp = user_time_stamp.timestamp()
        if file_time_stamp < user_time_stamp:
            return False
        else:
            return True
