#!/usr/bin/env python3
"""Pinterest登录工具快速启动脚本。"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_environment():
    """检查环境配置。"""
    print("🔍 检查环境配置...")
    
    # 检查OpenAI API密钥
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ 未找到OPENAI_API_KEY环境变量")
        print("   请设置: export OPENAI_API_KEY='your-api-key'")
        return False
    else:
        print(f"✅ OpenAI API密钥已设置 (长度: {len(api_key)} 字符)")
    
    # 检查必要的包
    required_packages = ['browser_use', 'crewai', 'langchain_openai', 'playwright', 'pydantic']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n请安装缺失的包:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True


def interactive_login():
    """交互式登录测试。"""
    print("\n🚀 Pinterest登录工具交互式测试")
    print("=" * 50)
    
    # 获取用户输入
    username = input("请输入Pinterest用户名或邮箱: ").strip()
    if not username:
        print("❌ 用户名不能为空")
        return
    
    password = input("请输入Pinterest密码: ").strip()
    if not password:
        print("❌ 密码不能为空")
        return
    
    headless_input = input("是否使用无头模式? (y/N): ").strip().lower()
    headless = headless_input in ['y', 'yes', '1', 'true']
    
    timeout_input = input("超时时间（秒，默认30）: ").strip()
    try:
        timeout = int(timeout_input) if timeout_input else 30
    except ValueError:
        timeout = 30
    
    print(f"\n📋 配置信息:")
    print(f"   用户名: {username}")
    print(f"   密码: {'*' * len(password)}")
    print(f"   无头模式: {headless}")
    print(f"   超时时间: {timeout}秒")
    
    confirm = input("\n确认执行登录? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes', '1', 'true']:
        print("❌ 用户取消操作")
        return
    
    # 执行登录
    print("\n🔄 开始执行Pinterest登录...")
    try:
        from pinterest_login_tool import PinterestLoginTool
        
        tool = PinterestLoginTool()
        result = tool._run(
            username=username,
            password=password,
            headless=headless,
            timeout=timeout
        )
        
        print(f"\n📊 登录结果:")
        print(f"   {result}")
        
    except Exception as e:
        print(f"\n❌ 登录失败: {str(e)}")


def run_example():
    """运行示例代码。"""
    print("\n📚 运行示例代码...")
    try:
        exec(open('example.py').read())
    except FileNotFoundError:
        print("❌ 未找到example.py文件")
    except Exception as e:
        print(f"❌ 运行示例失败: {str(e)}")


def run_tests():
    """运行测试。"""
    print("\n🧪 运行单元测试...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'test_pinterest_tool.py'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ 运行测试失败: {str(e)}")


def show_menu():
    """显示主菜单。"""
    print("\n🎯 Pinterest登录工具 - 快速启动")
    print("=" * 50)
    print("1. 检查环境配置")
    print("2. 交互式登录测试")
    print("3. 运行示例代码")
    print("4. 运行单元测试")
    print("5. 查看帮助文档")
    print("0. 退出")
    print("=" * 50)


def show_help():
    """显示帮助信息。"""
    print("\n📖 帮助文档")
    print("=" * 50)
    print("这是一个基于browser-use库的Pinterest自动登录工具。")
    print("\n🔧 环境要求:")
    print("- Python 3.8+")
    print("- OpenAI API密钥")
    print("- 网络连接")
    print("\n📦 安装依赖:")
    print("pip install -r requirements.txt")
    print("playwright install chromium")
    print("\n🚀 快速使用:")
    print("1. 设置环境变量: export OPENAI_API_KEY='your-key'")
    print("2. 运行本脚本选择交互式测试")
    print("3. 输入Pinterest账号信息")
    print("\n📚 更多信息请查看README.md文件")


def main():
    """主函数。"""
    print("🌟 欢迎使用Pinterest登录工具！")
    
    while True:
        show_menu()
        choice = input("\n请选择操作 (0-5): ").strip()
        
        if choice == '0':
            print("👋 再见！")
            break
        elif choice == '1':
            check_environment()
        elif choice == '2':
            if check_environment():
                interactive_login()
            else:
                print("❌ 环境检查失败，请先解决环境问题")
        elif choice == '3':
            run_example()
        elif choice == '4':
            run_tests()
        elif choice == '5':
            show_help()
        else:
            print("❌ 无效选择，请重新输入")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    main()
