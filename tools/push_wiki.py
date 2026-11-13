"""
Helper Script to Push Wiki Markdown & Assets to GitHub Wiki
Run this script once LLMWiki_Project repository is published and Wiki is initialized.
"""

import os
import sys
import subprocess
import shutil

PROJECT_DIR = r"C:\Users\kylem\Desktop\程式期中"
WIKI_SOURCE = os.path.join(PROJECT_DIR, "wiki")
GIT_EXE = r"C:\Users\kylem\AppData\Local\GitHubDesktop\app-3.6.11\resources\app\git\cmd\git.exe"
TEMP_WIKI_DIR = os.path.join(PROJECT_DIR, ".wiki_git_clone")
WIKI_REMOTE_URL = "https://github.com/kylemily105221-lab/LLMWiki_Project.wiki.git"

def main():
    print("=" * 60)
    print("  GitHub Wiki 同步推送工具 (Sync to GitHub Wiki)")
    print("=" * 60)
    
    if os.path.exists(TEMP_WIKI_DIR):
        shutil.rmtree(TEMP_WIKI_DIR, ignore_errors=True)
        
    print(f"[1/4] 嘗試 Clone 遠端 Wiki 倉庫: {WIKI_REMOTE_URL} ...")
    res = subprocess.run([GIT_EXE, "clone", WIKI_REMOTE_URL, TEMP_WIKI_DIR], capture_output=True, text=True)
    if res.returncode != 0:
        print("Clone 失敗。原因可能是：")
        print("  1. 遠端 Repository 尚未建立或尚未於 GitHub 點擊 'Create the first page' 啟用 Wiki。")
        print("  2. 尚未於瀏覽器登入或尚未取得 Git 存取授權。")
        print(f"錯誤訊息: {res.stderr.strip()}")
        return False
        
    print("[2/4] 複製 wiki/ 內所有 Markdown 與 assets 圖表至 Wiki 倉庫...")
    for item in os.listdir(WIKI_SOURCE):
        src_path = os.path.join(WIKI_SOURCE, item)
        dst_path = os.path.join(TEMP_WIKI_DIR, item)
        if os.path.isdir(src_path):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
            
    print("[3/4] 加入版本控制並提交 Commit...")
    subprocess.run([GIT_EXE, "-C", TEMP_WIKI_DIR, "add", "."], check=True)
    subprocess.run([GIT_EXE, "-C", TEMP_WIKI_DIR, "commit", "-m", "Deploy full technical research wiki chapters and figures"], check=True)
    
    print("[4/4] 推送至 GitHub Wiki 遠端...")
    push_res = subprocess.run([GIT_EXE, "-C", TEMP_WIKI_DIR, "push", "origin", "master"], capture_output=True, text=True)
    if push_res.returncode != 0:
        push_res = subprocess.run([GIT_EXE, "-C", TEMP_WIKI_DIR, "push", "origin", "main"], capture_output=True, text=True)
        
    if push_res.returncode == 0:
        print("\n Wiki 成功推送上線！")
        print(f"線上查看網址: https://github.com/kylemily105221-lab/LLMWiki_Project/wiki")
        shutil.rmtree(TEMP_WIKI_DIR, ignore_errors=True)
        return True
    else:
        print(f"推送失敗: {push_res.stderr.strip()}")
        return False

if __name__ == "__main__":
    main()
