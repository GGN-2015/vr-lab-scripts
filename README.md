# vr-lab-scripts
用于维护实验室网站的 md 生成脚本

- 网站主页：https://vr-pan-junjun.github.io/
- 网站项目：https://github.com/vr-pan-junjun/vr-pan-junjun.github.io

## 如何新增学生/老师

- 首先，确定学生的英文名称 `<英文名>`。
- 在 `avatar` 文件夹中放入学生头像的 `<英文名>.jpg` 文件
    - 注意：英文名应当注意首字母与姓氏首字母大写，但 `.jpg` 应当保持小写
    - 建议仅使用 `jpg` 文件格式
- 将 `template.json` 复制到 `./json/<英文名>.json`
    - 编辑 `./json/<英文名>.json` 填写其中的相关内容
    - 关于重名问题：我们要求同一个学生使用的所有英文名都相同，这个名字将被用于在 publication 中引用
    - 关于身份：身份有 "教师"、"学生"、"毕业生" 三种
- 运行 `scripts/make_markdown.py` 脚本
- 将 `output` 文件夹中的所有内容
    - 拷贝并覆盖到 `https://github.com/vr-pan-junjun/vr-pan-junjun.github.io` 项目中 `./content/authors` 目录内
- 把更改后的项目 push 到 github
