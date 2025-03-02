# 知识问答平台

这是一个面向教育领域的知识问答/考试平台，可用于课程测验、知识竞赛或自我学习评估。系统支持多选题、单选题等题型，并提供答题记录和成绩统计功能。

## 功能特点

- 用户认证：学生登录系统进行答题
- 随机出题：从题库中随机抽取题目
- 答题评分：自动计算得分并记录
- 历史记录：查看历史答题记录
- 管理功能：管理员可查看所有用户的答题情况

## 项目结构

```
├── server/           # 后端服务器代码
│   ├── app.py        # Flask应用主程序
│   └── setup_db.py   # 数据库初始化脚本
├── web/              # 前端代码
│   ├── src/          # Vue源代码
│   └── public/       # 静态资源
└── data/             # 数据文件
    ├── questions.csv.example  # 题库示例
    └── users.csv     # 用户数据
```

## 安装与运行

### 前提条件

- Python 3.6+
- Node.js 14+
- npm 或 yarn

## 数据格式

### 题库格式

题库使用CSV格式，示例位于 `data/questions.csv.example`。CSV文件应包含以下列：“序号,题目,A,B,C,D,答案”

```csv
序号,题目,A,B,C,D,答案
1,AIGC的英文全称是什么？,Artificial Intelligence Generated Content,Automated Intelligence Graphic Creation,Advanced Intelligent Generated Content,Algorithmic Image Generation Creation,A
2,下列哪个不属于AIGC的应用领域？,文本生成,图像生成,音乐创作,半导体制造,D
3,ChatGPT是基于哪种AI模型架构开发的？,CNN（卷积神经网络）,RNN（循环神经网络）,Transformer,GAN（生成对抗网络）,C
4,以下哪个不是知名的AI图像生成模型？,DALL-E,Midjourney,Stable Diffusion,AlexNet,D
5,大语言模型（LLM）主要用于处理什么类型的任务？,图像识别,语音识别,自然语言处理,视频编辑,C
6,"AIGC技术中的""提示工程""（Prompt Engineering）是指什么？",设计电脑硬件的技术,编写能引导AI生成特定输出的提示语的技术,提示用户完成任务的界面设计,加速AI模型训练的技术,B
7,下列哪项不是生成式AI面临的主要挑战？,版权问题,内容真实性,伦理考量,硬件兼容性,D
```

### 用户数据

用户数据位于 `data/users.csv`，包含用户ID、密码、姓名、角色和班级信息。

```csv
S1001,pass1,张三,student,一班
T1002,pass2,李老师,admin,教工
```

### 1. 后端设置

```bash
# 进入后端目录
cd server

# 安装依赖
pip install flask flask_cors pandas

# 初始化数据库（首次运行需要），务必先配置好用户数据和题目格式。
python setup_db.py

# 启动Flask服务器
flask run
```

服务器将在 http://localhost:5000 上运行。

### 2. 前端设置

```bash
# 进入前端目录
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:5173 上运行。
