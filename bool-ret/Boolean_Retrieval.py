#!/usr/bin/env python
# coding: utf-8

# In[107]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re


# In[108]:


def empty(data):
    data=data.replace("\n"," ")
    data=data.replace("\r"," ")
    data=data.replace("\t"," ")
    data=data.replace("."," ")
    data=data.replace(","," ")
    data=data.replace("!"," ")
    data=data.replace("?"," ")
    data=data.replace("-"," ")
    data=data.replace("("," ")
    data=data.replace(")"," ")
    data=data.replace("["," ")
    data=data.replace("]"," ")
    data=data.replace("{"," ")
    data=data.replace("}"," ")
    data=data.replace("/"," ")
    data=data.replace("\\"," ")
    data=data.replace("*"," ")
    data=data.replace("+"," ")
    data=data.replace("="," ")
    data=data.replace("<"," ")
    data=data.replace(">"," ")
    data=data.replace("|"," ")
    data=data.replace(";"," ")
    data=data.replace(":"," ")
    data=data.replace("\""," ")
    data=data.replace("%"," ")
    data=data.replace("&"," ")
    data=data.replace("$"," ")
    data=data.replace("#"," ")
    data=data.replace("@"," ")
    data=data.replace("^"," ")
    data=data.replace("`"," ")
    data=data.replace("~"," ")
    data=data.replace("_"," ")
    data=data.replace("-"," ")
    data=data.replace("="," ")
    data=re.sub('[0-9]+'," ",data)
    data=re.sub(" +"," ",data)
    return data


# In[109]:


def remove_stopwords(data):
    stopwords=["a","about","above","after","again","against","all","am","an","and","any","are","as","at","be","because","been","before","being","below","between","both","but","by","can","did","do","does","doing","down","during","each","few","for","from","further","had","has","have","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","it","its","itself","let","me","more","most","my","myself","nor","of","on","once","only","or","other","our","ours","ourselves","out","over","own","same","she","should","so","some","such","than","that","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","very","was","we","were","what","when","where","which","while","who","whom","why","with","would","you","your","yours","yourself","yourselves"]
    data=data.lower()
    data=data.split()
    data=[i for i in data if i not in stopwords]
    data=" ".join(data)
    return data


# In[110]:


class PorterStemmer:
    def isCons(self, letter):
        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':
            return False
        else:
            return True

    def isConsonant(self, word, i):
        letter = word[i]
        z=0
        if(i==0-len(word)):
            z=i
        else:
            z=i-1
        if self.isCons(letter):
            if letter == 'y' and self.isCons(word[z]):
                return False
            else:
                return True
        else:
            return False

    def isVowel(self, word, i):
        return not(self.isConsonant(word, i))

    # *S
    def endsWith(self, stem, letter):
        if stem.endswith(letter):
            return True
        else:
            return False

    # *v*
    def containsVowel(self, stem):
        for i in stem:
            if not self.isCons(i):
                return True
        return False

    # *d
    def doubleCons(self, stem):
        if len(stem) >= 2:
            if self.isConsonant(stem, -1) and self.isConsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False

    def getForm(self, word):
        form = []
        formStr = ''
        for i in range(len(word)):
            if self.isConsonant(word, i):
                if i != 0:
                    prev = form[-1]
                    if prev != 'C':
                        form.append('C')
                else:
                    form.append('C')
            else:
                if i != 0:
                    prev = form[-1]
                    if prev != 'V':
                        form.append('V')
                else:
                    form.append('V')
        for j in form:
            formStr += j
        return formStr

    def getM(self, word):
        form = self.getForm(word)
        m = form.count('VC')
        return m

    # *o
    def cvc(self, word):
        if len(word) >= 3:
            f = -3
            s = -2
            t = -1
            third = word[t]
            if self.isConsonant(word, f) and self.isVowel(word, s) and self.isConsonant(word, t):
                if third != 'w' and third != 'x' and third != 'y':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def replace(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        replaced = base + rep
        return replaced

    def replaceM0(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 0:
            replaced = base + rep
            return replaced
        else:
            return orig

    def replaceM1(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 1:
            replaced = base + rep
            return replaced
        else:
            return orig

    def step1a(self, word):
        if word.endswith('sses'):
            word = self.replace(word, 'sses', 'ss')
        elif word.endswith('ies'):
            word = self.replace(word, 'ies', 'i')
        elif word.endswith('ss'):
            word = self.replace(word, 'ss', 'ss')
        elif word.endswith('s'):
            word = self.replace(word, 's', '')
        else:
            pass
        return word

    def step1b(self, word):
        flag = False
        if word.endswith('eed'):
            result = word.rfind('eed')
            base = word[:result]
            if self.getM(base) > 0:
                word = base
                word += 'ee'
        elif word.endswith('ed'):
            result = word.rfind('ed')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                flag = True
        elif word.endswith('ing'):
            result = word.rfind('ing')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                flag = True
        if flag:
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                word += 'e'
            elif self.doubleCons(word) and not self.endsWith(word, 'l') and not self.endsWith(word, 's') and not self.endsWith(word, 'z'):
                word = word[:-1]
            elif self.getM(word) == 1 and self.cvc(word):
                word += 'e'
            else:
                pass
        else:
            pass
        return word

    def step1c(self, word):
        if word.endswith('y'):
            result = word.rfind('y')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                word += 'i'
        return word

    def step2(self, word):
        if word.endswith('ational'):
            word = self.replaceM0(word, 'ational', 'ate')
        elif word.endswith('tional'):
            word = self.replaceM0(word, 'tional', 'tion')
        elif word.endswith('enci'):
            word = self.replaceM0(word, 'enci', 'ence')
        elif word.endswith('anci'):
            word = self.replaceM0(word, 'anci', 'ance')
        elif word.endswith('izer'):
            word = self.replaceM0(word, 'izer', 'ize')
        elif word.endswith('abli'):
            word = self.replaceM0(word, 'abli', 'able')
        elif word.endswith('alli'):
            word = self.replaceM0(word, 'alli', 'al')
        elif word.endswith('entli'):
            word = self.replaceM0(word, 'entli', 'ent')
        elif word.endswith('eli'):
            word = self.replaceM0(word, 'eli', 'e')
        elif word.endswith('ousli'):
            word = self.replaceM0(word, 'ousli', 'ous')
        elif word.endswith('ization'):
            word = self.replaceM0(word, 'ization', 'ize')
        elif word.endswith('ation'):
            word = self.replaceM0(word, 'ation', 'ate')
        elif word.endswith('ator'):
            word = self.replaceM0(word, 'ator', 'ate')
        elif word.endswith('alism'):
            word = self.replaceM0(word, 'alism', 'al')
        elif word.endswith('iveness'):
            word = self.replaceM0(word, 'iveness', 'ive')
        elif word.endswith('fulness'):
            word = self.replaceM0(word, 'fulness', 'ful')
        elif word.endswith('ousness'):
            word = self.replaceM0(word, 'ousness', 'ous')
        elif word.endswith('aliti'):
            word = self.replaceM0(word, 'aliti', 'al')
        elif word.endswith('iviti'):
            word = self.replaceM0(word, 'iviti', 'ive')
        elif word.endswith('biliti'):
            word = self.replaceM0(word, 'biliti', 'ble')
        return word

    def step3(self, word):
        if word.endswith('icate'):
            word = self.replaceM0(word, 'icate', 'ic')
        elif word.endswith('ative'):
            word = self.replaceM0(word, 'ative', '')
        elif word.endswith('alize'):
            word = self.replaceM0(word, 'alize', 'al')
        elif word.endswith('iciti'):
            word = self.replaceM0(word, 'iciti', 'ic')
        elif word.endswith('ful'):
            word = self.replaceM0(word, 'ful', '')
        elif word.endswith('ness'):
            word = self.replaceM0(word, 'ness', '')
        return word

    def step4(self, word):
        if word.endswith('al'):
            word = self.replaceM1(word, 'al', '')
        elif word.endswith('ance'):
            word = self.replaceM1(word, 'ance', '')
        elif word.endswith('ence'):
            word = self.replaceM1(word, 'ence', '')
        elif word.endswith('er'):
            word = self.replaceM1(word, 'er', '')
        elif word.endswith('ic'):
            word = self.replaceM1(word, 'ic', '')
        elif word.endswith('able'):
            word = self.replaceM1(word, 'able', '')
        elif word.endswith('ible'):
            word = self.replaceM1(word, 'ible', '')
        elif word.endswith('ant'):
            word = self.replaceM1(word, 'ant', '')
        elif word.endswith('ement'):
            word = self.replaceM1(word, 'ement', '')
        elif word.endswith('ment'):
            word = self.replaceM1(word, 'ment', '')
        elif word.endswith('ent'):
            word = self.replaceM1(word, 'ent', '')
        elif word.endswith('ou'):
            word = self.replaceM1(word, 'ou', '')
        elif word.endswith('ism'):
            word = self.replaceM1(word, 'ism', '')
        elif word.endswith('ate'):
            word = self.replaceM1(word, 'ate', '')
        elif word.endswith('iti'):
            word = self.replaceM1(word, 'iti', '')
        elif word.endswith('ous'):
            word = self.replaceM1(word, 'ous', '')
        elif word.endswith('ive'):
            word = self.replaceM1(word, 'ive', '')
        elif word.endswith('ize'):
            word = self.replaceM1(word, 'ize', '')
        elif word.endswith('ion'):
            result = word.rfind('ion')
            base = word[:result]
            if self.getM(base) > 1 and (self.endsWith(base, 's') or self.endsWith(base, 't')):
                word = base
            word = self.replaceM1(word, '', '')
        return word

    def step5a(self, word):
        if word.endswith('e'):
            base = word[:-1]
            if self.getM(base) > 1:
                word = base
            elif self.getM(base) == 1 and not self.cvc(base):
                word = base
        return word

    def step5b(self, word):
        if self.getM(word) > 1 and self.doubleCons(word) and self.endsWith(word, 'l'):
            word = word[:-1]
        return word

    def stem(self, word):
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word


# In[111]:


doc_num={}
i=1
for filename in os.listdir(r"./Dataset"):
    doc_num[filename]=i
    i+=1


# In[112]:


def rotate(word,n):
    return word[n:]+word[:n]


# In[113]:


def preprocessing():
    inverted_index={}
    permuterm_index={}
    for filename in os.listdir(r"./Dataset"):
        s=r"./Dataset"+"/"+filename
        with open(s,"r") as f:
            data=f.read()
            data=data.lower()
            data=empty(data)
            data=remove_stopwords(data)
            p=PorterStemmer()
            words=data.split(" ")
            #print(words)
            stemmed_data=""
            for wordz in words:
                #print(wordz)
                if len(wordz) > 2:
                    stemmed_data+=p.stem(wordz)+" "
                else:
                    stemmed_data+=wordz+" "
            stemmed_data=stemmed_data.replace("'","")
            stemmed_words=[]
            stemmed=stemmed_data.split(" ")
            for word in stemmed:
                word=word+"$"
                stemmed_words.append(word)
            for word in stemmed_words:
                if word not in inverted_index:
                    inverted_index[word]=[]
                    for i in range(len(word),0,-1):
                        permuterm_index[rotate(word,i)]=word
                if word in inverted_index:
                    if doc_num[filename] not in inverted_index[word]:
                        inverted_index[word].append(doc_num[filename])
    return inverted_index,permuterm_index        

inverted_index,permuterm_index=preprocessing()


# In[114]:


def wildcard_search(query):
    parts=query.split('*')
    if len(parts)==3:
        case=4
    elif parts[1]=='':
        case=1
    elif parts[0]=='':
        case=2
    elif parts[0]!='' and parts[1]!='':
        case=3

    if case==4 and parts[0]=='':
        case=1
    
    def match(term,prefix):
        term_list=[]
        for i in term.keys():
            if i.startswith(prefix):
                term_list.append(term[i])
        return term_list

    def bitwise_and(a,b):
        return set(a).intersection(b)

    def process(query):
        term_list=match(permuterm_index,query)
        doc_ID_list=[]
        for term in term_list:
            doc_ID_list.append(inverted_index[term])
        
        temp=[]
        for j in doc_ID_list:
            for k in j:
                if k not in temp:
                    temp.append(k)

        temp=[int(x) for x in temp]
        
        return temp

    if case == 1:
        query = parts[0]
    elif case == 2:
        query = parts[1] + "$"
    elif case == 3:
        query = parts[1] + "$" + parts[0]
    elif case == 4:
        queryA = parts[2] + "$" + parts[0]
        queryB = parts[1]

    if case!=4:
        doc_list=process(query)
        return doc_list
    else:
        doc_listA=process(queryA)
        doc_listB=process(queryB)
        doc_list=bitwise_and(doc_listA,doc_listB)
        return doc_list


# In[115]:


def query_processing(query):
    query=query.lower()
    query=empty(query)
    query=remove_stopwords(query)
    p=PorterStemmer()
    stemmed_query=""
    if len(query) > 2:
        stemmed_query+=p.stem(query)
    else:
        stemmed_query+=query
    return inverted_index[stemmed_query+"$"]


# In[117]:


Univ= []
for i in range(1,len(doc_num)):
    Univ.append(i)


# In[118]:


query=(input('Enter the query: '))
flag=1
if(query==""):
    print("Enter a valid query")
    flag=0
stack=[]
if flag==1:
    split_query=query.split(" ")
    if len(split_query)==1 and split_query[0] not in ["AND","OR","NOT","(",")"]:
        if "*" in split_query[0]:
            print(wildcard_search(split_query[0]))
        else:
            print(query_processing(split_query[0]))
    else:
        for i in split_query:
            if i=="(":
                stack.append(i)

            elif i==")":
                temp=[]
                while stack[-1]!="(":
                    temp.append(stack.pop())
                temp.reverse()
                if temp[0]=="NOT":
                    stack.pop()
                    if type(temp[1])==type(" "):
                        if "*" in temp[1]:
                            stack.append(list(set(Univ)-set(wildcard_search(temp[1]))))
                        else:
                            stack.append(list(set(Univ)-set(query_processing(temp[1]))))
                    else:
                        stack.append(list(set(Univ)-set(temp[1])))
                elif temp[1]=="AND":
                    stack.pop()
                    if type(temp[0])==type(" "):
                        if "*" in temp[0]:
                            A=wildcard_search(temp[0])
                        else:
                            A=query_processing(temp[0])
                    else:
                        A=temp[0]
                    if type(temp[2])==type(" "):
                        if "*" in temp[2]:
                            B=(wildcard_search(temp[2]))
                        else:
                            B=(query_processing(temp[2]))
                    else:
                        B=temp[2]
                    stack.append(set(A).intersection(set(B)))
                elif temp[1]=="OR":
                    stack.pop()
                    if type(temp[0])==type(" "):
                        if "*" in temp[0]:
                            A=(wildcard_search(temp[0]))
                        else:
                            A=(query_processing(temp[0]))
                    else:
                        A=temp[0]
                    if type(temp[2])==type(" "):
                        if "*" in temp[2]:
                            B=(wildcard_search(temp[2]))
                        else:
                            B=(query_processing(temp[2]))
                    else:
                        B=temp[2]
                    stack.append(set(A).union(set(B)))
                else:
                    print("Enter a valid query")
                    flag=0
            else:
                stack.append(i)
if flag==1:
    print(stack[0])

