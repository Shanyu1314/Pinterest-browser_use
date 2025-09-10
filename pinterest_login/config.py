"""Pinterest登录工具配置文件。"""

import os
from typing import Dict, Any


class PinterestConfig:
    """Pinterest登录工具配置类。"""
    
    # Pinterest网站URL
    PINTEREST_URL = "https://www.pinterest.com"
    PINTEREST_LOGIN_URL = "https://www.pinterest.com/login/"
    
    # 默认配置
    DEFAULT_TIMEOUT = 30
    DEFAULT_HEADLESS = True
    DEFAULT_VIEWPORT = {"width": 1920, "height": 1080}
    
    # 浏览器配置
    BROWSER_CONFIG = {
        "headless": DEFAULT_HEADLESS,
        "timeout": DEFAULT_TIMEOUT * 1000,  # 转换为毫秒
        "viewport": DEFAULT_VIEWPORT,
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    
    # 登录相关的CSS选择器和XPath
    SELECTORS = {
        "login_button": "button[data-test-id='registerFormSubmitButton'], a[href='/login/']",
        "username_input": "input[id='email'], input[name='id'], input[type='email']",
        "password_input": "input[id='password'], input[name='password'], input[type='password']",
        "submit_button": "button[type='submit'], button[data-test-id='registerFormSubmitButton']",
        "error_message": ".error, .errorMessage, [data-test-id='error']",
        "success_indicator": "[data-test-id='header-profile'], .profileImage, .headerAvatar"
    }
    
    # 登录任务模板
    LOGIN_TASK_TEMPLATE = """
    请帮我登录Pinterest网站，具体步骤如下：
    1. 打开Pinterest网站 ({pinterest_url})
    2. 如果不在登录页面，点击登录按钮
    3. 输入用户名/邮箱：{username}
    4. 输入密码：{password}
    5. 点击登录按钮完成登录
    6. 等待页面加载，确认登录成功（检查是否跳转到主页或出现用户头像）
    
    注意事项：
    - 如果遇到验证码，请尝试识别并处理
    - 如果遇到"记住我"选项，可以勾选
    - 如果登录失败，请报告具体的错误信息
    - 最后确认登录状态并返回结果
    
    请返回登录是否成功的明确状态。
    """
    
    @classmethod
    def get_browser_config(cls, headless: bool = None, timeout: int = None) -> Dict[str, Any]:
        """获取浏览器配置。
        
        Args:
            headless: 是否无头模式
            timeout: 超时时间（秒）
            
        Returns:
            Dict[str, Any]: 浏览器配置字典
        """
        config = cls.BROWSER_CONFIG.copy()
        
        if headless is not None:
            config["headless"] = headless
            
        if timeout is not None:
            config["timeout"] = timeout * 1000  # 转换为毫秒
            
        return config
    
    @classmethod
    def get_login_task(cls, username: str, password: str) -> str:
        """获取登录任务描述。
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            str: 格式化的登录任务描述
        """
        return cls.LOGIN_TASK_TEMPLATE.format(
            pinterest_url=cls.PINTEREST_URL,
            username=username,
            password="*" * len(password)  # 隐藏密码显示
        )
    
    @classmethod
    def validate_credentials(cls, username: str, password: str) -> tuple[bool, str]:
        """验证登录凭据格式。
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            tuple[bool, str]: (是否有效, 错误信息)
        """
        if not username or not username.strip():
            return False, "用户名不能为空"
            
        if not password or not password.strip():
            return False, "密码不能为空"
            
        if len(password) < 6:
            return False, "密码长度至少为6位"
            
        # 简单的邮箱格式验证
        if "@" in username and "." in username:
            # 看起来像邮箱
            email_parts = username.split("@")
            if len(email_parts) != 2 or not email_parts[0] or not email_parts[1]:
                return False, "邮箱格式不正确"
                
        return True, ""


# 环境变量配置
def get_openai_api_key() -> str:
    """获取OpenAI API密钥。
    
    Returns:
        str: API密钥
        
    Raises:
        ValueError: 如果未设置API密钥
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError(
            "未找到OpenAI API密钥。请设置OPENAI_API_KEY环境变量。"
        )
    return api_key


def get_debug_mode() -> bool:
    """获取调试模式设置。
    
    Returns:
        bool: 是否启用调试模式
    """
    return os.getenv('PINTEREST_DEBUG', 'false').lower() in ('true', '1', 'yes')
