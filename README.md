# gender-discrimination-hiring

这个repo为获取以下论文的后续实验所需的数据使用的代码：

#### *Li K.*, *L. Li*, *W. Si* and *Z. Xu* (2022) "**Childbearing Age and Gender Discrimination in Hiring Decisions: A Large-scale Field Experiment**" 

论文地址： [here](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4199754).



# 爬虫：

`save_search_pc_responses.py`

mitmproxy脚本，抓取需要的response。



`Selenium.py`

Selenium脚本，完成在特定网站（51job搜索界面）的翻页功能，每次翻页都会产生一个response。注意，偶尔会出现滑块验证，本次需要抓取的数据较少，因此采用手动解决。



`51job_sele.py`

一个静态的HTML网页，但使用responses库时出现了SSL相关的问题，可以用subprocess调用curl解决。因为数据量较小，还是使用了Selenium进行抓取。



# 数据清洗脚本

`final_progressing.ipynb`

完成指定的数据清洗功能



`json2excel_all.py`

把json文件转成excel



其他：

暂未整理好，整理完毕再发。



# 废弃

Creeps：仅使用Selenium实现，效果不太好。

older version：用于存放上次实验中使用过的代码。

