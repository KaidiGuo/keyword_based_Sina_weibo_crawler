# 前言

简单介绍一下我写用这个爬虫想做的项目是什么样的.
我旨在分析中国微博用户对不同国家新闻&信息的关注程度来了解民间方向上的我国国际关系: **中国网民是如何看待全世界其他国家的，关注点在哪里.**
同时用获得的数据制作一个可交互的可视化微博分析结果.

所以我以193个[联合国会员国](https://zh.wikipedia.org/wiki/%E5%9B%BD%E5%AE%B6%E5%88%97%E8%A1%A8_(%E6%8C%89%E6%B4%B2%E6%8E%92%E5%88%97))加两个联合国观察员国:梵蒂冈，巴勒斯坦, 
去掉中国后的一共194个国家为查询列表.
（基于个人兴趣我在列表中也加入了“台湾”为关键词，但是当然把台湾认定为一个独立国家并不是正确的，所以我并不会在论文和可视化过程中用到来自台湾的数据）
写了一个非常简单的小爬虫，通过通过[移动版微博](http://m.weibo.cn/p/100103type%3D2%26q%3D%E5%BE%B7%E5%9B%BD?type=wb&queryVal=%E5%BE%B7%E5%9B%BD&luicode=10000011&lfid=106003type%3D1&title=%E5%BE%B7%E5%9B%BD)**搜索微博**功能爬取按照这个国家列表查询到的微博.

# What I got

已获取的微博JSON数据按照request发起的日期分别存在相应的文件夹内部。WBTestdata>04-12.

![微博数据文件夹](http://upload-images.jianshu.io/upload_images/42676-240c3aee71891a4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

每一页JSON包含十条微博数据（一般情况），将每次返回的JSON单调存在一个txt里，命名规则为“国家名”+“日期”+“页码”.

![微博数据命名规则](http://upload-images.jianshu.io/upload_images/42676-a97b05ccb71dba86.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以使用在线[JSON结构化工具](http://www.jsoneditoronline.org/)进行审查。

# 载入数据

因为我的数据是包含日期的，这就使得我可以载入指定日期内的数据.
为此，我先写了一个根据给出起始日期生成日期列表的方法：
```
def creat_date_list(month,i,j):
    dates = []
    for n in range(i,j):
        date = month + "-" +str(n).zfill(2)
        dates.append(date)
    return dates
```
在调用的时候例如`dateList = creat_date_list("04",27,28)`就会产生只有一个值的列表.
然后，按照list的内容生成文件夹地址，检查此文件夹是否存在，如果存在则可以进行下一步的文件遍历了.
```
for date in dateList:
    thisDate = date
    datapath = "../WBTestdata/" + thisDate + "/"
    if os.path.exists(datapath):
        print "got data"
    else:
        print "Did not find this day´s data, next day!!"
        time.sleep(5)
        continue
```
当准确获取到存放微博元数据的文件夹路径了以后，我们面对的是上百个txt.
遍历它们，提取我想要的那几个属性内容，再按照一定的规则写入新的txt.
数据量在提取过后必然会变得小很多，那我希望将某一天request到的所有微博写入一个新的，单一的，以当天日期命名的txt.
所以，我的输出路径和文件名就很好规划了，我将输出数据存放在一个叫做WBDatabase的文件夹内，因为目前的输出txt数据是根据日期命名和分割的，所以再丢进一个叫time的文件夹：
```
outputPath = "../WBDatabase/time/"
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    outputFile = outputPath + thisDate + ".txt"
    with open(outputFile, "a") as output:
        output.write("\n")
```
在这里，我在文件开头的第一行写了一个换行符是因为当载入txt文件进MYSQL数据库的时候，第一行出现了一些无法识别数据的错误，所以我将这一行空出，再在数据导入后从数据库中删掉这一空白行.

接下来回到刚说的遍历文件夹.
`os.walk(datapath)`方法可以实现快速的文件夹内部遍历.
在这里通过文件名获取到的`thisCountry`就是我们本条微博的keyword.
注意，中文的编码转换非常复杂，需要仔细耐心.
```
list_dirs = os.walk(datapath)
    for root, dirs, files in list_dirs:
        for f in files:
            filename = f.decode("gbk").encode("UTF-8")
            thisfilepath = datapath + filename.decode("UTF-8")
            thisCountry = filename.split(thisDate)[0].decode("UTF-8")
```
通过遍历文件夹获取到文件名后，就可以打开指定的txt文件进行JSON装载了.
```
with codecs.open(thisfilepath, "r", "utf-8") as thisfile:
        content = thisfile.read()
        thisdata = json.loads(content)
```
装载完JSON，接下来即可进行微博相关数据的提取.
# 微博数据提取思路

JSON结构非常清楚，我觉得有用的微博属性：
* 数据微博ID
* 微博创建时间
* 微博转发数 
* 微博发布平台
* 微博用户名
* 微博用户ID
* 微博用户性别
* 微博用户粉丝数
* 微博内容

分别可以用以下代码来表示和提取.
```
itemID = str(thisdata['cards'][0]['card_group'][i]['mblog']['id'])
itemCreat = thisdata['cards'][0]['card_group'][i]['mblog']['created_at'].encode("UTF-8")
itemRepostCount = str(thisdata['cards'][0]['card_group'][i]['mblog']['reposts_count'])
itemSource = puncfilter(thisdata['cards'][0]['card_group'][i]['mblog']['source'])
itemUser = thisdata['cards'][0]['card_group'][i]['mblog']['user']['screen_name']
itemUserID = str(thisdata['cards'][0]['card_group'][i]['mblog']['user']['id'])
itemUserGender = str(thisdata['cards'][0]['card_group'][i]['mblog']['user']['gender'])
itemUserFollower = str(thisdata['cards'][0]['card_group'][i]['mblog']['user']['followers_count'])
itemText = thisdata['cards'][0]['card_group'][i]['mblog']['text']
```
提取了以上信息以后，还要对对微博文本进行关键词条的Tag提取。此处将会用到[结巴分词](https://github.com/fxsjy/jieba).

前面提到了，为了导入MYSQL方便，但同时又保留原数据，我将会把每一条微博提取到的相关数据组成一行，存在新的以日期命名的txt中.
每一行，既每一条微博，其每一个属性间用tab分割（MYSQL导入时将以\t为分隔符），最后的tag属性我取了5个词，用空格区分.
```
0		Staunch17	5985880084	123	f	在爱的国度，我唯一爱的，就是你致敬不丹，这是一个充满幸福感的国家 ​	 幸福感 国度 不丹 致敬 充满
```
相应的MYSQL数据表创建语句则为：
```
CREATE TABLE wbdata (	
    creat_at DATETIME NOT NULL,
    keyword VARCHAR(30) NOT NULL,
    wid BIGINT NOT NULL,
    repost INT NOT NULL,
    platform CHAR(35) ,
    user CHAR(45) NOT NULL,
    uid INT NOT NULL,
    follower INT NOT NULL,
    gender VARCHAR(2),
    text VARCHAR(500),
    tags VARCHAR(500)

) character set = utf8mb4 COLLATE = utf8mb4_unicode_ci;
```
keyword属性即是前面获取到的`thisCountry`国家名.

# 数据过滤细节

在思路清晰了以后就可以着手于细节的处理了。
这里我们有以下几个问题需要进行处理，
1. 每条微博的创建时间需要由访问时间来进行推算并进行统一化
2. 微博中可能出现HTML标签，换行标签等需要进行摘除
3.  微博文本中出现的大量表情符号需要被初步过滤
4.  微博出现的多人连续@需要剔除
5. 微博发布平台信息也包含用户自定义数据，需要规范化



#### 时间格式转换
对于第一个问题，当知道本次request的时间戳以后，就可以通过换算得到每一条微博创建的时间了.
本次request的时间戳在JSON里的位置为：
```
thisdata['cardlistInfo']['starttime']
```
对于元数据中creat_at属性，值一般为三种结构：“04-16 20:00”， “3分钟前”， “今天 20:00”.
标准时间格式还应当有秒，所以在处理的时候应当加入缺失部分默认为00秒.
在这里要注意一下，localtime转换默认跟着计算机时间走，因为我不在国内，所以时区不一样，算出来的微博发布时间错了6个小时，没有什么转换时区的好办法，我就直接把我电脑系统的默认时区调成了中国时间.
但是理论上哪怕错了6个小时也影响不大，因为我的每日热点分析统计以及后面的可视化都应当是按照天为单位的.
```
def process_time(input, starttime):
    if "今天" in input:
        thisStartTime = time.localtime(float(starttime))
        otherStyleTime = str(time.strftime("%Y-%m-%d", thisStartTime))
        creatTime = otherStyleTime + " " + input.split(" ")[1]+":00"
        return creatTime
    elif "分钟前" in input:
        creatTime = 60 * float(input.strip("分钟前"))
        thisStartTime = time.localtime(float(starttime) - creatTime)
        otherStyleTime = str(time.strftime("%Y-%m-%d %H:%M:%S", thisStartTime))
        return otherStyleTime
    else:
        return "2017-"+input+":00"
```
#### 文本中HTML标签去除
初步提取的微博文本包含HTML标签.

![包含HTML的微博文本](http://upload-images.jianshu.io/upload_images/42676-e1415e327a5e2e7a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

需要进行再次提取.
这里用到[Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/).
它是一个可以从HTML或XML文件中提取数据的Python库.
以下代码可以把输入元文本中的所有tag里的内容提取出来并跳过空白行，输出形式为列表.
但是当然实现办法有很多，B4S提供了许多其他可能的方式.
```
from bs4 import BeautifulSoup

soup = BeautifulSoup(itemText, "html.parser")
itemTextPretty = ""
for string in soup.stripped_strings:
     itemTextPretty += string
```
然后是去掉文本中的URL和连续@.
两个简单的小方法来实现.
```
itemTextPretty = removepeople(itemTextPretty)
itemTextPretty = removeurl(itemTextPretty)
```
```
def removeurl(urlline):
    results = re.compile(r'http://[a-zA-Z0-9.?/&=:]*', re.S)
    dd = results.sub("", urlline)
    return dd

def removepeople(peopleline):
    pattern = peopleline.split("//@")
    outputline = ""
    for name in pattern:
        name = name.split(":")[-1]
        outputline += name
    return outputline
```
接下来是粗步过滤掉一些标点符号.
```
def puncfilter(line):  
    r1 = u'[’!"#$%&\'()*+,-./:;<=>?@；；：．｜～\≧▽—°❄×🍀🐾🍓🐋▲♥♀☀●巜「」☕／↓→<=>?@⁄•ω★💊🙈☕💰😂·、…★、​…【】《》『』（）？“”‘’！[\\]^_`{|}~]+'
    return re.sub(r1, '', line)
```
过滤完以后就可以进行结巴分词的Tag提取了：
在这里`topk=5`规定了提取重要性前五的单词.
因为结巴分词方法返回的是一连串tupe，每一个tupe里的第一位为词语，第二位为重要值，我只需要词，所以用for方法提取，赋值给extracline以空格分割.
```
extract = jieba.analyse.extract_tags(itemTextP, topK=5, withWeight=True, allowPOS=())
extractline = ""
for word in extract:
    co = word[0]
    extractline = extractline + " " + co
```
#### 微博发布平台的规范化
那么，除了微博文本要进行符号过滤之外，用户发布平台也需要，因为微博用户可以自己修改发布平台的原因，收集到的很多平台信息为累赘信息：

![微博发布平台中的累赘信息](http://upload-images.jianshu.io/upload_images/42676-41401bfd178c7fb0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我要去除这些用户自定义的部分，对于iphone用户，我直接建了张型号表进行匹配。
而对于像是红米这样的情况，为了便于后期统计，我加入小米前缀，同理还有魅蓝，加入魅族前缀，荣耀加入华为前缀。
但是当然，能兼顾到的也只是大部分用户而已，过于小众的一些手机的某些型号则无法做到百分百的规范化。
```
def platformUni(platform):
    if 'iPhone' in platform:
        iphonelist =[ "iPhone 5s", "iPhone 5c", "iPhone 5",  "iPhone 6 Plus", "iPhone 6s Plus", "iPhone 6s","iPhone 6", "iPhone 7 Plus", "iPhone 7","iPhone SE", "iPhone"]
        for phone in iphonelist:
            if phone in platform:
                new = phone
                return new
        # new = "iPhone" + platform.split('iPhone')[1]
    elif 'iOS' in platform:
        new = "iPhone"
        return new
    elif 'Android' in platform:
        new = "Android" + platform.split('Android')[1]
        return new
    elif 'iPad' in platform:
        new = "iPad" + platform.split('iPad')[1]
        return new
    elif '360手机' in platform:
        new = "360手机"
        return new
    elif '魅族' in platform:
        new = "魅族" + platform.split('魅族')[1]
        return new
    elif 'MEIZU' in platform:
        new = "魅族" + platform.split('MEIZU')[1]
        return new
    elif '魅蓝' in platform:
        new = "魅族 魅蓝" + platform.split('魅蓝')[1]
        return new
    elif 'Galaxy' in platform:
        new = "三星 Galaxy" + platform.split('Galaxy')[1]
        return new
    elif 'GALAXY' in platform:
        new = "三星 Galaxy" + platform.split('GALAXY')[1]
        return new
    elif 'Samsung' in platform:
        new = "三星" + platform.split('Samsung')[1]
        return new
    elif '360' in platform:
        new = "360" + platform.split('360')[1]
        return new
    elif '小米' in platform:
        new = "小米" + platform.split('小米')[1]
        return new
    elif '红米' in platform:
        new = "小米 红米" + platform.split('红米')[1]
        return new
    elif 'xiaomi' in platform:
        new = "小米" + platform.split('小米')[1]
        return new
    elif '荣耀' in platform:
        new = "华为荣耀" + platform.split('荣耀')[1]
        return new
    elif 'vivo' in platform:
        new = "vivo" + platform.split('vivo')[1]
        return new
    elif 'HUAWEI' in platform:
        new = "华为" + platform.split('HUAWEI')[1]
        return new
    elif 'OnePlus' in platform:
        new = "一加" + platform.split('OnePlus')[1]
        return new
    elif 'Smartisan' in platform:
        new = "锤子" + platform.split('Smartisan')[1]
        return new
    elif '坚果' in platform:
        new = "锤子 坚果" + platform.split('坚果')[1]
        return new
    elif 'Xperia' in platform:
        new = "索尼 Xperia" + platform.split('Xperia')[1]
        return new
    else:
        return platform
```
规范化是一方面，但是介于后期我可能会需要统计不同品牌的手机型号占比，我在这里就直接再添加了一个属性段，即把发布平台进行笼统分类，所有iphone的各种型号都归为一类，所有三星手机归为三星类这样.
```
def platformSimp(platform):
    platformlist = ["iPhone", "iPad", "秒拍", "三星", "华为", "小米", "OPPO", "vivo", "魅族","索尼","锤子","一加","Android"]
    thisphone = platform
    for phone in platformlist:
        if phone in platform:
            return phone
    return platform
```


#### 写行
在做完这一切以后，就可以把属性按顺序组成一行写入了.
```
 dataLine = itemCreatFormat + "\t" + itemKeyword.encode("UTF-8") + "\t" + str(itemID)  + "\t" + str(itemRepostCount) + "\t" + itemSourceUni + "\t" + itemSourceSimp + "\t" +itemUser.encode("UTF-8") + "\t" + str(itemUserID) + "\t" + str(itemUserFollower) + "\t" + itemUserGender + "\t" +itemTextP.encode("UTF-8")+ "\t"+ extractline.encode("UTF-8") + '\n'
                        
```
最终结果如下：

![输出结果](http://upload-images.jianshu.io/upload_images/42676-42873661df77c15c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这个文本文件就可以很轻松的导入mysql进行下一步的去重，分析等操作了.
