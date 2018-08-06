import re
from requests_html import HTMLSession
class grade:
    def __init__(self):
        self.__course=[]
        self.__credit=0

    def Course(self,name,necessary,credits,hours,time):
        for i in self.__course:
            if name == i['Name']:
                return
        pattern1=r'GENERAL EDUCATION'
        pattern2=r'PHYSICAL EDUCATION (3)'
        match1=re.search(pattern1,name)
        if match1 is not None:
            return
        if pattern2 == name:
            return
        if credits is '':
            credits=0
        else:
            credits=float(credits)
        pattern=r'Elective'
        match=re.search(pattern,necessary)
        if match is not None:
            return   
        else:
            yn=True
        Subject={
            'Name':name,
            'Necessary':yn,
            'Credits':float(credits),
            'Hours':hours,
            'Time':time
        }
        crash=self.Crash(Subject)
        if crash is True:
            self.__course.append(Subject)
            self.__credit+=credits
        else:
            return
        
    def credit(self):
        return self.__credit

    def course(self):
        return self.__course
    
    def Crash(self,check_course):
        for i in self.__course:
            judge=self.__crash(i,check_course)
            if judge is False:
                return False
        return True

    def __crash(self,course,check):#use intersection to judge the crash class
        course_day=set(list(course['Time']))
        check_course_day=set(list(check['Time']))
        day_intersrction=course_day & check_course_day
        if len(day_intersrction) == 0:
            return True
        else:
            for i in day_intersrction:
                course_time=set(list(course['Time'][i]))
                check_time=set(list(check['Time'][i]))
                time_intersection=course_time & check_time
                if len(time_intersection) != 0:
                    return False
            return True

    

def times(time):    #time function is to change the time data get from website.ex:'[1]5~6' become '[1]':[5,6] also compute the course time
    a=time[0:3]
    if len(time)>3:
        b=time[3:].split('~')
        num=[]
        for i in b:
            if i is 'N':
                i=4.5
                num.append(float(i))
            elif i is 'A':
                i=10
                num.append(i)
            elif i is 'B':
                i=11
                num.append(i)
            elif i is 'C':
                i=12
                num.append(i)
            elif i is 'D':
                i=13
                num.append(i)
            elif i is 'E':
                i=14
                num.append(i)
            else:
                num.append(int(i))
        if len(num)>=2:
            if num[1]-num[0]>1:
                final=num.pop()
                for i in range(int(num[0])+1,int(final+1)):
                    num.append(i)
        hours=len(num)
        
        return [a,num],hours
    else:
        return [a,[0]],0

class department():
    def __init__(self):
        self.__grade_data={}
        self.__grade={}
        self.__crash_num={}
        self.__grade_data['total']=0 
        self.__grade_data['average']=1
    
    def Grade(self,course,grade):
        self.__grade_data[grade]=course.course()
        self.__grade[grade]=course
        self.__grade_data['total']+=course.credit()
        self.__crash_num[grade]=0
        self.__average_credits()
    
    def __average_crash_num(self,num):
        return round(num/len(list(self.__grade)),3)
    
    def Crash(self,course):
        grades=list(self.__grade)
        time=0
        for i in grades:
            crash=self.__grade[i].Crash(course)
            if crash is False:
                self.__crash_num[i]+=1
            time+=self.__crash_num[i]
              
        self.__crash_num['total']=time
        self.__crash_num['average']=self.__average_crash_num(time)

        return self.__crash_num
    
    def grade(self):
        return self.__grade

    def Crash_data(self):
        return self.__crash_num

    def Crash_data_init(self):
        grades=list(self.__grade)
        for i in grades:
            self.__crash_num[i]=0

    def __average_credits(self):
        num=len(list(self.__grade_data))-2
        if num!=0:
            self.__grade_data['average']=round(self.__grade_data['total']/num,3)

    def total_credits(self):
        return self.__grade_data['total']

    def average_credits(self):
        self.__average_credits()
        return self.__grade_data['average']

    def grade_data(self):
        return self.__grade_data
            

class school():
    def __init__(self):
        self.__department_data={}
        self.__department={}
        self.__school_credits=0
        self.__dept_num=0
        self.__crash_data={}
        self.__CrashStatic={}
    def Department(self,department,fule_name):
        name=fule_name[1:4]
        self.__department_data[name]=department.grade_data()
        self.__department[name]=department
        self.__school_credits+=department.total_credits()
        self.__crash_data[name]={}
        self.__dept_num+=1
    def avg_credits(self):
        self.__avgcredits=round(self.__school_credits/self.__dept_num,3)
        return(self.__avgcredits)
    def Crash(self,course):
        departments=list(self.__department)
        for i in departments:
            self.__crash_data[i]=self.__department[i].Crash(course)
        return self.__crash_data
    def Crash_data(self):
        return self.__crash_data    
    def Crash_data_init(self):
        departments=list(self.__department)
        for i in departments:
            self.__department[i].Crash_data_init()
    def dept_amount(self):
        return self.__dept_num
    def department_data(self):
        return self.__department_data
    def department(self):
        return self.__department



class Ncku():
    def __init__(self):
        self.__school_data={}
        self.__school={}
        self.__crash_data={}
    
    def School(self,school,name):
        self.__school_data[name]=school.department_data()
        self.__school[name]=school
        self.__crash_data[name]={}
   
    def Search(self):
        url='http://course-query.acad.ncku.edu.tw/qry/'
        en_url='http://course-query.acad.ncku.edu.tw/qry/index.php?lang=en'
        session=HTMLSession()
        response=session.get(en_url)
        blocks=response.html.find('ul[id=dept_list] li')
        pattern=r'College'
        for i in blocks[3:]:
            dept=i.find('.dept')
            schoo=school()
            for j in dept:
                element=j.find('a')
                url_dept=url+element[0].attrs['href']
                response2=session.get(url_dept)                    
                depmnt=department()
                match=re.search(pattern,j.text)
                if match is not None or len(j.text)<=7:
                    continue                      
                for k in range(1,4):
                    Grade=grade()
                    elements=response2.html.find('.course_y{}'.format(k))
                    if len(elements) is 0:
                        break
                    for l in elements:#l is a subject
                        class_time={}
                        hours=0
                        h=0
                        sub=l.find('td')
                        classtime=sub[16].find('br')
                        for m in classtime:
                            cltime,h=times(m.text)                                    
                            hours+=h                                
                            class_time[cltime[0]]=cltime[1]
                        Grade.Course(sub[10].text,sub[11].text,sub[12].text,hours,class_time)
                    depmnt.Grade(Grade,str(k))
                schoo.Department(depmnt,str(j.text))
            self.School(schoo,i.find('.theader')[0].text)
        return self
        
    def Crash(self,course):
        schools=list(self.__school)
        for i in schools:
            self.__crash_data[i]=self.__school[i].Crash(course)
            
        return self.__crash_data

    def Crash_data(self):
        return self.__crash_data
        
    def Crash_data_init(self):
        schools=list(self.__school)
        for i in schools:
            self.__school[i].Crash_data_init()
    
    def school(self):
        return self.__school
    
    def school_data(self):
        return self.__school_data