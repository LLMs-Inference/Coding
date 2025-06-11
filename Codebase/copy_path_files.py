import os
import shutil
from pathlib import Path


def copy_folder(
    src_path: Path,
    dst_path: Path,
    exclude_dirs: list = None,
    exclude_suffixes: list = None,
    exclude_filenames: list = None,
) -> None:
    """
    复制文件夹及其所有内容到目标路径, 支持排除特定目录、文件后缀和文件名。

    参数:
        src_path: 源文件夹路径
        dst_path: 目标文件夹路径
        exclude_dirs: 要排除的目录名列表
        exclude_suffixes: 要排除的文件后缀列表
        exclude_filenames: 要排除的文件名列表
    """
    # 设置默认值
    exclude_dirs = exclude_dirs or []
    exclude_suffixes = exclude_suffixes or []
    exclude_filenames = exclude_filenames or []

    # 确保源路径存在且是目录
    if not src_path.exists():
        raise FileNotFoundError(f"源路径不存在: {src_path}")
    if not src_path.is_dir():
        raise NotADirectoryError(f"源路径不是目录: {src_path}")

    # 创建目标文件夹 (如果不存在)
    dst_path.mkdir(parents=True, exist_ok=True)

    # 遍历源文件夹中的所有项目
    for item in src_path.iterdir():
        # 获取相对路径部分
        rel_path = item.relative_to(src_path)
        target_path = dst_path / rel_path

        # 先判断以及处理目录
        if item.is_dir():
            # 检查是否应排除此目录
            if item.name in exclude_dirs:
                continue

            # 递归复制子目录
            copy_folder(
                item, target_path, exclude_dirs, exclude_suffixes, exclude_filenames
            )

        # 再是处理文件
        elif item.is_file():
            # 检查是否应排除此文件
            if item.name in exclude_filenames or any(
                item.name.endswith(suffix) for suffix in exclude_suffixes
            ):
                continue

            # 确保目标文件的父目录存在
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # 复制文件
            shutil.copy2(item, target_path)


# 使用示例:
if __name__ == "__main__":
    # 注意修改你的源文件夹和目标文件夹路径
    source = Path("./source_folder")
    destination = Path("./destination_folder")

    copy_folder(
        source,
        destination,
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
