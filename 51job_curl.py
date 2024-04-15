import subprocess
import gzip
import os
import json
from time import sleep


""" # 替换为你的job IDs文件路径
jobids_file_path = 'jobids.txt'


# 读取job IDs
with open(jobids_file_path, 'r') as file:
    jobids = [line.strip() for line in file if line.strip()]
 """

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


data=read_json_file(r"C:\Users\Xue\Documents\GitHub\gender-discrimination-hiring\added.json")

jobids=[]
for job in data:
    jobids.append(job["jobId"])


# 循环处理每个job ID
for jobid in jobids:
    # 构造curl命令
    url = f"https://i.51job.com/userset/compete.php?jobid={jobid}&resumeid=468287804&accountid=241451461&lang=c"
    curl_command = [
        'curl', url, '-k',
        '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        '-H', 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        '-H', 'Cache-Control: max-age=0',
        '-H', 'Connection: keep-alive',
        '-H', ('Cookie: guid=d0f03d872be69bcd8cca452f8b982cee; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; ps=needv%3D0; 51job=cuid=241451461%26cusername=5tPr3OojqzBIvVkQD8w4PerBrId4KfXPcACVxts0hrg%253D; ...[其他cookie信息]'),
        '-H', 'Host: i.51job.com',
        '-H', 'Referer: https://i.51job.com/userset/bounce_window_redirect.php?jobid=153623467&redirect_type=2',
        '-H', 'Sec-Fetch-Dest: document',
        '-H', 'Sec-Fetch-Mode: navigate',
        '-H', 'Sec-Fetch-Site: same-origin',
        '-H', 'Sec-Fetch-User: ?1',
        '-H', 'Upgrade-Insecure-Requests: 1',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        '-H', 'sec-ch-ua: "Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        '-H', 'sec-ch-ua-mobile: ?0',
        '-H', 'sec-ch-ua-platform: "Windows"',
        '-o', f'{jobid}.html.gz'  # 输出文件
    ]
    
    # 执行curl命令
    subprocess.run(curl_command, check=True)
    
    # 解压gzip文件
    with gzip.open(f'{jobid}.html.gz', 'rb') as f_in:
        with open(f'{jobid}.html', 'wb') as f_out:
            f_out.write(f_in.read())
    
    print(f'Job ID {jobid}的页面已保存和解压。')

    sleep(1)
