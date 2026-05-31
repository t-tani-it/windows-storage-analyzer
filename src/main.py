import os
import ctypes
import argparse
from ctypes import wintypes

# デフォルト設定
DEFAULT_TARGET_DIR = r"C:\Users"
DEFAULT_THRESHOLD_MB = 100

# Windows API: GetCompressedFileSizeW
GetCompressedFileSizeW = ctypes.windll.kernel32.GetCompressedFileSizeW
GetCompressedFileSizeW.argtypes = [wintypes.LPCWSTR, wintypes.LPVOID]
GetCompressedFileSizeW.restype = wintypes.DWORD


def get_physical_size(path):
    """Explorer と同じ「物理ディスク使用量」を返す"""
    high = wintypes.DWORD(0)
    low = GetCompressedFileSizeW(path, ctypes.byref(high))
    if low == 0xFFFFFFFF:
        err = ctypes.GetLastError()
        if err != 0:
            return 0
    return (high.value << 32) + low


def folder_physical_size(folder):
    total = 0
    for root, dirs, files in os.walk(folder, topdown=True):
        for f in files:
            fp = os.path.join(root, f)
            try:
                total += get_physical_size(fp)
            except Exception:
                pass
    return total


def scan_two_levels_grouped(root, threshold_mb):
    threshold_bytes = threshold_mb * 1024 * 1024

    for d1 in os.listdir(root):
        p1 = os.path.join(root, d1)
        if not os.path.isdir(p1):
            continue

        size1 = folder_physical_size(p1)
        printed = False

        if size1 > threshold_bytes:
            print(f"{p1}  {size1/1024/1024/1024:.2f} GB")
            printed = True

        try:
            for d2 in os.listdir(p1):
                p2 = os.path.join(p1, d2)
                if os.path.isdir(p2):
                    size2 = folder_physical_size(p2)

                    if size2 > threshold_bytes:
                        print(f"    {p2}  {size2/1024/1024/1024:.2f} GB")
        except PermissionError:
            pass

        if printed:
            print()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Windows で指定フォルダを走査し、2 階層までのフォルダ容量を表示します。"
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=DEFAULT_TARGET_DIR,
        help=f"調べたいフォルダのパス（デフォルト: {DEFAULT_TARGET_DIR}）",
    )
    parser.add_argument(
        "threshold_mb",
        nargs="?",
        type=int,
        default=DEFAULT_THRESHOLD_MB,
        help=f"表示する最小サイズ（MB）（デフォルト: {DEFAULT_THRESHOLD_MB}）",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    scan_two_levels_grouped(args.target_dir, args.threshold_mb)
