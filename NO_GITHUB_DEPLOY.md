# 🚀 无需GitHub的公网部署方案

## 🎯 三种简单方案

---

## 方案A：ngrok内网穿透 ⭐ **最简单推荐**

### 优点
- ✅ 无需任何账号注册
- ✅ 1分钟获得公网地址
- ✅ 完全免费使用
- ✅ 自动HTTPS加密

### 使用步骤

#### 方式1：一键启动（推荐）

```bash
./start_public.sh
```

这个脚本会自动：
1. 安装ngrok
2. 启动应用服务
3. 创建公网访问地址

#### 方式2：手动操作

```bash
# 1. 安装ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# 2. 启动应用
python src/main.py -m http -p 8000 &

# 3. 启动ngrok
ngrok http 8000
```

### 获取公网地址

运行后会显示类似这样的界面：
```
Session Status                online
Account                       未注册 (Plan: Free)
Version                       3.x.x

Forwarding                    https://a1b2c3d4.ngrok.io -> http://localhost:8000
```

**`https://a1b2c3d4.ngrok.io` 就是你的公网地址！**

### 使用限制
- 免费版每次启动地址会变化
- 如需固定地址，可免费注册ngrok账号

---

## 方案B：使用Render平台部署

### 优点
- ✅ 免费永久使用
- ✅ 固定域名
- ✅ 自动HTTPS
- ✅ 不需要GitHub

### 操作步骤

1. **打包代码**
```bash
tar -czf pet-system.tar.gz --exclude='.git' --exclude='.venv' --exclude='__pycache__' .
```

2. **访问Render**
   - 打开：https://dashboard.render.com/
   - 用Google或GitLab账号登录（不需要GitHub）

3. **创建Web Service**
   - 点击 "New" -> "Web Service"
   - 选择 "Upload a tarball"
   - 上传 `pet-system.tar.gz`

4. **配置服务**
   ```
   Name: shanhai-pet-system
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python src/main.py -m http -p $PORT
   ```

5. **部署**
   - 点击 "Create Web Service"
   - 等待5分钟部署完成

6. **获取地址**
   - 得到类似：`https://shanhai-pet-system.onrender.com`

---

## 方案C：PythonAnywhere部署

### 优点
- ✅ 专为Python设计
- ✅ 免费套餐
- ✅ 简单易用

### 操作步骤

1. **注册账号**
   - 访问：https://www.pythonanywhere.com/
   - 免费注册

2. **上传代码**
   - 在"Files"标签页上传代码
   - 或使用git clone（支持其他git服务器）

3. **创建Web应用**
   - "Web"标签页 -> "Add a new web app"
   - 选择Python版本：3.12
   - 设置入口文件：`src/main.py`

4. **配置WSGI**
   ```python
   import sys
   sys.path.insert(0, '/home/你的用户名/pet-system/src')
   from main import app as application
   ```

5. **访问地址**
   - `https://你的用户名.pythonanywhere.com`

---

## 💡 我的推荐

根据你的情况，我推荐：

### 立即使用：**方案A (ngrok)**
- 最快最简单
- 现在就能获得公网地址
- 适合临时使用或测试

### 长期使用：**方案B (Render)**
- 完全免费
- 固定域名
- 更稳定可靠

---

## 🚀 立即开始

### 选择方案A（ngrok）

运行以下命令：

```bash
./start_public.sh
```

几分钟后你就能得到一个公网地址！

---

## ❓ 常见问题

**Q: ngrok地址每次都会变吗？**
A: 免费版是的。如需固定地址，可以：
- 免费注册ngrok账号
- 或使用Render等平台

**Q: 哪个方案最稳定？**
A: Render平台最稳定，适合长期使用

**Q: 需要花钱吗？**
A: 所有推荐方案都有免费选项，足够班级使用

**Q: 学生能随时访问吗？**
A: 是的，所有方案都提供24小时访问

---

## 📞 需要帮助？

告诉我你想使用哪个方案，我会帮你完成部署！
