import tkinter as tk  # Импорт библиотеки для создания графического интерфейса
from tkinter import messagebox, simpledialog, filedialog, ttk  # Дополнительные компоненты GUI
import logging  # Для логирования событий
import os  # Для работы с файловой системой
import pickle  # Для сохранения/загрузки данных
import sys  # Для обработки ошибок импорта

# Попытка импорта pygame с обработкой ошибок
try:
    import pygame  # Импорт библиотеки для работы со звуком

    pygame.mixer.init()  # Инициализация звуковой системы
    pygame_available = True  # Флаг доступности pygame
except ImportError:
    pygame = None  # Создаем пустой объект, если pygame недоступен
    pygame_available = False  # Устанавливаем флаг недоступности
    print("Pygame не установлен, звуки отключены")  # Информационное сообщение

# Настройка логирования
logging.basicConfig(
    filename="zoo_log.txt",  # Файл для записи логов
    level=logging.INFO,  # Уровень логирования (информационные сообщения и выше)
    format="%(asctime)s — %(levelname)s — %(message)s"  # Формат записи логов
)

# Глобальная переменная для хранения пароля администратора
admin_password = "admin123"  # Начальный пароль администратора


class Animal:
    """Базовый класс для всех животных в зоопарке"""

    def __init__(self, name, age):
        self.name = name  # Имя животного
        self.age = age  # Возраст животного в месяцах

    def make_sound(self):
        """Метод для издания звука животным (должен быть переопределен в дочерних классах)"""
        pass

    def eat(self):
        """Метод, описывающий процесс питания животного"""
        logging.info(f"{self.name} ест.")  # Запись в лог
        print(f"{self.name} ест.")  # Вывод в консоль

    def __str__(self):
        """Строковое представление объекта животного"""
        return f"{self.__class__.__name__} - {self.name}, возраст {self.age} лет"  # Форматированная строка


class Bird(Animal):
    """Класс птиц, наследуется от Animal"""

    def make_sound(self):
        """Издание звука, характерного для птиц"""
        logging.info(f"{self.name} чирикает.")  # Запись в лог
        print(f"{self.name} чирикает.")  # Вывод в консоль
        if pygame_available:  # Проверка доступности pygame
            try:
                pygame.mixer.music.load("bird_sound.mp3")  # Загрузка звукового файла
                pygame.mixer.music.play()  # Воспроизведение звука
            except Exception as e:
                print(f"Ошибка воспроизведения звука птицы: {e}")  # Сообщение об ошибке


class Mammal(Animal):
    """Класс млекопитающих, наследуется от Animal"""

    def make_sound(self):
        """Издание звука, характерного для млекопитающих"""
        logging.info(f"{self.name} рычит.")  # Запись в лог
        print(f"{self.name} рычит.")  # Вывод в консоль
        if pygame_available:  # Проверка доступности pygame
            try:
                pygame.mixer.music.load("mammal_sound.mp3")  # Загрузка звукового файла
                pygame.mixer.music.play()  # Воспроизведение звука
            except Exception as e:
                print(f"Ошибка воспроизведения звука млекопитающего: {e}")  # Сообщение об ошибке


class Reptile(Animal):
    """Класс рептилий, наследуется от Animal"""

    def make_sound(self):
        """Издание звука, характерного для рептилий"""
        logging.info(f"{self.name} шипит.")  # Запись в лог
        print(f"{self.name} шипит.")  # Вывод в консоль
        if pygame_available:  # Проверка доступности pygame
            try:
                pygame.mixer.music.load("reptile_sound.mp3")  # Загрузка звукового файла
                pygame.mixer.music.play()  # Воспроизведение звука
            except Exception as e:
                print(f"Ошибка воспроизведения звука рептилии: {e}")  # Сообщение об ошибке


class Zoo:
    """Класс для управления зоопарком"""

    def __init__(self, name):
        self.name = name  # Название зоопарка
        self.animals = []  # Список животных
        self.staff = []  # Список сотрудников

    def add_animal(self, animal):
        """Добавление животного в зоопарк"""
        self.animals.append(animal)  # Добавление животного в список
        logging.info(f"Животное {animal.name} добавлено в зоопарк.")  # Запись в лог

    def add_staff(self, staff_member):
        """Добавление сотрудника в зоопарк"""
        self.staff.append(staff_member)  # Добавление сотрудника в список
        logging.info(f"Сотрудник {staff_member.name} нанят.")  # Запись в лог

    def save_zoo(self, filename="zoo_data.pkl"):
        """Сохранение состояния зоопарка в файл"""
        try:
            with open(filename, 'wb') as file:  # Открытие файла в бинарном режиме записи
                pickle.dump(self, file)  # Сериализация объекта зоопарка
            logging.info(f"Состояние зоопарка сохранено в {filename}.")  # Запись в лог
            return True  # Успешное завершение
        except (IOError, pickle.PicklingError) as e:  # Обработка конкретных исключений
            logging.error(f"Ошибка сохранения зоопарка: {e}")  # Запись ошибки
            return False  # Неудачное завершение

    @staticmethod
    def load_zoo(filename="zoo_data.pkl"):
        """Загрузка состояния зоопарка из файла"""
        try:
            with open(filename, 'rb') as file:  # Открытие файла в бинарном режиме чтения
                zoo_obj = pickle.load(file)  # Десериализация объекта
            logging.info(f"Состояние зоопарка загружено из {filename}.")  # Запись в лог
            return zoo_obj  # Возврат загруженного объекта
        except FileNotFoundError:  # Обработка отсутствия файла
            logging.error(f"Файл {filename} не найден.")  # Запись ошибки
            raise  # Повторное возбуждение исключения
        except (IOError, pickle.UnpicklingError) as e:  # Обработка ошибок ввода/вывода
            logging.error(f"Ошибка загрузки зоопарка: {e}")  # Запись ошибки
            raise  # Повторное возбуждение исключения


class Staff:
    """Базовый класс для сотрудников зоопарка"""

    def __init__(self, name):
        self.name = name  # Имя сотрудника


class ZooKeeper(Staff):
    """Класс смотрителя зоопарка, наследуется от Staff"""

    def feed_animal(self, animal):
        """Метод кормления животного"""
        logging.info(f"{self.name} кормит {animal.name}.")  # Запись в лог
        print(f"{self.name} кормит {animal.name}.")  # Вывод в консоль


class Veterinarian(Staff):
    """Класс ветеринара, наследуется от Staff"""

    def heal_animal(self, animal):
        """Метод лечения животного"""
        logging.info(f"{self.name} лечит {animal.name}.")  # Запись в лог
        print(f"{self.name} лечит {animal.name}.")  # Вывод в консоль


def run_gui(zoo):
    """Функция для запуска графического интерфейса управления зоопарком"""
    # Создание главного окна
    root_window = tk.Tk()
    root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")  # Установка заголовка
    root_window.geometry("500x740")  # Увеличенная высота для отображения всех элементов

    # Цветовая схема приложения
    colors = {
        'bg_color': "#dce2b9",  # Светло-оливковый фон
        'btn_color': "#a9c186",  # Цвет кнопок (оливковый)
        'text_color': "#5D4037",  # Шоколадно-коричневый текст
        'entry_bg': "#f8f8f8",  # Фон полей ввода
        'accent_color': "#8D6E63",  # Акцентный цвет
        'success_bg': "#a9c186",  # Цвет фона для успешных сообщений
        'success_fg': "#5D4037"  # Цвет текста для успешных сообщений
    }

    # Установка фона главного окна
    root_window.configure(bg=colors['bg_color'])

    # Попытка загрузки иконки приложения
    try:
        root_window.iconbitmap("zoo_logo.ico")  # Загрузка иконки
    except Exception as icon_exc:
        logging.warning(f"Иконка не найдена: {icon_exc}")  # Логирование предупреждения

    # Функция для создания вспомогательных окон
    def create_toplevel(title, width=400, height=300):
        """Создание дочернего окна с заданными параметрами"""
        window = tk.Toplevel(root_window)  # Создание дочернего окна
        window.title(title)  # Установка заголовка
        window.geometry(f"{width}x{height}")  # Установка размеров
        window.configure(bg=colors['bg_color'])  # Установка фона
        return window  # Возврат созданного окна

    # Функция создания стилизованных меток
    def create_label(parent, text, bg=None, fg=None, font_size=10):
        """Создание метки с заданными параметрами"""
        bg = bg or colors['bg_color']  # Фон по умолчанию
        fg = fg or colors['text_color']  # Цвет текста по умолчанию
        return tk.Label(  # Создание и возврат метки
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Arial", font_size)
        )

    # Функция создания стилизованных кнопок (увеличена ширина)
    def create_button(parent, text, command, width=50, font_size=9):
        """Создание кнопки с заданными параметрами"""
        return tk.Button(  # Создание и возврат кнопки
            parent,
            text=text,
            command=command,
            bg=colors['btn_color'],
            fg=colors['text_color'],
            width=width,
            font=("Arial", font_size)  # Уменьшенный размер шрифта для лучшего отображения
        )

    # Функция создания стилизованных выпадающих меню
    def create_option_menu(parent, variable, options, width=47):
        """Создание выпадающего меню с заданными параметрами"""
        menu = tk.OptionMenu(parent, variable, *options)  # Создание меню
        menu.config(  # Настройка внешнего вида
            bg=colors['btn_color'],  # Цвет фона
            fg=colors['text_color'],  # Цвет текста
            width=width,  # Ширина
            font=("Arial", 9)  # Размер шрифта
        )
        return menu  # Возврат созданного меню

    # Функция применения цветовой схемы ко всем виджетам
    def apply_colors():
        """Применение цветовой схемы ко всем элементам интерфейса"""
        root_window.configure(bg=colors['bg_color'])  # Фон главного окна
        # Обход всех виджетов в главном окне
        for widget in root_window.winfo_children():
            if isinstance(widget, tk.Button):  # Для кнопок
                widget.configure(bg=colors['btn_color'], fg=colors['text_color'])
            elif isinstance(widget, tk.Label):  # Для меток
                widget.configure(bg=colors['bg_color'], fg=colors['text_color'])
            elif isinstance(widget, tk.Entry):  # Для полей ввода
                widget.configure(bg=colors['entry_bg'], fg=colors['text_color'])
            elif isinstance(widget, tk.OptionMenu):  # Для выпадающих меню
                widget.configure(bg=colors['btn_color'], fg=colors['text_color'])

    # Функция отображения кастомного сообщения об успехе
    def show_success_message(title, message):
        """Отображение кастомного сообщения об успехе"""
        success_window = tk.Toplevel(root_window)
        success_window.title(title)
        success_window.geometry("400x150")
        success_window.configure(bg=colors['success_bg'])
        success_window.resizable(False, False)

        # Центрирование окна
        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        success_window.geometry(f"400x150+{x}+{y}")

        # Содержимое окна
        label = tk.Label(
            success_window,
            text=message,
            bg=colors['success_bg'],
            fg=colors['success_fg'],
            font=("Arial", 11),
            wraplength=380
        )
        label.pack(expand=True, padx=20, pady=20)

        # Кнопка закрытия
        button = tk.Button(
            success_window,
            text="OK",
            command=success_window.destroy,
            bg=colors['btn_color'],
            fg=colors['text_color'],
            width=15,
            font=("Arial", 9)
        )
        button.pack(pady=(0, 15))

    # Функция настройки цветов интерфейса
    def configure_colors():
        """Окно для настройки цветовой схемы приложения"""
        color_window = create_toplevel("Настройки цветов | Color Settings", 300, 300)  # Создание окна

        def update_color(color_var, color_key):
            """Обновление цвета в схеме"""
            new_color = color_var.get()  # Получение нового цвета
            if new_color:  # Если цвет задан
                colors[color_key] = new_color  # Обновление схемы
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
        create_button(color_window, "Применит | Apply", lambda: update_color(text_var, 'text_color'), width=20).pack(
            pady=5)

        # Элементы для настройки фона полей ввода
        create_label(color_window, "Фон полей ввода: | Entry Background:").pack(pady=5)
        entry_var = tk.StringVar(value=colors['entry_bg'])
        tk.Entry(color_window, textvariable=entry_var).pack(pady=5)
        create_button(color_window, "Применить | Apply", lambda: update_color(entry_var, 'entry_bg'), width=20).pack(
            pady=5)

    # Функция смены пароля администратора
    def change_admin_password():
        """Изменение пароля администратора"""
        global admin_password  # Использование глобальной переменной
        # Запрос текущего пароля
        current = simpledialog.askstring("Смена пароля | Password Change",
                                         "Введите текущий пароль: | Enter current password:", show='*')
        if current != admin_password:  # Проверка совпадения
            messagebox.showerror("Ошибка | Error", "Неверный текущий пароль! | Incorrect current password!")
            return

        # Запрос нового пароля
        new_pass = simpledialog.askstring("Смена пароля | Password Change",
                                          "Введите новый пароль: | Enter new password:", show='*')
        # Подтверждение нового пароля
        confirm = simpledialog.askstring("Смена пароля | Password Change",
                                         "Подтвердите новый пароль: | Confirm new password:", show='*')

        if new_pass and new_pass == confirm:  # Проверка совпадения
            admin_password = new_pass  # Обновление пароля
            show_success_message("Успех | Success", "Пароль успешно изменен! | Password changed successfully!")
            logging.info("Пароль администратора изменен. | Admin password changed.")
        else:
            messagebox.showerror("Ошибка | Error", "Пароли не совпадают! | Passwords do not match!")

    # Функция аутентификации администратора
    def authenticate_admin():
        """Проверка пароля администратора"""
        password = simpledialog.askstring("Аутентификация | Authentication",
                                          "Введите пароль администратора: | Enter admin password:", show='*')
        return password == admin_password  # Возврат результата проверки

    # Функция просмотра объектов зоопарка
    def view_entities():
        """Окно для просмотра животных и сотрудников"""
        view_window = create_toplevel("Объекты зоопарка | Zoo Entities", 650, 450)  # Увеличенные размеры окна

        # Создание стиля для вкладок (оливковые кнопки)
        style = ttk.Style()
        style.configure("TNotebook", background=colors['bg_color'])
        style.configure("TNotebook.Tab",
                        background=colors['btn_color'],  # Оливковый цвет
                        foreground=colors['text_color'],  # Цвет текста
                        font=("Arial", 10, "bold"),  # Жирный шрифт
                        padding=[10, 5])  # Отступы
        style.map("TNotebook.Tab",
                  background=[("selected", colors['accent_color'])])  # Цвет активной вкладки

        # Создание набора вкладок
        notebook = ttk.Notebook(view_window)
        notebook.pack(fill='both', expand=True)  # Расположение с заполнением пространства

        # Создание фрейма для животных
        animals_frame = ttk.Frame(notebook)
        notebook.add(animals_frame, text="Животные | Animals")  # Добавление вкладки

        # Создание фрейма для сотрудников
        staff_frame = ttk.Frame(notebook)
        notebook.add(staff_frame, text="Сотрудники | Staff")  # Добавление вкладки

        # Функция обновления данных
        def refresh_data():
            """Обновление данных в таблицах"""
            # Обновление данных о животных
            animal_tree.delete(*animal_tree.get_children())  # Очистка таблицы
            for animal in zoo.animals:  # Заполнение данными
                animal_tree.insert("", "end", values=(animal.name, animal.age, animal.__class__.__name__))

            # Обновление данных о сотрудниках
            staff_tree.delete(*staff_tree.get_children())  # Очистка таблицы
            for staff_member in zoo.staff:  # Заполнение данными
                staff_tree.insert("", "end", values=(staff_member.name, staff_member.__class__.__name__))

        # Создание таблицы для животных
        animal_columns = ("Имя | Name", "Возраст | Age", "Тип | Type")  # Заголовки столбцов
        animal_tree = ttk.Treeview(animals_frame, columns=animal_columns, show="headings")  # Создание таблицы
        for col in animal_columns:  # Настройка столбцов
            animal_tree.heading(col, text=col)  # Установка заголовка
            animal_tree.column(col, width=100)  # Установка ширины
        animal_tree.pack(fill='both', expand=True)  # Расположение с заполнением пространства

        # Создание таблицы для сотрудников
        staff_columns = ("Имя | Name", "Должность | Position")  # Заголовки столбцов
        staff_tree = ttk.Treeview(staff_frame, columns=staff_columns, show="headings")  # Создание таблицы
        for col in staff_columns:  # Настройка столбцов
            staff_tree.heading(col, text=col)  # Установка заголовка
            staff_tree.column(col, width=100)  # Установка ширины
        staff_tree.pack(fill='both', expand=True)  # Расположение с заполнением пространства

        # Первоначальное заполнение таблиц
        refresh_data()

        # Функция применения фильтра
        def apply_filter():
            """Фильтрация данных в таблицах"""
            filter_text = filter_entry.get().lower()  # Текст фильтра
            selected_type = filter_type_var.get()  # Выбранный тип

            # Фильтрация животных
            animal_tree.delete(*animal_tree.get_children())  # Очистка таблицы
            for animal in zoo.animals:  # Применение фильтра
                if selected_type == "Все | All" or animal.__class__.__name__ == selected_type.split(" | ")[0]:
                    if filter_text in animal.name.lower():  # Проверка соответствия имени
                        # Добавление отфильтрованной записи
                        animal_tree.insert("", "end", values=(animal.name, animal.age, animal.__class__.__name__))

            # Фильтрация сотрудников
            staff_tree.delete(*staff_tree.get_children())  # Очистка таблицы
            for staff_member in zoo.staff:  # Применение фильтра
                if selected_type == "Все | All" or staff_member.__class__.__name__ == selected_type.split(" | ")[0]:
                    if filter_text in staff_member.name.lower():  # Проверка соответствия имени
                        # Добавление отфильтрованной записи
                        staff_tree.insert("", "end", values=(staff_member.name, staff_member.__class__.__name__))

        # Создание панели фильтров
        filter_frame = tk.Frame(view_window, bg=colors['bg_color'])
        filter_frame.pack(fill='x', padx=5, pady=5)  # Расположение с заполнением по X

        # Элементы фильтрации - первая строка
        filter_row1 = tk.Frame(filter_frame, bg=colors['bg_color'])
        filter_row1.pack(fill='x', pady=5)

        create_label(filter_row1, "Фильтр: | Filter:").pack(side='left')
        filter_entry = tk.Entry(filter_row1)  # Поле ввода фильтра
        filter_entry.pack(side='left', padx=5, fill='x', expand=True)

        # Элементы фильтрации - вторая строка
        filter_row2 = tk.Frame(filter_frame, bg=colors['bg_color'])
        filter_row2.pack(fill='x', pady=5)

        # Выпадающий список для выбора типа фильтра (уменьшенная ширина)
        filter_type_var = tk.StringVar(value="Все | All")
        filter_types = ["Все | All", "Bird | Птица", "Mammal | Млекопитающее", "Reptile | Рептилия",
                        "ZooKeeper | Смотритель", "Veterinarian | Ветеринар"]
        create_label(filter_row2, "Тип: | Type:").pack(side='left')
        filter_menu = create_option_menu(filter_row2, filter_type_var, filter_types, width=15)  # Уменьшенная ширина
        filter_menu.pack(side='left', padx=5)

        # Кнопка применения фильтра
        create_button(filter_row2, "Применить фильтр | Apply Filter", apply_filter, width=20).pack(side='left', padx=5)

        # Функция удаления объекта
        def delete_entity():
            """Удаление выбранного объекта"""
            if not authenticate_admin():  # Проверка прав администратора
                messagebox.showerror("Ошибка | Error",
                                     "Ошибка аутентификации администратора! | Admin authentication failed!")
                return

            current_tab = notebook.index(notebook.select())  # Получение текущей вкладки

            if current_tab == 0:  # Вкладка животных
                selected = animal_tree.selection()  # Получение выделенной строки
                if not selected:  # Проверка выбора
                    return
                item_data = animal_tree.item(selected[0])  # Получение данных
                name = item_data['values'][0]  # Имя животного

                # Подтверждение удаления
                if messagebox.askyesno("Подтверждение | Confirm", f"Удалить животное {name}? | Delete animal {name}?"):
                    for animal in zoo.animals[:]:  # Поиск животного
                        if animal.name == name:
                            zoo.animals.remove(animal)  # Удаление
                            logging.info(f"Животное {name} удалено. | Animal {name} deleted.")
                            break
                    refresh_data()  # Обновление данных

            elif current_tab == 1:  # Вкладка сотрудников
                selected = staff_tree.selection()  # Получение выделенной строки
                if not selected:  # Проверка выбора
                    return
                item_data = staff_tree.item(selected[0])  # Получение данных
                name = item_data['values'][0]  # Имя сотрудника

                # Подтверждение удаления
                if messagebox.askyesno("Подтверждение | Confirm",
                                       f"Удалить сотрудника {name}? | Delete staff member {name}?"):
                    for staff_member in zoo.staff[:]:  # Поиск сотрудника
                        if staff_member.name == name:
                            zoo.staff.remove(staff_member)  # Удаление
                            logging.info(f"Сотрудник {name} удален. | Staff {name} deleted.")
                            break
                    refresh_data()  # Обновление данных

        # Функция редактирования объекта
        def edit_entity():
            """Редактирование выбранного объекта"""
            if not authenticate_admin():  # Проверка прав администратора
                messagebox.showerror("Ошибка | Error",
                                     "Ошибка аутентификации администратора! | Admin authentication failed!")
                return

            current_tab = notebook.index(notebook.select())  # Получение текущей вкладки
            selected = animal_tree.selection() if current_tab == 0 else staff_tree.selection()  # Выбор таблицы

            if not selected:  # Проверка выбора
                return

            if current_tab == 0:  # Редактирование животных
                item_data = animal_tree.item(selected[0])  # Получение данных
                name, age, animal_class = item_data['values']  # Распаковка значений
                animal = next((a for a in zoo.animals if a.name == name), None)  # Поиск животного
                if not animal:  # Проверка наличия
                    return

                edit_window = create_toplevel("Редактировать животное | Edit Animal", 300, 150)  # Создание окна

                # Поля для редактирования
                create_label(edit_window, "Новое имя: | New Name:").pack(pady=5)
                name_var = tk.StringVar(value=name)
                name_entry_edit = tk.Entry(edit_window, textvariable=name_var, bg=colors['entry_bg'],
                                           fg=colors['text_color'])
                name_entry_edit.pack(pady=5)

                create_label(edit_window, "Новый возраст: | New Age:").pack(pady=5)
                age_var = tk.StringVar(value=str(age))
                age_entry_edit = tk.Entry(edit_window, textvariable=age_var, bg=colors['entry_bg'],
                                          fg=colors['text_color'])
                age_entry_edit.pack(pady=5)

                def save_changes():
                    """Сохранение изменений животного"""
                    new_name = name_var.get()  # Новое имя
                    try:
                        new_age = float(age_var.get())  # Новый возраст
                        if new_age <= 0:  # Проверка корректности
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Ошибка | Error", "Некорректное значение возраста! | Invalid age value!")
                        return

                    # Обновление данных
                    animal.name = new_name
                    animal.age = new_age
                    logging.info(f"Животное {name} обновлено: {new_name}, возраст {new_age}")
                    refresh_data()  # Обновление таблицы
                    edit_window.destroy()  # Закрытие окна
                    show_success_message("Успех | Success", "Данные животного обновлены! | Animal updated!")

                create_button(edit_window, "Сохранить | Save", save_changes, width=20).pack(pady=10)

            elif current_tab == 1:  # Редактирование сотрудников
                item_data = staff_tree.item(selected[0])  # Получение данных
                name = item_data['values'][0]  # Имя сотрудника
                staff = next((s for s in zoo.staff if s.name == name), None)  # Поиск сотрудника
                if not staff:  # Проверка наличия
                    return

                edit_window = create_toplevel("Редактировать сотрудника | Edit Staff", 300, 150)  # Создание окна

                # Поле для редактирования
                create_label(edit_window, "Новое имя: | New Name:").pack(pady=5)
                name_var = tk.StringVar(value=name)
                name_entry_edit = tk.Entry(edit_window, textvariable=name_var, bg=colors['entry_bg'],
                                           fg=colors['text_color'])
                name_entry_edit.pack(pady=5)

                def save_changes():
                    """Сохранение изменений сотрудника"""
                    new_name = name_var.get()  # Новое имя
                    staff.name = new_name  # Обновление
                    logging.info(f"Сотрудник {name} обновлен: {new_name}")
                    refresh_data()  # Обновление таблицы
                    edit_window.destroy()  # Закрытие окна
                    show_success_message("Успех | Success", "Данные сотрудника обновлены! | Staff updated!")

                create_button(edit_window, "Сохранить | Save", save_changes, width=20).pack(pady=10)

        # Создание панели кнопок управления
        btn_frame = tk.Frame(view_window, bg=colors['bg_color'])
        btn_frame.pack(fill='x', padx=5, pady=5)  # Расположение с заполнением по X

        # Кнопки управления с увеличенной шириной и уменьшенным шрифтом
        delete_btn = create_button(btn_frame, "Удалить выбранное | Delete Selected", delete_entity, width=28,
                                   font_size=8)
        delete_btn.pack(side='left', padx=2, fill='x', expand=True)

        edit_btn = create_button(btn_frame, "Редактировать выбранное | Edit Selected", edit_entity, width=28,
                                 font_size=8)
        edit_btn.pack(side='left', padx=2, fill='x', expand=True)

        refresh_btn = create_button(btn_frame, "Обновить | Refresh", refresh_data, width=20, font_size=9)
        refresh_btn.pack(side='right', padx=2, fill='x', expand=True)

    # Функция воспроизведения звука животного
    def play_animal_sound():
        """Окно для воспроизведения звуков животных"""
        if not zoo.animals:  # Проверка наличия животных
            messagebox.showinfo("Информация | Info", "В зоопарке пока нет животных. | No animals in the zoo yet.")
            return

        sound_window = create_toplevel("Воспроизвести звук животного | Play Animal Sound", 350,
                                       180)  # Увеличенные размеры

        create_label(sound_window, "Выберите животное: | Select an animal:").pack(pady=10)

        animal_var = tk.StringVar()  # Переменная для выбора
        animal_names = [animal.name for animal in zoo.animals]  # Список имен животных
        if not animal_names:  # Проверка наличия
            create_label(sound_window, "Нет животных для воспроизведения звука. | No animals available.").pack()
            return

        # Создание выпадающего списка
        animal_menu = create_option_menu(sound_window, animal_var, animal_names)
        animal_menu.pack(pady=5)

        def play_sound():
            """Воспроизведение звука выбранного животного"""
            selected_name = animal_var.get()  # Получение выбора
            if not selected_name:  # Проверка выбора
                return

            # Поиск животного
            animal = next((a for a in zoo.animals if a.name == selected_name), None)
            if animal:  # Если найдено
                animal.make_sound()  # Воспроизведение звука
                logging.info(f"Воспроизведен звук животного: {animal.name}")

        # Кнопка воспроизведения
        create_button(sound_window, "Воспроизвести звук | Play Sound", play_sound, width=30).pack(pady=10)

    # Функция добавления животного
    def add_animal_gui():
        """Добавление животного через GUI"""
        name = name_entry.get()  # Получение имени
        if not name:  # Проверка ввода
            messagebox.showerror("Ошибка | Error", "Введите имя животного! | Enter animal name!")
            return

        try:  # Обработка возраста
            age = float(age_entry.get())  # Преобразование
            if age <= 0:  # Проверка корректности
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка | Error",
                                 "Возраст должен быть положительным числом! | Age must be a positive number!")
            return

        # Определение типа животного
        selected_type = animal_type_var.get().split(" | ")[0]  # Получаем русскую часть

        # Создание объекта соответствующего типа
        if selected_type == "Птица":
            animal = Bird(name, age)
        elif selected_type == "Млекопитающее":
            animal = Mammal(name, age)
        elif selected_type == "Рептилия":
            animal = Reptile(name, age)
        else:
            messagebox.showerror("Ошибка | Error", "Выберите тип животного! | Select animal type!")
            return

        zoo.add_animal(animal)  # Добавление в зоопарк
        show_success_message("Успех | Success",
                             f"{selected_type} {name} добавлен в зоопарк. | {selected_type} {name} added to zoo.")
        logging.info(f"Добавлено животное: {name} ({selected_type})")

        # Очистка полей
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)

    # Функция добавления смотрителя
    def add_keeper():
        """Добавление смотрителя зоопарка"""
        name = keeper_entry.get()  # Получение имени
        if not name:  # Проверка ввода
            messagebox.showerror("Ошибка | Error", "Введите имя смотрителя! | Enter keeper name!")
            return

        zoo.add_staff(ZooKeeper(name))  # Добавление сотрудника
        show_success_message("Успех | Success", f"Смотритель {name} добавлен. | ZooKeeper {name} added.")
        logging.info(f"Добавлен сотрудник: {name} (Смотритель)")
        keeper_entry.delete(0, tk.END)  # Очистка поля

    # Функция добавления ветеринара
    def add_vet():
        """Добавление ветеринара"""
        name = vet_entry.get()  # Получение имени
        if not name:  # Проверка ввода
            messagebox.showerror("Ошибка | Error", "Введите имя ветеринара! | Enter veterinarian name!")
            return

        zoo.add_staff(Veterinarian(name))  # Добавление сотрудника
        show_success_message("Успех | Success", f"Ветеринар {name} добавлен. | Veterinarian {name} added.")
        logging.info(f"Добавлен сотрудник: {name} (Ветеринар)")
        vet_entry.delete(0, tk.END)  # Очистка поля

    # Функция сохранения зоопарка
    def save_zoo():
        """Сохранение состояния зоопарка в файл"""
        save_filename = filedialog.asksaveasfilename(  # Диалог сохранения
            defaultextension=".pkl",
            filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
            title="Сохранить зоопарк | Save Zoo"
        )
        if save_filename:  # Если выбран файл
            if zoo.save_zoo(save_filename):  # Попытка сохранения
                show_success_message("Успех | Success",
                                     f"Зоопарк сохранен в {os.path.basename(save_filename)} | Zoo saved to {os.path.basename(save_filename)}")
                logging.info(f"Зоопарк сохранен в {save_filename}")
            else:
                messagebox.showerror("Ошибка | Error", "Не удалось сохранить зоопарк! | Failed to save zoo!")

    # Функция загрузки зоопарка
    def load_zoo():
        """Загрузка состояния зоопарка из файла"""
        load_filename = filedialog.askopenfilename(  # Диалог открытия
            filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
            title="Загрузить зоопарк | Load Zoo"
        )
        if load_filename:  # Если выбран файл
            try:
                loaded_zoo = Zoo.load_zoo(load_filename)  # Попытка загрузки
                # Обновление данных текущего зоопарка
                zoo.animals = loaded_zoo.animals
                zoo.staff = loaded_zoo.staff
                zoo.name = loaded_zoo.name
                # Обновление заголовка окна
                root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
                show_success_message("Успех | Success",
                                     f"Зоопарк загружен из {os.path.basename(load_filename)} | Zoo loaded from {os.path.basename(load_filename)}")
                logging.info(f"Зоопарк загружен из {load_filename}")
            except Exception as load_exc:
                logging.error(f"Ошибка загрузки зоопарка: {load_exc}")
                # Предложение создать новый зоопарк при ошибке
                if messagebox.askyesno("Ошибка | Error",
                                       "Не удалось загрузить зоопарк. Создать новый? | Failed to load zoo. Create new zoo?"):
                    zoo.animals = []  # Очистка животных
                    zoo.staff = []  # Очистка сотрудников
                    zoo.name = "Новый зоопарк | New Zoo"  # Установка имени
                    root_window.title(
                        f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")  # Обновление заголовка
                    logging.info("Создан новый зоопарк после ошибки загрузки")

    # ================================ ГЛАВНЫЙ ИНТЕРФЕЙС ================================
    # Убрана верхняя надпись "Управление зоопарком" для освобождения места

    # Секция добавления животных
    create_label(root_window, "Добавление животных | Add Animals", font_size=11).pack(pady=(10, 5))

    # Поле для имени животного
    create_label(root_window, "Имя животного: | Animal Name:").pack()
    name_entry = tk.Entry(root_window, width=48, bg=colors['entry_bg'], fg=colors['text_color'])
    name_entry.pack(pady=2)

    # Поле для возраста животного
    create_label(root_window, "Возраст (месяцев): | Age (months):").pack()
    age_entry = tk.Entry(root_window, width=48, bg=colors['entry_bg'], fg=colors['text_color'])
    age_entry.pack(pady=2)

    # Выпадающий список для выбора типа животного
    animal_type_var = tk.StringVar(value="Птица | Bird")
    create_label(root_window, "Тип животного: | Animal Type:").pack(pady=2)

    # Создание выпадающего меню с двойными названиями
    animal_types = ["Птица | Bird", "Млекопитающее | Mammal", "Рептилия | Reptile"]
    animal_type_menu = create_option_menu(root_window, animal_type_var, animal_types)
    animal_type_menu.pack(pady=2)

    # Кнопка добавления животного
    create_button(root_window, "Добавить животное | Add Animal", add_animal_gui).pack(pady=7)

    # Секция добавления сотрудников
    create_label(root_window, "Добавление персонала | Add Staff", font_size=11).pack(pady=(15, 5))

    # Поле для имени смотрителя
    create_label(root_window, "Имя смотрителя: | ZooKeeper Name:").pack()
    keeper_entry = tk.Entry(root_window, width=48, bg=colors['entry_bg'], fg=colors['text_color'])
    keeper_entry.pack(pady=2)

    # Кнопка добавления смотрителя
    create_button(root_window, "Добавить смотрителя | Add ZooKeeper", add_keeper).pack(pady=7)

    # Поле для имени ветеринара
    create_label(root_window, "Имя ветеринара: | Veterinarian Name:").pack()
    vet_entry = tk.Entry(root_window, width=48, bg=colors['entry_bg'], fg=colors['text_color'])
    vet_entry.pack(pady=2)

    # Кнопка добавления ветеринара
    create_button(root_window, "Добавить ветеринара | Add Veterinarian", add_vet).pack(pady=7)

    # Кнопки управления зоопарком
    create_button(root_window, "Воспроизвести звук животного | Play Animal Sound", play_animal_sound).pack(pady=7)
    create_button(root_window, "Просмотр животных и персонала | View Animals and Staff", view_entities).pack(pady=7)
    create_button(root_window, "Сохранить зоопарк | Save Zoo", save_zoo).pack(pady=7)
    create_button(root_window, "Загрузить зоопарк | Load Zoo", load_zoo).pack(pady=7)
    create_button(root_window, "Сменить пароль администратора | Change Admin Password", change_admin_password).pack(
        pady=7)
    create_button(root_window, "Настройки цветов | Color Settings", configure_colors).pack(pady=7)
    create_button(root_window, "Выход | Exit", root_window.destroy).pack(pady=12)

    # Применение цветовой схемы
    apply_colors()
    # Запуск главного цикла обработки событий
    root_window.mainloop()


# Точка входа в программу
if __name__ == "__main__":
    zoo_instance = None  # Переменная для экземпляра зоопарка

    # Попытка загрузки последнего состояния зоопарка
    try:
        zoo_instance = Zoo.load_zoo("last_zoo.pkl")  # Загрузка из файла
        logging.info("Автоматически загружено состояние зоопарка")
    except Exception as auto_load_error:
        logging.warning(f"Ошибка автоматической загрузки: {auto_load_error}")
        # Предложение создать новый зоопарк
        if messagebox.askyesno("Ошибка загрузки | Load Error",
                               "Не удалось загрузить зоопарк. Создать новый? | Failed to load zoo. Create new zoo?"):
            zoo_instance = Zoo("Новый зоопарк | New Zoo")  # Создание нового зоопарка
            logging.info("Создан новый зоопарк после ошибки загрузки")
        else:
            # Ручной выбор файла зоопарка
            manual_filename = filedialog.askopenfilename(
                filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
                title="Выберите файл зоопарка | Select Zoo File"
            )
            if manual_filename:
                try:
                    # Попытка загрузки выбранного файла
                    zoo_instance = Zoo.load_zoo(manual_filename)
                    logging.info(f"Ручная загрузка зоопарка из {manual_filename}")
                except Exception as manual_load_error:
                    logging.error(f"Ошибка ручной загрузки: {manual_load_error}")
                    # Создание нового зоопарка при ошибке
                    messagebox.showerror("Ошибка | Error",
                                         "Не удалось загрузить зоопарк. Создаётся новый. | Failed to load zoo. Creating new one.")
                    zoo_instance = Zoo("Новый зоопарк | New Zoo")
            else:
                # Создание нового зоопарка по умолчанию
                zoo_instance = Zoo("Новый зоопарк | New Zoo")

    # Запуск GUI, если зоопарк создан
    if zoo_instance:
        run_gui(zoo_instance)  # Запуск графического интерфейса

    # Попытка сохранения состояния при выходе
    try:
        zoo_instance.save_zoo("last_zoo.pkl")  # Сохранение в файл
        logging.info("Состояние зоопарка сохранено при выходе")
    except Exception as save_exc:
        logging.error(f"Ошибка сохранения при выходе: {save_exc}")  # Логирование ошибки
