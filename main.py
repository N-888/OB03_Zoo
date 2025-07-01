# Импорт необходимых модулей
import tkinter as tk  # Основной модуль для создания графического интерфейса
from tkinter import messagebox  # Модуль для отображения диалоговых окон
from tkinter import simpledialog  # Модуль для простых диалогов ввода
from tkinter import filedialog  # Модуль для диалогов работы с файлами
from tkinter import ttk  # Модуль для расширенных виджетов Tkinter
import logging  # Модуль для логирования событий
import os  # Модуль для работы с операционной системой
import pickle  # Модуль для сериализации объектов

# Попытка импорта библиотеки pygame для работы со звуками
try:
    import pygame  # Импорт библиотеки pygame

    pygame.mixer.init()  # Инициализация звукового модуля pygame
    pygame_available = True  # Установка флага доступности pygame
except ImportError:  # Обработка ошибки, если pygame не установлен
    pygame = None  # Установка значения None для pygame
    pygame_available = False  # Установка флага недоступности pygame
    print("Pygame не установлен, звуки отключены")  # Вывод сообщения об ошибке в консоль

# Настройка системы логирования
logging.basicConfig(
    filename="zoo_log.txt",  # Имя файла для сохранения логов
    level=logging.INFO,  # Уровень логирования (запись информационных сообщений)
    format="%(asctime)s — %(levelname)s — %(message)s"  # Формат записей в логе
)

# Пароль администратора по умолчанию
admin_password = "admin123"


# Класс Animal - базовый класс для всех животных в зоопарке
class Animal:
    # Конструктор класса Animal
    def __init__(self, name, age):
        self.name = name  # Имя животного
        self.age = age  # Возраст животного

    # Метод для издания звука (должен быть переопределен в дочерних классах)
    def make_sound(self):
        pass  # Заглушка, реализация будет в наследниках

    # Метод, описывающий процесс питания животного
    def eat(self):
        logging.info(f"{self.name} ест.")  # Запись действия в лог
        print(f"{self.name} ест.")  # Вывод действия в консоль

    # Метод для строкового представления объекта
    def __str__(self):
        # Возвращает строку с информацией о животном
        return f"{self.__class__.__name__} - {self.name}, возраст {self.age} лет"


# Класс Bird (Птица) - наследуется от класса Animal
class Bird(Animal):
    # Реализация метода издания звука для птицы
    def make_sound(self):
        logging.info(f"{self.name} чирикает.")  # Запись действия в лог
        print(f"{self.name} чирикает.")  # Вывод действия в консоль
        # Проверка доступности библиотеки pygame
        if pygame_available:
            try:
                # Загрузка звукового файла для птицы
                pygame.mixer.music.load("bird_sound.mp3")
                # Воспроизведение звука
                pygame.mixer.music.play()
            except Exception as e:  # Обработка возможных ошибок
                # Вывод сообщения об ошибке в консоль
                print(f"Ошибка воспроизведения звука птицы: {e}")


# Класс Mammal (Млекопитающее) - наследуется от класса Animal
class Mammal(Animal):
    # Реализация метода издания звука для млекопитающего
    def make_sound(self):
        logging.info(f"{self.name} рычит.")  # Запись действия в лог
        print(f"{self.name} рычит.")  # Вывод действия в консоль
        # Проверка доступности библиотеки pygame
        if pygame_available:
            try:
                # Загрузка звукового файла для млекопитающего
                pygame.mixer.music.load("mammal_sound.mp3")
                # Воспроизведение звука
                pygame.mixer.music.play()
            except Exception as e:  # Обработка возможных ошибок
                # Вывод сообщения об ошибке в консоль
                print(f"Ошибка воспроизведения звука млекопитающего: {e}")


# Класс Reptile (Рептилия) - наследуется от класса Animal
class Reptile(Animal):
    # Реализация метода издания звука для рептилии
    def make_sound(self):
        logging.info(f"{self.name} шипит.")  # Запись действия в лог
        print(f"{self.name} шипит.")  # Вывод действия в консоль
        # Проверка доступности библиотеки pygame
        if pygame_available:
            try:
                # Загрузка звукового файла для рептилии
                pygame.mixer.music.load("reptile_sound.mp3")
                # Воспроизведение звука
                pygame.mixer.music.play()
            except Exception as e:  # Обработка возможных ошибок
                # Вывод сообщения об ошибке в консоль
                print(f"Ошибка воспроизведения звука рептилии: {e}")


# Класс Zoo для управления зоопарком
class Zoo:
    # Конструктор класса Zoo
    def __init__(self, name):
        self.name = name  # Название зоопарка
        self.animals = []  # Список животных в зоопарке
        self.staff = []  # Список сотрудников зоопарка

    # Метод для добавления животного в зоопарк
    def add_animal(self, animal):
        self.animals.append(animal)  # Добавление животного в список
        # Запись информации о добавлении животного в лог
        logging.info(f"Животное {animal.name} добавлено в зоопарк.")

    # Метод для добавления сотрудника в зоопарк
    def add_staff(self, staff_member):
        self.staff.append(staff_member)  # Добавление сотрудника в список
        # Запись информации о добавлении сотрудника в лог
        logging.info(f"Сотрудник {staff_member.name} нанят.")

    # Метод для сохранения состояния зоопарка в файл
    def save_zoo(self, filename="zoo_data.pkl"):
        try:
            # Открытие файла для бинарной записи
            with open(filename, 'wb') as file:
                # Сериализация объекта зоопарка и запись в файл
                pickle.dump(self, file)
            # Запись информации о сохранении в лог
            logging.info(f"Состояние зоопарка сохранено в {filename}.")
            return True  # Возврат успешного статуса
        except (IOError, pickle.PicklingError) as e:  # Обработка ошибок ввода/вывода и сериализации
            # Запись ошибки в лог
            logging.error(f"Ошибка сохранения зоопарка: {e}")
            return False  # Возврат статуса ошибки

    # Статический метод для загрузки состояния зоопарка из файла
    @staticmethod
    def load_zoo(filename="zoo_data.pkl"):
        try:
            # Открытие файла для бинарного чтения
            with open(filename, 'rb') as file:
                # Десериализация объекта зоопарка из файла
                zoo_obj = pickle.load(file)
            # Запись информации о загрузке в лог
            logging.info(f"Состояние зоопарка загружено из {filename}.")
            return zoo_obj  # Возврат загруженного объекта
        except FileNotFoundError:  # Обработка ошибки отсутствия файла
            # Запись ошибки в лог
            logging.error(f"Файл {filename} не найден.")
            raise  # Повторное возбуждение исключения
        except (IOError, pickle.UnpicklingError) as e:  # Обработка других ошибок
            # Запись ошибки в лог
            logging.error(f"Ошибка загрузки зоопарка: {e}")
            raise  # Повторное возбуждение исключения


# Базовый класс Staff для сотрудников зоопарка
class Staff:
    # Конструктор класса Staff
    def __init__(self, name):
        self.name = name  # Имя сотрудника


# Класс ZooKeeper (Смотритель) - наследуется от класса Staff
class ZooKeeper(Staff):
    # Метод для кормления животного
    def feed_animal(self, animal):
        # Запись действия в лог
        logging.info(f"{self.name} кормит {animal.name}.")
        # Вывод действия в консоль
        print(f"{self.name} кормит {animal.name}.")


# Класс Veterinarian (Ветеринар) - наследуется от класса Staff
class Veterinarian(Staff):
    # Метод для лечения животного
    def heal_animal(self, animal):
        # Запись действия в лог
        logging.info(f"{self.name} лечит {animal.name}.")
        # Вывод действия в консоль
        print(f"{self.name} лечит {animal.name}.")


# Функция для запуска графического интерфейса управления зоопарком
def run_gui(zoo):
    # Создание главного окна приложения
    root_window = tk.Tk()
    # Установка заголовка окна с названием зоопарка
    root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
    # Установка размеров главного окна
    root_window.geometry("500x750")

    # Цветовая схема приложения
    colors = {
        'bg_color': "#dce2b9",  # Цвет фона
        'btn_color': "#a9c186",  # Цвет кнопок
        'text_color': "#5D4037",  # Цвет текста
        'entry_bg': "#f8f8f8",  # Фон полей ввода
        'accent_color': "#8D6E63",  # Акцентный цвет
        'success_bg': "#dce2b9",  # Фон сообщений об успехе
        'success_fg': "#5D4037",  # Текст сообщений об успехе
        'tab_bg': "#a9c186",  # Фон вкладок
        'tab_fg': "#5D4037"  # Текст вкладок
    }

    # Настройка фона главного окна
    root_window.configure(bg=colors['bg_color'])

    # Попытка загрузки иконки приложения
    try:
        # Загрузка иконки из файла
        root_window.iconbitmap("zoo_logo.ico")
    except Exception as icon_exc:  # Обработка ошибки загрузки иконки
        # Запись предупреждения в лог
        logging.warning(f"Иконка не найдена: {icon_exc}")

    # Функция для создания дочернего окна
    def create_toplevel(title, width=400, height=300):
        # Создание дочернего окна
        window = tk.Toplevel(root_window)
        # Установка заголовка окна
        window.title(title)
        # Установка размеров окна
        window.geometry(f"{width}x{height}")
        # Настройка фона окна
        window.configure(bg=colors['bg_color'])
        return window  # Возврат созданного окна

    # Функция для создания текстовой метки
    def create_label(parent, text, bg=None, fg=None, font_size=10):
        # Установка цвета фона по умолчанию
        bg = bg or colors['bg_color']
        # Установка цвета текста по умолчанию
        fg = fg or colors['text_color']
        # Создание и возврат метки
        return tk.Label(
            parent,  # Родительский виджет
            text=text,  # Текст метки
            bg=bg,  # Цвет фона
            fg=fg,  # Цвет текста
            font=("Arial", font_size)  # Шрифт и размер
        )

    # Функция для создания кнопки
    def create_button(parent, text, command, width=50, font_size=9):
        # Создание и возврат кнопки
        return tk.Button(
            parent,  # Родительский виджет
            text=text,  # Текст на кнопке
            command=command,  # Команда, выполняемая при нажатии
            bg=colors['btn_color'],  # Цвет фона кнопки
            fg=colors['text_color'],  # Цвет текста кнопки
            width=width,  # Ширина кнопки в символах
            font=("Arial", font_size)  # Шрифт и размер текста
        )

    # Функция для создания выпадающего меню
    def create_option_menu(parent, variable, options, width=50):
        # Создание выпадающего меню
        menu = tk.OptionMenu(parent, variable, *options)
        # Настройка внешнего вида меню
        menu.config(
            bg=colors['btn_color'],  # Цвет фона
            fg=colors['text_color'],  # Цвет текста
            width=width,  # Ширина в символах
            font=("Arial", 9)  # Шрифт и размер
        )
        return menu  # Возврат созданного меню

    # Функция для применения цветовой схемы
    def apply_colors():
        # Настройка фона главного окна
        root_window.configure(bg=colors['bg_color'])
        # Обход всех дочерних виджетов
        for widget in root_window.winfo_children():
            # Для кнопок
            if isinstance(widget, tk.Button):
                # Настройка цветов кнопки
                widget.configure(bg=colors['btn_color'], fg=colors['text_color'])
            # Для текстовых меток
            elif isinstance(widget, tk.Label):
                # Настройка цветов метки
                widget.configure(bg=colors['bg_color'], fg=colors['text_color'])
            # Для полей ввода
            elif isinstance(widget, tk.Entry):
                # Настройка цветов поля ввода
                widget.configure(bg=colors['entry_bg'], fg=colors['text_color'])
            # Для выпадающих меню
            elif isinstance(widget, tk.OptionMenu):
                # Настройка цветов меню
                widget.configure(bg=colors['btn_color'], fg=colors['text_color'])

    # Функция для отображения сообщения об успехе
    def show_success_message(title, message):
        # Создание окна для сообщения
        success_window = tk.Toplevel(root_window)
        # Установка заголовка окна
        success_window.title(title)
        # Настройка фона окна
        success_window.configure(bg=colors['success_bg'])

        # Создание текстовой метки с сообщением
        label = tk.Label(
            success_window,  # Родительское окно
            text=message,  # Текст сообщения
            bg=colors['success_bg'],  # Цвет фона
            fg=colors['success_fg'],  # Цвет текста
            font=("Arial", 11),  # Шрифт и размер
            wraplength=380  # Максимальная ширина текста перед переносом
        )
        # Размещение метки с заполнением пространства
        label.pack(expand=True, padx=20, pady=20)

        # Создание кнопки "OK"
        button = tk.Button(
            success_window,  # Родительское окно
            text="OK",  # Текст на кнопке
            command=success_window.destroy,  # Закрытие окна при нажатии
            bg=colors['btn_color'],  # Цвет фона кнопки
            fg=colors['text_color'],  # Цвет текста кнопки
            width=15,  # Ширина кнопки
            font=("Arial", 9)  # Шрифт и размер
        )
        # Размещение кнопки с отступами
        button.pack(pady=(0, 15))

        # Обновление геометрии окна для корректного расчета размеров
        success_window.update_idletasks()
        # Расчет минимальной ширины окна
        req_width = max(400, success_window.winfo_reqwidth())
        # Расчет минимальной высоты окна
        req_height = max(150, success_window.winfo_reqheight())

        # Получение размеров экрана
        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()
        # Расчет позиции для центрирования окна
        x = (screen_width - req_width) // 2
        y = (screen_height - req_height) // 2
        # Установка размеров и позиции окна
        success_window.geometry(f"{req_width}x{req_height}+{x}+{y}")
        # Запрет изменения размеров окна
        success_window.resizable(False, False)

    # Функция для настройки цветов интерфейса
    def configure_colors():
        # Создание окна для настройки цветов
        color_window = create_toplevel("Настройки цветов | Color Settings", 300, 300)

        # Функция для обновления цвета
        def update_color(color_var, color_key):
            # Получение нового цвета из переменной
            new_color = color_var.get()
            if new_color:
                # Обновление цвета в схеме
                colors[color_key] = new_color
                # Применение новых цветов
                apply_colors()

        # Создание элементов для настройки цвета фона
        create_label(color_window, "Цвет фона: | Background Color:").pack(pady=5)
        # Переменная для цвета фона
        bg_var = tk.StringVar(value=colors['bg_color'])
        # Поле ввода для цвета фона
        tk.Entry(color_window, textvariable=bg_var).pack(pady=5)
        # Кнопка для применения цвета фона
        create_button(color_window, "Применить | Apply", lambda: update_color(bg_var, 'bg_color'), width=20).pack(
            pady=5)

        # Создание элементов для настройки цвета кнопок
        create_label(color_window, "Цвет кнопок: | Button Color:").pack(pady=5)
        # Переменная для цвета кнопок
        btn_var = tk.StringVar(value=colors['btn_color'])
        # Поле ввода для цвета кнопок
        tk.Entry(color_window, textvariable=btn_var).pack(pady=5)
        # Кнопка для применения цвета кнопок
        create_button(color_window, "Применить | Apply", lambda: update_color(btn_var, 'btn_color'), width=20).pack(
            pady=5)

        # Создание элементов для настройки цвета текста
        create_label(color_window, "Цвет текста: | Text Color:").pack(pady=5)
        # Переменная для цвета текста
        text_var = tk.StringVar(value=colors['text_color'])
        # Поле ввода для цвета текста
        tk.Entry(color_window, textvariable=text_var).pack(pady=5)
        # Кнопка для применения цвета текста
        create_button(color_window, "Применить | Apply", lambda: update_color(text_var, 'text_color'), width=20).pack(
            pady=5)

        # Создание элементов для настройки фона полей ввода
        create_label(color_window, "Фон полей ввода: | Entry Background:").pack(pady=5)
        # Переменная для фона полей ввода
        entry_var = tk.StringVar(value=colors['entry_bg'])
        # Поле ввода для фона полей ввода
        tk.Entry(color_window, textvariable=entry_var).pack(pady=5)
        # Кнопка для применения фона полей ввода
        create_button(color_window, "Применить | Apply", lambda: update_color(entry_var, 'entry_bg'), width=20).pack(
            pady=5)

    # Функция для изменения пароля администратора
    def change_admin_password():
        global admin_password  # Использование глобальной переменной
        # Запрос текущего пароля
        current = simpledialog.askstring("Смена пароля | Password Change",
                                         "Введите текущий пароль: | Enter current password:", show='*')
        # Проверка правильности текущего пароля
        if current != admin_password:
            # Отображение сообщения об ошибке
            messagebox.showerror("Ошибка | Error", "Неверный текущий пароль! | Incorrect current password!")
            return

        # Запрос нового пароля
        new_pass = simpledialog.askstring("Смена пароля | Password Change",
                                          "Введите новый пароль: | Enter new password:", show='*')
        # Подтверждение нового пароля
        confirm = simpledialog.askstring("Смена пароля | Password Change",
                                         "Подтвердите новый пароль: | Confirm new password:", show='*')

        # Проверка совпадения паролей
        if new_pass and new_pass == confirm:
            # Установка нового пароля
            admin_password = new_pass
            # Отображение сообщения об успехе
            show_success_message("Успех | Success", "Пароль успешно изменен! | Password changed successfully!")
            # Запись в лог об изменении пароля
            logging.info("Пароль администратора изменен. | Admin password changed.")
        else:
            # Отображение сообщения об ошибке
            messagebox.showerror("Ошибка | Error", "Пароли не совпадают! | Passwords do not match!")

    # Функция для аутентификации администратора
    def authenticate_admin():
        # Запрос пароля администратора
        password = simpledialog.askstring("Аутентификация | Authentication",
                                          "Введите пароль администратора: | Enter admin password:", show='*')
        # Проверка правильности пароля
        return password == admin_password

    # Функция для просмотра объектов зоопарка (животных и сотрудников)
    def view_entities():
        # Создание окна для просмотра объектов
        view_window = create_toplevel("Объекты зоопарка | Zoo Entities", 650, 450)

        # Словарь для перевода типов объектов на два языка
        type_translations = {
            "Bird": "Птица | Bird",
            "Mammal": "Млекопитающее | Mammal",
            "Reptile": "Рептилия | Reptile",
            "ZooKeeper": "Смотритель | ZooKeeper",
            "Veterinarian": "Ветеринар | Veterinarian"
        }

        # Создание стиля для вкладок
        style = ttk.Style()
        # Настройка стиля панели вкладок
        style.configure("TNotebook", background=colors['bg_color'])
        # Настройка стиля отдельных вкладок
        style.configure("TNotebook.Tab",
                        background=colors['tab_bg'],
                        foreground=colors['tab_fg'],
                        font=("Arial", 10, "bold"),
                        padding=[10, 5])
        # Настройка цвета активной вкладки
        style.map("TNotebook.Tab",
                  background=[("selected", colors['accent_color'])])

        # Создание панели вкладок
        notebook = ttk.Notebook(view_window)
        # Размещение панели вкладок с заполнением пространства
        notebook.pack(fill='both', expand=True)

        # Создание фрейма для вкладки животных
        animals_frame = ttk.Frame(notebook)
        # Добавление вкладки животных с названием
        notebook.add(animals_frame, text="Животные | Animals")

        # Создание фрейма для вкладки сотрудников
        staff_frame = ttk.Frame(notebook)
        # Добавление вкладки сотрудников с названием
        notebook.add(staff_frame, text="Сотрудники | Staff")

        # Функция для обновления данных в таблицах
        def refresh_data():
            # Очистка таблицы животных
            animal_tree.delete(*animal_tree.get_children())
            # Перебор всех животных в зоопарке
            for animal in zoo.animals:
                # Получение переведенного типа животного
                animal_type = type_translations.get(animal.__class__.__name__, animal.__class__.__name__)
                # Добавление животного в таблицу
                animal_tree.insert("", "end", values=(animal.name, animal.age, animal_type))

            # Очистка таблицы персонала
            staff_tree.delete(*staff_tree.get_children())
            # Перебор всех сотрудников в зоопарке
            for staff_member in zoo.staff:
                # Получение переведенного типа сотрудника
                staff_type = type_translations.get(staff_member.__class__.__name__, staff_member.__class__.__name__)
                # Добавление сотрудника в таблицу
                staff_tree.insert("", "end", values=(staff_member.name, staff_type))

        # Названия столбцов для таблицы животных
        animal_columns = ("Имя | Name", "Возраст | Age", "Тип | Type")
        # Создание таблицы для животных
        animal_tree = ttk.Treeview(animals_frame, columns=animal_columns, show="headings")
        # Настройка заголовков столбцов
        for col in animal_columns:
            animal_tree.heading(col, text=col)  # Установка названия столбца
            animal_tree.column(col, width=100)  # Установка ширины столбца
        # Размещение таблицы с заполнением пространства
        animal_tree.pack(fill='both', expand=True)

        # Названия столбцов для таблицы персонала
        staff_columns = ("Имя | Name", "Должность | Position")
        # Создание таблицы для персонала
        staff_tree = ttk.Treeview(staff_frame, columns=staff_columns, show="headings")
        # Настройка заголовков столбцов
        for col in staff_columns:
            staff_tree.heading(col, text=col)  # Установка названия столбца
            staff_tree.column(col, width=100)  # Установка ширины столбца
        # Размещение таблицы с заполнением пространства
        staff_tree.pack(fill='both', expand=True)

        # Первоначальное заполнение таблиц данными
        refresh_data()

        # Функция для применения фильтра
        def apply_filter():
            # Получение текста фильтра и приведение к нижнему регистру
            filter_text = filter_entry.get().lower()
            # Получение выбранного типа для фильтрации
            selected_type = filter_type_var.get()

            # Очистка таблицы животных
            animal_tree.delete(*animal_tree.get_children())
            # Применение фильтра к животным
            for animal in zoo.animals:
                # Проверка соответствия типу и имени
                if selected_type == "Все | All" or animal.__class__.__name__ == selected_type.split(" | ")[0]:
                    if filter_text in animal.name.lower():
                        # Получение переведенного типа
                        animal_type = type_translations.get(animal.__class__.__name__, animal.__class__.__name__)
                        # Добавление животного в таблицу
                        animal_tree.insert("", "end", values=(animal.name, animal.age, animal_type))

            # Очистка таблицы персонала
            staff_tree.delete(*staff_tree.get_children())
            # Применение фильтра к сотрудникам
            for staff_member in zoo.staff:
                # Проверка соответствия типу и имени
                if selected_type == "Все | All" or staff_member.__class__.__name__ == selected_type.split(" | ")[0]:
                    if filter_text in staff_member.name.lower():
                        # Получение переведенного типа
                        staff_type = type_translations.get(staff_member.__class__.__name__,
                                                           staff_member.__class__.__name__)
                        # Добавление сотрудника в таблицу
                        staff_tree.insert("", "end", values=(staff_member.name, staff_type))

        # Создание фрейма для элементов фильтрации
        filter_frame = tk.Frame(view_window, bg=colors['bg_color'])
        # Размещение фрейма с отступами
        filter_frame.pack(fill='x', padx=5, pady=5)

        # Создание первой строки фильтра
        filter_row1 = tk.Frame(filter_frame, bg=colors['bg_color'])
        filter_row1.pack(fill='x', pady=5)

        # Создание метки для фильтра
        create_label(filter_row1, "Фильтр: | Filter:").pack(side='left')
        # Создание поля ввода для фильтра
        filter_entry = tk.Entry(filter_row1)
        # Размещение поля ввода с отступами и заполнением по горизонтали
        filter_entry.pack(side='left', padx=5, fill='x', expand=True)

        # Создание второй строки фильтра
        filter_row2 = tk.Frame(filter_frame, bg=colors['bg_color'])
        filter_row2.pack(fill='x', pady=5)

        # Переменная для типа фильтра
        filter_type_var = tk.StringVar(value="Все | All")
        # Список типов для фильтрации
        filter_types = ["Все | All", "Bird | Птица", "Mammal | Млекопитающее", "Reptile | Рептилия",
                        "ZooKeeper | Смотритель", "Veterinarian | Ветеринар"]
        # Создание метки для типа
        create_label(filter_row2, "Тип: | Type:").pack(side='left')
        # Создание выпадающего меню для выбора типа
        filter_menu = create_option_menu(filter_row2, filter_type_var, filter_types, width=25)
        # Размещение меню с отступом
        filter_menu.pack(side='left', padx=5)

        # Создание кнопки для применения фильтра
        apply_filter_btn = create_button(filter_row2, "Применить фильтр | Apply Filter", apply_filter, width=30,
                                         font_size=9)
        # Размещение кнопки с отступом
        apply_filter_btn.pack(side='left', padx=5)

        # Функция для удаления выбранной сущности
        def delete_entity():
            # Проверка аутентификации администратора
            if not authenticate_admin():
                # Отображение сообщения об ошибке аутентификации
                messagebox.showerror("Ошибка | Error",
                                     "Ошибка аутентификации администратора! | Admin authentication failed!")
                return

            # Определение текущей активной вкладки
            current_tab = notebook.index(notebook.select())

            # Если активна вкладка животных
            if current_tab == 0:
                # Получение выбранных элементов
                selected = animal_tree.selection()
                # Проверка наличия выбранных элементов
                if not selected:
                    return
                # Получение данных выбранного элемента
                item_data = animal_tree.item(selected[0])
                # Извлечение имени животного
                name = item_data['values'][0]

                # Подтверждение удаления
                if messagebox.askyesno("Подтверждение | Confirm", f"Удалить животное {name}? | Delete animal {name}?"):
                    # Поиск и удаление животного
                    for animal in zoo.animals[:]:
                        if animal.name == name:
                            zoo.animals.remove(animal)
                            # Запись в лог об удалении
                            logging.info(f"Животное {name} удалено. | Animal {name} deleted.")
                            break
                    # Обновление данных
                    refresh_data()

            # Если активна вкладка персонала
            elif current_tab == 1:
                # Получение выбранных элементов
                selected = staff_tree.selection()
                # Проверка наличия выбранных элементов
                if not selected:
                    return
                # Получение данных выбранного элемента
                item_data = staff_tree.item(selected[0])
                # Извлечение имени сотрудника
                name = item_data['values'][0]

                # Подтверждение удаления
                if messagebox.askyesno("Подтверждение | Confirm",
                                       f"Удалить сотрудника {name}? | Delete staff member {name}?"):
                    # Поиск и удаление сотрудника
                    for staff_member in zoo.staff[:]:
                        if staff_member.name == name:
                            zoo.staff.remove(staff_member)
                            # Запись в лог об удалении
                            logging.info(f"Сотрудник {name} удален. | Staff {name} deleted.")
                            break
                    # Обновление данных
                    refresh_data()

        # Функция для редактирования выбранной сущности
        def edit_entity():
            # Проверка аутентификации администратора
            if not authenticate_admin():
                # Отображение сообщения об ошибке аутентификации
                messagebox.showerror("Ошибка | Error",
                                     "Ошибка аутентификации администратора! | Admin authentication failed!")
                return

            # Определение текущей активной вкладки
            current_tab = notebook.index(notebook.select())
            # Получение выбранных элементов в зависимости от вкладки
            selected = animal_tree.selection() if current_tab == 0 else staff_tree.selection()

            # Проверка наличия выбранных элементов
            if not selected:
                return

            # Если активна вкладка животных
            if current_tab == 0:
                # Получение данных выбранного элемента
                item_data = animal_tree.item(selected[0])
                # Извлечение данных о животном
                name, age, animal_class = item_data['values']
                # Поиск животного по имени
                animal = next((a for a in zoo.animals if a.name == name), None)
                # Проверка найден ли объект
                if not animal:
                    return

                # Увеличение высоты окна редактирования до 220 пикселей
                edit_window = create_toplevel("Редактировать животное | Edit Animal", 450, 220)

                # Создание фрейма для формы редактирования
                form_frame = tk.Frame(edit_window, bg=colors['bg_color'])
                # Размещение фрейма с отступами и заполнением пространства
                form_frame.pack(fill='both', padx=20, pady=10, expand=True)

                # Создание метки для нового имени
                create_label(form_frame, "Новое имя: | New Name:").pack(anchor='w', pady=5)
                # Переменная для нового имени
                name_var = tk.StringVar(value=name)
                # Создание поля ввода для имени
                name_entry_edit = tk.Entry(
                    form_frame,  # Родительский виджет
                    textvariable=name_var,  # Привязанная переменная
                    width=40,  # Ширина в символах
                    bg=colors['entry_bg'],  # Цвет фона
                    fg=colors['text_color']  # Цвет текста
                )
                # Размещение поля ввода с заполнением по горизонтали
                name_entry_edit.pack(fill='x', pady=5)

                # Создание метки для нового возраста
                create_label(form_frame, "Новый возраст: | New Age:").pack(anchor='w', pady=5)
                # Переменная для нового возраста
                age_var = tk.StringVar(value=str(age))
                # Создание поля ввода для возраста
                age_entry_edit = tk.Entry(
                    form_frame,  # Родительский виджет
                    textvariable=age_var,  # Привязанная переменная
                    width=40,  # Ширина в символах
                    bg=colors['entry_bg'],  # Цвет фона
                    fg=colors['text_color']  # Цвет текста
                )
                # Размещение поля ввода с заполнением по горизонтали
                age_entry_edit.pack(fill='x', pady=5)

                # Функция для сохранения изменений
                def save_changes():
                    # Получение нового имени из переменной
                    new_name = name_var.get()
                    try:
                        # Преобразование возраста в число
                        new_age = float(age_var.get())
                        # Проверка на положительное значение
                        if new_age <= 0:
                            raise ValueError
                    except ValueError:
                        # Отображение сообщения об ошибке
                        messagebox.showerror("Ошибка | Error", "Некорректное значение возраста! | Invalid age value!")
                        return

                    # Обновление имени животного
                    animal.name = new_name
                    # Обновление возраста животного
                    animal.age = new_age
                    # Запись в лог об обновлении
                    logging.info(f"Животное {name} обновлено: {new_name}, возраст {new_age}")
                    # Обновление данных в таблице
                    refresh_data()
                    # Закрытие окна редактирования
                    edit_window.destroy()
                    # Отображение сообщения об успехе
                    show_success_message("Успех | Success", "Данные животного обновлены! | Animal updated!")

                # Создание фрейма для кнопки
                button_frame = tk.Frame(edit_window, bg=colors['bg_color'])
                # Размещение фрейма с увеличенным отступом снизу
                button_frame.pack(fill='x', padx=20, pady=20)
                # Создание кнопки сохранения
                create_button(button_frame, "Сохранить | Save", save_changes, width=20).pack(pady=5)

            # Если активна вкладка персонала
            elif current_tab == 1:
                # Получение данных выбранного элемента
                item_data = staff_tree.item(selected[0])
                # Извлечение имени сотрудника
                name = item_data['values'][0]
                # Поиск сотрудника по имени
                staff = next((s for s in zoo.staff if s.name == name), None)
                # Проверка найден ли объект
                if not staff:
                    return

                # Увеличение высоты окна редактирования до 220 пикселей
                edit_window = create_toplevel("Редактировать сотрудника | Edit Staff", 450, 220)

                # Создание фрейма для формы редактирования
                form_frame = tk.Frame(edit_window, bg=colors['bg_color'])
                # Размещение фрейма с отступами и заполнением пространства
                form_frame.pack(fill='both', padx=20, pady=10, expand=True)

                # Создание метки для нового имени
                create_label(form_frame, "Новое имя: | New Name:").pack(anchor='w', pady=5)
                # Переменная для нового имени
                name_var = tk.StringVar(value=name)
                # Создание поля ввода для имени
                name_entry_edit = tk.Entry(
                    form_frame,  # Родительский виджет
                    textvariable=name_var,  # Привязанная переменная
                    width=40,  # Ширина в символах
                    bg=colors['entry_bg'],  # Цвет фона
                    fg=colors['text_color']  # Цвет текста
                )
                # Размещение поля ввода с заполнением по горизонтали
                name_entry_edit.pack(fill='x', pady=5)

                # Функция для сохранения изменений
                def save_changes():
                    # Получение нового имени из переменной
                    new_name = name_var.get()
                    # Обновление имени сотрудника
                    staff.name = new_name
                    # Запись в лог об обновлении
                    logging.info(f"Сотрудник {name} обновлен: {new_name}")
                    # Обновление данных в таблице
                    refresh_data()
                    # Закрытие окна редактирования
                    edit_window.destroy()
                    # Отображение сообщения об успехе
                    show_success_message("Успех | Success", "Данные сотрудника обновлены! | Staff updated!")

                # Создание фрейма для кнопки
                button_frame = tk.Frame(edit_window, bg=colors['bg_color'])
                # Размещение фрейма с увеличенным отступом снизу
                button_frame.pack(fill='x', padx=20, pady=20)
                # Создание кнопки сохранения
                create_button(button_frame, "Сохранить | Save", save_changes, width=20).pack(pady=5)

        # Создание фрейма для кнопок управления
        btn_frame = tk.Frame(view_window, bg=colors['bg_color'])
        # Размещение фрейма с отступами
        btn_frame.pack(fill='x', padx=5, pady=5)

        # Создание кнопки удаления
        delete_btn = create_button(btn_frame, "Удалить выбранное | Delete Selected", delete_entity, width=28,
                                   font_size=9)
        # Размещение кнопки слева с заполнением пространства
        delete_btn.pack(side='left', padx=2, fill='x', expand=True)

        # Создание кнопки редактирования
        edit_btn = create_button(btn_frame, "Редактировать выбранное | Edit Selected", edit_entity, width=30,
                                 font_size=9)
        # Размещение кнопки слева с заполнением пространства
        edit_btn.pack(side='left', padx=2, fill='x', expand=True)

        # Создание кнопки обновления
        refresh_btn = create_button(btn_frame, "Обновить | Refresh", refresh_data, width=18, font_size=9)
        # Размещение кнопки справа с заполнением пространства
        refresh_btn.pack(side='right', padx=2, fill='x', expand=True)

    # Функция для воспроизведения звука животного
    def play_animal_sound():
        # Проверка наличия животных в зоопарке
        if not zoo.animals:
            # Отображение информационного сообщения
            messagebox.showinfo("Информация | Info", "В зоопарке пока нет животных. | No animals in the zoo yet.")
            return

        # Создание окна для воспроизведения звуков
        sound_window = create_toplevel("Воспроизвести звук животного | Play Animal Sound", 350, 180)

        # Создание метки для выбора животного
        create_label(sound_window, "Выберите животное: | Select an animal:").pack(pady=10)

        # Переменная для выбранного животного
        animal_var = tk.StringVar()
        # Список имен животных
        animal_names = [animal.name for animal in zoo.animals]
        # Проверка наличия животных
        if not animal_names:
            # Создание метки об отсутствии животных
            create_label(sound_window, "Нет животных для воспроизведения звука. | No animals available.").pack()
            return

        # Создание выпадающего меню для выбора животного
        animal_menu = create_option_menu(sound_window, animal_var, animal_names)
        # Размещение меню с отступом
        animal_menu.pack(pady=5)

        # Функция для воспроизведения звука
        def play_sound():
            # Получение выбранного имени
            selected_name = animal_var.get()
            # Проверка выбора
            if not selected_name:
                return

            # Поиск животного по имени
            animal = next((a for a in zoo.animals if a.name == selected_name), None)
            # Проверка найден ли объект
            if animal:
                # Воспроизведение звука животного
                animal.make_sound()
                # Запись в лог о воспроизведении
                logging.info(f"Воспроизведен звук животного: {animal.name}")

        # Создание кнопки воспроизведения звука
        create_button(sound_window, "Воспроизвести звук | Play Sound", play_sound, width=30).pack(pady=10)

    # Функция для добавления животного через GUI
    def add_animal_gui():
        # Получение имени животного из поля ввода
        name = name_entry.get()
        # Проверка введено ли имя
        if not name:
            # Отображение сообщения об ошибке
            messagebox.showerror("Ошибка | Error", "Введите имя животного! | Enter animal name!")
            return

        try:
            # Преобразование возраста в число
            age = float(age_entry.get())
            # Проверка на положительное значение
            if age <= 0:
                raise ValueError
        except ValueError:
            # Отображение сообщения об ошибке
            messagebox.showerror("Ошибка | Error",
                                 "Возраст должен быть положительным числом! | Age must be a positive number!")
            return

        # Получение выбранного типа животного
        full_type = animal_type_var.get()
        # Разделение строки на части (русское и английское название)
        parts = full_type.split(" | ")
        # Русское название типа
        russian_type = parts[0]
        # Английское название типа (если есть, иначе русское)
        english_type = parts[1] if len(parts) > 1 else russian_type

        # Создание животного в зависимости от выбранного типа
        if russian_type == "Птица":
            animal = Bird(name, age)
        elif russian_type == "Млекопитающее":
            animal = Mammal(name, age)
        elif russian_type == "Рептилия":
            animal = Reptile(name, age)
        else:
            # Отображение сообщения об ошибке
            messagebox.showerror("Ошибка | Error", "Выберите тип животного! | Select animal type!")
            return

        # Добавление животного в зоопарк
        zoo.add_animal(animal)
        # Отображение сообщения об успехе
        show_success_message("Успех | Success",
                             f"{russian_type} {name} добавлен в зоопарк. | {english_type} {name} added to zoo.")
        # Запись в лог о добавлении животного
        logging.info(f"Добавлено животное: {name} ({russian_type})")

        # Очистка поля ввода имени
        name_entry.delete(0, tk.END)
        # Очистка поля ввода возраста
        age_entry.delete(0, tk.END)

    # Функция для добавления смотрителя
    def add_keeper():
        # Получение имени смотрителя из поля ввода
        name = keeper_entry.get()
        # Проверка введено ли имя
        if not name:
            # Отображение сообщения об ошибке
            messagebox.showerror("Ошибка | Error", "Введите имя смотрителя! | Enter keeper name!")
            return

        # Добавление смотрителя в зоопарк
        zoo.add_staff(ZooKeeper(name))
        # Отображение сообщения об успехе
        show_success_message("Успех | Success", f"Смотритель {name} добавлен. | ZooKeeper {name} added.")
        # Запись в лог о добавлении смотрителя
        logging.info(f"Добавлен сотрудник: {name} (Смотритель)")
        # Очистка поля ввода
        keeper_entry.delete(0, tk.END)

    # Функция для добавления ветеринара
    def add_vet():
        # Получение имени ветеринара из поля ввода
        name = vet_entry.get()
        # Проверка введено ли имя
        if not name:
            # Отображение сообщения об ошибке
            messagebox.showerror("Ошибка | Error", "Введите имя ветеринара! | Enter veterinarian name!")
            return

        # Добавление ветеринара в зоопарк
        zoo.add_staff(Veterinarian(name))
        # Отображение сообщения об успехе
        show_success_message("Успех | Success", f"Ветеринар {name} добавлен. | Veterinarian {name} added.")
        # Запись в лог о добавлении ветеринара
        logging.info(f"Добавлен сотрудник: {name} (Ветеринар)")
        # Очистка поле ввода
        vet_entry.delete(0, tk.END)

    # Функция для сохранения зоопарка в файл
    def save_zoo():
        # Открытие диалога сохранения файла
        save_filename = filedialog.asksaveasfilename(
            defaultextension=".pkl",  # Расширение по умолчанию
            # Фильтры типов файлов
            filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
            title="Сохранить зоопарк | Save Zoo"  # Заголовок диалога
        )
        # Проверка выбран ли файл
        if save_filename:
            # Попытка сохранения зоопарка
            if zoo.save_zoo(save_filename):
                # Отображение сообщения об успехе
                show_success_message("Успех | Success",
                                     f"Зоопарк сохранен в {os.path.basename(save_filename)} | Zoo saved to {os.path.basename(save_filename)}")
                # Запись в лог о сохранении
                logging.info(f"Зоопарк сохранен в {save_filename}")
            else:
                # Отображение сообщения об ошибке
                messagebox.showerror("Ошибка | Error", "Не удалось сохранить зоопарк! | Failed to save zoo!")

    # Функция для загрузки зоопарка из файла
    def load_zoo():
        # Открытие диалога выбора файла
        load_filename = filedialog.askopenfilename(
            # Фильтры типов файлов
            filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
            title="Загрузить зоопарк | Load Zoo"  # Заголовок диалога
        )
        # Проверка выбран ли файл
        if load_filename:
            try:
                # Загрузка зоопарка из файла
                loaded_zoo = Zoo.load_zoo(load_filename)
                # Обновление списка животных
                zoo.animals = loaded_zoo.animals
                # Обновление списка сотрудников
                zoo.staff = loaded_zoo.staff
                # Обновление названия зоопарка
                zoo.name = loaded_zoo.name
                # Обновление заголовка главного окна
                root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
                # Отображение сообщения об успехе
                show_success_message("Успех | Success",
                                     f"Зоопарк загружен из {os.path.basename(load_filename)} | Zoo loaded from {os.path.basename(load_filename)}")
                # Запись в лог о загрузке
                logging.info(f"Зоопарк загружен из {load_filename}")
            except Exception as load_exc:  # Обработка ошибок загрузки
                # Запись ошибки в лог
                logging.error(f"Ошибка загрузки зоопарка: {load_exc}")
                # Предложение создать новый зоопарк при ошибке
                if messagebox.askyesno("Ошибка | Error",
                                       "Не удалось загрузить зоопарк. Создать новый? | Failed to load zoo. Create new zoo?"):
                    # Очистка списка животных
                    zoo.animals = []
                    # Очистка списка сотрудников
                    zoo.staff = []
                    # Установка нового названия зоопарка
                    zoo.name = "Новый зоопарк | New Zoo"
                    # Обновление заголовка главного окна
                    root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
                    # Запись в лог о создании нового зоопарка
                    logging.info("Создан новый зоопарк после ошибки загрузки")

    # Установка единой ширины для элементов интерфейса
    element_width = 50  # Ширина в символах

    # Создание метки для секции добавления животных
    create_label(root_window, "Добавление животных | Add Animals", font_size=11).pack(pady=(10, 5))

    # Создание метки для поля ввода имени животного
    create_label(root_window, "Имя животного: | Animal Name:").pack()
    # Создание поля ввода для имени животного
    name_entry = tk.Entry(root_window, width=element_width, bg=colors['entry_bg'], fg=colors['text_color'])
    # Размещение поля ввода с отступом
    name_entry.pack(pady=2)

    # Создание метки для поля ввода возраста животного
    create_label(root_window, "Возраст (месяцев): | Age (months):").pack()
    # Создание поля ввода для возраста животного
    age_entry = tk.Entry(root_window, width=element_width, bg=colors['entry_bg'], fg=colors['text_color'])
    # Размещение поля ввода с отступом
    age_entry.pack(pady=2)

    # Переменная для выбранного типа животного
    animal_type_var = tk.StringVar(value="Птица | Bird")
    # Создание метки для выбора типа животного
    create_label(root_window, "Выберите Тип животного: | Select Animal Type:").pack(pady=2)

    # Список типов животных
    animal_types = ["Птица | Bird", "Млекопитающее | Mammal", "Рептилия | Reptile"]
    # Создание выпадающего меню для выбора типа животного
    animal_type_menu = create_option_menu(root_window, animal_type_var, animal_types, width=element_width)
    # Размещение меню с отступом (фиксированная ширина)
    animal_type_menu.pack(pady=2)

    # Создание кнопки для добавления животного
    create_button(root_window, "Добавить животное | Add Animal", add_animal_gui, width=element_width).pack(pady=7)

    # Создание метки для секции добавления персонала
    create_label(root_window, "Добавление персонала | Add Staff", font_size=11).pack(pady=(15, 5))

    # Создание метки для поля ввода имени смотрителя
    create_label(root_window, "Имя смотрителя: | ZooKeeper Name:").pack()
    # Создание поля ввода для имени смотрителя
    keeper_entry = tk.Entry(root_window, width=element_width, bg=colors['entry_bg'], fg=colors['text_color'])
    # Размещение поля ввода с отступом
    keeper_entry.pack(pady=2)

    # Создание кнопки для добавления смотрителя
    create_button(root_window, "Добавить смотрителя | Add ZooKeeper", add_keeper, width=element_width).pack(pady=7)

    # Создание метки для поля ввода имени ветеринара
    create_label(root_window, "Имя ветеринара: | Veterinarian Name:").pack()
    # Создание поля ввода для имени ветеринара
    vet_entry = tk.Entry(root_window, width=element_width, bg=colors['entry_bg'], fg=colors['text_color'])
    # Размещение поля ввода с отступом
    vet_entry.pack(pady=2)

    # Создание кнопки для добавления ветеринара
    create_button(root_window, "Добавить ветеринара | Add Veterinarian", add_vet, width=element_width).pack(pady=7)

    # Создание кнопки для воспроизведения звука животного
    create_button(root_window, "Воспроизвести звук животного | Play Animal Sound", play_animal_sound,
                  width=element_width).pack(pady=7)
    # Создание кнопки для просмотра объектов зоопарка
    create_button(root_window, "Просмотр животных и персонала | View Animals and Staff", view_entities,
                  width=element_width).pack(pady=7)
    # Создание кнопки для сохранения зоопарка
    create_button(root_window, "Сохранить зоопарк | Save Zoo", save_zoo, width=element_width).pack(pady=7)
    # Создание кнопки для загрузки зоопарка
    create_button(root_window, "Загрузить зоопарк | Load Zoo", load_zoo, width=element_width).pack(pady=7)
    # Создание кнопки для смены пароля администратора
    create_button(root_window, "Сменить пароль администратора | Change Admin Password", change_admin_password,
                  width=element_width).pack(pady=7)
    # Создание кнопки для настройки цветов
    create_button(root_window, "Настройки цветов | Color Settings", configure_colors, width=element_width).pack(pady=7)
    # Создание кнопки для выхода из приложения
    create_button(root_window, "Выход | Exit", root_window.destroy, width=element_width).pack(pady=12)

    # Применение цветовой схемы
    apply_colors()
    # Запуск главного цикла обработки событий
    root_window.mainloop()


# Основной блок выполнения программы
if __name__ == "__main__":
    zoo_instance = None  # Переменная для экземпляра зоопарка

    try:
        # Попытка загрузить последнее состояние зоопарка
        zoo_instance = Zoo.load_zoo("last_zoo.pkl")
        # Запись в лог об успешной загрузке
        logging.info("Автоматически загружено состояние зоопарка")
    except Exception as auto_load_error:  # Обработка ошибок загрузки
        # Запись предупреждения в лог
        logging.warning(f"Ошибка автоматической загрузки: {auto_load_error}")
        # Предложение создать новый зоопарк
        if messagebox.askyesno("Ошибка загрузки | Load Error",
                               "Не удалось загрузить зоопарк. Создать новый? | Failed to load zoo. Create new zoo?"):
            # Создание нового зоопарка
            zoo_instance = Zoo("Новый зоопарк | New Zoo")
            # Запись в лог о создании нового зоопарка
            logging.info("Создан новый зоопарк после ошибки загрузки")
        else:
            # Ручной выбор файла зоопарка
            manual_filename = filedialog.askopenfilename(
                # Фильтры типов файлов
                filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
                title="Выберите файл зоопарка | Select Zoo File"  # Заголовок диалога
            )
            # Проверка выбран ли файл
            if manual_filename:
                try:
                    # Загрузка зоопарка из выбранного файла
                    zoo_instance = Zoo.load_zoo(manual_filename)
                    # Запись в лог о ручной загрузке
                    logging.info(f"Ручная загрузка зоопарка из {manual_filename}")
                except Exception as manual_load_error:  # Обработка ошибок загрузки
                    # Запись ошибки в лог
                    logging.error(f"Ошибка ручной загрузки: {manual_load_error}")
                    # Отображение сообщения об ошибке
                    messagebox.showerror("Ошибка | Error",
                                         "Не удалось загрузить зоопарк. Создаётся новый. | Failed to load zoo. Creating new one.")
                    # Создание нового зоопарка
                    zoo_instance = Zoo("Новый зоопарк | New Zoo")
            else:
                # Создание нового зоопарка
                zoo_instance = Zoo("Новый зоопарк | New Zoo")

    # Проверка создан ли экземпляр зоопарка
    if zoo_instance:
        # Запуск графического интерфейса
        run_gui(zoo_instance)

    try:
        # Попытка сохранения состояния зоопарка при выходе
        zoo_instance.save_zoo("last_zoo.pkl")
        # Запись в лог об успешном сохранении
        logging.info("Состояние зоопарка сохранено при выходе")
    except Exception as save_exc:  # Обработка ошибок сохранения
        # Запись ошибки в лог
        logging.error(f"Ошибка сохранения при выходе: {save_exc}")