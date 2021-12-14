import HtmlSpyder as hs

def CookGuanWang():
    ul=hs.openUrl("GuanWang")
    for url in ul:
        html=hs.getHtml(url)
        print(html.text)

if __name__=="__main__":
    CookGuanWang()