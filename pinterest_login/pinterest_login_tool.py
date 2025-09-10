"""Pinterest Login Tool using browser-use library."""

import asyncio
import os
from typing import Any, Optional, Type, List
import logging

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from config import PinterestConfig, get_openai_api_key, get_debug_mode


class PinterestLoginToolSchema(BaseModel):
    """Input schema for Pinterest Login Tool."""
    
    username: str = Field(..., description="Pinterest账号用户名或邮箱")
    password: str = Field(..., description="Pinterest账号密码")
    headless: bool = Field(default=True, description="是否以无头模式运行浏览器")
    timeout: int = Field(default=30, description="登录超时时间（秒）")


class PinterestLoginTool(BaseTool):
    """Pinterest登录工具，基于browser-use库实现自动化登录功能。
    
    该工具可以自动打开Pinterest网站，输入用户提供的账号密码进行登录，
    并返回登录结果状态。
    
    Args:
        openai_api_key: OpenAI API密钥，用于browser-use库的AI功能
    """
    
    name: str = "Pinterest登录工具"
    description: str = (
        "使用browser-use库自动登录Pinterest网站。"
        "需要提供Pinterest账号的用户名/邮箱和密码。"
        "工具会自动打开浏览器，导航到Pinterest登录页面，"
        "填写登录信息并完成登录过程。"
    )
    args_schema: Type[BaseModel] = PinterestLoginToolSchema
    package_dependencies: List[str] = ["browser-use", "playwright"]
    
    def __init__(self, openai_api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        
        try:
            openai_api_key = openai_api_key or get_openai_api_key()
            object.__setattr__(self,"openai_api_key", openai_api_key)   
        except ValueError as e:
            raise ValueError(str(e))
        
        # 配置日志
        #self.logger = logging.getLogger(__name__)
        object.__setattr__(self,"logger", logging.getLogger(__name__))
        if get_debug_mode():
            self.logger.setLevel(logging.DEBUG)
        
    def _run(self, **kwargs: Any) -> str:
        """执行Pinterest登录操作。
        
        Returns:
            str: 登录结果描述
        """
        username = kwargs.get("username")
        password = kwargs.get("password")
        headless = kwargs.get("headless", True)
        timeout = kwargs.get("timeout", 30)
        
        if not username or not password:
            return "错误：必须提供用户名和密码"
        
        # 验证凭据格式
        is_valid, error_msg = PinterestConfig.validate_credentials(username, password)
        if not is_valid:
            return f"错误：{error_msg}"
        
        try:
            # 运行异步登录操作
            result = asyncio.run(self._async_login(username, password, headless, timeout))
            return result
        except Exception as e:
            error_msg = f"Pinterest登录失败：{str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    async def _async_login(self, username: str, password: str, headless: bool, timeout: int) -> str:
        """异步执行Pinterest登录。
        
        Args:
            username: 用户名或邮箱
            password: 密码
            headless: 是否无头模式
            timeout: 超时时间
            
        Returns:
            str: 登录结果
        """
        try:
            from browser_use import Agent
            from browser_use.llm import ChatOpenAI
            
            # 初始化LLM
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=self.openai_api_key,
                temperature=0.1,
                base_url=os.getenv('OPENAI_API_BASE', 'https://api.apiyi.com/v1')
            )
            
            # 获取浏览器配置
            browser_config = PinterestConfig.get_browser_config(headless=headless, timeout=timeout)
            
            # 获取登录任务描述
            task_description = PinterestConfig.get_login_task(username, password)
            
            # 创建浏览器代理
            agent = Agent(
                task=task_description,
                llm=llm,
                browser_config=browser_config
            )
            
            # 执行登录任务
            result = await agent.run()
            
            # 分析结果
            if result and "成功" in str(result):
                return f"Pinterest登录成功！用户：{username}"
            elif result and ("失败" in str(result) or "错误" in str(result)):
                return f"Pinterest登录失败：{result}"
            else:
                return f"Pinterest登录完成，结果：{result}"
                
        except ImportError as e:
            return f"缺少必要的依赖包：{str(e)}。请安装browser-use和langchain-openai。"
        except Exception as e:
            return f"登录过程中发生错误：{str(e)}"
    
    async def close(self):
        """清理资源。"""
        # 如果需要清理浏览器资源，可以在这里实现
        pass


# 便捷函数
def create_pinterest_login_tool(openai_api_key: Optional[str] = None) -> PinterestLoginTool:
    """创建Pinterest登录工具实例。
    
    Args:
        openai_api_key: OpenAI API密钥
        
    Returns:
        PinterestLoginTool: 工具实例
    """
    return PinterestLoginTool(openai_api_key=openai_api_key)
