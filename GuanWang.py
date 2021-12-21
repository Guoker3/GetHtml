import HtmlSpyder as hs
import HtmlReader as hr
def CookGuanWang():
    dataSet=list()
    ul=hs.openUrl("GuanWang")
    for url in ul:
        if (url == ""):
            continue
        html=hs.getHtml(url)
        if(html is None):
            continue
        soup=hs.cookSoup(html)
        #print("url:"+url)

        #img Tag
        imgs=soup.find_all("img")
        imgTag=hr.ImgTag(soup,url)
        totalDepth=imgTag.getDepthDistance(imgTag.soup)
        totalWidth=imgTag.getTreeWidth(imgTag.soup)
        for img in imgs:
            features=dict()
            features["websiteUrl"]=url
            features["depth"]=imgTag.getDepthDistance(img)/totalDepth
            features["width"]=imgTag.getWidthDistance(img)/totalWidth

        ew=hr.ElementWeaver(soup)
        print("depth:"+ew.getTreeDepth(ew.soup))
        print("width"+ew.getTreeWidth(ew.soup))


        print(ew.getDepthDistance(soup.find_all("img")[0]))
        print(ew.getWidthDistance(soup.find_all("img")[0]))
        #print(html.text)
        #print(ew.imgFilter(soup))

if __name__=="__main__":
    CookGuanWang()