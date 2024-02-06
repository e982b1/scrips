import json
import csv

header = ["漏洞编号", "漏洞描述", "危害等级","漏洞产品","产品所属公司","漏洞类型","披露时间","POC","POC链接"]

# json列表
file_list = ["output.json"]
filename = "cve.csv"
with open(filename, "w", encoding="UTF8") as f:
    writer = csv.writer(f)
    # 写入头
    writer.writerow(header)

for file_name in file_list:
    with open(file_name,"r") as file:
        # 读取JSON数据
        data = json.load(file)
        print("条数：",len(data))
        for i in range(len(data)):
            cve_name = data[i]["cve_id"]
            cve_description = str(data[i]["cve_description"]).replace("\n","")
            # 风险等级
            severity = data[i]["severity"]
            # 漏洞发布日期
            published_at = data[i]["published_at"]
            # 漏洞点
            if "weaknesses" in data[i]:
                weaknesses = str(data[i]["weaknesses"])
            else:
                weaknesses = "无"
            # poc
            if "poc" in data[i]:
                if len(data[i]["poc"]) > 0:
                    poc = str(data[i]["poc"])
                    is_poc = "有"
                else:
                    is_poc = "无"
            else:
                is_poc = "无"
                poc = "无"
            
            if "cpe" in data[i]:
                # 漏洞产品
                product = str(data[i]["cpe"]["product"])
                # 产品所属公司
                vendor = str(data[i]["cpe"]["vendor"])
            else:
                # 漏洞产品
                product = "无"
                # 产品所属公司
                vendor = "无"
    # ["漏洞编号", "漏洞描述", "危害等级","漏洞产品","产品所属公司","漏洞类型","披露时间","是否有POC","POC链接"]
            time_ip_args_rule = cve_name + " #### " + cve_description + " #### " + severity + " #### " + product + " #### " +vendor + " #### " + weaknesses + " #### " + published_at + " #### " + is_poc + " #### " + poc
            new_data = [str(time_ip_args_rule).split(" #### ")]
#            print(new_data)
            # 打开 CSV 文件，以追加模式写入数据
            with open(filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(new_data)
