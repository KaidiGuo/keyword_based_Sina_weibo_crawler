# keyword_based_Sina_weibo_crawler
A web crawler for Sina, search and retrieve microblogs that contain certain keywords  一个简单的python爬虫实践，爬取包含关键词的新浪微博

[中文](./README.md)
***

# Information
- Based on python 2
- add your own Email setting in email_info.py
- change your own search list at the beginning of sina_crawler.py
- data format and other functions are all contained in function.py
***
# Introduction
- No UI, looks shabby but this is my first crawler I am happy it function all well
- Could and should run 24/7 to get a better resort (data quality)
- You will reveive an Email when mission start, end and meet request failure
- Write JSON data into txt file, managed by structured file and folder name
- Check [用python处理微博JSON数据范例](https://www.jianshu.com/p/2e3356b730a7) for later txt file handling

<img src="https://upload-images.jianshu.io/upload_images/42676-9c6525e2ba7ca429.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

file and forder name based on the date: WBTestdata>04-12.

<img src="http://upload-images.jianshu.io/upload_images/42676-240c3aee71891a4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

Every page of JSON data contains 10 records (in most case). Write each JSON into a txt file name with "keyword"+"date"+"page number"

<img src="http://upload-images.jianshu.io/upload_images/42676-a97b05ccb71dba86.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">


<img src="https://upload-images.jianshu.io/upload_images/42676-2b895873f7334562.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

you could use [JSON editor](http://www.jsoneditoronline.org/)to check the data.

<img src="http://upload-images.jianshu.io/upload_images/42676-f8b5c11d84d127dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

***
# Background

Sina Weibo provides normal user search function in all its client platforms. 

Theoretically, the page source contains all the content we see on a page, after downloading the HTML source we could analyze and extract useful data from it. 

However, most of the well-developed dynamic websites nowadays use AJAX techniques which is not easy to "crawl".

Good news is, Sina still keeping the m.weibo.cn site for smartphone browser user.

The mobile version site only realizes a small part of functions compare to PC Web version, but the general search function is kept.

Much like Web version, through [](m.weibo.cn), the search operation will return weibos from most recent post to older, 10 weibos in each page, and when user scroll down, new pages will be loaded from JSON files— which can be accessed by HTTP request.

For instance, search [Germany](https://m.weibo.cn/p/100103type=2&q=%E5%BE%B7%E5%9B%BD?type=wb) the page looks like this：


<img src="https://upload-images.jianshu.io/upload_images/42676-3db34e5731d91564.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

Open developer tool，check *network*-->*XHR*，and scroll down till new feeds show up. Then you can see this link：

<img src="https://upload-images.jianshu.io/upload_images/42676-ad890fefddf44f53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

click for preview：

<img src="https://upload-images.jianshu.io/upload_images/42676-135fd42d7312073b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

Yes, this is our data.

check the format of this link：
```
https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%E5%BE%B7%E5%9B%BD&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=%E5%BE%B7%E5%9B%BD&containerid=100103type%3D1%26q%3D%E5%BE%B7%E5%9B%BD&page=2
```
decode URL，it actually is the same as：
```
https://m.weibo.cn/api/container/getIndex?type=all&queryVal=德国& featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=德国&containerid=100103type%3D1%26q%3D德国&page= 1%26q%3D%E5% BE%B7%E5%9B%BD&page=1
```
So the key information is obvious，`queryVal=德国` and `page=1`.
Based on this rule we can now make our own url to retreive data.

***
# Code structure
- import library request `import requests`
- Define header
```
# add header for the crawler
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
```
- Add your own keyword list
```
# Add in your search list!
search_list = ["Germany", "Austria", "China",]
......
```
- Encode Chinese into url format (if necessary)
```
# Create url encoded search list based on the word list you have gaven
urlencoded_search_list = url_encoding(search_list)
urls = create_url_list(urlencoded_search_list)
```
- Write `while: 1` to perform daily loop.

The "mission" for each day as I defined is：
**Start from page1 and continue to page+1, on the same time, get the creat time of last record in this page，if this record was created within two days,
we continue to next page, if not, we stop, and move to next word.**

Reason is, Sina seems not really return all records based on time. The 10 records from two requests on the same time may end up with one or two different weibo.
And the older the posts, the bigger the time interval -- page 1 may contain 10 posts from within 10 minutes, while page 100 will contain 10 posts from within 3 hours. 

- Inside the while loop
  1. Send an Email to myself when program start
  2. Creat folder according to the date
  3. Start from page 1 request data untill the last record was post longer than two days
  4. Finish all keyword search, send me another Email
  5. Print some information about the mission, and write the report into a log.txt
***
The comment line in the code is very into detail, please check for any further question.


