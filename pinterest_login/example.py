"""Pinterest登录工具使用示例。"""

import os
import asyncio
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from pinterest_login_tool import PinterestLoginTool


async def main():
    """主函数示例。"""
    
    # 确保设置了OpenAI API密钥
    if not os.getenv('OPENAI_API_KEY'):
        print("请设置OPENAI_API_KEY环境变量")
        return
    
    # 创建Pinterest登录工具
    pinterest_tool = PinterestLoginTool()
    
    # 示例1：基本登录
    print("=== 示例1：基本登录 ===")
    result1 = pinterest_tool._run(
        username="your_username@email.com",  # 替换为实际的用户名
        password="your_password",            # 替换为实际的密码
        headless=True,                       # 无头模式
        timeout=30                           # 30秒超时
    )
    print(f"登录结果1：{result1}")
    
    # 示例2：有头模式登录（可以看到浏览器界面）
    print("\n=== 示例2：有头模式登录 ===")
    result2 = pinterest_tool._run(
        username="your_username@email.com",  # 替换为实际的用户名
        password="your_password",            # 替换为实际的密码
        headless=False,                      # 有头模式，可以看到浏览器
        timeout=60                           # 60秒超时
    )
    print(f"登录结果2：{result2}")


def crewai_example():
    """在CrewAI中使用Pinterest登录工具的示例。"""
    
    from crewai import Agent, Task, Crew
    
    # 创建Pinterest登录工具
    pinterest_tool = PinterestLoginTool()
    
    # 创建社交媒体管理员代理
    social_media_agent = Agent(
        role='社交媒体管理员',
        goal='管理和维护Pinterest账号',
        backstory='''
        你是一个专业的社交媒体管理员，具有丰富的Pinterest平台运营经验。
        你的职责是帮助用户管理Pinterest账号，包括登录、发布内容、管理看板等。
        你总是确保操作的安全性和有效性。
        ''',
        tools=[pinterest_tool],
        verbose=True
    )
    
    # 创建登录任务
    login_task = Task(
        description='''
        使用提供的账号信息登录Pinterest：
        - 用户名：your_username@email.com
        - 密码：your_password
        
        请确保登录成功，并报告登录状态。
        如果遇到任何问题，请详细说明。
        ''',
        agent=social_media_agent,
        expected_output="详细的登录结果报告，包括是否成功以及任何遇到的问题。"
    )
    
    # 创建团队并执行任务
    crew = Crew(
        agents=[social_media_agent],
        tasks=[login_task],
        verbose=True
    )
    
    # 执行任务
    print("=== CrewAI团队执行Pinterest登录任务 ===")
    result = crew.kickoff()
    print(f"团队执行结果：{result}")


if __name__ == "__main__":
    print("Pinterest登录工具示例")
    print("=" * 50)
    
    # 运行基本示例
    asyncio.run(main())
    
    print("\n" + "=" * 50)
    
    # 运行CrewAI示例
    try:
        crewai_example()
    except ImportError:
        print("CrewAI未安装，跳过CrewAI示例")
        print("安装命令：pip install crewai")
    
    print("\n示例执行完成！")
    print("\n注意：")
    print("1. 请将示例中的用户名和密码替换为实际的Pinterest账号信息")
    print("2. 确保已设置OPENAI_API_KEY环境变量")
    print("3. 首次运行可能需要下载浏览器，请耐心等待")
