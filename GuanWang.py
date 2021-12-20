import HtmlSpyder as hs
import HtmlReader as hr
def CookGuanWang():
    count=1
    ul=hs.openUrl("GuanWang")
    for url in ul:
        print("count:"+str(count))
        count=count+1
        if (url == ""):
            continue
        html=hs.getHtml(url)
        if(html is None):
            continue
        soup=hs.cookSoup(html)
        print("url:"+url)

        ew=hr.ElementWeaver(soup)
        print("depth:"+ew.getTreeDepth(ew.soup))
        print("width"+ew.getTreeWidth(ew.soup))


        print(ew.getDepthDistance(soup.find_all("img")[0]))
        print(ew.getWidthDistance(soup.find_all("img")[0]))
        #print(html.text)
        #print(ew.imgFilter(soup))

if __name__=="__main__":
    CookGuanWang()