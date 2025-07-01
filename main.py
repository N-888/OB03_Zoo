# Импорт необходимых модулей
import tkinter as tk  # Основной модуль для создания GUI
from tkinter import messagebox, simpledialog, filedialog, ttk  # Компоненты Tkinter
import logging  # Модуль для логирования
import os  # Модуль для работы с операционной системой
import pickle  # Модуль для сериализации объектов

# Попытка импорта pygame для работы со звуками
try:
    import pygame  # Импорт библиотеки pygame

    pygame.mixer.init()  # Инициализация звукового модуля
    pygame_available = True  # Флаг доступности pygame
except ImportError:  # Обработка ошибки если pygame не установлен
    pygame = None  # Установка значения None для pygame
    pygame_available = False  # Установка флага недоступности
    print("Pygame не установлен, звуки отключены")  # Информационное сообщение

# Настройка системы логирования
logging.basicConfig(
    filename="zoo_log.txt",  # Имя файла для логов
    level=logging.INFO,  # Уровень логирования (INFO)
    format="%(asctime)s — %(levelname)s — %(message)s"  # Формат записей лога
)

# Пароль администратора по умолчанию
admin_password = "admin123"


# Класс Animal - базовый класс для всех животных
class Animal:
    # Конструктор класса Animal
    def __init__(self, name, age):
        self.name = name  # Имя животного
        self.age = age  # Возраст животного

    # Метод для издания звука (переопределяется в дочерних классах)
    def make_sound(self):
        pass  # Заглушка

    # Метод приема пищи
    def eat(self):
        logging.info(f"{self.name} ест.")  # Запись в лог
        print(f"{self.name} ест.")  # Вывод в консоль

    # Метод для строкового представления объекта
    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}, возраст {self.age} лет"  # Форматированная строка


# Класс Bird (Птица) - наследуется от Animal
class Bird(Animal):
    # Реализация метода издания звука для птицы
    def make_sound(self):
        logging.info(f"{self.name} чирикает.")  # Запись в лог
        print(f"{self.name} чирикает.")  # Вывод в консоль
        if pygame_available:  # Проверка доступности pygame
            try:
                pygame.mixer.music.load("bird_sound.mp3")  # Загрузка звукового файла
                pygame.mixer.music.play()  # Воспроизведение звука
            except Exception as e:  # Обработка исключений
                print(f"Ошибка воспроизведения звука птицы: {e}")  # Сообщение об ошибке


# Класс Mammal (Млекопитающее) - наследуется от Animal
class Mammal(Animal):
    # Реализация метода издания звука для млекопитающего
    def make_sound(self):
        logging.info(f"{self.name} рычит.")  # Запись в лог
        print(f"{self.name} рычит.")  # Вывод в консоль
        if pygame_available:  # Проверка доступности pygame
            try:
                pygame.mixer.music.load("mammal_sound.mp3")  # Загрузка звукового файла
                pygame.mixer.music.play()  # Воспроизведение звука
            except Exception as e:  # Обработка исключений
                print(f"Ошибка воспроизведения звука млекопитающего: {e}")  # Сообщение об ошибке


# Класс Reptile (Рептилия) - наследуется от Animal
class Reptile(Animal):
    # Реализация метода издания звука для рептилии
    def make_sound(self):
        logging.info(f"{self.name} шипит.")  # Запись в лог
        print(f"{self.name} шипит.")  # Вывод в консоль
        if pygame_available:  # Проверка доступности pygame
            try:
                pygame.mixer.music.load("reptile_sound.mp3")  # Загрузка звукового файла
                pygame.mixer.music.play()  # Воспроизведение звука
            except Exception as e:  # Обработка исключений
                print(f"Ошибка воспроизведения звука рептилии: {e}")  # Сообщение об ошибке


# Класс Zoo для управления зоопарком
class Zoo:
    # Конструктор класса Zoo
    def __init__(self, name):
        self.name = name  # Название зоопарка
        self.animals = []  # Список животных
        self.staff = []  # Список сотрудников

    # Метод добавления животного
    def add_animal(self, animal):
        self.animals.append(animal)  # Добавление животного в список
        logging.info(f"Животное {animal.name} добавлено в зоопарк.")  # Запись в лог

    # Метод добавления сотрудника
    def add_staff(self, staff_member):
        self.staff.append(staff_member)  # Добавление сотрудника в список
        logging.info(f"Сотрудник {staff_member.name} нанят.")  # Запись в лог

    # Метод сохранения состояния зоопарка в файл
    def save_zoo(self, filename="zoo_data.pkl"):
        try:
            with open(filename, 'wb') as file:  # Открытие файла для бинарной записи
                pickle.dump(self, file)  # Сериализация объекта зоопарка
            logging.info(f"Состояние зоопарка сохранено в {filename}.")  # Запись в лог
            return True  # Возврат успешного статуса
        except (IOError, pickle.PicklingError) as e:  # Обработка ошибок
            logging.error(f"Ошибка сохранения зоопарка: {e}")  # Запись ошибки
            return False  # Возврат статуса ошибки

    # Статический метод загрузки зоопарка из файла
    @staticmethod
    def load_zoo(filename="zoo_data.pkl"):
        try:
            with open(filename, 'rb') as file:  # Открытие файла для бинарного чтения
                zoo_obj = pickle.load(file)  # Десериализация объекта
            logging.info(f"Состояние зоопарка загружено из {filename}.")  # Запись в лог
            return zoo_obj  # Возврат загруженного объекта
        except FileNotFoundError:  # Обработка отсутствия файла
            logging.error(f"Файл {filename} не найден.")  # Запись ошибки
            raise  # Повторное возбуждение исключения
        except (IOError, pickle.UnpicklingError) as e:  # Обработка других ошибок
            logging.error(f"Ошибка загрузки зоопарка: {e}")  # Запись ошибки
            raise  # Повторное возбуждение исключения


# Базовый класс Staff для сотрудников
class Staff:
    # Конструктор класса Staff
    def __init__(self, name):
        self.name = name  # Имя сотрудника


# Класс ZooKeeper (Смотритель) - наследуется от Staff
class ZooKeeper(Staff):
    # Метод кормления животного
    def feed_animal(self, animal):
        logging.info(f"{self.name} кормит {animal.name}.")  # Запись в лог
        print(f"{self.name} кормит {animal.name}.")  # Вывод в консоль


# Класс Veterinarian (Ветеринар) - наследуется от Staff
class Veterinarian(Staff):
    # Метод лечения животного
    def heal_animal(self, animal):
        logging.info(f"{self.name} лечит {animal.name}.")  # Запись в лог
        print(f"{self.name} лечит {animal.name}.")  # Вывод в консоль


# Функция запуска графического интерфейса
def run_gui(zoo):
    # Создание главного окна
    root_window = tk.Tk()  # Создание экземпляра Tk
    # Установка заголовка окна
    root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
    root_window.geometry("500x750")  # Установка размеров окна

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

    root_window.configure(bg=colors['bg_color'])  # Установка фона главного окна

    # Попытка загрузки иконки приложения
    try:
        root_window.iconbitmap("zoo_logo.ico")  # Загрузка иконки
    except Exception as icon_exc:  # Обработка ошибки
        logging.warning(f"Иконка не найдена: {icon_exc}")  # Запись предупреждения

    # Функция создания дочернего окна
    def create_toplevel(title, width=400, height=300):
        window = tk.Toplevel(root_window)  # Создание дочернего окна
        window.title(title)  # Установка заголовка
        window.geometry(f"{width}x{height}")  # Установка размеров
        window.configure(bg=colors['bg_color'])  # Установка фона
        return window  # Возврат созданного окна

    # Функция создания метки
    def create_label(parent, text, bg=None, fg=None, font_size=10):
        bg = bg or colors['bg_color']  # Фон по умолчанию
        fg = fg or colors['text_color']  # Цвет текста по умолчанию
        return tk.Label(  # Создание и возврат метки
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Arial", font_size)
        )

    # Функция создания кнопки
    def create_button(parent, text, command, width=50, font_size=9):
        return tk.Button(  # Создание и возврат кнопки
            parent,
            text=text,
            command=command,
            bg=colors['btn_color'],
            fg=colors['text_color'],
            width=width,
            font=("Arial", font_size)
        )

    # Функция создания выпадающего меню
    def create_option_menu(parent, variable, options, width=50):
        menu = tk.OptionMenu(parent, variable, *options)  # Создание меню
        menu.config(  # Настройка внешнего вида
            bg=colors['btn_color'],
            fg=colors['text_color'],
            width=width,
            font=("Arial", 9)
        )
        return menu  # Возврат созданного меню

    # Функция применения цветовой схемы
    def apply_colors():
        root_window.configure(bg=colors['bg_color'])  # Обновление фона главного окна
        # Обновление цветов для всех дочерних виджетов
        for widget in root_window.winfo_children():
            if isinstance(widget, tk.Button):  # Для кнопок
                widget.configure(bg=colors['btn_color'], fg=colors['text_color'])
            elif isinstance(widget, tk.Label):  # Для меток
                widget.configure(bg=colors['bg_color'], fg=colors['text_color'])
            elif isinstance(widget, tk.Entry):  # Для полей ввода
                widget.configure(bg=colors['entry_bg'], fg=colors['text_color'])
            elif isinstance(widget, tk.OptionMenu):  # Для выпадающих меню
                widget.configure(bg=colors['btn_color'], fg=colors['text_color'])

    # Функция показа сообщения об успехе
    def show_success_message(title, message):
        success_window = tk.Toplevel(root_window)  # Создание окна сообщения
        success_window.title(title)  # Установка заголовка
        success_window.configure(bg=colors['success_bg'])  # Установка фона

        # Создание метки с сообщением
        label = tk.Label(
            success_window,
            text=message,
            bg=colors['success_bg'],
            fg=colors['success_fg'],
            font=("Arial", 11),
            wraplength=380  # Ширина переноса текста
        )
        label.pack(expand=True, padx=20, pady=20)  # Размещение метки

        # Создание кнопки OK
        button = tk.Button(
            success_window,
            text="OK",
            command=success_window.destroy,
            bg=colors['btn_color'],
            fg=colors['text_color'],
            width=15,
            font=("Arial", 9)
        )
        button.pack(pady=(0, 15))  # Размещение кнопки

        # Рассчет необходимого размера окна
        success_window.update_idletasks()  # Обновление геометрии
        req_width = max(400, success_window.winfo_reqwidth())  # Минимальная ширина 400
        req_height = max(150, success_window.winfo_reqheight())  # Минимальная высота 150

        # Центрирование окна на экране
        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()
        x = (screen_width - req_width) // 2
        y = (screen_height - req_height) // 2
        # Установка размеров и позиции
        success_window.geometry(f"{req_width}x{req_height}+{x}+{y}")
        success_window.resizable(False, False)  # Запрет изменения размера

    # Функция настройки цветов
    def configure_colors():
        color_window = create_toplevel("Настройки цветов | Color Settings", 300, 300)  # Создание окна

        # Функция обновления цвета
        def update_color(color_var, color_key):
            new_color = color_var.get()  # Получение нового цвета
            if new_color:
                colors[color_key] = new_color  # Обновление цветовой схемы
                apply_colors()  # Применение изменений

        # Элементы для настройки цвета фона
        create_label(color_window, "Цвет фона: | Background Color:").pack(pady=5)
        bg_var = tk.StringVar(value=colors['bg_color'])
        tk.Entry(color_window, textvariable=bg_var).pack(pady=5)
        create_button(color_window, "Применить | Apply", lambda: update_color(bg_var, 'bg_color'), width=20).pack(
            pady=5)

        # Элементы для настройки цвета кнопок
        create_label(color_window, "Цвет кнопок: | Button Color:").pack(pady=5)
        btn_var = tk.StringVar(value=colors['btn_color'])
        tk.Entry(color_window, textvariable=btn_var).pack(pady=5)
        create_button(color_window, "Применить | Apply", lambda: update_color(btn_var, 'btn_color'), width=20).pack(
            pady=5)

        # Элементы для настройки цвета текста
        create_label(color_window, "Цвет текста: | Text Color:").pack(pady=5)
        text_var = tk.StringVar(value=colors['text_color'])
        tk.Entry(color_window, textvariable=text_var).pack(pady=5)
        create_button(color_window, "Применить | Apply", lambda: update_color(text_var, 'text_color'), width=20).pack(
            pady=5)

        # Элементы для настройки фона полей ввода
        create_label(color_window, "Фон полей ввода: | Entry Background:").pack(pady=5)
        entry_var = tk.StringVar(value=colors['entry_bg'])
        tk.Entry(color_window, textvariable=entry_var).pack(pady=5)
        create_button(color_window, "Применить | Apply", lambda: update_color(entry_var, 'entry_bg'), width=20).pack(
            pady=5)

    # Функция смены пароля администратора
    def change_admin_password():
        global admin_password  # Использование глобальной переменной
        # Запрос текущего пароля
        current = simpledialog.askstring("Смена пароля | Password Change",
                                         "Введите текущий пароль: | Enter current password:", show='*')
        if current != admin_password:  # Проверка пароля
            messagebox.showerror("Ошибка | Error", "Неверный текущий пароль! | Incorrect current password!")
            return

        # Запрос нового пароля
        new_pass = simpledialog.askstring("Смена пароля | Password Change",
                                          "Введите новый пароль: | Enter new password:", show='*')
        # Подтверждение пароля
        confirm = simpledialog.askstring("Смена пароля | Password Change",
                                         "Подтвердите новый пароль: | Confirm new password:", show='*')

        if new_pass and new_pass == confirm:  # Проверка совпадения
            admin_password = new_pass  # Установка нового пароля
            # Показ сообщения об успехе
            show_success_message("Успех | Success", "Пароль успешно изменен! | Password changed successfully!")
            logging.info("Пароль администратора изменен. | Admin password changed.")  # Запись в лог
        else:
            messagebox.showerror("Ошибка | Error",
                                 "Пароли не совпадают! | Passwords do not match!")  # Сообщение об ошибке

    # Функция аутентификации администратора
    def authenticate_admin():
        password = simpledialog.askstring("Аутентификация | Authentication",
                                          "Введите пароль администратора: | Enter admin password:", show='*')
        return password == admin_password  # Проверка пароля

    # Функция просмотра объектов зоопарка
    def view_entities():
        view_window = create_toplevel("Объекты зоопарка | Zoo Entities", 650, 450)  # Создание окна

        # Словарь для перевода типов на два языка
        type_translations = {
            "Bird": "Птица | Bird",
            "Mammal": "Млекопитающее | Mammal",
            "Reptile": "Рептилия | Reptile",
            "ZooKeeper": "Смотритель | ZooKeeper",
            "Veterinarian": "Ветеринар | Veterinarian"
        }

        # Настройка стиля вкладок
        style = ttk.Style()
        style.configure("TNotebook", background=colors['bg_color'])
        style.configure("TNotebook.Tab",
                        background=colors['tab_bg'],
                        foreground=colors['tab_fg'],
                        font=("Arial", 10, "bold"),
                        padding=[10, 5])
        style.map("TNotebook.Tab",
                  background=[("selected", colors['accent_color'])])

        notebook = ttk.Notebook(view_window)  # Создание виджета вкладок
        notebook.pack(fill='both', expand=True)  # Размещение виджета

        # Создание фреймов для вкладок
        animals_frame = ttk.Frame(notebook)
        notebook.add(animals_frame, text="Животные | Animals")  # Добавление вкладки животных

        staff_frame = ttk.Frame(notebook)
        notebook.add(staff_frame, text="Сотрудники | Staff")  # Добавление вкладки сотрудников

        # Функция обновления данных
        def refresh_data():
            animal_tree.delete(*animal_tree.get_children())  # Очистка таблицы животных
            for animal in zoo.animals:
                # Получение переведенного типа животного
                animal_type = type_translations.get(animal.__class__.__name__, animal.__class__.__name__)
                # Добавление животного в таблицу
                animal_tree.insert("", "end", values=(animal.name, animal.age, animal_type))

            staff_tree.delete(*staff_tree.get_children())  # Очистка таблицы персонала
            for staff_member in zoo.staff:
                # Получение переведенного типа сотрудника
                staff_type = type_translations.get(staff_member.__class__.__name__, staff_member.__class__.__name__)
                # Добавление сотрудника в таблицу
                staff_tree.insert("", "end", values=(staff_member.name, staff_type))

        # Настройка таблицы животных
        animal_columns = ("Имя | Name", "Возраст | Age", "Тип | Type")
        animal_tree = ttk.Treeview(animals_frame, columns=animal_columns, show="headings")  # Создание таблицы
        for col in animal_columns:
            animal_tree.heading(col, text=col)  # Установка заголовков столбцов
            animal_tree.column(col, width=100)  # Установка ширины столбцов
        animal_tree.pack(fill='both', expand=True)  # Размещение таблицы

        # Настройка таблицы персонала
        staff_columns = ("Имя | Name", "Должность | Position")
        staff_tree = ttk.Treeview(staff_frame, columns=staff_columns, show="headings")  # Создание таблицы
        for col in staff_columns:
            staff_tree.heading(col, text=col)  # Установка заголовков столбцов
            staff_tree.column(col, width=100)  # Установка ширины столбцов
        staff_tree.pack(fill='both', expand=True)  # Размещение таблицы

        refresh_data()  # Первоначальное заполнение таблиц

        # Функция применения фильтра
        def apply_filter():
            filter_text = filter_entry.get().lower()  # Текст фильтра
            selected_type = filter_type_var.get()  # Выбранный тип

            animal_tree.delete(*animal_tree.get_children())  # Очистка таблицы животных
            for animal in zoo.animals:
                # Проверка типа и имени
                if selected_type == "Все | All" or animal.__class__.__name__ == selected_type.split(" | ")[0]:
                    if filter_text in animal.name.lower():
                        # Получение переведенного типа животного
                        animal_type = type_translations.get(animal.__class__.__name__, animal.__class__.__name__)
                        # Добавление животного в таблицу
                        animal_tree.insert("", "end", values=(animal.name, animal.age, animal_type))

            staff_tree.delete(*staff_tree.get_children())  # Очистка таблицы персонала
            for staff_member in zoo.staff:
                # Проверка типа и имени
                if selected_type == "Все | All" or staff_member.__class__.__name__ == selected_type.split(" | ")[0]:
                    if filter_text in staff_member.name.lower():
                        # Получение переведенного типа сотрудника
                        staff_type = type_translations.get(staff_member.__class__.__name__,
                                                           staff_member.__class__.__name__)
                        # Добавление сотрудника в таблицу
                        staff_tree.insert("", "end", values=(staff_member.name, staff_type))

        # Создание элементов управления фильтрацией
        filter_frame = tk.Frame(view_window, bg=colors['bg_color'])
        filter_frame.pack(fill='x', padx=5, pady=5)

        filter_row1 = tk.Frame(filter_frame, bg=colors['bg_color'])
        filter_row1.pack(fill='x', pady=5)

        create_label(filter_row1, "Фильтр: | Filter:").pack(side='left')
        filter_entry = tk.Entry(filter_row1)
        filter_entry.pack(side='left', padx=5, fill='x', expand=True)

        filter_row2 = tk.Frame(filter_frame, bg=colors['bg_color'])
        filter_row2.pack(fill='x', pady=5)

        filter_type_var = tk.StringVar(value="Все | All")
        filter_types = ["Все | All", "Bird | Птица", "Mammal | Млекопитающее", "Reptile | Рептилия",
                        "ZooKeeper | Смотритель", "Veterinarian | Ветеринар"]
        create_label(filter_row2, "Тип: | Type:").pack(side='left')
        filter_menu = create_option_menu(filter_row2, filter_type_var, filter_types, width=25)
        filter_menu.pack(side='left', padx=5)

        apply_filter_btn = create_button(filter_row2, "Применить фильтр | Apply Filter", apply_filter, width=30,
                                         font_size=9)
        apply_filter_btn.pack(side='left', padx=5)

        # Функция удаления сущности
        def delete_entity():
            if not authenticate_admin():  # Проверка прав администратора
                messagebox.showerror("Ошибка | Error",
                                     "Ошибка аутентификации администратора! | Admin authentication failed!")
                return

            current_tab = notebook.index(notebook.select())  # Определение текущей вкладки

            if current_tab == 0:  # Вкладка животных
                selected = animal_tree.selection()  # Выбранные элементы
                if not selected:
                    return
                item_data = animal_tree.item(selected[0])  # Данные выбранного элемента
                name = item_data['values'][0]  # Имя животного

                # Подтверждение удаления
                if messagebox.askyesno("Подтверждение | Confirm", f"Удалить животное {name}? | Delete animal {name}?"):
                    for animal in zoo.animals[:]:
                        if animal.name == name:
                            zoo.animals.remove(animal)  # Удаление животного
                            logging.info(f"Животное {name} удалено. | Animal {name} deleted.")  # Запись в лог
                            break
                    refresh_data()  # Обновление данных

            elif current_tab == 1:  # Вкладка персонала
                selected = staff_tree.selection()  # Выбранные элементы
                if not selected:
                    return
                item_data = staff_tree.item(selected[0])  # Данные выбранного элемента
                name = item_data['values'][0]  # Имя сотрудника

                # Подтверждение удаления
                if messagebox.askyesno("Подтверждение | Confirm",
                                       f"Удалить сотрудника {name}? | Delete staff member {name}?"):
                    for staff_member in zoo.staff[:]:
                        if staff_member.name == name:
                            zoo.staff.remove(staff_member)  # Удаление сотрудника
                            logging.info(f"Сотрудник {name} удален. | Staff {name} deleted.")  # Запись в лог
                            break
                    refresh_data()  # Обновление данных

        # Функция редактирования сущности
        def edit_entity():
            if not authenticate_admin():  # Проверка прав администратора
                messagebox.showerror("Ошибка | Error",
                                     "Ошибка аутентификации администратора! | Admin authentication failed!")
                return

            current_tab = notebook.index(notebook.select())  # Определение текущей вкладки
            # Получение выбранного элемента
            selected = animal_tree.selection() if current_tab == 0 else staff_tree.selection()

            if not selected:
                return

            if current_tab == 0:  # Редактирование животного
                item_data = animal_tree.item(selected[0])
                name, age, animal_class = item_data['values']
                # Поиск животного по имени
                animal = next((a for a in zoo.animals if a.name == name), None)
                if not animal:
                    return

                edit_window = create_toplevel("Редактировать животное | Edit Animal", 450, 180)  # Создание окна

                form_frame = tk.Frame(edit_window, bg=colors['bg_color'])
                form_frame.pack(fill='both', padx=20, pady=10, expand=True)

                create_label(form_frame, "Новое имя: | New Name:").pack(anchor='w', pady=5)
                name_var = tk.StringVar(value=name)
                name_entry_edit = tk.Entry(
                    form_frame,
                    textvariable=name_var,
                    width=40,
                    bg=colors['entry_bg'],
                    fg=colors['text_color']
                )
                name_entry_edit.pack(fill='x', pady=5)

                create_label(form_frame, "Новый возраст: | New Age:").pack(anchor='w', pady=5)
                age_var = tk.StringVar(value=str(age))
                age_entry_edit = tk.Entry(
                    form_frame,
                    textvariable=age_var,
                    width=40,
                    bg=colors['entry_bg'],
                    fg=colors['text_color']
                )
                age_entry_edit.pack(fill='x', pady=5)

                # Функция сохранения изменений
                def save_changes():
                    new_name = name_var.get()  # Новое имя
                    try:
                        new_age = float(age_var.get())  # Новый возраст
                        if new_age <= 0:  # Проверка возраста
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Ошибка | Error", "Некорректное значение возраста! | Invalid age value!")
                        return

                    # Обновление данных животного
                    animal.name = new_name
                    animal.age = new_age
                    logging.info(f"Животное {name} обновлено: {new_name}, возраст {new_age}")  # Запись в лог
                    refresh_data()  # Обновление таблицы
                    edit_window.destroy()  # Закрытие окна
                    show_success_message("Успех | Success",
                                         "Данные животного обновлены! | Animal updated!")  # Сообщение

                button_frame = tk.Frame(edit_window, bg=colors['bg_color'])
                button_frame.pack(fill='x', padx=20, pady=10)

                create_button(button_frame, "Сохранить | Save", save_changes, width=20).pack(pady=5)

            elif current_tab == 1:  # Редактирование сотрудника
                item_data = staff_tree.item(selected[0])
                name = item_data['values'][0]
                # Поиск сотрудника по имени
                staff = next((s for s in zoo.staff if s.name == name), None)
                if not staff:
                    return

                edit_window = create_toplevel("Редактировать сотрудника | Edit Staff", 450, 180)  # Создание окна

                form_frame = tk.Frame(edit_window, bg=colors['bg_color'])
                form_frame.pack(fill='both', padx=20, pady=10, expand=True)

                create_label(form_frame, "Новое имя: | New Name:").pack(anchor='w', pady=5)
                name_var = tk.StringVar(value=name)
                name_entry_edit = tk.Entry(
                    form_frame,
                    textvariable=name_var,
                    width=40,
                    bg=colors['entry_bg'],
                    fg=colors['text_color']
                )
                name_entry_edit.pack(fill='x', pady=5)

                # Функция сохранения изменений
                def save_changes():
                    new_name = name_var.get()  # Новое имя
                    staff.name = new_name  # Обновление имени
                    logging.info(f"Сотрудник {name} обновлен: {new_name}")  # Запись в лог
                    refresh_data()  # Обновление таблицы
                    edit_window.destroy()  # Закрытие окна
                    show_success_message("Успех | Success",
                                         "Данные сотрудника обновлены! | Staff updated!")  # Сообщение

                button_frame = tk.Frame(edit_window, bg=colors['bg_color'])
                button_frame.pack(fill='x', padx=20, pady=10)

                create_button(button_frame, "Сохранить | Save", save_changes, width=20).pack(pady=5)

        # Панель кнопок управления
        btn_frame = tk.Frame(view_window, bg=colors['bg_color'])
        btn_frame.pack(fill='x', padx=5, pady=5)

        # Кнопки управления
        delete_btn = create_button(btn_frame, "Удалить выбранное | Delete Selected", delete_entity, width=28,
                                   font_size=9)
        delete_btn.pack(side='left', padx=2, fill='x', expand=True)

        edit_btn = create_button(btn_frame, "Редактировать выбранное | Edit Selected", edit_entity, width=30,
                                 font_size=9)
        edit_btn.pack(side='left', padx=2, fill='x', expand=True)

        refresh_btn = create_button(btn_frame, "Обновить | Refresh", refresh_data, width=18, font_size=9)
        refresh_btn.pack(side='right', padx=2, fill='x', expand=True)

    # Функция воспроизведения звука животного
    def play_animal_sound():
        if not zoo.animals:  # Проверка наличия животных
            messagebox.showinfo("Информация | Info", "В зоопарке пока нет животных. | No animals in the zoo yet.")
            return

        # Создание окна выбора животного
        sound_window = create_toplevel("Воспроизвести звук животного | Play Animal Sound", 350, 180)

        create_label(sound_window, "Выберите животное: | Select an animal:").pack(pady=10)

        animal_var = tk.StringVar()
        animal_names = [animal.name for animal in zoo.animals]  # Список имен животных
        if not animal_names:  # Проверка наличия имен
            create_label(sound_window, "Нет животных для воспроизведения звука. | No animals available.").pack()
            return

        # Выпадающий список животных
        animal_menu = create_option_menu(sound_window, animal_var, animal_names)
        animal_menu.pack(pady=5)

        # Функция воспроизведения звука
        def play_sound():
            selected_name = animal_var.get()  # Выбранное имя
            if not selected_name:
                return

            # Поиск животного по имени
            animal = next((a for a in zoo.animals if a.name == selected_name), None)
            if animal:
                animal.make_sound()  # Воспроизведение звука
                logging.info(f"Воспроизведен звук животного: {animal.name}")  # Запись в лог

        # Кнопка воспроизведения
        create_button(sound_window, "Воспроизвести звук | Play Sound", play_sound, width=30).pack(pady=10)

    # Функция добавления животного через GUI
    def add_animal_gui():
        name = name_entry.get()  # Получение имени
        if not name:  # Проверка имени
            messagebox.showerror("Ошибка | Error", "Введите имя животного! | Enter animal name!")
            return

        try:
            age = float(age_entry.get())  # Получение возраста
            if age <= 0:  # Проверка возраста
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка | Error",
                                 "Возраст должен быть положительным числом! | Age must be a positive number!")
            return

        full_type = animal_type_var.get()  # Получение типа
        parts = full_type.split(" | ")
        russian_type = parts[0]  # Русское название типа
        english_type = parts[1] if len(parts) > 1 else russian_type  # Английское название

        # Создание животного соответствующего типа
        if russian_type == "Птица":
            animal = Bird(name, age)
        elif russian_type == "Млекопитающее":
            animal = Mammal(name, age)
        elif russian_type == "Рептилия":
            animal = Reptile(name, age)
        else:
            messagebox.showerror("Ошибка | Error", "Выберите тип животного! | Select animal type!")
            return

        zoo.add_animal(animal)  # Добавление животного в зоопарк
        # Показ сообщения об успехе
        show_success_message("Успех | Success",
                             f"{russian_type} {name} добавлен в зоопарк. | {english_type} {name} added to zoo.")
        logging.info(f"Добавлено животное: {name} ({russian_type})")  # Запись в лог

        # Очистка полей ввода
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)

    # Функция добавления смотрителя
    def add_keeper():
        name = keeper_entry.get()  # Получение имени
        if not name:  # Проверка имени
            messagebox.showerror("Ошибка | Error", "Введите имя смотрителя! | Enter keeper name!")
            return

        zoo.add_staff(ZooKeeper(name))  # Добавление смотрителя
        # Показ сообщения об успехе
        show_success_message("Успех | Success", f"Смотритель {name} добавлен. | ZooKeeper {name} added.")
        logging.info(f"Добавлен сотрудник: {name} (Смотритель)")  # Запись в лог
        keeper_entry.delete(0, tk.END)  # Очистка поля

    # Функция добавления ветеринара
    def add_vet():
        name = vet_entry.get()  # Получение имени
        if not name:  # Проверка имени
            messagebox.showerror("Ошибка | Error", "Введите имя ветеринара! | Enter veterinarian name!")
            return

        zoo.add_staff(Veterinarian(name))  # Добавление ветеринара
        # Показ сообщения об успехе
        show_success_message("Успех | Success", f"Ветеринар {name} добавлен. | Veterinarian {name} added.")
        logging.info(f"Добавлен сотрудник: {name} (Ветеринар)")  # Запись в лог
        vet_entry.delete(0, tk.END)  # Очистка поля

    # Функция сохранения зоопарка в файл
    def save_zoo():
        save_filename = filedialog.asksaveasfilename(  # Диалог выбора файла
            defaultextension=".pkl",
            filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
            title="Сохранить зоопарк | Save Zoo"
        )
        if save_filename:
            if zoo.save_zoo(save_filename):  # Сохранение зоопарка
                # Показ сообщения об успехе
                show_success_message("Успех | Success",
                                     f"Зоопарк сохранен в {os.path.basename(save_filename)} | Zoo saved to {os.path.basename(save_filename)}")
                logging.info(f"Зоопарк сохранен в {save_filename}")  # Запись в лог
            else:
                messagebox.showerror("Ошибка | Error", "Не удалось сохранить зоопарк! | Failed to save zoo!")  # Ошибка

    # Функция загрузки зоопарка из файла
    def load_zoo():
        load_filename = filedialog.askopenfilename(  # Диалог выбора файла
            filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
            title="Загрузить зоопарк | Load Zoo"
        )
        if load_filename:
            try:
                loaded_zoo = Zoo.load_zoo(load_filename)  # Загрузка зоопарка
                # Обновление данных текущего зоопарка
                zoo.animals = loaded_zoo.animals
                zoo.staff = loaded_zoo.staff
                zoo.name = loaded_zoo.name
                # Обновление заголовка окна
                root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
                # Показ сообщения об успехе
                show_success_message("Успех | Success",
                                     f"Зоопарк загружен из {os.path.basename(load_filename)} | Zoo loaded from {os.path.basename(load_filename)}")
                logging.info(f"Зоопарк загружен из {load_filename}")  # Запись в лог
            except Exception as load_exc:  # Обработка ошибок
                logging.error(f"Ошибка загрузки зоопарка: {load_exc}")  # Запись ошибки
                # Предложение создать новый зоопарк
                if messagebox.askyesno("Ошибка | Error",
                                       "Не удалось загрузить зоопарк. Создать новый? | Failed to load zoo. Create new zoo?"):
                    zoo.animals = []
                    zoo.staff = []
                    zoo.name = "Новый зоопарк | New Zoo"
                    root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
                    logging.info("Создан новый зоопарк после ошибки загрузки")  # Запись в лог

    # Ширина всех элементов главного окна
    element_width = 50  # Общая ширина элементов

    # Создание элементов интерфейса
    create_label(root_window, "Добавление животных | Add Animals", font_size=11).pack(pady=(10, 5))

    create_label(root_window, "Имя животного: | Animal Name:").pack()
    name_entry = tk.Entry(root_window, width=element_width, bg=colors['entry_bg'], fg=colors['text_color'])
    name_entry.pack(pady=2)

    create_label(root_window, "Возраст (месяцев): | Age (months):").pack()
    age_entry = tk.Entry(root_window, width=element_width, bg=colors['entry_bg'], fg=colors['text_color'])
    age_entry.pack(pady=2)

    animal_type_var = tk.StringVar(value="Птица | Bird")
    create_label(root_window, "Выберите Тип животного: | Select Animal Type:").pack(pady=2)

    animal_types = ["Птица | Bird", "Млекопитающее | Mammal", "Рептилия | Reptile"]

    # Создание контейнера для выравнивания OptionMenu
    type_menu_frame = tk.Frame(root_window, bg=colors['bg_color'])
    type_menu_frame.pack(fill='x', padx=5, pady=2)

    # Создание OptionMenu с выравниванием по ширине
    animal_type_menu = create_option_menu(type_menu_frame, animal_type_var, animal_types, width=element_width)
    animal_type_menu.pack(fill='x', expand=True)  # Растягивание на всю ширину

    create_button(root_window, "Добавить животное | Add Animal", add_animal_gui, width=element_width).pack(pady=7)

    create_label(root_window, "Добавление персонала | Add Staff", font_size=11).pack(pady=(15, 5))

    create_label(root_window, "Имя смотрителя: | ZooKeeper Name:").pack()
    keeper_entry = tk.Entry(root_window, width=element_width, bg=colors['entry_bg'], fg=colors['text_color'])
    keeper_entry.pack(pady=2)

    create_button(root_window, "Добавить смотрителя | Add ZooKeeper", add_keeper, width=element_width).pack(pady=7)

    create_label(root_window, "Имя ветеринара: | Veterinarian Name:").pack()
    vet_entry = tk.Entry(root_window, width=element_width, bg=colors['entry_bg'], fg=colors['text_color'])
    vet_entry.pack(pady=2)

    create_button(root_window, "Добавить ветеринара | Add Veterinarian", add_vet, width=element_width).pack(pady=7)

    # Создание кнопок управления
    create_button(root_window, "Воспроизвести звук животного | Play Animal Sound", play_animal_sound,
                  width=element_width).pack(pady=7)
    create_button(root_window, "Просмотр животных и персонала | View Animals and Staff", view_entities,
                  width=element_width).pack(pady=7)
    create_button(root_window, "Сохранить зоопарк | Save Zoo", save_zoo, width=element_width).pack(pady=7)
    create_button(root_window, "Загрузить зоопарк | Load Zoo", load_zoo, width=element_width).pack(pady=7)
    create_button(root_window, "Сменить пароль администратора | Change Admin Password", change_admin_password,
                  width=element_width).pack(pady=7)
    create_button(root_window, "Настройки цветов | Color Settings", configure_colors, width=element_width).pack(pady=7)
    create_button(root_window, "Выход | Exit", root_window.destroy, width=element_width).pack(pady=12)

    apply_colors()  # Применение цветовой схемы
    root_window.mainloop()  # Запуск главного цикла обработки событий


# Основной блок программы
if __name__ == "__main__":
    zoo_instance = None  # Экземпляр зоопарка

    try:
        # Попытка загрузки последнего состояния зоопарка
        zoo_instance = Zoo.load_zoo("last_zoo.pkl")
        logging.info("Автоматически загружено состояние зоопарка")  # Запись в лог
    except Exception as auto_load_error:  # Обработка ошибки
        logging.warning(f"Ошибка автоматической загрузки: {auto_load_error}")  # Запись предупреждения
        # Предложение создать новый зоопарк
        if messagebox.askyesno("Ошибка загрузки | Load Error",
                               "Не удалось загрузить зоопарк. Создать новый? | Failed to load zoo. Create new zoo?"):
            zoo_instance = Zoo("Новый зоопарк | New Zoo")  # Создание нового зоопарка
            logging.info("Создан новый зоопарк после ошибки загрузки")  # Запись в лог
        else:
            # Ручной выбор файла зоопарка
            manual_filename = filedialog.askopenfilename(
                filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
                title="Выберите файл зоопарка | Select Zoo File"
            )
            if manual_filename:
                try:
                    # Загрузка выбранного файла
                    zoo_instance = Zoo.load_zoo(manual_filename)
                    logging.info(f"Ручная загрузка зоопарка из {manual_filename}")  # Запись в лог
                except Exception as manual_load_error:  # Обработка ошибки
                    logging.error(f"Ошибка ручной загрузки: {manual_load_error}")  # Запись ошибки
                    # Создание нового зоопарка при ошибке
                    messagebox.showerror("Ошибка | Error",
                                         "Не удалось загрузить зоопарк. Создаётся новый. | Failed to load zoo. Creating new one.")
                    zoo_instance = Zoo("Новый зоопарк | New Zoo")
            else:
                zoo_instance = Zoo("Новый зоопарк | New Zoo")  # Создание нового зоопарка

    if zoo_instance:
        run_gui(zoo_instance)  # Запуск GUI если зоопарк создан

    try:
        # Сохранение состояния при выходе
        zoo_instance.save_zoo("last_zoo.pkl")
        logging.info("Состояние зоопарка сохранено при выходе")  # Запись в лог
    except Exception as save_exc:  # Обработка ошибки
        logging.error(f"Ошибка сохранения при выходе: {save_exc}")  # Запись ошибки