from calendar import c
import errno
from filecmp import cmp
from re import A
import tkinter.messagebox
from tkinter import *
from tkinter import messagebox
from turtle import end_fill
from warnings import catch_warnings
from numpy import append, sort
import functools
import math
import os
import jieba
from regex import P

#查询语句显示
se=""
#链表类
class Posting():
    def __init__(self,docID,term_freq):
        self.docID = docID
        self.term_freq = term_freq
        self.weight = 0
        self.next = None
#字典类
class Dictionary():
    def __init__(self,term,Doc_num,Coll_freq):
        self.term = term
        self.Doc_num = Doc_num
        self.Coll_freq = Coll_freq
        # idf = lg(N/Doc_num)N为文档总数，Doc_num为term项出现的文档个数
        self.idf = math.log(n/Doc_num,10)
        self.posting_list = None

#路经
path = os.getcwd() + '\\唐诗三百首\\'
files_path = os.listdir(path)

#诗词总数
n = 294

#正文二元组
bigram_list = []

#剔除标点
punctuation = ['，','。','？','！','；']

#正文字典
dictionary = {}

#标提二元组
bigram_list_title=[]
#标题字典
dictionary_title={}

#title二元组生成
for i in range(0,n):
    bigram = {}
    poet = files_path[i].replace(" ","")
    test=jieba.lcut(poet)
    for character in test:
        if character in punctuation: continue
        else:
            if character in bigram.keys():
                bigram[character] = bigram[character]+1
            else:
                bigram[character] = 1
    for character in poet:
        if character in punctuation:
            continue
        else:
            if character in bigram.keys():
                bigram[character] = bigram[character] + 1
            else:
                bigram[character] = 1
    bigram_list_title.append(bigram)

#标题字典生成
for i in range(0,n):
    for character in bigram_list_title[i]:
        if character in punctuation: continue
        else:
            if character in dictionary_title.keys():
                dictionary_title[character].Doc_num = dictionary_title[character].Doc_num + 1
                dictionary_title[character].Coll_freq = dictionary_title[character].Coll_freq + bigram_list_title[i][character]
                posting = Posting(i,bigram_list_title[i][character])
                ptr = dictionary_title[character].posting_list
                # 查找最后一个文档
                while ptr.next!=None:
                    ptr = ptr.next
                ptr.next = posting
            else:
                dictionary_title[character] = Dictionary(character,1,bigram_list_title[i][character])
                posting = Posting(i,bigram_list_title[i][character])
                dictionary_title[character].posting_list = posting

# 生成正文2元组,(term,freq)
for i in range(0,n):
    bigram = {}
    f = open(path+files_path[i],'r')
    poet = f.read()
    test=jieba.lcut(poet)
    for character in test:
        if character in punctuation: continue
        else:
            if character in bigram.keys():
                bigram[character] = bigram[character]+1
            else:
                bigram[character] = 1
    for character in poet:
        if character in punctuation:
            continue
        else:
            if character in bigram.keys():
                bigram[character] = bigram[character] + 1
            else:
                bigram[character] = 1
    bigram_list.append(bigram)
# 生成一个dict(term,term对应的Dictionary)包含Posting_list
# Dictionray: term, Doc_num, Coll_freq(总频率), posting_list
# posting_list链表，Posting: DocID, term_freq
for i in range(0,n):
    for character in bigram_list[i]:
        if character in punctuation: continue
        else:
            if character in dictionary.keys():
                dictionary[character].Doc_num = dictionary[character].Doc_num + 1
                dictionary[character].Coll_freq = dictionary[character].Coll_freq + bigram_list[i][character]
                posting = Posting(i,bigram_list[i][character])
                ptr = dictionary[character].posting_list
                # 查找最后一个文档
                while ptr.next!=None and ptr.next.term_freq >= posting.term_freq:
                    ptr = ptr.next
                if ptr.next == None:
                    ptr.next = posting
                else:
                    posting.next = ptr.next
                    ptr.next = posting
            else:
                dictionary[character] = Dictionary(character,1,bigram_list[i][character])
                posting = Posting(i,bigram_list[i][character])
                dictionary[character].posting_list = posting
# 生成权值
for i in dictionary.keys():
    ptr = dictionary[i].posting_list
    while ptr!= None:
        ptr.weight = dictionary[i].idf * ptr.term_freq
        ptr = ptr.next

#与运算
def AND(p1,p2):
    ans = Posting(0, 0)
    p3 = p1
    p4 = p2
    while (p3.next != None):
        if (p3.docID > p3.next.docID):
            n_docid = p3.docID
            n_tef = p3.term_freq
            p3.docID = p3.next.docID
            p3.term_freq = p3.next.term_freq
            p3.next.docID = n_docid
            p3.next.term_freq = n_tef
            p3 = p3.next
        else:
            p3 = p3.next
    while (p4.next != None):
        if (p4.docID > p4.next.docID):
            n_docid = p4.docID
            n_tef = p4.term_freq
            p4.docID = p4.next.docID
            p4.term_freq = p4.next.term_freq
            p4.next.docID = n_docid
            p4.next.term_freq = n_tef
            p4 = p4.next
        else:
            p4 = p4.next
    ptr = ans
    while (p1 != None and p2 != None):
        if (p1.docID == p2.docID):
            ptr.next = Posting(p1.docID, 1)
            ptr = ptr.next
            p1 = p1.next
            p2 = p2.next

        else :
            if (p1.docID<p2.docID):
                p1 = p1.next
            else:
                p2 = p2.next
    return ans.next

#与非运算
def NOTAND(p1 ,p2):
    p3 = p1
    p4 = p2
    while (p3.next != None):
        if (p3.docID > p3.next.docID):
            n_docid = p3.docID
            n_tef = p3.term_freq
            p3.docID = p3.next.docID
            p3.term_freq = p3.next.term_freq
            p3.next.docID = n_docid
            p3.next.term_freq = n_tef
            p3 = p3.next
        else:
            p3 = p3.next
    while (p4.next != None):
        if (p4.docID > p4.next.docID):
            n_docid = p4.docID
            n_tef = p4.term_freq
            p4.docID = p4.next.docID
            p4.term_freq = p4.next.term_freq
            p4.next.docID = n_docid
            p4.next.term_freq = n_tef
            p4 = p4.next
        else:
            p4 = p4.next
    list1 = Posting(0, 0)
    ptr = list1
    while (p1 != None):
        if p2 is None:
            ptr.next = Posting(p1.docID, 1)
            ptr = ptr.next
            p1 = p1.next
        elif (p1.docID == p2.docID):
            p1 = p1.next
            p2 = p2.next

        else:
            if (p1.docID < p2.docID):
                ptr.next = Posting(p1.docID, 1)
                ptr = ptr.next
                p1 = p1.next
            else:
                p2 = p2.next
    # 生成相应临时Dictionary项
    temp1 = list1.next
    count = 0
    while temp1 != None:
        temp1 = temp1.next
        count = count + 1
    ans = Dictionary('0','count',0)
    ans.posting_list = list1.next
    return ans

#或运算
def OR(p1,p2):
    p3 = p1
    p4 = p2
    while (p3.next != None):
        if (p3.docID > p3.next.docID):
            n_docid = p3.docID
            n_tef=p3.term_freq
            p3.docID = p3.next.docID
            p3.term_freq=p3.next.term_freq
            p3.next.docID = n_docid
            p3.next.term_freq=n_tef
            p3=p3.next
        else:
            p3=p3.next
    while (p4.next != None):
        if (p4.docID > p4.next.docID):
            n_docid = p4.docID
            n_tef = p4.term_freq
            p4.docID = p4.next.docID
            p4.term_freq = p4.next.term_freq
            p4.next.docID = n_docid
            p4.next.term_freq = n_tef
            p4=p4.next
        else:
            p4=p4.next
    ans = Posting(0,0)
    ptr = ans
    while (p1 != None or p2 != None):
        if p1 == None and p2 != None:
            ptr.next = Posting(p2.docID,1)
            # ptr.next.weight = p2.weight
            ptr = ptr.next
            p2 = p2.next
        elif p2 == None and p1 != None:
            ptr.next = Posting(p1.docID,1)
            # ptr.next.weight = p1.weight
            ptr = ptr.next
            p1 = p1.next
        elif (p1.docID == p2.docID):
            ptr.next = Posting(p1.docID,1)
            # ptr.next.weight = p1.weight + p2.weight
            ptr = ptr.next
            p1 = p1.next
            p2 = p2.next
        else:
            if (p1.docID < p2.docID):
                ptr.next = Posting(p1.docID,1)
                # ptr.next.weight = p1.weight
                ptr = ptr.next
                p1 = p1.next
            else:
                ptr.next = Posting(p2.docID,1)
                ptr.next.weight = p2.weight
                ptr = ptr.next
                p2 = p2.next
    return ans.next

#AND(p1,p2,....pt)
def AND_LIST(p_list):
    p_list = sorted(p_list,key=functools.cmp_to_key(lambda x,y: x.Doc_num-y.Doc_num))
    list1 = p_list[0].posting_list
    a = len(p_list)
    for i in range(1,a):
        list1 = AND(list1,p_list[i].posting_list)
    temp1 = list1
    count = 0
    while temp1 != None:
        temp1 = temp1.next
        count = count + 1
    ans = Dictionary('0',count,0)
    ans.posting_list = list1
    return ans

#OR(p1,p2,....pt)
def OR_LIST(p_list):
    list1 = p_list[0].posting_list
    a = len(p_list)
    for i in range(1,a):
        list1 = OR(list1,p_list[i].posting_list)
    temp1 = list1
    count = 0
    while temp1 != None:
        temp1 = temp1.next
        count = count + 1
    ans = Dictionary('0',count,0)
    ans.posting_list = list1
    return ans

#显示
def pri(b):
    Doc_num = b.Doc_num
    b = b.posting_list
    li = []
    while b!= None:
        li.append(b)
        b = b.next
    li = sorted(li,key=functools.cmp_to_key(lambda x,y: y.weight-x.weight))
    for i in li:
        print(files_path[i.docID],i.weight)
        # print(b.docID)
        # b = b.next



def addLIST ():
    x = ""
    LISTO=[]
    while (x != "0"):
        x = input("请输入列表元素（输入0时停止）:" + "\n")
        if x not in dictionary.keys():
            print("没有响应字段")
            continue
        else:
            LISTO.append(dictionary[x])
    return LISTO

def addx(x):
    if x not in dictionary.keys():
        print("没有响应字段"+x+"\n")
        addx(input("请重新输入:"))
    else:
        global se
        se=x
        ans=dictionary[x].posting_list
    return ans
switch = {
    # "ADD_LIST":lambda ans, listO:addLIST(),
    "AND_LIST":lambda listO:AND_LIST(listO),
    "OR_LIST":lambda listO:OR_LIST(listO),
    "AND": lambda ans, listO: AND(ans,listO),#addx(input("请输入需要进行与操作的字词："))
    "OR": lambda ans, listO: OR(ans,listO),#addx(input("请输入需要进行或操作的字词："))
    "NOTAND": lambda ans, listO: NOTAND(ans,listO),#addx(input("请输入需要进行与非操作的字词："))
    # "AND_L": lambda ans, listO: AND(ans,listO),
    # "OR_L": lambda ans, listO: OR(ans,listO),
    # "NOTAND_L": lambda ans, listO: NOTAND(ans,listO),
    }
'''
s=""
ans = addx(input("请输入初始字段的字词："))
listo = []
seq=se
while (True):
    seq = seq + " " + s + " " + se
    #print("当前已写查询语句"+seq)
    s = input("请选择需要进行的操作："+"\n"+"ADD_LIST"+"\n"+"AND_LIST"+"\n"+"OR_LIST"+ "\n" + "AND" + "\n"
              + "OR" + "\n" + "NOTAND" + "\n"+ "AND_L" + "\n" + "OR_L" + "\n" + "NOTAND_L" + "\n" + "quit" + "\n")
    if s=="quit":
        break
    elif s== "AND" or s=="OR" or s=="NOTAND":
        ans = switch[s](ans, listo)
    elif s=="AND_LIST" or s=="OR_LIST" or s=="ADD_LIST":
        listo = switch[s](ans, listo)
    elif s=="AND_L" or s=="OR_L" or s=="NOTAND_L" :
        ans = switch[s](ans, listo)
        se="list"
        listo=[]

'''

# cxyj=input("请输入查询语句：")
# listI=cxyj.split(" ")
# list_terms = []
# before = None
# for i in listI:

#     if i in switch.keys():
#         if before == None:
#             before = i
#         elif before == 'NOTAND':
#             ans = switch[before](list_terms[0].posting_list,list_terms[1].posting_list)
#             list_terms.clear()
#             list_terms.append(ans)
#             before = i
#         elif before != i:
#             ans = switch[before+'_LIST'](list_terms)
#             list_terms.clear()
#             list_terms.append(ans)
#             before = i
        
#     elif i in dictionary.keys():
#         list_terms.append(dictionary[i])
#     else: 
#         a = jieba.lcut(i)
#         a = Dictionary(i,0,0)
#         a.posting_list = None
#         list_terms.append(a)
        
# if before is None:
#     ans = list_terms[0]
# elif before == 'NOTAND':
#     ans = switch[before](list_terms[0].posting_list,list_terms[1].posting_list)
# else:
#     ans = switch[before+'_LIST'](list_terms)
# if ans.posting_list == None:
#     print('None')
# else:
#     pri(ans)
        
class Applicantion(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        
        self.label01 = Label(self, text='查询语句输入')
        self.label01.grid(row=0, column=0)
        
        self.lanel02=Label(self,text='标题输入')
        self.lanel02.grid(row=1,column=0)

        v1 = StringVar()  # 查询语句输入
        self.entry01 = Entry(self, textvariable=v1)
        self.entry01.grid(row=0, column=1,columnspan=2)

        v2 = StringVar()  # 查询语句输入
        self.entry02 = Entry(self, textvariable=v2)
        self.entry02.grid(row=1, column=1, columnspan=2)

        # 查询按钮
        Button(self, text='查询', command=self.chaxun)\
            .grid(row=2, column=1, padx=10, sticky=NSEW)

    def chaxun(self):  # 登录事件
        cxyj = self.entry01.get()
        cxbt=self.entry02.get()

if __name__ == '__main__':
    root = Tk()
    root.geometry('500x600+200+300')
    root.title('唐诗三百首查询')
    app = Applicantion(master=root)
    root.mainloop()




'''
#查询语句
#1
print("\n"+'first:')
listA=[dictionary['北'],dictionary['千'],dictionary['一']]
listO=[dictionary['雪'],dictionary['云'],dictionary['风']]
pri(AND(OR_LIST(listO),AND_LIST(listA)))

#2
print("\n"+'second:')
listA=[dictionary['八月'],dictionary['珠帘'],dictionary['将军']]
listO=[dictionary['雪'],dictionary['云'],dictionary['风']]
pri(NOTAND(AND_LIST(listA),OR_LIST(listO)))

#3
print("\n"+'third:')
listA=[dictionary['八月'],dictionary['珠帘'],dictionary['将军']]
listO=[dictionary['江水'],dictionary['白云'],dictionary['晚']]
pri(OR(AND_LIST(listA),OR_LIST(listO)))

#4
print("\n"+'forth:')
listA=[dictionary['情'],dictionary['苦'],dictionary['军']]
listO=[dictionary['冬'],dictionary['乡'],dictionary['不敢']]
pri(NOTAND(AND_LIST(listA),OR_LIST(listO)))

#5
print("\n"+'fifth:')
listA=[dictionary['先皇'],dictionary['故国'],dictionary['断']]
listO=[dictionary['冬'],dictionary['乡'],dictionary['不敢']]
pri(NOTAND(AND_LIST(listA),OR_LIST(listO)))
'''