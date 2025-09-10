# Pinterest登录工具

基于browser-use库实现的Pinterest自动登录工具，适用于CrewAI框架。

## 功能特性

- 🤖 **智能登录**：使用AI驱动的浏览器自动化技术
- 🔒 **安全可靠**：支持处理验证码和安全验证
- ⚙️ **可配置**：支持有头/无头模式，自定义超时时间
- 📊 **详细反馈**：提供详细的登录状态和错误信息

## 安装依赖

```bash
pip install browser-use langchain-openai playwright
```

安装Playwright浏览器：
```bash
playwright install chromium
```

## 环境配置

设置OpenAI API密钥：
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

## 使用方法

### 在CrewAI中使用

```python
from crewai import Agent, Task, Crew
from backend.crewai.tools.pinterest_login import PinterestLoginTool

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
crew = Crew(
    agents=[agent],
    tasks=[task]
)

result = crew.kickoff()
```

### 直接使用工具

```python
from backend.crewai.tools.pinterest_login import PinterestLoginTool

# 创建工具实例
tool = PinterestLoginTool(openai_api_key="your-openai-api-key")

# 执行登录
result = tool._run(
    username="your_username@email.com",
    password="your_password",
    headless=True,
    timeout=30
)

print(result)
```

## 参数说明

- `username` (str): Pinterest账号用户名或邮箱地址
- `password` (str): Pinterest账号密码
- `headless` (bool, 可选): 是否以无头模式运行浏览器，默认为True
- `timeout` (int, 可选): 登录操作超时时间（秒），默认为30秒

## 返回值

工具会返回登录操作的详细结果：

- **成功**：`"Pinterest登录成功！用户：username"`
- **失败**：`"Pinterest登录失败：具体错误信息"`
- **错误**：`"登录过程中发生错误：错误详情"`

## 注意事项

1. **API密钥**：确保已正确设置OpenAI API密钥
2. **网络环境**：确保能够正常访问Pinterest网站
3. **账号安全**：建议使用测试账号，避免使用重要的个人账号
4. **频率限制**：避免频繁登录，以免触发Pinterest的安全机制
5. **验证码处理**：工具会尝试处理验证码，但复杂的验证可能需要人工干预

## 故障排除

### 常见问题

1. **依赖包缺失**
   ```bash
   pip install browser-use langchain-openai playwright
   playwright install chromium
   ```

2. **API密钥错误**
   - 检查OPENAI_API_KEY环境变量是否正确设置
   - 确认API密钥有效且有足够的配额

3. **登录失败**
   - 检查用户名和密码是否正确
   - 确认Pinterest账号状态正常
   - 尝试增加timeout参数值

4. **浏览器启动失败**
   - 确保已安装Playwright浏览器
   - 检查系统权限和防火墙设置

## 技术原理

该工具基于以下技术栈：

- **browser-use**：AI驱动的浏览器自动化库
- **Playwright**：跨平台浏览器自动化引擎
- **OpenAI GPT**：提供智能决策和页面理解能力
- **CrewAI BaseTool**：标准化的工具接口

工具通过AI理解Pinterest登录页面的结构，智能识别登录表单元素，并执行相应的操作序列来完成登录过程。
