#coding=utf-8
from functions import *
from emailsender import *
from email_infor import *
import requests
import time
import random
import os.path


# add header for the crawler
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

# Add in your search list!
search_list = ["所罗门群岛", "斯洛伐克", "贝宁", "圣多美和普林西比", "埃及", "中非", "冈比亚", "以色列", "科特迪瓦", "佛得角", "亚美尼亚", "波斯尼亚", "阿尔巴尼亚",
               "比利时", "马来西亚", "伊拉克", "苏里南", "津巴布韦", "伊朗", "布隆迪", "巴勒斯坦", "秘鲁", "立陶宛", "几内亚比绍", "智利", "新加坡", "卡塔尔", "利比亚",
               "萨摩亚", "墨西哥", "朝鲜", "缅甸", "柬埔寨", "英国", "巴西", "阿富汗", "日本", "格鲁吉亚", "巴基斯坦", "爱沙尼亚", "孟加拉", "毛里塔尼亚", "马尔代夫",
               "匈牙利", "沙特", "尼日尔", "拉脱维亚", "文莱", "哈萨克斯坦", "波兰", "安道尔", "卢森堡", "塞拉利昂", "阿曼", "台湾", "印度", "毛里求斯", "斯洛文尼亚",
               "韩国", "古巴", "希腊", "蒙古", "纳米比亚", "乍得", "摩纳哥", "埃塞俄比亚", "丹麦", "挪威", "哥伦比亚", "格林纳达", "摩洛哥", "德国", "斯里兰卡", "苏丹",
               "汤加", "澳大利亚", "新西兰", "叙利亚", "突尼斯", "刚果金", "阿根廷", "阿尔及利亚", "南非", "奥地利", "乌干达", "特立尼达和多巴哥", "喀麦隆", "塞舌尔",
               "葡萄牙", "保加利亚", "不丹", "东帝汶", "乌拉圭", "委内瑞拉", "瑞士", "玻利维亚", "西班牙", "摩尔多瓦", "加纳", "土库曼斯坦", "圭亚那", "吉尔吉斯",
               "坦桑尼亚", "尼日利亚", "塔吉克斯坦", "乌兹别克斯坦", "阿联酋", "马里", "瑞典", "白俄罗斯", "多哥", "法国", "罗马尼亚", "圣卢西亚", "俄罗斯", "赞比亚",
               "加蓬", "科威特", "卢旺达", "几内亚", "塞内加尔", "赤道几内亚", "泰国", "瑙鲁", "厄瓜多尔", "老挝", "荷兰", "马耳他", "越南", "尼泊尔", "博茨瓦纳",
               "利比里亚", "约旦", "多米尼克", "爱尔兰", "也门", "安哥拉", "吉布提", "巴林", "瓦努阿图", "土耳其", "美国", "刚果布", "塞浦路斯", "冰岛", "莱索托",
               "巴哈马", "意大利", "菲律宾", "索马里", "印尼", "阿塞拜疆", "肯尼亚", "巴巴多斯", "牙买加", "塞尔维亚", "列支敦士登", "密克罗尼西亚", "马其顿", "新几内亚",
               "黎巴嫩", "斐济", "莫桑比克", "厄立特里亚", "圣马力诺", "布基纳法索", "捷克", "芬兰", "科摩罗", "克罗地亚", "加拿大", "安提瓜和巴布达", "马达加斯加",
               "乌克兰", "图瓦卢", "圣文森特和格林纳丁斯", "多米尼加", "哥斯达黎加", "基里巴斯", "斯威士兰", "巴拉圭", "帕劳", "马拉维", "萨尔瓦多", "尼加拉瓜", "海地",
               "南苏丹", "伯利兹", "危地马拉", "洪都拉斯", "黑山共和国", "圣基茨和尼维斯","梵蒂冈", "马绍尔群岛"]

# Create url encoded search list based on the word list you have gaven
urlencoded_search_list = url_encoding(search_list)
urls = create_url_list(urlencoded_search_list)

# loop for none stop run
day_count = 0
while 1:
    # you can personalize your own report email here
    # send an email to you when everyday's mission start
    start_title = "Program start!"
    start_report = str(datetime.now())
    send_email(user, pwd, recipient, start_title, start_report)

    # define folder path
    yesterday_folder = "../WBTestdata/" + yesterday()
    today_folder = "../WBTestdata/" + today()

    # Testify if today's folder exist, if not, create
    if not os.path.exists(today_folder):
        print "Today's first run! Create new folder."
        os.mkdir(today_folder)

    # start mission, set 0, print out mission information: start time, date of today, how many days this program has run
    word_count = 0
    total_page_count = 0
    today_start_time = datetime.now()
    print "Start time: ", today_start_time
    print "Today is: " + today()
    print "daycount: ", day_count

    # Print out welcome message
    if not os.path.exists(yesterday_folder):
        print "No data from yesterday, the first run!"
    else:
        print "Detect ysterday's data! Welcome back!"

    # loop for every word in the list
    for country in range(len(search_list)):
        word_count += 1
        unico_this_word = search_list[country].decode('UTF-8')  # get current country in UNICODE
        this_baseurl = urls[country]  # create base url: without page number
        initial_page_number = 1  # define start page
        str_initial_page_number = str(initial_page_number)
        exception_count = 0  # exception count
        end_date = days_ago(2)  # Determine the date of when to end, format [03-30]

        # loop for adding page number and requesting them in succession
        # The date below all follow format [04-02], check function.py for more information
        for i in range(initial_page_number, initial_page_number + 300):  # Let's say, no more than 300 pages per word
            this_page_number = str(i)
            this_url = this_baseurl + this_page_number  # generate current url with current page number
            print "This is word number", word_count, ", the word is ", unico_this_word, ", this is page ", this_page_number

            # Get and write down JSON data into txt file with structured file name
            try:
                req = requests.get(this_url, headers=headers, timeout=4)
                content = req.content
                this_file_path = "../WBTestdata/" + today() + "/" + unico_this_word + today() + "page" + this_page_number + ".txt"  # generate txt file name and path
                try:
                    with open(this_file_path, "w") as f:
                        f.write(content)  # write down data

                # This situation happens when today's mission did not finished on time before 24:00
                # So there is not folder exist for today's file path: this_file_path
                # Need to create the folder first
                except OSError:
                    if not os.path.exists(today_folder):
                        print "Why you are so late? ok ok, create the new folder for you..."
                        os.mkdir(today_folder)
                        with open(this_file_path, "w") as f:
                            f.write(content)  # write down data
                print "total page count: ", total_page_count
                total_page_count += 1

                # Get this page's end time to determine to continue to next page or to next word
                try:
                    this_end_time = get_this_endtime_text(content)

                # This situation happens when the server changed the JSON structure,
                # if happens, please check the JSON data and change the retrieve structure accordingly
                except Exception, e:
                    print "Get this endtime fail! jump to next country."
                    break

                if end_date > this_end_time:
                    print "current endtime: ", this_end_time
                    print "We reached 2 days ago's data! Now sleep a while and call for next country!"
                    break
                else:
                    print "current page's endtime: ", this_end_time
                    print "Not enough! Sleep a while and continue requesting for next page!"
                    time.sleep(random.randint(2, 8))

            # This situation happens when there is no weibo exist for the word your try to search
            # Pleas double check on the web page
            except IndexError:
                print "There is no data! to the next country!"
                break

            # Other than index error, it could also be request rejecting due to high frequency
            except Exception, e:
                exception_count += 1
                if exception_count > 6:
                    print "ehhhhh! I have failed 5 times for this country, I got to stop really long! 1 hour!"

                    # you can personalize your own report email here
                    # send an email to you when exception received more than 6 time
                    error_title = "Error!"
                    error_report = str(datetime.now())
                    send_email(user, pwd, recipient, error_title, error_report)

                    exception_count = 0  # Set exception count back to 0 and sleep for 1 hour
                    time.sleep(600)

                print "request has been rejected or failed! Sleep 1 minutes and try next page!"
                print e
                time.sleep(50)
                continue
        print "Finish: " + unico_this_word + " sleep 10 seconds"
        time.sleep(10)

    # Print out today's mission information
    print "Finish today's work, sleep for tomorrow..."
    today_end_time = datetime.now()
    sleep_time = sleep_how_long(24, today_start_time, today_end_time)
    print "Today's sleep time is: ", sleep_time
    print "Today start at: ",today_start_time
    print "Today end at: ", today_end_time
    print "Duration: ", today_end_time - today_start_time
    print "Total page: ", total_page_count

    # you can personalize your own report email here
    # send an email to you when everyday's mission finished
    daily_title = today() + "  Report"
    daily_report = today() + ", Total page: " + str(total_page_count) + ", Starttime: " + str(today_start_time) + ", Endtime: " + str(today_end_time) + ", During: " + str(today_end_time - today_start_time) + "\n"
    #send_email(user, pwd, recipient, subject, body)
    send_email(user, pwd, recipient, daily_title, daily_report)

    # Create a txt file to save daily report
    logfile = "mylog.txt"
    with open(logfile, "a") as f:
        f.write(daily_report)
        print "Log output finished..."

    day_count += 1
    word_count = 0
    time.sleep(sleep_time)