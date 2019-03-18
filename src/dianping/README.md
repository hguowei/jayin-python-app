shop_list -> shop -> css -> svg.

下载流程：
1. download_shoplists.py:
下载或者手动保存店铺列表网页，保存到shop_lists目录。
解析shop_url和id，储存记录到shop_lists.csv文件。

2. download_shops.py
解析shop_lists.csv文件，下载店铺页面到htlms目录。

3. download_css.py
解析htmls目录网页，解析css_url，并下载到css目录。
或者，css文件，可以直接通过保存页面里面的css文件得到。即，
那就不需要自动下载css或者svg，而是可以直接搜索目录里面的文件得到。

4. download_svg.py: 待实现
下载所需的svg文件。

解析流程：
预解析css和svg文件，保存成json？
1. 读取css目录下，所有的css文件
2. 从css解析出svg路径，查找是否已有json文件，若无，则步骤3解析&创建；
3. 解析svg文件，存成json文件。
4. css所有的class对应的svg json文件
5. 写一个css class到真实文本的对应方法。


1. 读取网页：
shop_lists.csv，读取所有店铺记录，得到店铺页面。同时，遍历htmls目录，得到不是download的页面，即手动下载的页面。

2. 读取网页的评论数据
-> 根据css class，找到对应的css文件