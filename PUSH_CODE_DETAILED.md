# 🚀 推送代码到GitHub - 超详细步骤

## 方式一：网页上传（最简单，无需命令行）⭐推荐

### 第一步：准备文件

在你当前的项目中，我帮你列出所有需要上传的文件位置：

```bash
# 运行这个命令查看所有文件
ls -la
```

你需要找到这些文件：
- `src` 文件夹
- `config` 文件夹  
- `Procfile` 文件
- `runtime.txt` 文件
- `requirements.txt` 文件
- `railway.json` 文件
- `nixpacks.toml` 文件
- `.gitignore` 文件
- `README.md` 文件

---

### 第二步：访问你的GitHub仓库

1. 打开浏览器
2. 访问：**https://github.com/524181543-cmyk/shanhai-pet-system**
3. 如果需要，登录你的GitHub账号

---

### 第三步：开始上传

#### 方法A：拖拽上传（推荐）✅

1. 在GitHub仓库页面，找到并点击 **"uploading an existing file"** 链接
   - 或点击 **"Add file"** 按钮，选择 **"Upload files"**

2. **打开你的项目文件夹**（在你电脑上）

3. **拖拽以下文件到网页**：

   **📁 第一次拖拽：src文件夹**
   - 找到 `src` 文件夹
   - 整个拖到网页上传区域

   **📁 第二次拖拽：config文件夹**
   - 找到 `config` 文件夹
   - 拖到网页上传区域

   **📄 第三次拖拽：配置文件**
   - 找到并拖拽以下文件：
     - `Procfile`
     - `runtime.txt`
     - `requirements.txt`
     - `railway.json`
     - `nixpacks.toml`
     - `.gitignore`
     - `README.md`

4. **填写提交信息**
   - 在 "Commit changes" 下方的输入框填写：
     ```
     feat: 山海经班级宠物积分系统
     ```
   - 选择 **"Commit directly to the main branch"**（直接提交到main分支）

5. **点击绿色的 "Commit changes" 按钮**

---

#### 方法B：逐个创建文件（如果方法A不行）

**创建 Procfile：**

1. 点击 **"Add file"** → **"Create new file"**
2. 在文件名输入框输入：`Procfile`
3. 在内容区域输入：
   ```
   web: python src/main.py -m http -p $PORT
   ```
4. 点击绿色 **"Commit new file"** 按钮

**创建 runtime.txt：**

1. 再次点击 **"Add file"** → **"Create new file"**
2. 文件名输入：`runtime.txt`
3. 内容输入：
   ```
   python-3.12.3
   ```
4. 点击 **"Commit new file"**

**上传 requirements.txt：**

1. 点击 **"Add file"** → **"Upload files"**
2. 选择你的 `requirements.txt` 文件
3. 点击 **"Commit changes"**

**重复以上步骤上传其他文件...**

---

## 方式二：使用Git命令行（如果你会用Git）

### 如果你已经安装了Git

打开终端（Terminal），进入项目目录，运行：

```bash
# 1. 初始化Git仓库（如果还没有）
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "feat: 山海经班级宠物积分系统"

# 4. 添加远程仓库
git remote add origin https://github.com/524181543-cmyk/shanhai-pet-system.git

# 5. 推送到GitHub
git push -u origin main
```

### 如果提示需要认证

#### 方法1：使用Personal Access Token

1. **创建Token**
   - 访问：https://github.com/settings/tokens/new
   - Note填写：`shanhai-pet-system`
   - Expiration选择：`90 days` 或更长
   - 勾选：**"repo"**（所有repo相关选项）
   - 点击底部绿色 **"Generate token"** 按钮
   - **立即复制token**（只显示一次！）

2. **使用Token推送**
   ```bash
   git push https://YOUR_TOKEN@github.com/524181543-cmyk/shanhai-pet-system.git main
   ```
   把 `YOUR_TOKEN` 替换为你复制的token

   例如：
   ```bash
   git push https://ghp_xxxxxxxxxxxx@github.com/524181543-cmyk/shanhai-pet-system.git main
   ```

#### 方法2：使用GitHub CLI（如果已安装gh命令）

```bash
# 登录GitHub
gh auth login

# 推送代码
git push -u origin main
```

---

## 方式三：使用GitHub Desktop（图形界面工具）

### 第一步：安装GitHub Desktop

1. 访问：https://desktop.github.com/
2. 下载并安装
3. 打开GitHub Desktop
4. 登录你的GitHub账号

### 第二步：添加本地仓库

1. 点击 **"File"** → **"Add local repository"**
2. 选择你的项目文件夹
3. 点击 **"Add repository"**

### 第三步：推送到GitHub

1. 点击 **"Publish repository"**
2. 取消勾选 **"Keep this code private"**（保持公开）
3. 点击 **"Publish repository"**

---

## ✅ 检查是否推送成功

### 访问你的仓库

打开：**https://github.com/524181543-cmyk/shanhai-pet-system**

你应该能看到所有文件！

### 必需文件检查清单

- [ ] `src/` 文件夹存在
- [ ] `config/` 文件夹存在
- [ ] `Procfile` 文件存在
- [ ] `runtime.txt` 文件存在
- [ ] `requirements.txt` 文件存在
- [ ] `railway.json` 文件存在

---

## 🆘 常见问题

### Q: 提示"fatal: 'origin' already exists"
**A:** 运行这个命令更新地址：
```bash
git remote set-url origin https://github.com/524181543-cmyk/shanhai-pet-system.git
git push -u origin main
```

### Q: 提示"fatal: could not read Username"
**A:** 需要认证，使用Personal Access Token方法

### Q: 文件太大无法上传
**A:** GitHub单文件限制100MB，可以使用Git命令行推送

### Q: 找不到"uploading an existing file"链接
**A:** 确保仓库已经创建，点击 **"Add file"** → **"Upload files"**

---

## 📞 下一步

**推送成功后，告诉我"推送完成"，我会指导你：**

1. 在Railway创建项目
2. 部署应用
3. 获取公网访问地址

**整个过程只需要2-3分钟！** 🚀
