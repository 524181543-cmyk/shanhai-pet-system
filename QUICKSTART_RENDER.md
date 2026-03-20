# ⚡ Render快速部署（5分钟）

## 📦 已准备好

✅ 代码包：`shanhai-pet-system.tar.gz` (52KB)
✅ 配置文件：`render.yaml`、`build.sh`、`start.sh`
✅ 依赖清单：`requirements.txt`

---

## 🎯 5步部署

### 1️⃣ 访问Render
打开：https://dashboard.render.com/
用Google账号登录

### 2️⃣ 创建服务
点击 **"New +"** → 选择 **"Web Service"**

### 3️⃣ 上传代码
- 选择 **"Deploy from a tarball"**
- 上传 `shanhai-pet-system.tar.gz`

### 4️⃣ 配置服务
```
Name: shanhai-pet-system
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python src/main.py -m http -p $PORT
Instance: Free
```

### 5️⃣ 开始部署
点击 **"Create Web Service"**
等待3-5分钟

---

## 🎉 完成！

获得地址：`https://shanhai-pet-system.onrender.com`

---

详细步骤请查看：`RENDER_DEPLOY_GUIDE.md`
