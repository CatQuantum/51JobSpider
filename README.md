# 51Job数据挖掘与清洗

## 简介

本代码库主要使用 Selenium 和 Mitmproxy 工具从前程无忧网站上爬取特定条件的招聘岗位等信息，并通过一系列 Python 脚本进行数据清洗和分析。

本项目用于获取论文*Childbearing Age and Gender Discrimination in Hiring Decisions: A Large-scale Field Experiment* 中相关实验所需数据。此项研究旨在探究生育年龄和性别歧视在招聘决策中的影响，由 Li K., L. Li, W. Si, 和 Z. Xu 在2022年首次进行，并于2024年进行第二次实验。期间由于目标网站结构变化及开发人员变动，两次实验所用代码并不相同，该仓库仅供第二次实验使用。

第一次实验所用代码参见：[lunzheng-li/gender-discrimination-hiring](https://github.com/lunzheng-li/gender-discrimination-hiring)

论文完整内容可通过以下链接获取：[阅读论文.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4199754)


## 依赖

本项目主要依赖于 [Selenium](https://www.selenium.dev/zh-cn/) 和 [Mitmproxy](https://mitmproxy.org/)。在开始之前，请确保根据官方网站提供的指南正确安装并配置这两个工具。

接下来，请安装所需的 Python 库：

```
pip install -r requirements.txt
```

## 使用说明

### 获取岗位数据

1. 启动 Mitmproxy：
   ```
   mitmdump --ssl-insecure -s save_search_pc_responses.py
   ```

2. 配置并运行 `page_tuning_by_selenium.py` 来设定并抓取特定筛选条件下的岗位数据。

### 数据清洗

- `data_cleaning.py`：按以下条件清洗数据：
  - 工作地点为北京、上海、广州、深圳四大城市。
  - 发布日期在指定日期的30天内。
  - 月薪不超过40000元。
  - 排除应届生岗位。
  - 同一公司的多个岗位只随机保留一项。
  
  清洗完成后，数据将被随机分为六份。

- `file_processing.py`：实现 JSON 文件到 XLSX 文件的转换等功能。

### 其他

- `competition.ipynb`：使用 Selenium 抓取岗位竞争人数信息。
- `interest.ipynb`：获取用户投递简历后，公司对投递的兴趣程度及简历接收状态。
- `add_and_check.ipynb`：执行数据添加和检查等功能。
- `functions.json`: 前途无忧网站的岗位类别代码。

## 联系方式

遇到使用问题或需要获取论文相关数据时，请通过以下方式联系我们：

- WeChat: Cat_Quantum
