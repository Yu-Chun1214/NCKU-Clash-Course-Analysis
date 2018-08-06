import student
import pattern
import csvfile
import copy
from common_sense import General_edu
from requests_html import HTMLSession
import matplotlib.pyplot as plt

ncku=student.Ncku()
ncku.Search()

Gurl='http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=A9'
GE=General_edu(Gurl)
GE.Search('.course_y0')
GECrash=copy.deepcopy(GE.Crash(ncku))

GE.Statistic('GE')
GE.Visualize('General Education')
Crash_data=pattern.CrashVisualize(GECrash.Crash_data(),'average','The Statistic of Clash Course Between General Education Course and The Required Course of Departments','Department','Statistics')
Department_data=pattern.DepartmentVisualize(ncku.school(),'The Statistic of The Required Course Credits of Departments','Department','Statistics')
pattern.RelativeVisulize(Crash_data[1],Department_data[1],Crash_data[0],'The Statistic of The Correlation Between Required Credits and Clash Course Statistic of General Education Course','Statistic of Clash Course','Required Credits')



Purl='http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=A2'
PE=General_edu(Purl)
PE.Search('.course_y2')
PECrash=PE.Crash(ncku)
PE.Statistic('PE')
PE.Visualize("Physical Education")
#Crash_data=[]
Crash_data=pattern.CrashVisualize(PECrash.Crash_data(),'average','The Statistic of Clash Course Between Physical Education Course and The Required Course of Departments','Department','Statistics')
pattern.RelativeVisulize(Crash_data[1],Department_data[1],Crash_data[0],'The Statistic of The Correlation Between Required Credits and Clash Course Statistic of Physical Education Course','Statistic of Clash Course','Required Credits')


csvfile.form(GECrash,PECrash)