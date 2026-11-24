from pathlib import Path
import subprocess
import sys
import time
import uuid

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])
    import requests
    from bs4 import BeautifulSoup

url = "https://images.wallpaperscraft.ru/image/single/kamni_mlechnyj_put_noch_1307116_3840x2160.jpg"
file_path = Path(__file__).resolve().parent / url.split("/")[-1]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
}

times = []
total_bytes = 0

print(f"{'Запрос':<7} | {'Код ответа':<10} | {'Размер':<10} | {'Время'}")
print("-" * 44)

for i in range(1, 11):
    target = f"{url}?_={uuid.uuid4().hex}"

    start = time.perf_counter()
    resp = requests.get(target, headers=headers, timeout=30)
    elapsed = time.perf_counter() - start

    BeautifulSoup(resp.content, "html.parser", from_encoding="latin-1")
    file_path.write_bytes(resp.content)

    size = len(resp.content)
    times.append(elapsed)
    total_bytes += size

    req = f"[{i}/10]"
    size_str = f"{size / (1024 * 1024):.2f} МБ"
    print(f"{req:<7} | {resp.status_code:<10} | {size_str:<10} | {elapsed:.3f} с")

total_time = sum(times)
avg_time = total_time / len(times)
mbps = (total_bytes * 8) / total_time / 1_000_000

print(f"\nСреднее время: {avg_time:.3f} с")
print(f"Общий объём: {total_bytes / (1024 * 1024):.2f} МБ")
print(f"Средняя скорость: {mbps:.2f} Мбит/с")