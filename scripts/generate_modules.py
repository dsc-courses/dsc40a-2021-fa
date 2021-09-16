# generate_modules.py
# Use this to convert from the course calendar spreadsheet to modules that work with the course website template.
# Only run it on the weeks that haven't occurred yet, otherwise it'll erase any manual work.
# Run from the root directory of this repo, **not** from the scripts folder.

import pandas as pd
import os
import sys
import numpy as np

df = pd.read_csv('scripts/Lecture Schedule – DSC 40A, Fall 2021 - Sheet1.csv')

df['Week'] = df['Week'].fillna(method = 'ffill').astype(int)
df['#'] = df['#'].fillna(0).astype(int)
# df['Lab'] = df['Lab'].astype(str)
df['Homework'] = df['Homework'].astype(str)

# df = df.iloc[:-2]

month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

def round_format(i):
    return "0" + str(i) if int(i) <= 9 else str(i)

def date_conv(date, date_format='MONTH/DAY', YEAR=2021):
    if date_format == 'DATE. MONTH. DAY':
        try:
            _, month, day = date.split(" ")
        except:
            print(date)

        month = month_map[month]
        month = round_format(month)
        day = round_format(day)

        return f"{YEAR}-{month}-{day}"
    
    elif date_format == 'MONTH/DAY':
        try:
            month, day = date.split("/")
        except:
            print(date)
            
        return f"{YEAR}-{month}-{day}"

# for a single week
def write_week(i, dest = '_modules', write = True):
    week = df[df['Week'] == i].reset_index()
    outstr = f"""---
    title: Week {i}
    weekNumber: {i}
    days:"""
    for j in range(len(week)):
        lec_num = week.loc[j, '#']
        if lec_num != 0:
            date_formatted = date_conv(week.loc[j, 'Date'])
            outstr += f"""
      - date: {date_formatted}
        events:
          "**{lec_num}**{{: .label .label-gray }} {week.loc[j, 'Lecture']}":"""
        
        # a quiz or other non-instructional day
        if lec_num == 0:
            date_formatted = date_conv(week.loc[j, 'Date'])
            
            if 'Exam' in week.loc[j, 'Lecture']:
                outstr += f"""
      - date: {date_formatted}
        events:
          "**Midterm** {week.loc[j, 'Lecture']}":"""
            else:
                outstr += f"""
      - date: {date_formatted}
        events:
          "{week.loc[j, 'Lecture']}":"""
        
#         if week.loc[j, 'Lab'] != 'nan':
#             lab_num, lab_name = week.loc[j, 'Lab'].split('. ')
#             date_formatted = date_conv(week.loc[j, 'Date'])
#             outstr += f"""
#           "**Lab {lab_num}**{{: .label .label-lab }} {lab_name}":"""
            
#         if week.loc[j, 'Homework'] != 'nan':
#             hw_num, hw_name = week.loc[j, 'Homework'].split('. ', 1)
#             date_formatted = date_conv(week.loc[j, 'Date'])
#             outstr += f"""
#           "**Homework {hw_num}**{{: .label .label-hw }} {hw_name}":"""
    
    outstr += "\n---"
    
    if write:
        # if not dest in os.listdir():
        #     os.system(f'mkdir {dest}')

        # print(dest + '/week-' + round_format(i) + '.md')

        f = open(dest + '/week-' + round_format(i) + '.md', 'w')
        f.write(outstr)
        f.close()
    else:
        return outstr

if len(sys.argv) > 1:
    start_from = int(sys.argv[1])
else:
    start_from = np.min(df['Week'])

for i in range(start_from, 12):
    write_week(i)