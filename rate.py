import urllib
import re
from bs4 import BeautifulSoup

def countPositive(positive_words,negativeOfPositive,page):
    search=[]
    delete=[]
    for positiveWord in positive_words:
        search+=re.findall(positiveWord, page)
    for deleteWord in negativeOfPositive:
        delete+=re.findall(deleteWord,page)
    numOfPositiveWords=len(search)
    numOfNegPositive=len(delete)
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

def calc_point(link,course):
    page = urllib.urlopen(link).read()
    positive_words=["good","awesome","fantastic","like","recommend","best","enlightening","clear","amazing"]
    positive_words+=[word.title() for word in positive_words]
    negativeOfPositive=["isn't "+word for word in positive_words]+["not "+word for word in positive_words]+["doesn't "+word for word in positive_words]+["don't "+word for word in positive_words]
    negative_words=["bad","avoid","worst","never"]
    negative_words+=[word.title() for word in negative_words]
    #review={}

    num_comments=readWords(page)[0]
    dic_comments=readWords(page)[1]
    lst=dic_comments[course]
    sum_lst=0
    for elem in lst:
        sum_lst+=elem[0]-elem[1]
    result=(countPositive(positive_words,negativeOfPositive,page)-countNegative(negative_words,negativeOfPositive,page))/num_comments+sum_lst/num_comments
    return result

    
    
