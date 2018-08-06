import csv

def form(clash1,clash2):
    with open("statistic.csv","w",encoding='utf-8') as f:
        filewriter=csv.writer(f,delimiter=',')
        filewriter.writerow(['Department','Average Credits','statistic of Clash of General Education','statistic of Clash of Physical Education'])
        for i in list(clash1.school()):
            for j in list(clash1.school()[i].department()):
                filewriter.writerow([j,clash1.school()[i].department()[j].average_credits(),clash1.school()[i].department()[j].Crash_data()['average'],clash2.school()[i].department()[j].Crash_data()['average']])