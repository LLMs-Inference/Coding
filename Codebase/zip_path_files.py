import os
import zipfile
import pathlib
from typing import List, Union, Optional


def zip_directory(
    source_path: pathlib.Path,
    output_path: pathlib.Path,
    exclude_dirs: Optional[List[str]] = None,
    exclude_extensions: Optional[List[str]] = None,
    exclude_filenames: Optional[List[str]] = None,
) -> pathlib.Path:
    """
    将指定文件夹及其内容打包为 zip 文件, 支持排除特定子目录、文件后缀和文件名。

    形参:
        source_path: 要打包的源文件夹路径
        output_path: 输出的 zip 文件路径
        exclude_dirs: 要排除的目录名列表
        exclude_extensions: 要排除的文件扩展名列表
        exclude_filenames: 要排除的文件名列表

    返回:
        输出 zip 文件的 Path 对象
    """
    # 初始化排除列表
    exclude_dirs = exclude_dirs or []
    exclude_extensions = exclude_extensions or []
    exclude_filenames = exclude_filenames or []

    # 确保输出目录存在
    output_path.mkdir(mode=511, parents=True, exist_ok=True)

    # 创建 zip 文件
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 遍历源目录
        for root, dirs, files in os.walk(source_path):
            # 过滤排除的目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            # 相对路径, 用于 zip 内部结构。
            rel_dir = os.path.relpath(root, source_path.parent)

            # 添加文件到 zip
            for file in files:
                # 检查是否应该排除此文件
                if file in exclude_filenames:
                    continue

                # 检查文件扩展名
                file_ext = os.path.splitext(file)[1]
                if file_ext in exclude_extensions:
                    continue

                # 构建文件的完整路径
                file_path = os.path.join(root, file)

                # 将文件添加到 zip, 保持相对路径结构。
                archive_path = os.path.join(rel_dir, file)
                zipf.write(file_path, archive_path)

    return output_path


# 使用示例:
if __name__ == "__main__":
    source = pathlib.Path("./source_folder")
    output = pathlib.Path("./output/archive.zip")

    result = zip_directory(
        source,
        output,
        exclude_dirs=[
            "__pycache__",
            ".git",
            ".svn",
            ".venv",
            "venv",
            "env",
            "node_modules",
            ".idea",
            ".vscode",
            "dist",
            "build",
            "egg-info",
            ".pytest_cache",
            ".mypy_cache",
        ],
        exclude_suffixes=[
            ".tmp",
            ".temp",
            ".log",
            ".pyc",
            ".pyo",
            ".so",
            ".pyd",
            ".bak",
            ".backup",
            ".swp",
            ".swo",
            ".coverage",
            ".egg",
            ".ipynb_checkpoints",
            ".DS_Store",
        ],
        exclude_filenames=["config.ini", "secrets.json"],
    )

    print(f"压缩成功! 文件保存在: {result}")
