import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as matchs
from scipy import stats
__my_color=['r','g','b','c','k','lime','m','orange','purple','r','g','b']
def CrashVisualize(dic_data,for_what,title=None,xlabel=None,ylabel=None):
    x=[]
    y=[]
    k=0
    global __my_color
    school_color=[]
    barcolor=[]
    school_name=[]
    for i in list(dic_data):
        school_name.append(i)
        school_color.append(__my_color[k])
        for j in list(dic_data[i]):
            barcolor.append(__my_color[k])
            x.append(j)
            y.append(dic_data[i][j][for_what])
        k+=1
    graph(x,y,barcolor,school_name,school_color,title,xlabel,ylabel)
    
    return [x,y]

def DepartmentVisualize(dict_data,title,xlabel,ylabel):
    x=[]
    y=[]
    barcolor=[]
    school_name=[]
    school_color=[]
    k=0
    global __my_color
    for i in list(dict_data):
        school_name.append(i)
        school_color.append(__my_color[k])
        for j in list(dict_data[i].department()):
            barcolor.append(__my_color[k])
            y.append(dict_data[i].department()[j].average_credits())
            x.append(j)
        k+=1
    graph(x,y,barcolor,school_name,school_color,title,xlabel,ylabel)

    return [x,y]

def graph(x,y,barcolor,school,school_color,title,xlabel,ylabel):
    plt.figure(figsize=(20,5))
    barls=plt.bar(x,y)
    k=0
    while k<len(list(barls)):
        barls[k].set_color(barcolor[k])
        k+=1
    label=__match_color(school,school_color)
    plt.legend(handles=label)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)
    plt.show()


def __match_color(school,school_color):
    match=[]
    try:
        for i in range(len(school_color)):
            match.append(matchs.Patch(color=school_color[i],label=school[i]))
    except IndexError as p:
        print('barcolor',len(school_color))
        print('school',len(school))
        print(school)
        print(school_color)
    return match

def RelativeVisulize(x,y,text=None,title=None,xlabel=None,ylabel=None):
    plt.figure(figsize=(20,5))
    ax=plt.subplot()
    ax.scatter(x,y)
    if text is not None:
        for i,txt in enumerate(text):
            ax.annotate(txt,(x[i],y[i]))
    slope,intercept,r_value,p_value,std_err=stats.linregress(x,y)
    plt.plot(np.array(x),np.array(x)*slope+intercept,'r',label='y={:.2f}x+{:.2f}'.format(slope,intercept))
    plt.legend(['y={:.2f}x+{:.2f} Correlation Coefficient = {:2f}'.format(slope,intercept,r_value),'department'])
    #print(r_value)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.show()

