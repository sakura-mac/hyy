import os
from PIL import Image
import shutil

def compress_images(directory, quality=80, max_size=(1024, 1024)):
    # 确保备份目录存在
    backup_dir = os.path.join(directory, 'backup')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"创建备份目录: {backup_dir}")

    files = [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    total_saved = 0

    for filename in files:
        filepath = os.path.join(directory, filename)
        backup_path = os.path.join(backup_dir, filename)
        
        # 备份原文件
        if not os.path.exists(backup_path):
            shutil.copy2(filepath, backup_path)
        
        original_size = os.path.getsize(filepath)
        
        try:
            with Image.open(filepath) as img:
                # 转换颜色模式，防止 RGBA 保存为 JPEG 出错
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # 调整尺寸
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # 保存压缩后的图片
                img.save(filepath, "JPEG", quality=quality, optimize=True)
                
                new_size = os.path.getsize(filepath)
                saved = original_size - new_size
                total_saved += saved
                
                print(f"压缩 {filename}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB (节省 {saved/1024:.1f}KB)")
        except Exception as e:
            print(f"处理 {filename} 时出错: {e}")

    print(f"\n总共节省空间: {total_saved/1024/1024:.2f} MB")
    print("原文件已备份在 photos/backup 目录中")

if __name__ == "__main__":
    photos_dir = os.path.join(os.getcwd(), "public", "photos")
    if os.path.exists(photos_dir):
        print("开始压缩图片...")
        compress_images(photos_dir)
    else:
        print(f"找不到目录: {photos_dir}")
