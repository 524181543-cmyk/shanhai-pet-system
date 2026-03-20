# 🏗️ Render平台部署完整指南

## 📋 准备工作（已完成✅）

- ✅ 代码已打包：`shanhai-pet-system.tar.gz`
- ✅ 配置文件已创建：`render.yaml`、`build.sh`、`start.sh`
- ✅ 所有依赖已在 `requirements.txt` 中

---

## 🚀 部署步骤（5步完成）

### 第1步：注册Render账号

1. 打开浏览器，访问：**https://dashboard.render.com/**

2. 选择登录方式（任选其一）：
   - ✅ **Google账号** - 推荐，最简单
   - ✅ GitLab账号
   - ✅ Email注册

3. 授权并完成登录

---

### 第2步：创建新的Web Service

1. 登录后，在Dashboard页面点击 **"New +"** 按钮

2. 选择 **"Web Service"**

3. 在 **"Create a new Web Service"** 页面：
   - 找到 **"Deploy from a tarball"** 选项
   - 点击选择（不需要Git仓库）

---

### 第3步：上传代码包

1. 点击 **"Upload a tarball"**

2. 选择文件：
   - 点击 **"Choose File"** 按钮
   - 找到并选择 `shanhai-pet-system.tar.gz`
   - 点击 **"Upload"**

3. 等待上传完成（约30秒）

---

### 第4步：配置Web Service

填写以下信息：

```
Name: shanhai-pet-system
   （或你喜欢的名字，这将影响你的域名）

Environment: Python 3
   （自动检测或选择Python）

Region: Oregon (US West)
   （或Singapore，选择离中国近的）

Branch: main
   （默认即可）

Build Command:
   pip install -r requirements.txt

Start Command:
   python src/main.py -m http -p $PORT

Instance Type: Free
   （免费套餐）
```

**高级设置（点击"Advanced"展开）：**

```
Environment Variables:
   无需添加（系统会自动设置PORT）
```

---

### 第5步：开始部署

1. 确认所有信息无误

2. 点击 **"Create Web Service"** 按钮

3. 等待部署（约3-5分钟）

---

## 📊 部署过程

你会看到部署日志：

```
==> Cloning from tarball...
==> Installing Python...
==> Installing dependencies...
   Installing collected packages: ...
==> Build completed successfully!
==> Starting deployment...
==> Service is live at https://shanhai-pet-system.onrender.com
```

---

## 🎉 部署成功！

### 获取你的公网地址

部署完成后，你会看到：

**你的域名：**
```
https://shanhai-pet-system.onrender.com
```

**或者自定义名称：**
```
https://你的服务名.onrender.com
```

### 测试访问

1. 点击Render提供的URL
2. 你应该能看到山海经宠物系统的首页
3. 测试注册、领养宠物等功能

---

## 🔧 常见问题

### Q: 部署失败怎么办？

**查看日志：**
1. 在Render项目页面点击 **"Logs"** 标签
2. 查看错误信息
3. 常见错误：
   - 依赖安装失败：检查 `requirements.txt`
   - 启动命令错误：确认命令格式正确

### Q: 应用无法访问？

**检查服务状态：**
1. 确认状态显示为 **"Live"**
2. 检查健康检查路径：`/health`
3. 查看日志是否有错误

### Q: 如何更新代码？

**重新部署：**
1. 重新打包代码
2. 在Render项目页面点击 **"Manual Deploy"**
3. 选择 **"Deploy a tarball"**
4. 上传新的压缩包

### Q: 如何绑定自定义域名？

**配置域名：**
1. 在项目页面点击 **"Settings"**
2. 滚动到 **"Custom Domains"**
3. 点击 **"Add Custom Domain"**
4. 按提示配置DNS记录

---

## 💡 Render免费套餐说明

### 包含内容
- ✅ 750小时/月免费运行时间
- ✅ 自动SSL证书
- ✅ 自动扩容
- ✅ 健康检查
- ✅ 日志查看

### 限制
- ⚠️ 服务会在15分钟无访问后休眠
- ⚠️ 休眠后首次访问需要等待约30秒唤醒
- ⚠️ 适合中小型应用

### 如需升级
- 💰 $7/月起
- 不休眠
- 更高性能

---

## 🎯 部署后检查清单

- [ ] 能访问主页
- [ ] 能注册用户
- [ ] 能查看宠物类型
- [ ] 能领养宠物
- [ ] 能添加积分
- [ ] 能查看排行榜

---

## 📞 需要帮助？

如果遇到问题：
1. 查看Render日志
2. 运行本地测试：`python scripts/deploy_check.py`
3. 检查配置文件是否正确

---

## 🎊 完成！

**你的山海经班级宠物积分系统已成功部署！**

**公网地址：** `https://你的服务名.onrender.com`

**现在可以：**
- ✅ 分享地址给学生
- ✅ 开始使用系统
- ✅ 学生注册领养宠物
- ✅ 积累积分进化

---

**祝部署顺利！** 🚀
