from mitmproxy import http
import os
import time
from urllib.parse import urlparse, parse_qs

def response(flow: http.HTTPFlow) -> None:
    # 检查响应的URL中是否含有"search-pc"
    if "search-pc" in flow.request.pretty_url:
        # 解析URL获取查询参数
        parsed_url = urlparse(flow.request.pretty_url)
        query_params = parse_qs(parsed_url.query)
        
        # 提取需要的参数
        function = query_params.get('function', [''])[0]
        jobArea = query_params.get('jobArea', [''])[0]
        companySize = query_params.get('companySize', [''])[0]
        pageNum = query_params.get('pageNum', [''])[0]
        
        # 构建文件夹路径
        folder_name = f"{function}-{jobArea}-{companySize}"
        folder_path = os.path.join(os.getcwd(), folder_name)
        
        # 确保文件夹存在
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # 使用当前时间戳构造文件名
        timestamp = int(time.time())
        filename = os.path.join(folder_path, f"job-list_{pageNum}_{timestamp}.json")
        
        # 保存响应内容到指定文件夹
        with open(filename, "wb") as f:
            f.write(flow.response.content)
        print(f"Saved response to {filename}")




# mitmdump --ssl-insecure -s save_search_pc_responses.py
