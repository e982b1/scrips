import subprocess  
  
# 输入文本文件的路径  
input_file_path = 'index2.txt'  
# cvemap命令可能需要的其他参数（如果有的话）  
cvemap_args = '-json'  
# 输出JSON文件的路径  
output_json_path = 'output.json'  
  
try:  
    # 打开输入文件并读取内容  
    with open(input_file_path, 'r') as file:  
        input_data = file.read().strip()  
  
    # 构造cvemap命令  
    command = f'echo "{input_data}" | cvemap {cvemap_args}'  
  
    # 使用subprocess执行命令，并捕获输出  
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  
  
    # 检查命令是否成功执行  
    if result.returncode == 0:  
        # 获取cvemap的输出  
          
        #print(f"Processed line: '{input_data}'")  
        #print(f"Line '{input_data}' found match for 'CVE'.")  
        cvemap_output = result.stdout
  
        # 假设cvemap的输出已经是有效的JSON，直接写入文件  
        with open(output_json_path, 'w') as file:  
            file.write(cvemap_output)  
  
        print(f"cvemap results have been saved to {output_json_path}")  
    else:  
        # 如果命令执行失败，打印错误信息  
        print(f"Failed to execute cvemap, Error: {result.stderr}")  
 
except FileNotFoundError:  
    print(f"The input file {input_file_path} was not found.")  
except Exception as e:  
    print(f"An error occurred: {e}")
