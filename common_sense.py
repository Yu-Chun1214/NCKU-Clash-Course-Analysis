import re
import student
import pandas as pd
import json
import numpy as np
import matplotlib.patches as matchs
from pattern import graph
from matplotlib import pyplot as plt
from requests_html import HTMLSession
class General_edu(student.grade):
    def __init__(self,url):
        self.courses=[]
        self.amount=0
        self.url=url
    def Course(self,name,necessary,credits,hours,time,time_str,time_re):
        if credits is '':
            credits=0
        else:
            credits=float(credits)
        Subject={
            'Name':name,
            'Necessary':True,
            'Credits':float(credits),
            'Hours':hours,
            'Time':time,
            'Time_str':time_str,
            'Time_re':time_re
        }
        self.courses.append(Subject)
        self.amount+=1
    
    def course(self):
        return self.courses
    
    def Search(self,u_want):
        #url='http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=A9'
        session=HTMLSession()
        response=session.get(self.url)
        elements=response.html.find(u_want)
        #GE=General_edu()
        for i in elements:
            course=i.find('td')
            day_time,hours=student.times(course[16].text)
            self.Course(course[10].text,course[11].text,course[12].text,hours,{day_time[0]:day_time[1]},{course[16].text[3:]:course[16].text[0:3]},{course[16].text[0:3]:course[16].text[3:]})
        return self
    
    def Crash(self,university):
        university.Crash_data_init()
        for i in self.courses:
            university.Crash(i)
        return university

    def Statistic(self,name):
        self.__statisitc={}
        for i in self.courses:
            self.__judge(i['Time_str'],self.__statisitc)
        self.__re_statistic={}
        for i in self.courses:
            self.__judge(i['Time_re'],self.__re_statistic)
        with open('{} statistic.json'.format(name),'w') as f:
            f.write(json.dumps(self.__re_statistic,indent=4))
        #print(json.dumps(self.__statisitc,ensure_ascii=False,indent=4))
    def __judge(self,course_time,statistic):
        key = list(course_time)[0]
        class_time=course_time[key]
        if class_time == "未定" or class_time=='':
            class_time="Undecided"
        if key=='' or key=='未定':
            key='Undecided'
        days=list(statistic)
        for day in days:
            if key == day:
                for j in list(statistic[day]):
                    if j == class_time:
                        statistic[day][class_time]+=1
                        return
                statistic[day][class_time]=1
                return
        statistic[key]={}
        statistic[key][class_time] = 1 
        return
    def Visualize(self,title):
        x=[]
        bar_statistic={}
        colors=['k','r','g','b','m','lime','m','orange','k','grey']
        for i in list(self.__statisitc):
            for j in list(self.__statisitc[i]):
                x.append(j)
        lsSetx=list(set(x))
        lsx=self.__sort(lsSetx)
        time=list(self.__statisitc)
        ind=0
        bar_width = 0.18  # the width of the bars
        fig, ax = plt.subplots(figsize=(30,5))
        for i in time:
            position=ind-((len(list(self.__statisitc[i])))/2)*bar_width
            for j in list(self.__statisitc[i]):
                try:
                    ax.bar(position,self.__statisitc[i][j],width=bar_width,color=colors[int(j[1])])
                    position+=bar_width
                except:
                    ax.bar(position,self.__statisitc[i][j],width=bar_width,color='grey')
            ind+=1
        ind = np.arange(len(time))
        ax.set_xticks(ind-bar_width/2)
        ax.set_xticklabels(time)
        match=[]
        for i in lsx:
            try:
                match.append(matchs.Patch(color=colors[int(i[1])],label=i))
            except:
                match.append(matchs.Patch(color='grey',label=i))
        plt.legend(handles=match)
        plt.xlabel('{} Course Time'.format(title))
        plt.ylabel('Course Statistics')
        plt.show()

    def __sort(self,lsX):
        size=len(lsX)
        for i in range(size):
            try:
                int(lsX[i][1])
            except:
                temp=lsX[i]
                lsX[i]=lsX[size-1]
                lsX[size-1]=temp
                break
        
        for i in range(size-1):
            for j in range(size-2):
                try:
                    
                    if int(lsX[j][1]) > int(lsX[j+1][1]):
                        temp=lsX[j]
                        lsX[j]=lsX[j+1]
                        lsX[j+1]=temp
                except:
                    print("j",j)
                    print("j+1",j+1)
                    print("lsX[j+1][1]",lsX[j+1][1])
                    print("size",size)
                    input()
        
        return lsX