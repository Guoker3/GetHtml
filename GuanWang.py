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
        if imgs!=list():
            for img in imgs:
                features=dict()
                features["websiteUrl"]=url
                features["depth"]=imgTag.getDepthDistance(img)/totalDepth
                features["width"]=imgTag.getWidthDistance(img)/totalWidth
                imgFeature=imgTag.featureExtractor(img)
                if imgFeature==None:
                    continue
                features.update(imgFeature)
                found = imgTag.getNearbySameTagAmount(img)
                nearbyFeature=imgTag.analyseNearbySameTag(img, found)
                if nearbyFeature==None:
                    continue
                features.update(nearbyFeature)
                nearbyAmountFeature=imgTag.getNearbyAmount(img)
                if nearbyAmountFeature==None:
                    continue
                features.update(nearbyAmountFeature)
                print(features)
                #wash and save to file
if __name__=="__main__":
    CookGuanWang()