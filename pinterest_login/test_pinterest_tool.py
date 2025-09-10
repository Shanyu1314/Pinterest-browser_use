"""Pinterest登录工具测试文件。"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from pinterest_login_tool import PinterestLoginTool, PinterestLoginToolSchema
from config import PinterestConfig


class TestPinterestLoginTool(unittest.TestCase):
    """Pinterest登录工具测试类。"""
    
    def setUp(self):
        """测试前准备。"""
        # 模拟API密钥
        os.environ['OPENAI_API_KEY'] = 'test-api-key'
        self.tool = PinterestLoginTool()
    
    def tearDown(self):
        """测试后清理。"""
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
    
    def test_tool_initialization(self):
        """测试工具初始化。"""
        self.assertEqual(self.tool.name, "Pinterest登录工具")
        self.assertIn("Pinterest", self.tool.description)
        self.assertEqual(self.tool.args_schema, PinterestLoginToolSchema)
    
    def test_tool_initialization_without_api_key(self):
        """测试没有API密钥时的初始化。"""
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        with self.assertRaises(ValueError) as context:
            PinterestLoginTool()
        
        self.assertIn("OpenAI API密钥", str(context.exception))
    
    def test_schema_validation(self):
        """测试输入参数验证。"""
        # 有效参数
        valid_data = {
            "username": "test@example.com",
            "password": "testpassword123",
            "headless": True,
            "timeout": 30
        }
        schema = PinterestLoginToolSchema(**valid_data)
        self.assertEqual(schema.username, "test@example.com")
        self.assertEqual(schema.password, "testpassword123")
        self.assertTrue(schema.headless)
        self.assertEqual(schema.timeout, 30)
    
    def test_missing_required_parameters(self):
        """测试缺少必需参数。"""
        result = self.tool._run()
        self.assertIn("错误", result)
        self.assertIn("用户名和密码", result)
    
    @patch('pinterest_login_tool.asyncio.run')
    def test_run_with_valid_parameters(self, mock_asyncio_run):
        """测试使用有效参数运行。"""
        mock_asyncio_run.return_value = "登录成功"
        
        result = self.tool._run(
            username="test@example.com",
            password="testpassword123",
            headless=True,
            timeout=30
        )
        
        mock_asyncio_run.assert_called_once()
        self.assertEqual(result, "登录成功")
    
    @patch('pinterest_login_tool.asyncio.run')
    def test_run_with_exception(self, mock_asyncio_run):
        """测试运行时异常处理。"""
        mock_asyncio_run.side_effect = Exception("测试异常")
        
        result = self.tool._run(
            username="test@example.com",
            password="testpassword123"
        )
        
        self.assertIn("Pinterest登录失败", result)
        self.assertIn("测试异常", result)


class TestPinterestConfig(unittest.TestCase):
    """Pinterest配置测试类。"""
    
    def test_default_values(self):
        """测试默认配置值。"""
        self.assertEqual(PinterestConfig.DEFAULT_TIMEOUT, 30)
        self.assertTrue(PinterestConfig.DEFAULT_HEADLESS)
        self.assertIn("width", PinterestConfig.DEFAULT_VIEWPORT)
        self.assertIn("height", PinterestConfig.DEFAULT_VIEWPORT)
    
    def test_get_browser_config(self):
        """测试获取浏览器配置。"""
        config = PinterestConfig.get_browser_config()
        self.assertIn("headless", config)
        self.assertIn("timeout", config)
        self.assertIn("viewport", config)
        
        # 测试自定义参数
        custom_config = PinterestConfig.get_browser_config(headless=False, timeout=60)
        self.assertFalse(custom_config["headless"])
        self.assertEqual(custom_config["timeout"], 60000)  # 转换为毫秒
    
    def test_get_login_task(self):
        """测试获取登录任务描述。"""
        task = PinterestConfig.get_login_task("test@example.com", "password123")
        self.assertIn("test@example.com", task)
        self.assertNotIn("password123", task)  # 密码应该被隐藏
        self.assertIn("*", task)  # 应该有星号替代
    
    def test_validate_credentials(self):
        """测试凭据验证。"""
        # 有效凭据
        valid, msg = PinterestConfig.validate_credentials("test@example.com", "password123")
        self.assertTrue(valid)
        self.assertEqual(msg, "")
        
        # 空用户名
        valid, msg = PinterestConfig.validate_credentials("", "password123")
        self.assertFalse(valid)
        self.assertIn("用户名", msg)
        
        # 空密码
        valid, msg = PinterestConfig.validate_credentials("test@example.com", "")
        self.assertFalse(valid)
        self.assertIn("密码", msg)
        
        # 密码太短
        valid, msg = PinterestConfig.validate_credentials("test@example.com", "123")
        self.assertFalse(valid)
        self.assertIn("密码长度", msg)
        
        # 无效邮箱格式
        valid, msg = PinterestConfig.validate_credentials("invalid-email", "password123")
        self.assertTrue(valid)  # 非邮箱格式的用户名也是有效的
        
        valid, msg = PinterestConfig.validate_credentials("invalid@", "password123")
        self.assertFalse(valid)
        self.assertIn("邮箱格式", msg)


class TestIntegration(unittest.TestCase):
    """集成测试类。"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_tool_creation_with_config(self):
        """测试使用配置创建工具。"""
        tool = PinterestLoginTool()
        
        # 验证工具属性
        self.assertIsNotNone(tool.openai_api_key)
        self.assertEqual(tool.openai_api_key, 'test-key')
        
        # 验证配置访问
        config = PinterestConfig.get_browser_config()
        self.assertIsInstance(config, dict)
        
        # 验证凭据验证
        valid, msg = PinterestConfig.validate_credentials("test@example.com", "validpass123")
        self.assertTrue(valid)


if __name__ == '__main__':
    # 设置测试环境
    os.environ['OPENAI_API_KEY'] = 'test-api-key-for-testing'
    
    # 运行测试
    unittest.main(verbosity=2)
