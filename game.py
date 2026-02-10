import random
import os
import json
from typing import List, Set
MAX_ATTEMPTS = 6
STATS_FILE = "hangman_stats.json"
WORDS_FILE = "words.txt"
DEFAULT_WORDS = [
    "ПРОГРАММИРОВАНИЕ", "АЛГОРИТМ", "КОМПЬЮТЕР", "ВИСЕЛИЦА", 
    "СТУДЕНТ", "УНИВЕРСИТЕТ", "ЛЕКЦИЯ", "ПРАКТИКА", 
    "ПИТОН", "КОД", "ФУНКЦИЯ", "ПЕРЕМЕННАЯ", "ЦИКЛ", 
    "УСЛОВИЕ", "СПИСОК", "СЛОВАРЬ", "МНОЖЕСТВО"
]
stats = {
    "games_played": 0,
    "games_won": 0,
    "total_score": 0,
    "best_score": 0
}
def load_words_from_file() -> List[str]:
    """Загрузка слов из файла"""
    try:
        if os.path.exists(WORDS_FILE):
            with open(WORDS_FILE, 'r', encoding='utf-8') as f:
                words = [line.strip().upper() for line in f if line.strip()]
                if words:
                    return words
    except Exception as e:
        print(f"Не удалось загрузить слова из файла: {e}")
    return DEFAULT_WORDS
def load_stats() -> dict:
    """Загрузка статистики из файла"""
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                loaded_stats = json.load(f)
                for key in stats.keys():
                    if key not in loaded_stats:
                        loaded_stats[key] = stats[key]
                return loaded_stats
    except Exception as e:
        print(f"Не удалось загрузить статистику: {e}")
    return stats.copy()
def save_stats() -> None:
    """Сохранение статистики в файл"""
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Не удалось сохранить статистику: {e}")
def main():
    print("Добро пожаловать в игру 'Виселица'!")
    print("Попробуйте угадать слово по буквам.")
    global stats
    words = load_words_from_file()
    stats = load_stats()
    while True:
        secret_word = choose_random_word(words)
        guessed_letters = set()
        attempts_left = MAX_ATTEMPTS
        attempts_used = 0
        game_won = False
        while attempts_left > 0:
            clear_console()
            print(f"Попыток осталось: {attempts_left}")
            draw_gallows(attempts_left)
            print("\nСлово: " + get_masked_word(secret_word, guessed_letters))
            print("Использованные буквы: " + ", ".join(sorted(guessed_letters)))
            guess = get_user_guess(guessed_letters)
            guessed_letters.add(guess)
            if guess not in secret_word:
                attempts_left -= 1
                print(f"Буквы '{guess}' нет в слове.")
            else:
                print(f"Отлично! Буква '{guess}' есть в слове.")
            attempts_used = MAX_ATTEMPTS - attempts_left
            input("\nНажмите Enter чтобы продолжить...")
            if check_win(secret_word, guessed_letters):
                game_won = True
                break
        clear_console()
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            score = calculate_score(secret_word, attempts_used)
            print(f"Ваш счет: {score}")
            update_stats(True, score)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")
            update_stats(False, 0)
            draw_gallows(0)
        save_stats() 
        show_stats()
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру!")
            save_stats() 
            break
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
def choose_random_word(word_list: List[str]) -> str:
    """Выбор случайного слова из списка"""
    return random.choice(word_list)
def get_masked_word(secret_word: str, guessed_letters: Set[str]) -> str:
    """Генерация замаскированного слова"""
    result = []
    for letter in secret_word:
        if letter in guessed_letters:
            result.append(letter)
        else:
            result.append("_")
    return " ".join(result)
def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    stages = [
        """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |     / \\
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |     / 
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |      
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|
        |      |
        |      
        -
        """,
        """
        --------
        |      |
        |      O
        |      |
        |      |
        |      
        -
        """,
        """
        --------
        |      |
        |      O
        |      
        |      
        |      
        -
        """,
        """
        --------
        |      |
        |      
        |      
        |      
        |      
        -
        """
    ]
    
    print(stages[attempts_left])

def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    while True:
        guess = input("\nВведите букву: ").upper()
        
        if len(guess) != 1:
            print("Пожалуйста, введите только одну букву.")
            continue
        
        if not guess.isalpha() or guess not in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
            print("Пожалуйста, введите русскую букву.")
            continue
        
        if guess in guessed_letters:
            print("Вы уже вводили эту букву. Попробуйте другую.")
            continue
        
        return guess

def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""
    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    base_score = len(secret_word) * 10
    bonus = (MAX_ATTEMPTS - attempts_used) * 5
    return base_score + bonus

def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats
    stats["games_played"] += 1
    
    if won:
        stats["games_won"] += 1
        stats["total_score"] += score
        if score > stats["best_score"]:
            stats["best_score"] = score

def show_stats():
    """Отображение статистики"""
    global stats
    
    if stats["games_played"] == 0:
        win_percentage = 0
    else:
        win_percentage = (stats["games_won"] / stats["games_played"]) * 100
    
    if stats["games_won"] > 0:
        average_score = stats["total_score"] / stats["games_won"]
    else:
        average_score = 0
    
    print("\n=== Статистика ===")
    print(f"Всего игр: {stats['games_played']}")
    print(f"Побед: {stats['games_won']} ({win_percentage:.1f}%)")
    print(f"Лучший счет: {stats['best_score']}")
    
    if stats["games_won"] > 0:
        print(f"Средний счет за победу: {average_score:.1f}")

if __name__ == "__main__":
    main()