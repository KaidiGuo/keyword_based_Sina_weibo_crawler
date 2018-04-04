# keyword_based_Sina_weibo_crawler
A web crawler for Sina, search and retrieve microblogs that contain certain keywords  一个简单的python爬虫实践，爬取包含关键词的新浪微博

[English](./README_En.md)
***

此项目主要功能是通过微博“搜索”页面，每天自动爬取所有包含自定list中词汇的微博原数据。
原为本人研究生论文【Spatial-temporal Analysis of International Connections Based on Textual Social Media Data】获取数据所用。


**低速可控，简单粗暴，适合用来有针对性的搜集数据量不是很大的包含关键词的微博，每日可爬3-6万条**。

~~*不过后来发现其实新浪有这个API，但是隐藏得很深，等我发现的时候这个爬虫已经写完了，抹泪*~~ 

:(  

さぁ、始めよう~
***
# 说明
- 基于python 2
- 在 email_info.py中添加你自己的邮箱，密码，和接收邮箱
- 在sina_crawler.py开头替换你自己的关键词列表
- 日期格式转码和计算等方法都在function.py文件中
- 后续的处理JSON，提取有用信息和我目标项目的本体部分请看[用python处理微博JSON数据小例](./Weibo_Extract.md)
***
# 项目介绍
- 本项目没有UI，虽然简陋但是我写的第一个爬虫，贵在能跑
- 本项目可以24小时不间断运行以获得更完整的微博爬取
- 爬取微博启动和遇到bug的时候会发邮件给你
- 获取的JSON数据写入txt，靠文件夹&文件名进行管理
- 后续对获取到的JSON数据进行处理请查看 [用python处理微博JSON数据范例](https://www.jianshu.com/p/2e3356b730a7)

<img src="https://upload-images.jianshu.io/upload_images/42676-9c6525e2ba7ca429.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">


已获取的微博JSON数据按照request发起的日期分别存在相应的文件夹内部: WBTestdata>04-12.
<img src="http://upload-images.jianshu.io/upload_images/42676-240c3aee71891a4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

每一页JSON包含十条微博数据（一般情况），将每次返回的JSON单调存在一个txt里，命名规则为“国家名”+“日期”+“页码”.
<img src="http://upload-images.jianshu.io/upload_images/42676-a97b05ccb71dba86.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

<img src="https://upload-images.jianshu.io/upload_images/42676-2b895873f7334562.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

可以使用在线[JSON结构化工具](http://www.jsoneditoronline.org/)进行审查

<img src="http://upload-images.jianshu.io/upload_images/42676-f8b5c11d84d127dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

***
# 项目背景

新浪微博各个客户端都提供“搜索”功能，可以得到包含关键词的微博，一般默认按照从新到老的发布顺序显示.
这里我们的目标页面是手机版的新浪微博 m.weibo.cn（因为结构简单，加载的微博数据直接以JSON文件返回，很容易获取）
比如，搜索关键词为[德国](https://m.weibo.cn/p/100103type=2&q=%E5%BE%B7%E5%9B%BD?type=wb)时，页面显示如下：

![image.png](https://upload-images.jianshu.io/upload_images/42676-3db34e5731d91564.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

打开开发者工具，选择network--XHR，然后你往下滚动页面直到有新的微博加载进来，你会发现下面那个链接：

<img src="https://upload-images.jianshu.io/upload_images/42676-ad890fefddf44f53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">

点击它进行预览：

<img src="https://upload-images.jianshu.io/upload_images/42676-135fd42d7312073b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" width="50%" height="50%">


没错，这个就是我们的目标数据了--每当用户滚轮触底，就会通过此链接返回十条JSON格式的新微博.
我们看一下这个链接的格式：
```
https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%E5%BE%B7%E5%9B%BD&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=%E5%BE%B7%E5%9B%BD&containerid=100103type%3D1%26q%3D%E5%BE%B7%E5%9B%BD&page=2
```
解码一下URL，其实它就等于：
```
https://m.weibo.cn/api/container/getIndex?type=all&queryVal=德国& featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=德国&containerid=100103type%3D1%26q%3D德国&page= 1%26q%3D%E5% BE%B7%E5%9B%BD&page=1
```
关键信息一目了然，那就是`queryVal=德国` 和 `page=1`根据这个规则我们就可以构建目标链接进行数据爬取了。

新浪的这个JSON数据就是所谓的一页（1 page），每次返回大概10条微博记录，但有时候也会少于10条，上图中card_group中有几个数字就是有几条记录.

***
# 代码结构
- 先引入request`import requests`
- 定义header伪装浏览器
```
# add header for the crawler
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
```
- 添加你想要检索的关键字的list
```
# Add in your search list!
search_list = ["所罗门群岛", "斯洛伐克", "贝宁",]
......
```
- 将中文关键词转码成URL可以使用的，方便后面构造链接
```
# Create url encoded search list based on the word list you have gaven
urlencoded_search_list = url_encoding(search_list)
urls = create_url_list(urlencoded_search_list)
```
- 写一个`while: 1`的循环执行不停歇的运转，每一次循环是执行当天的任务.
当天的任务我规定为：
**从开始检索的page1开始持续往后搜索，并且获取每一page中最后一条微博的创建时间，如果这条微博创建于两天之内，那我们就继续往后获取页面，直到页面中最老一条的微博是两天前创建的，此时停止本词的搜索，进行下一个词语**

这里需要这样操作的原因在于，新浪似乎并不会真的按照创建时间顺序依次返回所有的微博，两次同一瞬间的检索分别得到的10条微博中可能会有几条不一样的，而越老的微博，新浪返回的时间间隔越大 -- 举个例子，假设用户创造微博的速率是稳定的，在进行包含关键词AAA的检索时，page1中的10条微博都创建于5分钟内，互相间隔几秒，但当你查看page 100时，其中的10条微博则可能互相间隔几个小时 -- 这肯定是不科学的.
这就限制了我们在爬取微博的时候必须从新到老，并且限制不要爬太多页面（因为老数据过于稀松价值会降低），而且对某一个时段最好能重叠搜索，所以我创造了上面的规则，使每天的任务其实为【到现在为止前72小时内发布的微博】，这样时间上的重叠能更多的获取到更全的“老”微博。

- 在while循环内
  1. 给自己发一封邮件提示程序开始了
  2. 根据日期创建每日数据的文件夹
  3. 对于每一个在list中的关键词从page=1开始往后检索，获取一页写下一页，同时获取每一页最后后一条微博的创建时间，判断是否停止搜索
  4.完成所有关键词检索后，给自己发一封邮件提示今日任务完成了
  5. 打印一些数据信息，写每日记录，计算需要睡多久（保证每天在同一时刻开始任务以减少额外的未知误差）
***
注释非常详细，细节就请直接参考代码.




