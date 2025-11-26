import psutil
import shutil
import os
import threading
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from datetime import timedelta

"""Buraya kopyalanmak istenen dosyanın uzantısı yazılacak"""
SOURCE_PATH = Path(r"") 

tasks = {}

def find_usb_drives():
    """Windows'ta takılı çıkarılabilir diskleri bulur."""
    drives = []
    for partition in psutil.disk_partitions(all=False):
        if "removable" in partition.opts.lower():
            drives.append(partition.device)
    return drives

def get_total_size(path: Path):
    """Klasörün toplam boyutunu hesapla (byte)."""
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            fp = Path(root) / f
            try:
                total += fp.stat().st_size
            except FileNotFoundError:
                continue
    return total

def format_time(seconds: float) -> str:
    """Saniyeyi HH:MM:SS formatına çevir."""
    return str(timedelta(seconds=int(seconds)))

def copy_with_progress(drive, source_path, progress_var, label_status, label_file, label_eta):
    """Her dosyayı tek tek kopyalayarak ilerlemeyi güncelle."""
    try:
        dest = Path(drive) / source_path.name

        # Eğer hedef klasör varsa, kopyalama yapılmaz
        if dest.exists():
            label_status.config(text="Zaten mevcut, kopyalanmadı", foreground="orange")
            label_eta.config(text="Tahmini süre: -")
            return

        total_size = get_total_size(source_path)
        copied_size = 0
        start_time = time.time()

        for root, _, files in os.walk(source_path):
            rel_path = os.path.relpath(root, source_path)
            dest_dir = Path(dest) / rel_path
            dest_dir.mkdir(parents=True, exist_ok=True)

            for f in files:
                src_file = Path(root) / f
                dest_file = dest_dir / f

                shutil.copy2(src_file, dest_file)

                copied_size += src_file.stat().st_size
                progress = int((copied_size / total_size) * 100)
                progress_var.set(progress)

                # Son kopyalanan dosyayı göster
                label_file.config(text=f"Son dosya: {src_file.name}")

                # ETA hesapla
                elapsed = time.time() - start_time
                if elapsed > 0 and copied_size > 0:
                    speed = copied_size / elapsed  # byte/s
                    remaining = (total_size - copied_size) / speed
                    label_eta.config(text=f"Tahmini süre: {format_time(remaining)}")

        label_status.config(text="Tamamlandı", foreground="green")
        label_eta.config(text="Tahmini süre: 00:00:00")
        print(f"[+] {source_path} -> {dest}")
    except Exception as e:
        label_status.config(text=f"Hata: {e}", foreground="red")
        label_eta.config(text="Tahmini süre: -")
        print(f"[!] {drive} için hata: {e}")

def monitor_usbs(root):
    """USB’leri sürekli izle, yeni takılanları iş parçacığı olarak başlat."""
    usbs = find_usb_drives()

    # Yeni takılan USB'ler için UI ve iş parçacığı başlat
    for usb in usbs:
        if usb not in tasks:
            frame = ttk.Frame(root)
            frame.pack(fill="x", pady=5, padx=10)

            title = ttk.Label(frame, text=f"USB {usb}", font=("Arial", 10, "bold"))
            title.pack(anchor="w")

            progress_var = tk.IntVar()
            progress = ttk.Progressbar(frame, maximum=100, variable=progress_var)
            progress.pack(fill="x", padx=5, pady=2)

            label_status = ttk.Label(frame, text="Kontrol ediliyor...", foreground="blue")
            label_status.pack(anchor="w")

            label_file = ttk.Label(frame, text="Son dosya: -", font=("Arial", 8))
            label_file.pack(anchor="w")

            label_eta = ttk.Label(frame, text="Tahmini süre: -", font=("Arial", 8, "italic"))
            label_eta.pack(anchor="w")

            # Dict'e kaydet
            tasks[usb] = {
                "frame": frame,
                "progress": progress_var,
                "status": label_status,
                "file": label_file,
                "eta": label_eta,
            }

            # Kopyalama thread'i başlat
            t = threading.Thread(
                target=copy_with_progress,
                args=(usb, SOURCE_PATH, progress_var, label_status, label_file, label_eta),
                daemon=True,
            )
            t.start()
            tasks[usb]["thread"] = t

    # Çıkarılan USB'leri UI'dan kaldır
    for usb in list(tasks.keys()):
        if usb not in usbs:
            frame = tasks[usb]["frame"]
            frame.destroy()  # UI’dan kaldır
            del tasks[usb]

    root.after(2000, monitor_usbs, root)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("USB Kopyalama Takip")
    root.geometry("500x450")

    ttk.Label(root, text="Takılan USB'lere otomatik klasör kopyalama",
              font=("Arial", 12, "bold")).pack(pady=10)

    monitor_usbs(root)

    root.mainloop()
