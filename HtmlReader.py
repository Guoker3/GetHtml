##TODO complete functions about soup
##TODO find  element about a pointed element

import re
import requests
from io import BytesIO  #eable pilow to read file in the memory
from PIL import Image
import numpy as np

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
            pn = len(element.parent.parent.contents)
            pnTag = 0
            for p in element.parent.parent.contents:
                if (str(type(p)) == "<class 'bs4.element.Tag'>"):
                    pnTag = pnTag + 1

        return {"childNumber":cn,"childTagNumber":cnTag,"siblingNumber":sn,"siblingTagNumber":snTag,"uncleNumber":pn,"uncleTagNumber":pnTag}

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
        totalLevelNumber=len(ancestor)

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


class ImgTag(ElementWeaver):
    def __init__(self,soup,url):
        ElementWeaver.__init__(self,soup)
        self.imgs = self.soup.find_all("img")
        self.features=list()
        self.url=url

    def readImg(self,imgElement):
        try:
            src=imgElement["src"]
        except Exception:
            return None,None
        #combine out the url of the img
        if src[0:7]=="http://":
            url=src
        elif src[0:8]=="https://":
            url=src
        elif src[0:2]=="//":
            url="http:"+src
        elif src[0:1]=="/":
            if self.url[-1]=="/":
                url=self.url+src[1:]
            else:
                url=self.url+src
        elif src=="":
            return None,None
        else:
            return None,None
            #raise Exception ("src:  " +str(src)+ "   imagine src UNKOWN")
        #extract information
        try:
            ret=requests.get(url)
        except Exception:
            return None,None
        img=ret.content
        return url,img

    def featureExtractor(self,imgElement):
        featureGet=dict()
        src,img=self.readImg(imgElement)
        if src==None:
            return None
        featureGet['src']=src
        try:
            imgPIL = Image.open(BytesIO(img))
        except Exception:
            return None
        featureGet["type"] = imgPIL.mode
        featureGet["shape"] = list(imgPIL.size)
        featureGet["widthHeightRatio"]=featureGet["shape"][0]/featureGet["shape"][1]
        #deal with the color
        imgRGB = imgPIL.convert("RGB")
        rgbMat = np.array(imgRGB)
        r=0
        g=0
        b=0
        for h in rgbMat:
            for w in h:
                r=r+w[0]
                g=g+w[1]
                b=b+w[2]
        size=imgPIL.size[0]*imgPIL.size[1]
        featureGet["color"]=[r/size/255,g/size/255,b/size/255]

        # imagine's color-kind it has
        LIMIT1 = 100
        COLORSTEP=16
        colorSet=set()
        hStep = imgPIL.size[1] / LIMIT1
        wStep = imgPIL.size[0] / LIMIT1
        for h in range(LIMIT1):
            for w in range(LIMIT1):
                colorSet.add(str([int(i/COLORSTEP) for i in rgbMat[int(h*hStep)][int(w*wStep)]]))
        colorNum=len(colorSet)
        featureGet['colorKinds']=colorNum/(int(255/COLORSTEP)**3)

        #   imagine contrasts
        # limit the size of the imagine
        LIMIT2 = 100
        if imgPIL.size[0] > LIMIT2 and imgPIL.size[1] > LIMIT2:
            imgPILGray = imgPIL.resize((LIMIT2, LIMIT2))
        elif imgPIL.size[0] > LIMIT2:
            imgPILGray = imgPIL.resize((LIMIT2, imgPIL.size[1]))
        else:
            imgPILGray = imgPIL.resize((imgPIL.size[0], LIMIT2))\

        imgGray = imgPIL.convert('L')
        grayMat = np.array(imgGray)
        shape = grayMat.shape
        d=0
        for h in range(shape[0]-1):
            for w in range(shape[1]-1):
                d=d+abs(int(grayMat[h][w])-int(grayMat[h][w+1]))
                d=d+abs(int(grayMat[h][w])-int(grayMat[h+1][w]))
        d=d/((shape[0]-1)*(shape[1]-1))/255
        featureGet["contrast"]=d

        return featureGet

    def analyseNearbySameTag(self,imgElement,found):   #analyse the data found from the getNearbySameTagAmount in father class ElementWeaver
        src,img=self.readImg(imgElement)
        if src==None:
            return None
        imgElementShape=Image.open(BytesIO(img)).size

        SIMILIAR=0.1
        levelCount=dict()
        levelSimiliarCount=dict()
        verticalCount={'minus':0,'zero':0,'positive':0}
        verticalSimiliarCount={'minus':0,'zero':0,'positive':0}
        horizonCount=dict()
        
        similiarFoundlevel = -1
        horizonCountInFoundLevel=dict()
        for fd in found:
            fdSrc,fdImg=self.readImg(fd["element"])
            if fdSrc== None:
                continue
            try:
                fdImgShape = Image.open(BytesIO(fdImg)).size
            except Exception:
                continue
            if abs((imgElementShape[0]/fdImgShape[0])-1)<SIMILIAR and  abs((imgElementShape[1]/fdImgShape[1])-1)<SIMILIAR:
                isSimiliar=True
            else:
                isSimiliar=False

            #percentage that tags have in different levelPoint
            try:
                levelCount[fd["levelPoint"]] += 1
            except Exception:
                levelCount[fd["levelPoint"]] = 1
            #percentage that simialr tags have in different levelPoint
            if(isSimiliar):
                try:
                    levelSimiliarCount[fd["levelPoint"]] += 1
                except Exception:
                    levelSimiliarCount[fd["levelPoint"]] = 1
            #percentage that tags' vertical is minus or not
            if(fd["vertical"])<0:
                verticalCount["minus"] += 1
            elif(fd["vertical"])>0:
                verticalCount["positive"] += 1
            else:
                verticalCount["zero"] += 1
            #percentage that similiar tags' vertical is minus or not
            if(isSimiliar):
                if (fd["vertical"]) < 0:
                    verticalSimiliarCount["minus"] += 1
                elif (fd["vertical"]) > 0:
                    verticalSimiliarCount["positive"] += 1
                else:
                    verticalSimiliarCount["zero"] += 1

            #percentage that tags are far or near in horizon in all level
            try:
                horizonCount[abs(fd["horizon"])] += 1
            except Exception:
                horizonCount[abs(fd["horizon"])] = 1
            #percentage that similiar tags are far or near in horizon in levelPoint smallest which has similiar tags ,or will be 0
            if (similiarFoundlevel == -1):
                if isSimiliar:
                    similiarFoundlevel=fd["levelPoint"]
                else:
                    pass
            else:
                if similiarFoundlevel==fd["levelPoint"]:
                    try:
                        horizonCountInFoundLevel[abs(fd["horizon"])] += 1
                    except Exception:
                        horizonCountInFoundLevel[abs(fd["horizon"])] = 1
                else:
                    pass
                
        nbFeature=dict()
        
        #levelCount = dict()
        levelNumber=int(len(levelCount)/2)
        low=0
        high=0
        while(levelNumber>0):
            try:
                low+=levelCount[int(len(levelCount)/2)-levelNumber]
            except Exception:
                pass
            try:
                high+=levelCount[len(levelCount)-(int(len(levelCount)/2))+levelNumber]
            except Exception:
                pass
            levelNumber-=1
        if low+high==0:
            nbFeature["levelDistanceLowRatio"]=0
            nbFeature["levelDistanceHighRatio"]=0
        else:
            nbFeature["levelDistanceLowRatio"]=low/(low+high)
            nbFeature["levelDistanceHighRatio"]=high/(low+high)

        #levelSimiliarCount = dict()
        levelNumber=int(len(levelSimiliarCount)/2)
        low=0
        high=0
        while(levelNumber>0):
            try:
                low+=levelSimiliarCount[int(len(levelSimiliarCount)/2)-levelNumber]
            except Exception:
                pass
            try:
                high+=levelSimiliarCount[len(levelSimiliarCount)-(int(len(levelSimiliarCount)/2))+levelNumber]
            except Exception:
                pass
            levelNumber-=1
        if low+high==0:
            nbFeature["levelSimiliarDistanceLowRatio"]=0
            nbFeature["levelSimiliarDistanceHighRatio"] =0
        else:
            nbFeature["levelSimiliarDistanceLowRatio"]=low/(low+high)
            nbFeature["levelSimiliarDistanceHighRatio"] = high / (low + high)
        #verticalCount = dict
        sum=verticalCount["minus"]+verticalCount["zero"]+verticalCount["positive"]
        if sum==0:
            sum=1
        nbFeature["verticalZeroRatio"]=verticalCount["zero"]/sum
        nbFeature["verticalMinusRatio"]=verticalCount["minus"]/sum
        nbFeature["verticalPositiveRatio"]=verticalCount["positive"]/sum
        #verticalSimiliarCount = dict()
        sum=verticalSimiliarCount["minus"]+verticalSimiliarCount["zero"]+verticalSimiliarCount["positive"]
        if sum==0:
            sum=1
        nbFeature["verticalSimiliarZeroRatio"]=verticalSimiliarCount["zero"]/sum
        nbFeature["verticalSimiliarMinusRatio"]=verticalSimiliarCount["minus"]/sum
        nbFeature["verticalSimiliarPositiveRatio"]=verticalSimiliarCount["positive"]/sum
        #horizonCount = dict()
        horizonNumber = int(len(horizonCount) / 2)
        low = 0
        high = 0
        while (horizonNumber > 0):
            try:
                low += horizonCount[int(len(horizonCount) / 2) - horizonNumber]
            except Exception:
                pass
            try:
                high += horizonCount[len(horizonCount) - (int(len(horizonCount) / 2)) + horizonNumber]
            except Exception:
                pass
            horizonNumber -= 1
        if low+high==0:
            nbFeature["horizonDistanceCloserRatio"] = 0
            nbFeature["horizonDistanceFatherRatio"] = 0
        else:
            nbFeature["horizonDistanceCloserRatio"] = low / (low+high)
            nbFeature["horizonDistanceFatherRatio"] = high / (low + high)
        #horizonCountInFoundLevel = dict()
        horizonNumber = int(len(horizonCountInFoundLevel) / 2)
        low = 0
        high = 0
        while (horizonNumber > 0):
            try:
                low += horizonCountInFoundLevel[int(len(horizonCountInFoundLevel) / 2) - horizonNumber]
            except Exception:
                pass
            try:
                high += horizonCountInFoundLevel[len(horizonCountInFoundLevel) - (int(len(horizonCountInFoundLevel) / 2)) + horizonNumber]
            except Exception:
                pass
            horizonNumber -= 1
        if low+high ==0:
            nbFeature["horizonDistanceInFoundLevelCloserRatio"] = 0
            nbFeature["horizonDistanceInFoundLevelFatherRatio"] = 0
        else:
            nbFeature["horizonDistanceInFoundLevelCloserRatio"] = low / (low+high)
            nbFeature["horizonDistanceInFoundLevelFatherRatio"] = high / (low + high)
        return nbFeature

if __name__=="__main__":
    testFlag="2"

    import HtmlSpyder as hs
    count = 1
    ul = hs.openUrl("GuanWang")[0:15]
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

        if "1" in testFlag:  # test elementWeaver
            ew = ElementWeaver(soup)
            print("tree depth: " + str(ew.getTreeDepth(ew.soup)))
            print("tree line amount: " + str(ew.getTreeWidth(ew.soup)))
            img=soup.find_all("img")
            if img != list():
                print("[cn,cnTag,sn,snTag,pn,pnTag]:  "+str(ew.getNearbyAmount(img[0])))
                print("img 0 depth: "+str(ew.getDepthDistance(img[0])))
                print("img 0 width: "+str(ew.getWidthDistance(img[0])))

                l=ew.getNearbySameTagAmount(img[-1])
                print("same tag:"+str(img[-1]))
                for i in l:
                    print("\n"+str(i))
            else:
                print("img not found")
            
        if("2" in testFlag):    #test imgTag
            tg=ImgTag(soup,url)
            img = soup.find_all("img")
            if img != list():
                print(tg.featureExtractor(img[0]))
                found= tg.getNearbySameTagAmount(img[-1])
                print(tg.analyseNearbySameTag(img[0],found))