"""
@author:Franco Mosquera Bonasorte
"""

import csv
import datetime

def storer(col1, col2, col3,col4):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    with open('data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([col1, col2, col3,col4, current_time])
        
def main():
    storer("dato1","dato2","dato3","dato4")
        
        
if __name__ == "__main__":
    main()