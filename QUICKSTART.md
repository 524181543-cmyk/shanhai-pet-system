# 🚀 快速部署到Railway

## 一键部署步骤

### 1️⃣ 准备GitHub仓库

首先需要将代码推送到GitHub：

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "feat: 山海经班级宠物积分系统"

# 添加远程仓库（替换为你的GitHub地址）
git remote add origin https://github.com/你的用户名/pet-system.git

# 推送
git push -u origin main
```

### 2️⃣ 登录Railway

访问 https://railway.app/ 并用GitHub账号登录

### 3️⃣ 创建新项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择你的仓库
4. 点击 **"Deploy Now"**

### 4️⃣ 等待部署完成（约2-3分钟）

Railway会自动：
- ✅ 检测Python项目
- ✅ 安装依赖
- ✅ 启动应用

### 5️⃣ 获取访问地址

部署完成后，Railway会给你一个公网地址：
```
https://你的项目名-production.up.railway.app
```

点击这个地址即可访问你的山海经宠物系统！

---

## 🎉 完成！

现在你可以：
- 分享这个地址给班级同学
- 学生可以注册账号、领养宠物、积累积分
- 查看排行榜和宠物进化

---

## 🔧 可选：绑定自定义域名

如果你想使用自己的域名（如 `pet.yourschool.com`）：

1. 在Railway项目中点击 **Settings**
2. 找到 **Domains** 部分
3. 点击 **Add Custom Domain**
4. 按照提示配置DNS记录

---

## 💡 提示

- Railway提供$5/月的免费额度
- 小型班级应用完全够用
- 自动扩容和负载均衡
- 支持自定义域名和SSL证书

---

**需要帮助？** 查看 `DEPLOY.md` 获取详细文档
