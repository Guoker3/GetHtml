##TODO complete functions about soup
##TODO find  element about a pointed element

import re

class ElementWeaver:
    def __init__(self,soup):
        self.soup=soup
        self.depth=-1.0
        self.width=-1.0
    #-------------------------functions below are design to get position relationship--------------------------------
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
        if element==None:
            return None
        if(self.depth<0):
            self.depth=self.getTreeDepth(self.soup)
        return (1-len(list(element.parents))/self.depth)

    def getWidthDistance(self,element):                  #relative line position
        if element==None:
            return None
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

    #Nearby means that similar elements near like sheet or list
    def getNearbyAmount(self,element):      #count the each number of child,sibling and parent+parent's sibling

        cn=len(element.contents)
        cnTag=0
        for c in element.contents:
            if (str(type(c)) == "<class 'bs4.element.Tag'>"):
                cnTag=cnTag+1

        sn=len(element.parent.contents)
        snTag = 0
        for s in element.parent.contents:
            if (str(type(s)) == "<class 'bs4.element.Tag'>"):
                snTag = snTag + 1

        if(element.parent.parent == None):
            pn=0
            pnTag=0
        else:
            pn = element.parent.parent.contents
            pnTag = 0
            for p in element.parent.parent.contents:
                if (str(type(p)) == "<class 'bs4.element.Tag'>"):
                    pnTag = pnTag + 1

        return [cn,cnTag,sn,snTag,pn,pnTag]

    #showed in the feature set by a coefficient describing the preference that has similar element nearby
    def getNearbySameTagAmount(self,element):   #search the same tag element ,record itself and its related position
        levelPoint=-1
        ancestor=[[element,0],]     #[ancestor,ancestors next position towards element]
        temp=element
        found=list()
        while (temp.parent!=None):
            count=0
            for c in temp.parent.children:
                if temp is c:
                    break
                if(str(type(c)) == "<class 'bs4.element.Tag'>"):
                    count = count + 1
            ancestor.append([temp.parent,count])
            temp=temp.parent

        for l in ancestor:
            inTree= l[0]
            #vertical = -levelPoint      # set siblings' depth equal to zero,and top level can be minus
            horizon=-l[1]                # distance between the two same tags' ancestor which is the child of the same ancestor
                                        ## found element at the right cane be minus

            # to get the horizon,go through the head's children specially
            for child in inTree:
                if (str(type(child)) == "<class 'bs4.element.Tag'>"):
                    vertical=-levelPoint
                    S=list()
                    if element.name == child.name and child is not element:
                        found.append({"element": child, "vertical": vertical, "horizon": horizon, "levelPoint": levelPoint})
                    for grandChild in child.children:
                        if (str(type(grandChild)) == "<class 'bs4.element.Tag'>"):
                            S.append(grandChild)

                    #mid-order leterate the grandchild by stack
                    while(S !=list()):
                        SS=list()
                        vertical=vertical+1
                        for tree in S:
                            if element.name == tree.name and tree is not element:
                                if horizon !=0: #avoid to appending the repeat item
                                    found.append({"element": tree, "vertical": vertical, "horizon": horizon, "levelPoint": levelPoint})
                            for c in tree.children:
                                if(str(type(c)) == "<class 'bs4.element.Tag'>"):
                                    SS.append(c)
                        S=SS
                    horizon=horizon+1
            levelPoint=levelPoint+1

        return found

    #-------------------------functions below are defined to locate elements and its' class----------------------------
    def classFinder(self,element):
        #inline inhead inhref
        pass
    def elementRecognizer(self):
        pass
    def getSize(self):
    # content padding border margin
        pass


class imgTag(ElementWeaver):
    def __init__(self,soup):
        ElementWeaver.__init__(soup)
        self.img=list()

    def imgFilter(self):
        #use img tag to find imagines,but ignore other forms of imagines which can be write later if neede
        self.img=self.soup.find_all("img")

    def featureExtracter(self):
        pass

if __name__=="__main__":
    import HtmlSpyder as hs
    count = 1
    ul = hs.openUrl("GuanWang")[0:5]
    for url in ul:
        print("\ncount:" + str(count))
        count = count + 1
        if (url == ""):
            continue
        html = hs.getHtml(url)
        if (html is None):
            continue
        soup = hs.cookSoup(html)
        print("url:" + url)
        #------------------------------------- test ElementWeaver-------------------------------------------------------
        ew = ElementWeaver(soup)
        print("tree depth: " + str(ew.getTreeDepth(ew.soup)))
        print("tree line amount: " + str(ew.getTreeWidth(ew.soup)))
        img=soup.find_all("img")
        if img != list():

            print("img 0 depth: "+str(ew.getDepthDistance(img[0])))
            print("img 0 width: "+str(ew.getWidthDistance(img[0])))

            l=ew.getNearbySameTagAmount(img[-1])
            print("same tag:"+str(img[-1]))
            for i in l:
                print("\n"+str(i))
        else:
            print("img not found")
            

        # print(html.text)
        # print(ew.imgFilter(soup))