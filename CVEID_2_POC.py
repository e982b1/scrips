import re  
import sys
import requests
import json
import os 
  
def extract_keywords(html_file_path):  
    # 打开HTML文件并解析内容  
    with open(html_file_path, "r") as file:  
        html_content = file.read()  
  
        # 定义要提取的关键字格式的正则表达式  
        pattern = r"CVE-[0-9]{4}-[0-9]+"  
  
        # 使用正则表达式查找匹配的关键字  
        matches = re.findall(pattern, html_content)  
  
        # 去重并输出结果到文本文件，使用输入的HTML文件名命名输出文件  
        with open(f"{html_file_name[:-5].replace('.', '_')}.txt", "w") as file:  
            unique_matches = list(set(matches))  # 去重  
            for match in unique_matches:  
                file.write(match + "\n")  # 写入文本文件  

def get_cve_info(cve_id):  
    api_url = f"https://poc-in-github.motikan2010.net/api/v1/?cve_id={cve_id}"  
    response = requests.get(api_url)  
    if response.status_code == 200:  
        return response.json()  
    else:  
        print(f"Error fetching CVE info for {cve_id}: {response.status_code}")  
        return None  

if __name__ == "__main__":  
    # 检查命令行参数数量  
    if len(sys.argv) < 2:  
        print("请提供HTML文件路径作为命令行参数")  
        sys.exit(1)  
  
    html_file_path = sys.argv[1]  # 获取HTML文件路径参数  
    html_file_name = html_file_path.split("/")[-1]  # 提取文件名  
  
    extract_keywords(html_file_path)

results = {}  # 创建一个空字典来保存所有结果  
with open(f"{html_file_name[:-5].replace('.', '_')}.txt", 'r') as file:
    cve_ids = [line.strip() for line in file]
    for cve_id in cve_ids:
       result = get_cve_info(cve_id)
       if result:
           results[cve_id] = result
    print("所有CVE ID处理完毕。")

if results:  # 检查是否有结果可以写入文件  
    with open(f"{html_file_name[:-5].replace('.', '_')}.json", 'w') as file:  # 创建一个名为output.json的文件来保存所有结果  
        json.dump(results, file, indent=4)  # 将结果字典格式化为JSON并写入文件，使用CVE ID作为键值对  
        print("所有结果已写入output.json文件。")   
