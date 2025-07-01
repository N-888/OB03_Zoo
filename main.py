# Импорт стандартных библиотек
import tkinter as tk  # GUI-библиотека для создания графического интерфейса
from tkinter import messagebox  # Для вывода всплывающих окон с сообщениями
import logging  # Для записи действий пользователя в лог-файл
import pickle  # Для сериализации и десериализации объектов (сохранение/загрузка состояния)
import io

# Настройка логирования: имя файла, уровень логирования, формат сообщений
logging.basicConfig(
    filename="zoo_log.txt",  # Имя лог-файла
    level=logging.INFO,  # Уровень логирования (INFO — информационные сообщения)
    format="%(asctime)s — %(levelname)s — %(message)s"  # Формат: время — уровень — сообщение
)

# Класс Animal — базовый класс для всех животных
class Animal:
    def __init__(self, name, age):
        self.name = name  # Имя животного
        self.age = age    # Возраст животного

    # Метод, который должен быть переопределен в подклассах — звук животного
    def make_sound(self):
        pass

    # Метод еды — выводит сообщение и логирует процесс
    def eat(self):
        logging.info(f"{self.name} is eating.")
        print(f"{self.name} is eating.")

    # Метод строкового представления объекта
    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}, {self.age} years old"

# Подкласс Bird — наследуется от Animal
class Bird(Animal):
    def make_sound(self):
        logging.info(f"{self.name} chirps.")
        print(f"{self.name} chirps.")

# Подкласс Mammal — млекопитающее
class Mammal(Animal):
    def make_sound(self):
        logging.info(f"{self.name} growls.")
        print(f"{self.name} growls.")

# Подкласс Reptile — рептилия
class Reptile(Animal):
    def make_sound(self):
        logging.info(f"{self.name} hisses.")
        print(f"{self.name} hisses.")

# Функция, которая заставляет всех животных издавать звуки
def animal_sound(animals):
    for animal in animals:  # Проходим по всем животным
        animal.make_sound()  # Вызываем метод make_sound

# Класс Zoo — представляет зоопарк (состоит из животных и сотрудников)
class Zoo:
    def __init__(self, name):
        self.name = name      # Название зоопарка
        self.animals = []     # Список животных
        self.staff = []       # Список сотрудников

    # Добавление животного в зоопарк
    def add_animal(self, animal):
        self.animals.append(animal)
        logging.info(f"Animal {animal.name} added to the zoo.")

    # Добавление сотрудника в зоопарк
    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        logging.info(f"Staff {staff_member.name} hired.")

    # Сохранение текущего состояния зоопарка в файл
    def save_zoo(self, filename="zoo_data.pkl"):
        with open(filename, 'wb') as f:  # type: io.BufferedWriter  # Открываем файл в бинарном режиме записи
            pickle.dump(self, f)  # Сохраняем объект с помощью pickle
        logging.info("Zoo state saved to file.")

    # Статический метод загрузки зоопарка из файла
    @staticmethod
    def load_zoo(filename="zoo_data.pkl"):
        try:
            with open(filename, 'rb') as f:
                zoo = pickle.load(f)
            logging.info("Zoo state loaded from file.")
            return zoo
        except FileNotFoundError:
            logging.error("File not found.")
            print("File not found.")
            return Zoo("Default Zoo")

# Класс Staff — базовый для сотрудников зоопарка
class Staff:
    def __init__(self, name):
        self.name = name  # Имя сотрудника

# Класс ZooKeeper — смотритель зоопарка
class ZooKeeper(Staff):
    def feed_animal(self, animal):
        logging.info(f"{self.name} feeds {animal.name}.")
        print(f"{self.name} feeds {animal.name}.")

# Класс Veterinarian — ветеринар
class Veterinarian(Staff):
    def heal_animal(self, animal):
        logging.info(f"{self.name} heals {animal.name}.")
        print(f"{self.name} heals {animal.name}.")

# Функция запуска графического интерфейса
def run_gui(zoo):
    # Создание основного окна
    root_window = tk.Tk()
    root_window.title(f"{zoo.name} Management") # Заголовок окна

    # Размеры окна
    root_window.geometry("500x629")

    # Устанавливаем фон окна (оливково-салатовая гамма)
    root_window.configure(bg="#dce2b9")

    # Попытка установить иконку (логотип)
    try:
        root_window.iconbitmap("zoo_logo.ico")  # путь к файлу-иконке
    except Exception as e:
        logging.warning(f"Icon not found: {e}")

    # Цвета для оформления элементов
    bg_color = "#dce2b8"         # фон для лэйблов и окна
    btn_color = "#a9c186"        # цвет кнопок
    text_color = "#333337"       # цвет текста
    entry_bg = "#f8f8f8"         # фон полей ввода

    # Вложенная функция для добавления животного через GUI
    def add_animal_gui():
        name = name_entry.get()  # Получаем имя из поля ввода
        try:
            age = float(age_entry.get())  # Преобразуем возраст в float
        except ValueError:
            messagebox.showerror("Error / Ошибка", "Age must be a positive number / Возраст должен быть положительным числом.")
            return

        animal_type = animal_type_var.get()  # Получаем тип животного

        # Создание животного в зависимости от выбранного типа
        if animal_type == "Bird":
            animal = Bird(name, age)
        elif animal_type == "Mammal":
            animal = Mammal(name, age)
        elif animal_type == "Reptile":
            animal = Reptile(name, age)
        else:
            messagebox.showerror("Error / Ошибка", "Select animal type / Выберите Тип Животного!")
            return

        zoo.add_animal(animal)  # Добавление животного в зоопарк
        messagebox.showinfo("Success / Успешно", f"{animal_type} {name} added to zoo / добавлен в зоопарк.")

        # Функция добавления смотрителя

    def add_keeper():
        name = simple_input("Enter ZooKeeper Name / Введите имя смотрителя:")
        if name:
            zoo.add_staff(ZooKeeper(name))
            messagebox.showinfo("Success / Успешно", f"ZooKeeper/ Смотритель {name} added/ добавлен.")

        # Функция добавления ветеринара

    def add_vet():
        name = simple_input("Enter Veterinarian Name / Введите имя ветеринара:")
        if name:
            zoo.add_staff(Veterinarian(name))
            messagebox.showinfo("Success / Успешно", f"Veterinarian/ Ветеринар {name} added/ добавлен.")

        # Функция вывода звуков животных

    def show_animal_sounds():
        if not zoo.animals:
            messagebox.showinfo("Info / Информация", "No animals in the zoo yet / Животных пока нет.")
            return
        sounds = "\n".join([f"{animal.name}: {animal.__class__.__name__} says…" for animal in zoo.animals])
        animal_sound(zoo.animals)
        messagebox.showinfo("Animal Sounds / Звуки животных", sounds)

        # Функция сохранения зоопарка

    def save_zoo():
        zoo.save_zoo()
        messagebox.showinfo("Success / Успешно", "Zoo state saved/ Зоопарк сохранен.")

        # Функция загрузки зоопарка

    def load_zoo():
        loaded = Zoo.load_zoo()
        zoo.animals = loaded.animals
        zoo.staff = loaded.staff
        zoo.name = loaded.name
        messagebox.showinfo("Loaded / Загружено", "Zoo state loaded/ Зоопарк загружен.")

        # Универсальный ввод через окно

    def simple_input(prompt):
        input_window = tk.Toplevel(root_window)
        input_window.title(prompt)
        input_window.configure(bg=bg_color)
        input_window.geometry("500x98")

        tk.Label(input_window, border=7, width=48, text=prompt, bg=bg_color, fg=text_color).pack()
        entry = tk.Entry(input_window, bg=entry_bg)
        entry.pack()

        result = {'value': None}

        def submit():
            result['value'] = entry.get()
            input_window.destroy()

        tk.Button(input_window, border=1, height=1, width=3, text="OK", command=submit, bg=btn_color,
                  fg=text_color).pack(pady=8)
        input_window.wait_window()
        return result['value']

        # Элементы интерфейса - оформление полей ввода и кнопок

        # Поле имени животного

    tk.Label(root_window, text="Name / введите Имя животного:",  border=18, width=48, bg=bg_color, fg=text_color).pack()
    name_entry = tk.Entry(root_window, width=48, bg=entry_bg)
    name_entry.pack(pady=5)

    # Поле возраста животного
    tk.Label(root_window, text="Age (months) / введите Возраст животного (мес):", border=18, width=48, bg=bg_color, fg=text_color).pack()
    age_entry = tk.Entry(root_window, width=48, bg=entry_bg)
    age_entry.pack(pady=5)

    # Радиокнопки для выбора типа животного
    animal_type_var = tk.StringVar(value="Bird")
    tk.Label(root_window, text="Type / выберите Тип животного:", border=18, width=48, bg=bg_color, fg=text_color).pack(pady=5)
    for animal_type, label in [("Bird", "Bird-Птица"), ("Mammal", "Mammal-Млекопитающее"),
                               ("Reptile", "Reptile-Рептилия")]:
        tk.Radiobutton(root_window, width=48, text=label, variable=animal_type_var, value=animal_type,
                       bg=bg_color, fg=text_color, selectcolor=entry_bg).pack(pady=5)

    # Кнопка добавления животного
    tk.Button(root_window, width=48, text="Add Animal / Добавить Животное", command=add_animal_gui, bg=btn_color,
              fg=text_color).pack(pady=5)

    # Кнопка добавления смотрителя
    tk.Button(root_window, width=48, text="Add ZooKeeper / Добавить смотрителя", command=add_keeper, bg=btn_color,
              fg=text_color).pack(pady=5)

    # Кнопка добавления ветеринара
    tk.Button(root_window, width=48, text="Add Veterinarian / Добавить ветеринара", command=add_vet, bg=btn_color,
              fg=text_color).pack(pady=5)

    # Кнопка вывода звуков животных
    tk.Button(root_window, width=48, text="Show Animal Sounds / Звуки животных", command=show_animal_sounds, bg=btn_color,
              fg=text_color).pack(pady=5)

    # Кнопка сохранения зоопарка
    tk.Button(root_window, width=48, text="Save Zoo / Сохранить зоопарк", command=save_zoo, bg=btn_color, fg=text_color).pack(
        pady=5)

    # Кнопка загрузки зоопарка
    tk.Button(root_window, width=48, text="Load Zoo / Загрузить зоопарк", command=load_zoo, bg=btn_color, fg=text_color).pack(
        pady=5)

    # Кнопка выхода
    tk.Button(root_window, width=48, text="Exit / Выход", command=root_window.destroy, bg=btn_color, fg=text_color).pack(pady=12)

    root_window.mainloop()  # Запуск главного цикла окна
