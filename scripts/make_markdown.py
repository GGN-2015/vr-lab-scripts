# 给定个人信息输出一个 markdown 文件
import os
import json
import shutil
dirnow     = os.path.dirname(os.path.abspath(__file__))
root_dir   = os.path.dirname(dirnow)
avatar_dir = os.path.join(root_dir, "avatar")
json_dir   = os.path.join(root_dir, "json")
output_dir = os.path.join(root_dir, "output")

# 学生和老师的公共属性
general_terms = [
    "英文姓名",
    "中文姓名",
    "英文姓",
    "英文名",
    "是否是教师",
    "邮箱",
    "谷歌学术链接",
    "个人主页",
    "研究方向",
]

# 老师的专有属性
teacher_terms = [
    "介绍",     # 如果有介绍，则不可以用后面三项目
    "个人履历", # 指的是工作经历
    "教育背景",
    "科研经历",
]

# 学生的专有属性
student_terms = [
    "年级",
    "学位",
    "毕业去向",
]

# 所有文件拓展名必须为小写
def get_all_json_file() -> list:
    return [
        os.path.join(json_dir, file)
        for file in os.listdir(json_dir)
        if file.endswith(".json")
    ]

# 读取一个 json 文件并且完成文件夹生成
def gen_output_folder_based_on_json(json_file_path):
    with open(json_file_path) as fp:
        json_obj = json.load(fp)
    file_index_name = os.path.basename(json_file_path).split(".")[0]
    print("%s ..." % file_index_name)

    # 如果文件夹已经存在就把现存文件夹删除再创建新文件夹
    output_dir_now  = os.path.join(output_dir, file_index_name)
    if os.path.isdir(output_dir_now):
        print("    rmtree ...")
        shutil.rmtree(output_dir_now)
    print("    makedirs ...")
    os.makedirs(output_dir_now, exist_ok=True)

    # 检查图标是否存在
    avatar = os.path.join(avatar_dir, "%s.jpg" % file_index_name)
    print("    avatar ...")
    assert os.path.isfile(avatar)

if __name__ == "__main__":
    for json_file_path in get_all_json_file():
        gen_output_folder_based_on_json(json_file_path)