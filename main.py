# Импорт стандартных модулей Python
import tkinter as tk  # GUI библиотека Tkinter
from tkinter import messagebox  # Для всплывающих сообщений
import logging  # Для логирования действий пользователя в файл
import pickle  # Для сохранения и загрузки состояния программы (зоопарка)

# Настройка логирования: файл, уровень, формат записи
logging.basicConfig(
    filename="zoo_log.txt",  # Имя файла для логов
    level=logging.INFO,  # Уровень логов (INFO — обычные действия)
    format="%(asctime)s — %(levelname)s — %(message)s"  # Формат записи логов
)

# 📌 Базовый класс Animal (Животное)
class Animal:
    def __init__(self, name, age):
        # Атрибуты name и age
        self.name = name
        self.age = age

    # Метод, который должен быть переопределён в потомках
    def make_sound(self):
        pass

    # Метод приёма пищи
    def eat(self):
        logging.info(f"{self.name} is eating.")
        print(f"{self.name} is eating.")

# 📌 Подкласс Bird (Птица)
class Bird(Animal):
    def make_sound(self):
        logging.info(f"{self.name} chirps.")
        print(f"{self.name} chirps.")

# 📌 Подкласс Mammal (Млекопитающее)
class Mammal(Animal):
    def make_sound(self):
        logging.info(f"{self.name} growls.")
        print(f"{self.name} growls.")

# 📌 Подкласс Reptile (Рептилия)
class Reptile(Animal):
    def make_sound(self):
        logging.info(f"{self.name} hisses.")
        print(f"{self.name} hisses.")

# 📌 Функция демонстрации полиморфизма: все животные из списка издают звук
def animal_sound(animals):
    for animal in animals:
        animal.make_sound()

# 📌 Класс Zoo (Композиция животных и сотрудников)
class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []  # Список животных
        self.staff = []  # Список сотрудников

    # Добавление животного
    def add_animal(self, animal):
        self.animals.append(animal)
        logging.info(f"Animal {animal.name} added to the zoo.")

    # Добавление сотрудника
    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        logging.info(f"Staff {staff_member.name} hired.")

    # Сохранение состояния зоопарка в файл
    def save_zoo(self, filename="zoo_data.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        logging.info("Zoo state saved to file.")

    # Загрузка состояния зоопарка из файла
    @staticmethod
    def load_zoo(filename="zoo_data.pkl"):
        with open(filename, 'rb') as f:
            zoo = pickle.load(f)
        logging.info("Zoo state loaded from file.")
        return zoo

# 📌 Базовый класс сотрудника
class Staff:
    def __init__(self, name):
        self.name = name

# 📌 Класс смотрителя зоопарка
class ZooKeeper(Staff):
    def feed_animal(self, animal):
        logging.info(f"{self.name} feeds {animal.name}.")
        print(f"{self.name} feeds {animal.name}.")

# 📌 Класс ветеринара
class Veterinarian(Staff):
    def heal_animal(self, animal):
        logging.info(f"{self.name} heals {animal.name}.")
        print(f"{self.name} heals {animal.name}.")

# 📌 GUI интерфейс на Tkinter
def run_gui(zoo):
    root_window = tk.Tk()
    root_window.title(f"{zoo.name} Management")

    # Функция для добавления животного через GUI
    def add_animal_gui():
        name = name_entry.get()
        age = int(age_entry.get())
        animal_type = animal_type_var.get()

        if animal_type == "Bird":
            animal = Bird(name, age)
        elif animal_type == "Mammal":
            animal = Mammal(name, age)
        elif animal_type == "Reptile":
            animal = Reptile(name, age)
        else:
            messagebox.showerror("Error", "Select animal type!")
            return

        zoo.add_animal(animal)
        messagebox.showinfo("Success", f"{animal_type} {name} added to zoo.")

    # Интерфейсные элементы окна
    tk.Label(root_window, text="Name:").pack()
    name_entry = tk.Entry(root_window)
    name_entry.pack()

    tk.Label(root_window, text="Age:").pack()
    age_entry = tk.Entry(root_window)
    age_entry.pack()

    animal_type_var = tk.StringVar(value="Bird")
    tk.Label(root_window, text="Type:").pack()

    # Радиокнопки выбора типа животного
    tk.Radiobutton(root_window, text="Bird", variable=animal_type_var, value="Bird").pack()
    tk.Radiobutton(root_window, text="Mammal", variable=animal_type_var, value="Mammal").pack()
    tk.Radiobutton(root_window, text="Reptile", variable=animal_type_var, value="Reptile").pack()

    # Кнопка добавления животного
    tk.Button(root_window, text="Add Animal", command=add_animal_gui).pack()

    root_window.mainloop()

# 📌 Консольное меню пользователя
def menu(zoo):
    while True:
        print("\nZoo Management System")
        print("1. Add Animal")
        print("2. Add ZooKeeper")
        print("3. Add Veterinarian")
        print("4. Show Animal Sounds")
        print("5. Save Zoo")
        print("6. Load Zoo")
        print("7. Open GUI")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Animal Name: ")
            age = int(input("Animal Age: "))
            type_choice = input("Type (Bird/Mammal/Reptile): ")
            if type_choice == "Bird":
                zoo.add_animal(Bird(name, age))
            elif type_choice == "Mammal":
                zoo.add_animal(Mammal(name, age))
            elif type_choice == "Reptile":
                zoo.add_animal(Reptile(name, age))
            else:
                print("Invalid animal type!")

        elif choice == "2":
            name = input("ZooKeeper Name: ")
            zoo.add_staff(ZooKeeper(name))

        elif choice == "3":
            name = input("Veterinarian Name: ")
            zoo.add_staff(Veterinarian(name))

        elif choice == "4":
            animal_sound(zoo.animals)

        elif choice == "5":
            zoo.save_zoo()

        elif choice == "6":
            zoo = Zoo.load_zoo()

        elif choice == "7":
            run_gui(zoo)

        elif choice == "0":
            break

        else:
            print("Invalid choice!")

# 📌 Запуск программы
if __name__ == "__main__":
    zoo = Zoo("City Zoo")
    menu(zoo)
