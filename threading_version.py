import os
import time
import threading


# Вказую папку з текстовими файлами та слова для пошуку
FOLDER = "texts"
KEYWORDS = ["Python", "threading", "multiprocessing", "Java"]


# Створюю функцію для пошуку слів у файлах
def search_words(files, keywords, results, lock):
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read().lower()

            # Перевіряю наявність кожного ключового слова
            for keyword in keywords:
                if keyword.lower() in text:
                    # Захищаю спільний словник від одночасного запису
                    with lock:
                        results[keyword].append(file_path)

        except OSError as error:
            print(f"Помилка читання файлу {file_path}: {error}")


if __name__ == "__main__":

    # Починаю вимірювати час виконання програми
    start_time = time.time()

    # Створюю словник для збереження результатів
    results = {keyword: [] for keyword in KEYWORDS}

    # Отримую список текстових файлів із папки
    try:
        files = [
            os.path.join(FOLDER, name)
            for name in os.listdir(FOLDER)
            if name.endswith(".txt")
        ]
    except OSError as error:
        print(f"Помилка доступу до папки: {error}")
        files = []

    # Створюю блокування для безпечної роботи зі словником
    lock = threading.Lock()

    # Визначаю кількість потоків
    thread_count = min(4, len(files))

    threads = []

    if thread_count > 0:

        # Розподіляю файли між потоками
        for i in range(thread_count):
            thread_files = files[i::thread_count]

            thread = threading.Thread(
                target=search_words,
                args=(thread_files, KEYWORDS, results, lock)
            )

            threads.append(thread)

            # Запускаю потік
            thread.start()

        # Очікую завершення всіх потоків
        for thread in threads:
            thread.join()

    # Виводжу знайдені слова та шляхи до файлів
    print("Результати багатопотокового пошуку:")

    for keyword, paths in results.items():
        print(f"{keyword}: {sorted(paths)}")

    # Виводжу час виконання програми
    end_time = time.time()
    print(f"Час виконання: {end_time - start_time:.6f} секунд")