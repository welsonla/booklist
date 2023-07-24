# -*- codeing=utf-8 -*-
import re
from bs4 import BeautifulSoup


# content = """
#  <li>
#     <div class="item">
#         <div class="pic">
#             <em class="">1</em>
#             <a href="https://movie.douban.com/subject/1292052/">
#                 <img width="100" alt="肖申克的救赎"
#                     src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg"
#                     class="">
#             </a>
#         </div>
#         <div class="info">
#             <div class="hd">
#                 <a href="https://movie.douban.com/subject/1292052/" class="">
#                     <span class="title">肖申克的救赎</span>
#                     <span class="title">&nbsp;/&nbsp;The Shawshank Redemption</span>
#                     <span class="other">&nbsp;/&nbsp;月黑高飞(港) / 刺激1995(台)</span>
#                 </a>
#
#
#                 <span class="playable">[可播放]</span>
#             </div>
#             <div class="bd">
#                 <p class="">
#                     导演: 弗兰克·德拉邦特 Frank Darabont&nbsp;&nbsp;&nbsp;主演: 蒂姆·罗宾斯 Tim Robbins /...<br>
#                     1994&nbsp;/&nbsp;美国&nbsp;/&nbsp;犯罪 剧情
#                 </p>
#
#
#                 <div class="star">
#                     <span class="rating5-t"></span>
#                     <span class="rating_num" property="v:average">9.7</span>
#                     <span property="v:best" content="10.0"></span>
#                     <span>2884072人评价</span>
#                 </div>
#
#                 <p class="quote">
#                     <span class="inq">希望让人自由。</span>
#                 </p>
#             </div>
#         </div>
#     </div>
# </li>
# """

# findLink = re.compile(r'<a href="(.*?)">')
# findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
# findTitle = re.compile(r'<span class="title">(.*)</span>')
# findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# findJudge = re.compile(r'<span>(\d{1,})人评价</span>')
# findInq = re.compile(r'<span class="inq">(.*)</span>')
# findBd = re.compile(r'<p class="">(.*>)</p>',re.S)
#
# soup = BeautifulSoup(content,"html.parser")
# for tag in soup.find_all('div', class_="item"):
#     # print(type(item))
#     item  =str(tag)
#     link = re.findall(findLink, item)[0]
#     imgSrc = re.findall(findImgSrc, item)[0]
#     titles = re.findall(findTitle, item)[0]
#     rating = re.findall(findRating, item)[0]
#     judgeNum = re.findall(findJudge, item)[0]
#     inq = re.findall(findInq, item)[0]
#     bd = re.findall(findBd, item)
#     # link = re.findall(findLink, content)[0]
#     # imgSrc = re.findall(findImgSrc, content)[0]
#     # titles = re.findall(findTitle, content)[0]
#     # rating = re.findall(findRating, content)[0]
#     # judgeNum = re.findall(findJudge, content)[0]
#     # inq = re.findall(findInq, content)[0]
#     # bd = re.findall(findBd, content)
#
#     print(f"{link} -- {imgSrc} --- {titles} ---{rating} --- {judgeNum} ---{inq}--- {bd}")


dom = """
<li class="subject-item">
<div class="pic">
<a class="nbg" href="https://book.douban.com/subject/4169399/" onclick="moreurl(this,{i:'15',query:'',subject_id:'4169399',from:'book_subject_search'})">
<img class="" src="https://img1.doubanio.com/view/subject/s/public/s4634788.jpg" width="90"/>
</a>
</div>
<div class="info">
<h2 class="">
<a href="https://book.douban.com/subject/4169399/" onclick="moreurl(this,{i:'15',query:'',subject_id:'4169399',from:'book_subject_search'})" title="The Unbearable Lightness of Being">

    The Unbearable Lightness of Being


    

  </a>
</h2>
<div class="pub">
        
  
 刘慈欣 / 重庆出版社 / 2010-11 / 38.00元
      </div>
<div class="star clearfix">
<span class="allstar45"></span>
<span class="rating_nums">9.3</span>
<span class="pl">
        (197人评价)
    </span>
</div>
<p>The Unbearable Lightness of Being (1984), written by Milan Kundera, is a philo... </p>
<div class="ft">
<div class="collect-info">
</div>
<div class="cart-actions">
</div>
</div>
</div>
</li>

"""

subject_url_patten = re.compile('<a class="nbg" href="(.*)" onclick=.*')
cover_url_patten = re.compile('<img class="" src="(.*)" width="90"/>')
rating_patten = re.compile('<span class="rating_nums">(.*)</span>')
reader_patten = re.compile('\((\d{1,})人评价\)')
title_patten = re.compile('title="(.*)"')
# auhor_patten = re.compile('<div class="pub">[\s\n]+ (.*) \/ (.*) \/ (.*) \/ (.*)(元|\(元\))[\s\n]+<\/div>')
author_patten = re.compile('<div class="pub">[\s\n]+(.*)[\s\n]+<\/div>')
desc_patten = re.compile("<p>(.*)</p>")
price_patten = re.compile('<span class="buy-info"><a .*>(.*)</a>')

url = re.findall(subject_url_patten, dom)[0]
cover_url = re.findall(cover_url_patten, dom)[0]
rating = re.findall(rating_patten, dom)
author_rslt = re.findall(author_patten, dom)
title  = re.findall(title_patten, dom)[0]
desc = re.findall(desc_patten, dom)
price = re.findall(price_patten, dom)
readers = re.findall(reader_patten, dom)

publish_date = ""
auhor_name = ""
publisher = ""
price = 0

print(author_rslt)

if len(author_rslt) > 0:
    content = author_rslt[0]
    #  刘慈欣 / 重庆出版社 / 2010-11 / 38.00元
    item_array = str(content).strip().split('/')

    if len(item_array) > 0:
        # print(f"查找作者{str(item_array[0]).rfind('出版社')}")
        if str(item_array[0]).rfind('出版社') == -1:
            auhor_name = item_array[0]
            print(f"作者是:{item_array[0]}")

    # 出版社
    publisher_patten = re.compile('\/\s?(.*出版社)\s?')
    publisher_list = re.findall(publisher_patten, content)
    if len(publisher_list) > 0:
        publisher = publisher_list[0]
    # 出版时间
    data_patten = re.compile("\s?(\d{4}.*)\s?\/")
    publish_date_list = re.findall(data_patten, content)
    if len(publish_date_list) > 0:
        publish_date = publish_date_list[0]

    # 价格
    price_patten = re.compile('\/\s*(\d{1,}\.?\d{1,}?)元\s?')
    price_list = re.findall(price_patten, content)
    if len(price_list) > 0:
        price = price_list[0] # str(price_list[0]).replace("元", "").replace("(元)", "")
    print(f"{content} --- {publisher} --- {publish_date} ---- {price}")
else:
    print("author null")

if len(desc) == 0:
    desc = ""
else:
    desc = re.findall(desc_patten, dom)[0]

print(rating)
# 评论人数少的图书会不显示评分
if len(rating) == 0 or rating[0] == '':
    rating = 0
else:
    rating = rating[0]

if len(readers) == 0:
    readers = 0
else:
    readers = readers[0]

# price = price.replace("元","").replace("(元)","")

print(author_rslt)
print(f"url:{url}, ----- cover:{cover_url} --- {author_rslt}  ---- {readers}--- {rating} --- {title} ---- {desc} --- {price}")
