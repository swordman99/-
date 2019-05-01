# 这个爬虫用于下载"笔趣阁"系列网站中的小说。
# main1需用到requests,beautifulsoup4两个Python库。
# main2除以上两个库外还需用到selenium，Chromedriver，因为使用了无头浏览器，main2的速度远慢于main1，但是新版的笔趣阁使用了动态加载页面的方式，所以使用main2才能下载，而老版的笔趣阁则二者均适用。