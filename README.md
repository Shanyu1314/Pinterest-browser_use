# Pinterest-browser_use
利用browser-ues自动登录北美小红书（Pinterest），处理LLM大模型无法调用、使用梯子无法连接playwright浏览器等细节问题
# Pinterest登录工具 🎯

基于 `browser-use` 库实现的 Pinterest 自动登录工具，支持 CrewAI 框架。使用 AI 驱动的浏览器自动化技术，智能识别页面元素并完成登录操作。

## ✨ 功能特性

- 🤖 **AI驱动**：使用多模态大语言模型理解页面内容
- 🔒 **安全可靠**：支持验证码识别和安全验证处理
- 🌐 **多API支持**：兼容 OpenAI、OpenRouter、API易等多种API服务
- ⚙️ **高度可配置**：支持有头/无头模式、超时设置等
- 📊 **详细反馈**：提供完整的操作日志和状态反馈
- 🚀 **开箱即用**：提供快速启动脚本和交互式测试

## 🚀 快速开始

### 1. 环境准备

**创建虚拟环境（推荐）：**
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/macOS:
source .venv/bin/activate
```

### 2. 安装依赖

**使用腾讯云镜像（国内推荐）：**
```bash
pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple/
```

**或使用默认源：**
```bash
pip install -r requirements.txt
```

**安装 Playwright 浏览器：**
```bash
playwright install chromium
```

### 3. 配置API密钥

创建 `.env` 文件并配置你的API信息：

```env
# 使用 API易 (推荐，便宜稳定)
OPENAI_API_KEY=你的API易密钥
OPENAI_API_BASE=https://api.apiyi.com/v1

# 或使用 OpenRouter
OPENAI_API_KEY=你的OpenRouter密钥
OPENAI_API_BASE=https://openrouter.ai/api/v1

# 或使用 OpenAI 官方
OPENAI_API_KEY=你的OpenAI密钥
OPENAI_API_BASE=https://api.openai.com/v1
```

### 4. 运行测试

```bash
python quick_start.py
```

## 🔑 API服务推荐

### API易 - 推荐使用 ⭐
- **官网**: https://api.apiyi.com/v1
- **注册地址**: https://api.apiyi.com/register/?aff_code=2p9q
- **优势**: 
  - 💰 新用户注册送 $0.1 免费额度
  - 🚀 响应速度快，服务稳定
  - 💵 价格便宜，性价比高
  - 🌍 国内访问友好
- **邀请码**: `2p9q` (注册时使用可获得额外优惠)

### 其他支持的API服务
- **OpenRouter**: 多模型选择，支持多种开源模型
- **OpenAI**: 官方服务，质量最高但价格较贵

## 📦 依赖说明

项目依赖包列表（`requirements.txt`）：
```
browser-use==0.7.5
crewai==0.177.0
langchain-openai==0.3.32
playwright==1.55.0
pydantic==2.11.7
pydantic-settings==2.10.1
pydantic_core==2.33.2
python-dotenv==1.0.0
```

## 🎮 使用方法

### 方法一：交互式测试（推荐新手）

```bash
python quick_start.py
```

选择 "2. 交互式登录测试"，按提示输入Pinterest账号信息即可。

### 方法二：在 CrewAI 中使用

```python
from crewai import Agent, Task, Crew
from pinterest_login_tool import PinterestLoginTool

# 创建工具实例
pinterest_tool = PinterestLoginTool()

# 创建代理
agent = Agent(
    role='社交媒体管理员',
    goal='管理Pinterest账号',
    backstory='你是一个专业的社交媒体管理员，负责管理Pinterest账号。',
    tools=[pinterest_tool]
)

# 创建任务
task = Task(
    description='使用用户名"your_username"和密码"your_password"登录Pinterest',
    agent=agent
)

# 执行任务
crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

### 方法三：直接使用工具

```python
from pinterest_login_tool import PinterestLoginTool

# 创建工具实例
tool = PinterestLoginTool()

# 执行登录
result = tool._run(
    username="your_username@email.com",
    password="your_password",
    headless=False,  # 设为False可以看到浏览器操作过程
    timeout=30
)

print(result)
```

## ⚙️ 参数配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `username` | str | 必填 | Pinterest账号用户名或邮箱地址 |
| `password` | str | 必填 | Pinterest账号密码 |
| `headless` | bool | True | 是否以无头模式运行浏览器 |
| `timeout` | int | 30 | 登录操作超时时间（秒） |

## 🎯 支持的模型

**⚠️ 重要：必须使用支持视觉功能的多模态模型**

### 推荐模型：
- `gpt-4o-mini` ⭐ - OpenAI最新模型，性价比最高
- `gpt-4o` - 功能最强但价格较高
- `openai/gpt-4o-mini` - OpenRouter平台
- `google/gemini-flash-1.5` - Google多模态模型

### ❌ 不支持的模型：
- `gpt-oss-120b:free` - 纯文本模型，无法处理网页截图
- 其他纯文本模型

## 📊 返回值说明

工具执行后返回字符串，包含以下几种情况：

- ✅ **成功**: `"Pinterest登录成功！用户：username"`
- ❌ **失败**: `"Pinterest登录失败：具体错误信息"`
- ⚠️ **错误**: `"登录过程中发生错误：错误详情"`

## 🛠️ 故障排除

### 常见问题及解决方案

#### 1. 导入错误
```
attempted relative import with no known parent package
```
**解决方案**: 已在代码中修复，使用绝对导入

#### 2. 模型不支持图像输入
```
No endpoints found that support image input
```
**解决方案**: 更换为支持视觉的多模态模型（如 `gpt-4o-mini`）

#### 3. API密钥错误
```
Incorrect API key provided
```
**解决方案**: 
- 检查 `.env` 文件中的 `OPENAI_API_KEY` 是否正确
- 确认 `OPENAI_API_BASE` 指向正确的API端点

#### 4. 依赖包缺失
```
ModuleNotFoundError: No module named 'browser_use'
```
**解决方案**:
```bash
pip install -r requirements.txt
playwright install chromium
```

#### 5. 虚拟环境激活失败（Windows PowerShell）
```
execution of scripts is disabled on this system
```
**解决方案**:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🔧 技术架构

### 核心技术栈
- **browser-use**: AI驱动的浏览器自动化框架
- **Playwright**: 跨平台浏览器控制引擎  
- **多模态LLM**: 理解网页内容和执行决策
- **CrewAI**: 智能代理框架
- **Pydantic**: 数据验证和设置管理

### 工作原理
1. 🌐 打开Pinterest网站
2. 📸 截取网页截图
3. 🧠 AI分析页面结构和元素
4. 🎯 智能定位登录表单
5. ⌨️ 自动填写用户名和密码
6. 🖱️ 点击登录按钮
7. ✅ 验证登录状态

## 📝 版本更新日志

### v1.1.0 (最新)
- ✅ 修复了相对导入问题
- ✅ 添加多API服务支持（API易、OpenRouter）
- ✅ 优化了LLM模型兼容性
- ✅ 添加环境变量配置支持
- ✅ 改进错误处理和日志输出
- ✅ 添加快速启动脚本

### v1.0.0
- 🎉 初始版本发布
- 🤖 基础Pinterest登录功能
- 🔧 CrewAI集成支持

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 💬 支持与反馈

- 🐛 **Bug报告**: 请在 [Issues](../../issues) 中提交
- 💡 **功能建议**: 欢迎在 [Issues](../../issues) 中讨论
- 📧 **联系作者**: 通过GitHub Issues联系

## 🙏 致谢

- [browser-use](https://github.com/browser-use/browser-use) - 优秀的AI浏览器自动化库
- [CrewAI](https://github.com/joaomdmoura/crewAI) - 智能代理框架
- [Playwright](https://playwright.dev/) - 强大的浏览器自动化工具

---

⭐ 如果这个项目对你有帮助，请给个星标支持一下！

💰 **免费试用**: 使用邀请码 `2p9q` 在 [API易](https://api.apiyi.com/register/?aff_code=2p9q) 注册，获得 $0.1 免费额度！

