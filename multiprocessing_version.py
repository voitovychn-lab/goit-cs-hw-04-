import os
import time
import multiprocessing


# Вказую папку з текстовими файлами та слова для пошуку
FOLDER = "texts"
KEYWORDS = ["Python", "threading", "multiprocessing", "Java"]


# Створюю функцію для пошуку слів в окремому процесі
def search_words(files, keywords, queue):
    results = {keyword: [] for keyword in keywords}

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read().lower()

            # Перевіряю наявність кожного ключового слова
            for keyword in keywords:
                if keyword.lower() in text:
                    results[keyword].append(file_path)

        except OSError as error:
            print(f"Помилка читання файлу {file_path}: {error}")

    # Передаю результати головному процесу через чергу
    queue.put(results)


if __name__ == "__main__":

    # Починаю вимірювати час виконання програми
    start_time = time.time()

    # Створюю словник для загальних результатів
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

    # Створюю чергу для передачі результатів між процесами
    queue = multiprocessing.Queue()

    # Визначаю кількість процесів
    process_count = min(4, len(files))

    processes = []

    if process_count > 0:

        # Розподіляю файли між процесами
        for i in range(process_count):
            process_files = files[i::process_count]

            process = multiprocessing.Process(
                target=search_words,
                args=(process_files, KEYWORDS, queue)
            )

            processes.append(process)

            # Запускаю процес
            process.start()

        # Отримую результати від кожного процесу
        for _ in processes:
            process_results = queue.get()

            # Об'єдную результати в один словник
            for keyword, paths in process_results.items():
                results[keyword].extend(paths)

        # Очікую завершення всіх процесів
        for process in processes:
            process.join()

    # Виводжу знайдені слова та шляхи до файлів
    print("Результати багатопроцесорного пошуку:")

    for keyword, paths in results.items():
        print(f"{keyword}: {sorted(paths)}")

    # Виводжу час виконання програми
    end_time = time.time()
    print(f"Час виконання: {end_time - start_time:.6f} секунд")