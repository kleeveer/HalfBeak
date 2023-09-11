'pcatlogy:0.1\nid:ip:username:action:target:status\n1:192.168.15.33:get:/:200'

def save_log_file(filename:str,title:str,header:list,data_to_save:list):
    """Save a log file

    Args:
        filename (str): name of file to save
        title (str): title of log
        header (list): header of log
        data_to_save (list): data of log
    """
    with open(f'{filename}.pclogy','w') as f:
        f.flush()
        f.write(f'info:pcatlogy:0.1\n')
        
        if ':' in title:
            title = title.replace(':','=')
        
        start_file = f'init:{title}\n'
        
        f.write(start_file)
        
        formated_header = 'head'
        for tag in header:
            formated_header += f':{tag}'
        formated_header += '\n'

        f.write(formated_header)
        
        formated_data = ''
        for row in data_to_save:
            formated_line = 'data'
            for column in row:
                formated_line += f':{column}'
            formated_line += '\n'
            formated_data += formated_line
        
        f.write(formated_data)
        
        endfile = f'stop:{title}'
        
        f.write(endfile)
        
def load_log_file(filename):
    """Load a log file by name

    Args:
        filename (string): name of file

    Returns:
        list: [title, header, data]
    """
    with open(f'{filename}.pclogy') as f:
        file_data = f.read()
        print(file_data.splitlines())
        
        file_data = f.read().splitlines()
        
        steps = [False,False,False]
        
        title = ''
        header = []
        data =  []
        
        for row in file_data:
            if ':' in row:
                row_data = row.split(':')
                if row[0] == 'init' and not steps[0]:
                    title = row[1]
                    steps[0] = True
                
                if row[0] == 'head' and not steps[1]:
                    header = row_data.remove(0)
                    steps[1] = True
                
                if row[0] == 'data' and steps[1]:
                    data.append(row_data.remove(0))
                                
                if row[0] == 'stop' and row[1] == title:
                    steps[2] = True
                    
        if all(steps):
            return title,header,data
        else:
            return steps
        




save_log_file('test','TEST',['id','home','pacts'],[[1,'a',32],[2,'b',64],[3,'c',128]])
load_log_file('test')