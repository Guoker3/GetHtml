##TODO complete functions about soup
##TODO find  element about a pointed element

import re

class ElementWeaver:
    def __init__(self,soup):
        self.soup=soup
        self.depth=-1.0
        self.width=-1.0
#-------------------------nctions below are design to get position relationship--------------------------------
    def getTreeDepth(self,head):
        deep=0
        S1=[head,]
        while(len(S1)!=0):
            S2=list()
            for p in S1:
                #print(str(type(p)))
                if(str(type(p))=="<class 'bs4.BeautifulSoup'>" or str(type(p))=="<class 'bs4.element.Tag'>"):
                    children=p.contents
                    for child in children:
                        S2.append(child)
            deep=deep+1
            S1=S2
        return deep

    def getTreeWidth(self,soup):
        width=len(re.split("[<>\n]",str(self.soup)))
        return width

    def getDepthDistance(self,element):          #relative embeded depth
        if(self.depth<0):
            self.depth=self.getTreeDepth(self.soup)
        return (1-len(list(element.parents))/self.depth)

    def getWidthDistance(self,element):                  #relative line position
        if(self.width<0):
            self.width=self.getTreeWidth(self.soup)
        e_tmp=re.split("[<>\n]",str(element))
        e=list()
        for ee in e_tmp:
            if ee!='':
                e.append(ee)
        s_tmp=re.split("[<>\n]",str(self.soup))
        s=list()
        for ss in s_tmp:
            if ss!='':
                s.append(ss)

        for i in range(len(s)):
            if (s[i]==e[0]):
                for ii in range(len(e)):
                    if s[i+ii]!=e[ii]:
                        break
                    if (ii+1)==len(e):
                        return i/self.width

    def getSiblingAmount(self):
        pass
    def getSiblingSameTagAmount(self,tag):
        pass




#-------------------------functions below are defign to locate elements and its' class----------------------------
    def classFinder(selfself):
        pass

class imgTag(ElementWeaver):
    def __init__(self,soup):
        ElementWeaver.__init__(soup)
        self.img=list()

    def imgFilter(self):
        #use img tag to find imagines,but ignore other forms of imagines which can be write later if neede       self.img = self.soup.find_all('img')
        self.img=self.soup.find_all("img")

    def featureExtracter(self):
        pass