import urllib.request
# coding: utf8

import urllib.request
from db import DBManager, Book

def download_img(img_url, api_token, name):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    request = urllib.request.Request(img_url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        img_name = f"{name}.png"
        filename = "./images/"+ img_name
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read()) # 将内容写入图片
            return filename
    except:
        return "failed"

if __name__ == '__main__':

    manager = DBManager()
    books = manager.books()
    print(f"books.count:{len(books)}")
    # 下载要的图片
    # img_url = "http://www.baidu.com/some_img_url"
    # api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"
    # download_img(img_url, api_token)
    for book in books:
        image_name = book.cover_url.split('/').pop()
        book.image_url = f"/static/images/book/{image_name}"
        manager.session.add(book)
        manager.session.commit()

        # download_img(book.cover_url, '', f"{image_name}")
    # download_img('https://img1.doubanio.com/view/subject/l/public/s34567210.jpg','', '124')
