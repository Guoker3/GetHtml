import requests
import bs4

def openUrl(fileName):
    fn=fileName+".ul"
    with open(fn,"r") as f:
        content=f.read()
        return (content.split("\n"))

def getHtml(url):
    try:
        res = requests.get(url)
    except Exception:
        print("can't get URL:  " + url)
        return None
    res.encoding = 'utf-8'
    return res


def cookSoup(res,ps="html.parser"):
    cookedSoup = bs4.BeautifulSoup(res.text,ps )
    return cookedSoup

    
if __name__ == "__main__":
    pass