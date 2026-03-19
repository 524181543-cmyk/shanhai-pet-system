# 🚀 GitHub + Railway 完整部署流程

## 第一步：创建GitHub仓库

### 方式A：在GitHub网站创建（推荐）

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `shanhai-pet-system`（或其他你喜欢的名字）
   - **Description**: 山海经班级宠物积分系统
   - **Public** 或 **Private**: 选择Public（Railway需要访问）
   - ❌ **不要勾选** "Add a README file"（我们已经有了）
   - ❌ **不要勾选** ".gitignore"（我们已经有了）
3. 点击 **"Create repository"**

### 方式B：使用GitHub CLI（如果已安装gh命令）

```bash
gh repo create shanhai-pet-system --public --source=. --remote=origin --push
```

---

## 第二步：推送代码到GitHub

创建好GitHub仓库后，复制仓库地址（类似 `https://github.com/你的用户名/shanhai-pet-system.git`）

然后运行以下命令：

```bash
# 添加远程仓库（替换为你的实际地址）
git remote add origin https://github.com/你的用户名/shanhai-pet-system.git

# 推送代码
git push -u origin main
```

---

## 第三步：在Railway创建项目

### 3.1 登录Railway

访问 https://railway.app/ 并用GitHub账号登录

### 3.2 授权Railway访问你的GitHub

首次使用需要授权Railway访问你的GitHub仓库

### 3.3 创建新项目

1. 在Railway首页点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 找到并选择 `shanhai-pet-system` 仓库
4. 点击 **"Deploy Now"**

### 3.4 等待部署（2-3分钟）

Railway会显示部署日志：
- ✅ Installing dependencies...
- ✅ Building application...
- ✅ Starting deployment...

---

## 第四步：获取公网地址

### 4.1 部署完成后

在Railway项目页面：
1. 点击你的服务名称
2. 点击 **"Settings"** 标签
3. 找到 **"Domains"** 部分
4. 点击 **"Generate Domain"**

### 4.2 你会得到一个地址

类似：
```
https://shanhai-pet-system-production.up.railway.app
```

**这就是你的公网访问地址！** 🎉

---

## 🎊 完成！

现在你可以：
- ✅ 访问你的山海经宠物系统
- ✅ 分享地址给班级同学
- ✅ 学生可以注册、领养宠物、积累积分

---

## 🔧 常见问题

### Q: 推送代码时提示"fatal: 'origin' already exists"
**A:** 运行以下命令更新远程地址：
```bash
git remote set-url origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

### Q: Railway找不到我的仓库
**A:**
1. 确保仓库是Public（公开）
2. 在Railway设置中重新授权GitHub
3. 刷新页面重试

### Q: 部署失败
**A:**
1. 点击部署日志查看错误信息
2. 确认所有文件都已推送
3. 运行 `python scripts/deploy_check.py` 检查

---

## 📱 下一步

部署成功后：
1. 在浏览器访问你的地址
2. 测试所有功能是否正常
3. 分享地址给学生开始使用！

---

**需要帮助？** 随时告诉我！ 🚀
