import urllib.request,re,http.cookiejar,urllib.parse

def saveFile(data, filename):
    path = "D:\\jav\\" +  filename +  ".txt"
    file = open(path,'wb')  
    for d in data:  
        d = str(d)+'\n'  
        file.write(d.encode('gbk'))  
    file.close() 

def parseVideos(data):
    videoStr = r'<div.*?video.*?"><a href=".(.*?)".*?title="(.*?)"'
    videoPattern = re.compile(videoStr, re.DOTALL)
    videoContents = re.findall(videoPattern, data)
    return videoContents;

def getPageContent(url):
    values = {}
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' 
    headers = { 'User-Agent' : user_agent }  
    request = urllib.request.Request(url,values,headers)
    response = urllib.request.urlopen(request) 
    data =response.read()
    data = data.decode('utf-8')
    return data

def getVideoDetailed(url, title):
    content = getPageContent(url)
    videoStr = r'<img.*?video_jacket_img".*?src="(.*?)".*?>.*?<div.*?video_info">.*?<td.*?class="text">(.*?)</td>.*?</div>.*?<div.*?video_date".*?>.*?<td.*?class="text">(.*?)</td>.*?<div.*?video_cast".*?>.*?<td.*?class="text">(.*?)</td>'
    videoPattern = re.compile(videoStr, re.DOTALL)
    items = re.findall(videoPattern, content);
    picUrl = items[0][0]
    id = items[0][1]
    date = items[0][2]
    cast = items[0][3]
    castStr = r'<span.*?><span.*?><a.*?href="(.*?)".*?>(.*?)</a>'
    castPattern = re.compile(castStr, re.DOTALL)
    castItems = re.findall(castPattern, cast)
    for c in castItems:
        castUrl = c[0]
        castName = c[1]
    print(items)

def getOpener(header):
    #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cookieJar = http.cookiejar.CookieJar()
    cp = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(cp)
    headers = []
    for key,value in header.items():
        elem = (key,value)
        headers.append(elem)
    opener.addheaders = headers
    return opener


def getBTLinks(id):
    baseUrl = "http://btkitty.pet"
    values = { "keyword":id ,"hidden": true }
    postData = urllib.parse.urlencode(values).encode()
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' 
    headers = { 'User-Agent' : user_agent }  
    request = urllib.request.Request(baseUrl,data,headers)
    response = urllib.request.urlopen(request) 
    data =response.read()
    data = data.decode('utf-8')
    return data


getBTLinks("JRZD-757")
baseUrl = "http://www.ja14b.com/cn"
content = getPageContent("http://www.ja14b.com/cn/vl_newrelease.php")
videos = parseVideos(content)
for video in videos:
    url = video[0]
    title = video[1]
    getVideoDetailed(baseUrl + url, title)



