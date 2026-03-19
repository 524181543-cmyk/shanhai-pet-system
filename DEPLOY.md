# 🚀 Railway部署指南

## 山海经班级宠物积分系统 - Railway部署

本指南将帮助你在Railway上免费部署山海经班级宠物积分系统。

---

## 📋 部署前准备

### 1. 注册Railway账号
访问 [Railway.app](https://railway.app/) 并使用GitHub账号登录

### 2. 准备GitHub仓库
你需要将代码推送到GitHub仓库

---

## 🚀 快速部署（推荐）

### 方式一：一键部署按钮

即将为你生成一键部署按钮...

### 方式二：手动部署步骤

#### 步骤1：推送代码到GitHub

```bash
# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "feat: 山海经班级宠物积分系统"

# 添加远程仓库（替换为你的GitHub仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送到GitHub
git push -u origin main
```

#### 步骤2：在Railway创建项目

1. 登录 [Railway.app](https://railway.app/)
2. 点击 **"New Project"**
3. 选择 **"Deploy from GitHub repo"**
4. 选择你的GitHub仓库
5. Railway会自动检测到Python项目并开始部署

#### 步骤3：等待部署完成

Railway会自动：
- 检测Python版本（使用runtime.txt）
- 安装依赖（使用requirements.txt）
- 启动应用（使用Procfile）

部署完成后，你会得到一个类似这样的公网地址：
```
https://你的项目名-production.up.railway.app
```

---

## 🔧 高级配置（可选）

### 配置自定义域名

1. 在Railway项目设置中点击 **"Settings"**
2. 找到 **"Domains"** 部分
3. 点击 **"Generate Domain"** 或添加自定义域名

### 配置环境变量

如果你的应用需要额外的环境变量：

1. 在Railway项目页面点击 **"Variables"**
2. 添加需要的环境变量，例如：
   - `PORT`: Railway会自动设置
   - 其他数据库连接字符串等

---

## 📊 监控和日志

### 查看实时日志
1. 在Railway项目页面点击 **"Deployments"**
2. 选择最新的部署
3. 点击 **"View Logs"**

### 监控应用状态
Railway提供：
- 实时日志
- 性能监控
- 自动重启（如果应用崩溃）

---

## 💰 费用说明

Railway提供：
- **免费额度**：每月$5的免费额度
- **试用期间**：500小时免费运行时间
- 对于小型应用，免费额度通常足够

---

## 🔍 故障排查

### 部署失败

**检查日志：**
```bash
# 在Railway的部署页面查看详细日志
```

**常见问题：**

1. **依赖安装失败**
   - 检查requirements.txt中的包名是否正确
   - 确保Python版本兼容（runtime.txt）

2. **端口问题**
   - 确保使用 `$PORT` 环境变量
   - 代码已自动处理

3. **启动失败**
   - 检查Procfile格式是否正确
   - 查看启动命令是否正确

### 应用无法访问

1. 检查Railway部署状态是否为"Success"
2. 确认域名是否正确配置
3. 查看应用日志是否有错误

---

## 📝 部署文件说明

项目中包含以下Railway部署所需文件：

- **`Procfile`**: 告诉Railway如何启动应用
- **`runtime.txt`**: 指定Python版本
- **`railway.json`**: Railway配置文件
- **`nixpacks.toml`**: 构建配置
- **`.railwayignore`**: 部署时忽略的文件

---

## 🎉 部署成功后

访问你的应用地址，你应该能看到：
- 🏠 山海经班级宠物积分系统首页
- 🐉 10种山海经神兽可供选择
- 🎮 完整的积分和进化系统

---

## 🆘 需要帮助？

如果遇到问题：
1. 查看Railway官方文档：https://docs.railway.app/
2. 检查应用日志
3. 联系我获取支持

---

## 🔄 更新部署

当你修改代码后：

```bash
git add .
git commit -m "更新说明"
git push
```

Railway会自动检测到推送并重新部署！

---

**祝你部署顺利！** 🎊
