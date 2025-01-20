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
    "是否是教师",
    "身份", # 教师、学生、毕业生
    "显示身份", # 教授，副教授，[空白]
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

# 计算用户所在分组
def get_user_group(iden: str):
    assert iden in ["教师", "学生", "毕业生"]
    if iden == "教师":
        return "Researchers"
    
    elif iden == "学生":
        return "Grad Students"
    
    elif iden == "毕业生":
        return "Alumni"
    assert False

# 生成 markdown 文件内容
def gen_index_md_content(json_obj):
    ans  = "---\n"

    # 姓名信息
    ans += "# Display name\n"
    ans += "title: %s（%s）\n" % (json_obj["英文姓名"], json_obj["中文姓名"])
    ans += "\n"

    ans += "# Full Name (for SEO)\n"
    ans += "first_name: %s\n" % json_obj["英文姓名"].split()[0]
    ans += "last_name: %s\n"  % json_obj["英文姓名"].split()[-1]
    ans += "\n"

    # 是否是教师
    is_teacher = ("true" if json_obj["是否是教师"] else "false")
    ans += "# Is this the primary user of the site?\n"
    ans += "superuser: %s\n" % is_teacher
    ans += "\n"

    # 填写角色身份
    if json_obj["年级"] and json_obj["学位"]: # 例如：2020 级青岛研院硕士
        role = "%s 级%s\n" % (json_obj["年级"], json_obj["学位"])
    elif json_obj["显示身份"]:
        role = json_obj["显示身份"]
    else:
        role = "" # 不显示身份
    ans += "# Role/position\n"
    ans += "role: %s\n" % role # 角色一定要填写
    ans += "\n"

    ans += "# Organizations/Affiliations\n"
    ans += "organizations:\n"
    ans += "  - name: Beihang University\n"
    ans += "    url: ''\n"
    ans += "\n"
    ans += "# Short bio (displayed in user profile at end of posts)\n"
    ans += "bio: \n\n\n"

    # 邮箱和谷歌学术
    ans += "# Social/Academic Networking\n"
    ans += "# For available icons, see: https://docs.hugoblox.com/getting-started/page-builder/#icons\n"
    ans += "#   For an email link, use \"fas\" icon pack, \"envelope\" icon, and a link in the\n"
    ans += "#   form \"mailto:your-email@example.com\" or \"#contact\" for contact widget.\n"
    ans += "social: \n"
    ans += "  - icon: envelope\n"
    ans += "    icon_pack: fas\n"
    ans += "    link: 'mailto:%s'\n" % json_obj["邮箱"]
    ans += "  - icon: google-scholar\n"
    ans += "    icon_pack: ai\n"
    ans += "    link: '%s'\n" % json_obj["谷歌学术链接"]
    ans += "\n"

    # 研究方向
    if json_obj["研究方向"]:
        ans += "interests:\n"
        for term in  json_obj["研究方向"]:
            ans += "  - %s\n" % term
    ans += "\n"

    ans += "# Enter email to display Gravatar (if Gravatar enabled in Config)\n"
    ans += "email: ''\n\n" # 这个是用来做无头像 avatar 的

    # 在作者列表中高亮老师的姓名吧
    ans += "highlight_name: %s\n" % is_teacher
    ans += "\n"

    # 身份填写
    ans += "user_groups: \n"
    ans += "  - %s\n" % get_user_group(json_obj["身份"])
    ans += "\n"

    # 开始 Markdown 正文
    ans += "---\n\n"
    ans += "# %s\n\n" % json_obj["中文姓名"]
    
    if role:
        ans += "%s\n\n" % role

    # 介绍
    for term_name in ["介绍", "个人履历", "教育背景", "科研经历", "毕业去向", "个人主页"]:
        if json_obj[term_name]:
            ans += "## %s\n" % term_name
            ans += "%s\n" % json_obj[term_name]
            ans += "\n"

    return ans

def gen_index_md(markdown_file, json_obj):
    content = gen_index_md_content(json_obj)
    with open(markdown_file, "w", encoding="utf-8")  as fp:
        fp.write(content)

# 读取一个 json 文件并且完成文件夹生成
def gen_output_folder_based_on_json(json_file_path):
    with open(json_file_path) as fp:
        json_obj = json.load(fp)
    file_index_name = os.path.basename(json_file_path).split(".")[0]
    print("%s ..." % file_index_name)

    # 如果文件夹已经存在就把现存文件夹删除再创建新文件夹
    output_dir_now  = os.path.join(output_dir, file_index_name)
    print("    makedirs ...")
    if os.path.isdir(output_dir_now):
        shutil.rmtree(output_dir_now)
    os.makedirs(output_dir_now, exist_ok=True)

    # 检查图标是否存在，如果存在就移动图标
    avatar = os.path.join(avatar_dir, "%s.jpg" % file_index_name)
    print("    copy avatar ...")
    assert os.path.isfile(avatar)
    shutil.copy2(avatar, os.path.join(output_dir_now, "avatar.jpg"))

    # 生成 markdown 文件
    print("    gen_index_md ...")
    markdown_file = os.path.join(output_dir_now, "_index.md")
    gen_index_md(markdown_file, json_obj)

if __name__ == "__main__":
    for json_file_path in get_all_json_file():
        gen_output_folder_based_on_json(json_file_path)
