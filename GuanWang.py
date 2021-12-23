import HtmlSpyder as hs
import HtmlReader as hr
import time
import csv
def CookGuanWang():
    controlFlag=list()
    controlFlag.append("print")
    controlFlag.append("save")
    ul=hs.openUrl("GuanWang")
    datasetName="GuanWangRaw2_firstTry.csv"
    f=open("../dataset/"+datasetName,"a+")
    writer=csv.writer(f)
    featureName=["embeddedDepth","lineNumber","imgWidth","imgHeight","red","green","blue","colorVariety","contrast"]
    featureName.extend(["levelDistanceLowRatio", "levelDistanceHighRatio", "levelSimiliarDistanceLowRatio", "levelSimiliarDistanceHighRatio"])
    featureName.extend(['verticalZeroRatio', 'verticalMinusRatio', 'verticalPositiveRatio', 'verticalSimiliarZeroRatio','verticalSimiliarMinusRatio', 'verticalSimiliarPositiveRatio'])
    featureName.extend(['horizonDistanceCloserRatio', 'horizonDistanceFatherRatio','horizonDistanceInFoundLevelCloserRatio', 'horizonDistanceInFoundLevelFatherRatio'])
    featureName.extend(['childNumber', 'childTagNumber', 'siblingNumber', 'siblingTagNumber', 'uncleNumber','uncleTagNumber'])
    writer.writerow(featureName)
    for url in ul:
        if (url == ""):
            continue
        print(time.strftime("Day%d %H:%M:%S", time.localtime()), "\t", url)
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
                if "print" in controlFlag:
                    print(features)
                #wash and save to file
                if "save" in controlFlag:
                    featureWashed=list()
                    featureWashed.extend([features['depth'],features['width'],features['shape'][0],features['shape'][1],features['color'][0],features['color'][1],features['color'][2],features['colorKinds'],features['contrast']])
                    featureWashed.extend([features['levelDistanceLowRatio'], features['levelDistanceHighRatio'], features['levelSimiliarDistanceLowRatio'], features['levelSimiliarDistanceHighRatio'], features['verticalZeroRatio'], features['verticalMinusRatio']])
                    featureWashed.extend([features['verticalPositiveRatio'], features['verticalSimiliarZeroRatio'], features['verticalSimiliarMinusRatio'], features['verticalSimiliarPositiveRatio']])                    
                    featureWashed.extend([features['horizonDistanceCloserRatio'],features['horizonDistanceFatherRatio'],features['horizonDistanceInFoundLevelCloserRatio'], features['horizonDistanceInFoundLevelFatherRatio']])
                    featureWashed.extend([features['childNumber'], features['childTagNumber'],features['siblingNumber'], features['siblingTagNumber'], features['uncleNumber'], features['uncleTagNumber']])
                    writer.writerow(featureWashed)
    f.close()
if __name__=="__main__":
    CookGuanWang()