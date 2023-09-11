import os

from datetime import timedelta, timezone, datetime

class Log:
    def __init__(self,log_name:str,header:list,base_log_dir='./log/folder'):
        self.base_log_dir=base_log_dir
        self.log_name = log_name
        header.insert(0,'horario')
        self.header = header
    
    def logger(self,log:list):
        abs_path = os.path.join(self.base_log_dir, self.log_name)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        
        current_date = datetime.now((timezone(timedelta(hours=-3))))
        file_name = f'{current_date.strftime("%x").replace("/", "-")}.log'
        abs_file_path = os.path.join(abs_path, file_name)
        
        if not os.path.isfile(abs_file_path):
            with open(abs_file_path, 'w') as f:
                f.write(self.format_to_log('H',self.header))
                f.close()
        
        with open(abs_file_path, 'a') as f: 
            log.insert(0,datetime.now().strftime('%X'))
            f.write(self.format_to_log('D',log))
            f.close()

    def format_to_log (self,mode,data:list):
        formated_text = '#'+mode
        for x in data:
            formated_text += f'&-{x}'
        return formated_text+'\n'
    
    def format_to_python (self,data:str):
        bunch_of_lines = data.splitlines()

        headers = []
        logs = []
        
        for line in bunch_of_lines:
            line_splited = line.split('&-')
            print(line_splited)
            if line_splited[0] == '#D':
                line_splited.pop(0)
                logs.append(line_splited)
            elif line_splited[0] == '#H':
                line_splited.pop(0)
                headers = line_splited
                
        return headers, logs