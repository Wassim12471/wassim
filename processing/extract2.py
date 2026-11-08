import re
def extract_from_row(row):

    pattern=re.compile(r'(\{3})\s+(\d{2})\s+(\d{2}:\d{2}:\d{2}).+:\s(\w+)')
    match=re.searsh(pattern,row)
    if match:
        print(f'month :{match.group(1)}\n day of month:{match.group(2)}\n'
              f'time :{match.group(3)}\n'
              f'message :{match.group(4)}'
        
        
        )