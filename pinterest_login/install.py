#!/usr/bin/env python3
"""Pinterest登录工具安装脚本。"""

import os
import sys
import subprocess
import platform


def run_command(command, description):
    """运行命令并显示结果。"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False


def check_python_version():
    """检查Python版本。"""
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    print("✅ Python版本满足要求")
    return True


def install_dependencies():
    """安装Python依赖。"""
    print("\n📦 安装Python依赖包...")
    
    # 升级pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip"):
        return False
    
    # 安装依赖
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_file):
        command = f"{sys.executable} -m pip install -r {requirements_file}"
        if not run_command(command, "安装依赖包"):
            return False
    else:
        # 手动安装核心依赖
        packages = [
            "browser-use>=0.7.0",
            "langchain-openai>=0.1.0", 
            "playwright>=1.40.0",
            "pydantic>=2.0.0",
            "crewai>=0.1.0",
            "python-dotenv"
        ]
        
        for package in packages:
            command = f"{sys.executable} -m pip install {package}"
            if not run_command(command, f"安装 {package}"):
                print(f"⚠️ {package} 安装失败，继续安装其他包...")
    
    return True


def install_playwright():
    """安装Playwright浏览器。"""
    print("\n🌐 安装Playwright浏览器...")
    
    # 安装chromium
    if not run_command("playwright install chromium", "安装Chromium浏览器"):
        return False
    
    # 安装系统依赖（Linux系统）
    if platform.system() == "Linux":
        if not run_command("playwright install-deps chromium", "安装系统依赖"):
            print("⚠️ 系统依赖安装失败，可能需要手动安装")
    
    return True


def create_env_file():
    """创建环境变量文件。"""
    print("\n📝 创建环境配置文件...")
    
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    
    if os.path.exists(env_file):
        print("✅ .env文件已存在")
        return True
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("# Pinterest登录工具环境配置\n")
            f.write("# 请设置你的OpenAI API密钥\n")
            f.write("OPENAI_API_KEY=your-openai-api-key-here\n")
            f.write("\n")
            f.write("# 调试模式（可选）\n")
            f.write("PINTEREST_DEBUG=false\n")
        
        print("✅ 创建.env文件成功")
        print("⚠️ 请编辑.env文件，设置你的OpenAI API密钥")
        return True
        
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")
        return False


def verify_installation():
    """验证安装。"""
    print("\n🔍 验证安装...")
    
    # 检查关键包
    packages_to_check = [
        'browser_use',
        'langchain_openai', 
        'playwright',
        'pydantic',
        'dotenv'
    ]
    
    all_ok = True
    for package in packages_to_check:
        try:
            __import__(package)
            print(f"✅ {package} 导入成功")
        except ImportError:
            print(f"❌ {package} 导入失败")
            all_ok = False
    
    if all_ok:
        print("✅ 所有依赖包验证通过")
    else:
        print("❌ 部分依赖包验证失败")
    
    return all_ok


def show_next_steps():
    """显示下一步操作。"""
    print("\n🎉 安装完成！")
    print("=" * 50)
    print("📋 下一步操作:")
    print("1. 编辑.env文件，设置你的OpenAI API密钥")
    print("2. 运行快速启动脚本: python quick_start.py")
    print("3. 或者查看README.md了解详细使用方法")
    print("4. 运行测试: python test_pinterest_tool.py")
    print("\n📚 相关文档:")
    print("- README.md: 详细使用说明")
    print("- example.py: 使用示例")
    print("- PROJECT_SUMMARY.md: 项目总结")
    print("\n🆘 如遇问题:")
    print("- 检查Python版本 (需要3.8+)")
    print("- 确认网络连接正常")
    print("- 查看错误日志排查问题")


def main():
    """主安装流程。"""
    print("🚀 Pinterest登录工具安装程序")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装Python依赖
    if not install_dependencies():
        print("❌ Python依赖安装失败")
        sys.exit(1)
    
    # 安装Playwright
    if not install_playwright():
        print("❌ Playwright安装失败")
        sys.exit(1)
    
    # 创建环境文件
    create_env_file()
    
    # 验证安装
    if not verify_installation():
        print("⚠️ 安装验证未完全通过，但可以尝试使用")
    
    # 显示下一步
    show_next_steps()


if __name__ == "__main__":
    main()
