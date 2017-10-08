import urllib
import re
from bs4 import BeautifulSoup

positive_words=["good","awesome","fantastic","like","recommend","best","enlightening","clear","amazing","kind","care"]
negativeOfPositive=["isn't "+word for word in positive_words]+["not "+word for word in positive_words]+["doesn't "+word for word in positive_words]+["don't "+word for word in positive_words]
negativeOfPositive+=[word.title() for word in negativeOfPositive]
positive_words+=[word.title() for word in positive_words]
negative_words=["bad","avoid","worst","never","accent"]
negative_words+=[word.title() for word in negative_words]


def getProfessorID():
    #math_url='http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=5000&callback=noCB&q=*%3A*+AND+schoolid_s%3A1072+AND+teacherdepartment_s%3A%22Mathematics%22&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=20&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq=&prefix=schoolname_t%3A%22University+of+California+Berkeley%22'
    url='http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=3580&callback=noCB&q=*%3A*+AND+schoolid_s%3A1072&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=20&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq=&prefix=schoolname_t%3A%22University+of+California+Berkeley%22'
    #cs_url='http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=2000&callback=noCB&q=*%3A*+AND+schoolid_s%3A1072+AND+teacherdepartment_s%3A%22Computer+Science%22&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=20&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq=&prefix=schoolname_t%3A%22University+of+California+Berkeley%22'
    lstOfProfessorID=[]
    lstOfProfessorName=[]
    dic={}
    sameName=[]
    page = urllib.urlopen(url).read()
    
    soup = BeautifulSoup(page,"html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    lines=list(text.splitlines())
    
    for i in range(len(lines)-4):
        if("pk_id" in lines[i]):
            professorID=int(lines[i][8:len(lines[i])-1])
            #lstOfProfessorID+=[int(lines[i][8:len(lines[i])-1])]
        if("teacherfirstname_t" in lines[i+3] and "teacherlastname_t" in lines[i+4]):
            professorName=lines[i+4][21:len(lines[i+4])-3]+', '+lines[i+3][22]
            #lstOfProfessorName+=[professorName.upper()]
            if(professorName.upper() not in dic):
                dic[professorName.upper()]=professorID
            else:
                sameName+=[professorName.upper()]
    return dic,sameName
    

def countPositive(positive_words,negativeOfPositive,page):
    search=[]
    delete=[]
    for positiveWord in positive_words:
        search+=re.findall(positiveWord, page)
    for deleteWord in negativeOfPositive:
        delete+=re.findall(deleteWord,page)
    numOfPositiveWords=len(search)
    numOfNegPositive=len(delete)
    print search
    return numOfPositiveWords-numOfNegPositive

def countNegative(negative_words,negativeOfPositive,page):
    search=[]
    delete=[]
    for negativeWord in negative_words:
        search+=re.findall(negativeWord, page)
    for deleteWord in negativeOfPositive:
        delete+=re.findall(deleteWord,page)
    numOfNegativeWords=len(search)
    numOfNegPositive=len(delete)
    return numOfNegativeWords+numOfNegPositive



def readWords(page):
    soup = BeautifulSoup(page,"html.parser")
    quality=[]
    difficulty=[]
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    lines=list(text.splitlines())
    classes=[]
    index_classes=0
    for i in range(len(lines)):
        if lines[i]=='All Classes':
            index_classes=i
            break
    for j in range(index_classes+1,len(lines)):
        if lines[j]=='Comment':
            break
        else:
            classes+=[lines[j]]
    dic={}
    p=re.compile('(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.](19|20)\d\d')
    num=0
    for i in range(len(lines)):
        if p.match(lines[i]):
            num+=1
            #quality+=[float(lines[i+2])]
            #difficulty+=[float(lines[i+4])]
            if lines[i+6] not in dic.keys():
                dic[lines[i+6]]=[(float(lines[i+2]),float(lines[i+4]))]
            else:
                dic[lines[i+6]]+=[(float(lines[i+2]),float(lines[i+4]))]
    return num,dic

def calc_point(nameOfProfessor,course):
    ID=str(getProfessorID()[0][nameOfProfessor])
    link="http://www.ratemyprofessors.com/ShowRatings.jsp?tid="+ID
    page = urllib.urlopen(link).read()

    num_comments=readWords(page)[0]
    dic_comments=readWords(page)[1]
    lst=dic_comments[course]
    sum_lst=0
    for elem in lst:
        sum_lst+=elem[0]-elem[1]
    result=sum_lst/num_comments
    return result/4


def ratemyprofessor():
    ratings={}
    names=(getProfessorID()[0]).keys()
    for name in names:
        ID=str(getProfessorID()[0][name])
        link="http://www.ratemyprofessors.com/ShowRatings.jsp?tid="+ID
        page = urllib.urlopen(link).read()
        num_comments,dic_comments=readWords(page)
        courses=dic_comments.keys()
        for course in courses:
            lst=dic_comments[course]
            sum_lst=0
            for elem in lst:
                sum_lst+=elem[0]-elem[1]
            result=sum_lst/(num_comments*4)
            ratings[(name,course)]=result
            print (name,course),result 
    return ratings
