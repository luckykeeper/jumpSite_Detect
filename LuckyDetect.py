# LuckyDetect.py LuckyBlog 跳转站智能检测程序
# 方法：每隔 x 分钟对博客站的情况进行检测，如果连续无法访问，判定站寄了
# 修改 HTML 到index.html
# Author：Luckykeeper <https://luckykeeper.site | luckykeeper@luckykeeper.site>
# Update：2022-04-11

# 基本设定
##################
# 调试模式
debug = True

# CDN 的地址
hbfuOA_url = 'https://oa.hbfu.edu.cn/backstage/filecenter/file/main::0cd05a5600b2433193054367efe9d17d'

# 博客站地址
luckyblog_url = 'https://blog.luckykeeper.site:24680/'

hbfuOA_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
    }

luckyblog_headers = {
    # "User-Agent": "LuckyPython By Luckykeeper"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
    }

# 输出文件
outHtml = "./html/index.html"

# OA&Blog 正常文件
all_normal = "./html/index_cdn.html"

# OA寄 Blog 正常
oa_g =  "./html/index.html"

# blog 寄
blog_g = "./html/Maintenance.html"
########################## 程序开始
import os,requests,datetime,shutil

def updateFile(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:旧字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

print("_____________________________________")
print("跳转站智能检测 By Luckykeeper!")
print("当前设定信息")
if debug:
    print("调试模式:ON!")
else:
    print("调试模式:OFF!")
print("CDN 地址: ",hbfuOA_url)
print("博客地址: ",luckyblog_url)
print("程序开始运行!")
print("_____________________________________")

try:
    # 获取当前时间
    now_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    if debug:
        print("当前时间: ",now_time,type(now_time))
    # 判断 OA 状态
    try:
        hbfuOA_status = requests.get(url=hbfuOA_url, headers=hbfuOA_headers)
        if debug:
            print("http_code: ",hbfuOA_status.status_code)
        if hbfuOA_status.status_code == 200:
            print("OA 正常!")
            oa_status = True
        else:
            print("OA 寄!")
            oa_status = False
    except:
        oa_status = False


    # 判断博客状态
    try:
        luckyblog_status = requests.get(url=luckyblog_url, headers=luckyblog_headers)
        if debug:
            print("http_code: ",luckyblog_status.status_code)
        if luckyblog_status.status_code == 200:
            print("LuckyBlog 正常!")
            blog_status = True
        else:
            print("LuckyBlog 寄!")
            blog_status = False
    except:
        blog_status = False

    # 生成替换内容
    # OA 和 Blog 都正常
    if oa_status and blog_status:
        add_html = "<center><p><font color=\"green\">OA 状态：正常！& Blog 状态：正常！ "+"检测时间(UTC+3)："+now_time+"</a></font></p></center>"
        index_cdn = True
        index = False
        Maintenance = False
    # OA 寄 Blog 正常
    elif oa_status == False and blog_status == True:
        add_html = "<center><p><font color=\"yellow\">OA 状态：异常！& Blog 状态：正常！ "+"检测时间(UTC+3)："+now_time+"</a></font></p></center>"
        index_cdn = False
        index = True
        Maintenance = False
    # OA 正常 Blog 寄
    elif oa_status == True and blog_status == False:
        add_html = "<center><p><font color=\"red\">OA 状态：正常！& Blog 状态：异常！ "+"检测时间(UTC+3)："+now_time+"</a></font></p></center>"
        index_cdn = False
        index = False
        Maintenance = True
    # OA Blog 都寄
    else:
        add_html = "<center><p><font color=\"red\">OA 状态：异常！& Blog 状态：异常！ "+"检测时间(UTC+3)："+now_time+"</a></font></p></center>"
        index_cdn = False
        index = True
        Maintenance = False

    if os.path.exists(outHtml):
        if debug:
            print("当前输出文件存在!删除旧文件")
        os.remove(outHtml)
    if index_cdn:
        shutil.copyfile(all_normal,outHtml)
        updateFile(outHtml,"<!-- devinput -->",add_html)
    elif index:
        shutil.copyfile(oa_g,outHtml)
        updateFile(outHtml,"<!-- devinput -->",add_html)
    elif Maintenance:
        shutil.copyfile(blog_g,outHtml)
        updateFile(outHtml,"<!-- devinput -->",add_html)



except:
    print("程序寄了")
    if os.path.exists(outHtml):
        if debug:
            print("当前输出文件存在!删除旧文件")
        os.remove(outHtml)
    add_html = "<center><p><font color=\"yellow\">OA & Blog 状态未知！ "+"检测时间(UTC+3)："+now_time+"</a></font></p></center>"
    shutil.copyfile(all_normal,outHtml)
    updateFile(outHtml,"<!-- devinput -->",add_html)