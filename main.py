import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
import logging
import os
import pickle
import sys

try:
    import pygame

    pygame.mixer.init()
    pygame_available = True
except ImportError:
    pygame = None
    pygame_available = False
    print("Pygame не установлен, звуки отключены")

logging.basicConfig(
    filename="zoo_log.txt",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

admin_password = "admin123"


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        pass

    def eat(self):
        logging.info(f"{self.name} ест.")
        print(f"{self.name} ест.")

    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}, возраст {self.age} лет"


class Bird(Animal):
    def make_sound(self):
        logging.info(f"{self.name} чирикает.")
        print(f"{self.name} чирикает.")
        if pygame_available:
            try:
                pygame.mixer.music.load("bird_sound.mp3")
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Ошибка воспроизведения звука птицы: {e}")


class Mammal(Animal):
    def make_sound(self):
        logging.info(f"{self.name} рычит.")
        print(f"{self.name} рычит.")
        if pygame_available:
            try:
                pygame.mixer.music.load("mammal_sound.mp3")
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Ошибка воспроизведения звука млекопитающего: {e}")


class Reptile(Animal):
    def make_sound(self):
        logging.info(f"{self.name} шипит.")
        print(f"{self.name} шипит.")
        if pygame_available:
            try:
                pygame.mixer.music.load("reptile_sound.mp3")
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Ошибка воспроизведения звука рептилии: {e}")


class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)
        logging.info(f"Животное {animal.name} добавлено в зоопарк.")

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        logging.info(f"Сотрудник {staff_member.name} нанят.")

    def save_zoo(self, filename="zoo_data.pkl"):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self, file)
            logging.info(f"Состояние зоопарка сохранено в {filename}.")
            return True
        except (IOError, pickle.PicklingError) as e:
            logging.error(f"Ошибка сохранения зоопарка: {e}")
            return False

    @staticmethod
    def load_zoo(filename="zoo_data.pkl"):
        try:
            with open(filename, 'rb') as file:
                zoo_obj = pickle.load(file)
            logging.info(f"Состояние зоопарка загружено из {filename}.")
            return zoo_obj
        except FileNotFoundError:
            logging.error(f"Файл {filename} не найден.")
            raise
        except (IOError, pickle.UnpicklingError) as e:
            logging.error(f"Ошибка загрузки зоопарка: {e}")
            raise


class Staff:
    def __init__(self, name):
        self.name = name


class ZooKeeper(Staff):
    def feed_animal(self, animal):
        logging.info(f"{self.name} кормит {animal.name}.")
        print(f"{self.name} кормит {animal.name}.")


class Veterinarian(Staff):
    def heal_animal(self, animal):
        logging.info(f"{self.name} лечит {animal.name}.")
        print(f"{self.name} лечит {animal.name}.")


def run_gui(zoo):
    root_window = tk.Tk()
    root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
    root_window.geometry("500x750")  # Increased height to 750

    colors = {
        'bg_color': "#dce2b9",
        'btn_color': "#a9c186",
        'text_color': "#5D4037",
        'entry_bg': "#f8f8f8",
        'accent_color': "#8D6E63",
        'success_bg': "#dce2b9",  # Changed to match main window background
        'success_fg': "#5D4037",
        'tab_bg': "#a9c186",
        'tab_fg': "#5D4037"
    }

    root_window.configure(bg=colors['bg_color'])

    try:
        root_window.iconbitmap("zoo_logo.ico")
    except Exception as icon_exc:
        logging.warning(f"Иконка не найдена: {icon_exc}")

    def create_toplevel(title, width=400, height=300):
        window = tk.Toplevel(root_window)
        window.title(title)
        window.geometry(f"{width}x{height}")
        window.configure(bg=colors['bg_color'])
        return window

    def create_label(parent, text, bg=None, fg=None, font_size=10):
        bg = bg or colors['bg_color']
        fg = fg or colors['text_color']
        return tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Arial", font_size)
        )

    def create_button(parent, text, command, width=50, font_size=9):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=colors['btn_color'],
            fg=colors['text_color'],
            width=width,
            font=("Arial", font_size)
        )

    def create_option_menu(parent, variable, options, width=47):
        menu = tk.OptionMenu(parent, variable, *options)
        menu.config(
            bg=colors['btn_color'],
            fg=colors['text_color'],
            width=width,
            font=("Arial", 9)
        )
        return menu

    def apply_colors():
        root_window.configure(bg=colors['bg_color'])
        for widget in root_window.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=colors['btn_color'], fg=colors['text_color'])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=colors['bg_color'], fg=colors['text_color'])
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=colors['entry_bg'], fg=colors['text_color'])
            elif isinstance(widget, tk.OptionMenu):
                widget.configure(bg=colors['btn_color'], fg=colors['text_color'])

    def show_success_message(title, message):
        success_window = tk.Toplevel(root_window)
        success_window.title(title)
        success_window.geometry("400x150")
        success_window.configure(bg=colors['success_bg'])  # Now matches main window
        success_window.resizable(False, False)

        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        success_window.geometry(f"400x150+{x}+{y}")

        label = tk.Label(
            success_window,
            text=message,
            bg=colors['success_bg'],
            fg=colors['success_fg'],
            font=("Arial", 11),
            wraplength=380
        )
        label.pack(expand=True, padx=20, pady=20)

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

    def configure_colors():
        color_window = create_toplevel("Настройки цветов | Color Settings", 300, 300)

        def update_color(color_var, color_key):
            new_color = color_var.get()
            if new_color:
                colors[color_key] = new_color
                apply_colors()

        create_label(color_window, "Цвет фона: | Background Color:").pack(pady=5)
        bg_var = tk.StringVar(value=colors['bg_color'])
        tk.Entry(color_window, textvariable=bg_var).pack(pady=5)
        create_button(color_window, "Применить | Apply", lambda: update_color(bg_var, 'bg_color'), width=20).pack(
            pady=5)

        create_label(color_window, "Цвет кнопок: | Button Color:").pack(pady=5)
        btn_var = tk.StringVar(value=colors['btn_color'])
        tk.Entry(color_window, textvariable=btn_var).pack(pady=5)
        create_button(color_window, "Применить | Apply", lambda: update_color(btn_var, 'btn_color'), width=20).pack(
            pady=5)

        create_label(color_window, "Цвет текста: | Text Color:").pack(pady=5)
        text_var = tk.StringVar(value=colors['text_color'])
        tk.Entry(color_window, textvariable=text_var).pack(pady=5)
        create_button(color_window, "Применит | Apply", lambda: update_color(text_var, 'text_color'), width=20).pack(
            pady=5)

        create_label(color_window, "Фон полей ввода: | Entry Background:").pack(pady=5)
        entry_var = tk.StringVar(value=colors['entry_bg'])
        tk.Entry(color_window, textvariable=entry_var).pack(pady=5)
        create_button(color_window, "Применить | Apply", lambda: update_color(entry_var, 'entry_bg'), width=20).pack(
            pady=5)

    def change_admin_password():
        global admin_password
        current = simpledialog.askstring("Смена пароля | Password Change",
                                         "Введите текущий пароль: | Enter current password:", show='*')
        if current != admin_password:
            messagebox.showerror("Ошибка | Error", "Неверный текущий пароль! | Incorrect current password!")
            return

        new_pass = simpledialog.askstring("Смена пароля | Password Change",
                                          "Введите новый пароль: | Enter new password:", show='*')
        confirm = simpledialog.askstring("Смена пароля | Password Change",
                                         "Подтвердите новый пароль: | Confirm new password:", show='*')

        if new_pass and new_pass == confirm:
            admin_password = new_pass
            show_success_message("Успех | Success", "Пароль успешно изменен! | Password changed successfully!")
            logging.info("Пароль администратора изменен. | Admin password changed.")
        else:
            messagebox.showerror("Ошибка | Error", "Пароли не совпадают! | Passwords do not match!")

    def authenticate_admin():
        password = simpledialog.askstring("Аутентификация | Authentication",
                                          "Введите пароль администратора: | Enter admin password:", show='*')
        return password == admin_password

    def view_entities():
        view_window = create_toplevel("Объекты зоопарка | Zoo Entities", 650, 450)

        style = ttk.Style()
        style.configure("TNotebook", background=colors['bg_color'])
        style.configure("TNotebook.Tab",
                        background=colors['tab_bg'],
                        foreground=colors['tab_fg'],
                        font=("Arial", 10, "bold"),
                        padding=[10, 5])
        style.map("TNotebook.Tab",
                  background=[("selected", colors['accent_color'])])

        notebook = ttk.Notebook(view_window)
        notebook.pack(fill='both', expand=True)

        animals_frame = ttk.Frame(notebook)
        notebook.add(animals_frame, text="Животные | Animals")

        staff_frame = ttk.Frame(notebook)
        notebook.add(staff_frame, text="Сотрудники | Staff")

        def refresh_data():
            animal_tree.delete(*animal_tree.get_children())
            for animal in zoo.animals:
                animal_tree.insert("", "end", values=(animal.name, animal.age, animal.__class__.__name__))

            staff_tree.delete(*staff_tree.get_children())
            for staff_member in zoo.staff:
                staff_tree.insert("", "end", values=(staff_member.name, staff_member.__class__.__name__))

        animal_columns = ("Имя | Name", "Возраст | Age", "Тип | Type")
        animal_tree = ttk.Treeview(animals_frame, columns=animal_columns, show="headings")
        for col in animal_columns:
            animal_tree.heading(col, text=col)
            animal_tree.column(col, width=100)
        animal_tree.pack(fill='both', expand=True)

        staff_columns = ("Имя | Name", "Должность | Position")
        staff_tree = ttk.Treeview(staff_frame, columns=staff_columns, show="headings")
        for col in staff_columns:
            staff_tree.heading(col, text=col)
            staff_tree.column(col, width=100)
        staff_tree.pack(fill='both', expand=True)

        refresh_data()

        def apply_filter():
            filter_text = filter_entry.get().lower()
            selected_type = filter_type_var.get()

            animal_tree.delete(*animal_tree.get_children())
            for animal in zoo.animals:
                if selected_type == "Все | All" or animal.__class__.__name__ == selected_type.split(" | ")[0]:
                    if filter_text in animal.name.lower():
                        animal_tree.insert("", "end", values=(animal.name, animal.age, animal.__class__.__name__))

            staff_tree.delete(*staff_tree.get_children())
            for staff_member in zoo.staff:
                if selected_type == "Все | All" or staff_member.__class__.__name__ == selected_type.split(" | ")[0]:
                    if filter_text in staff_member.name.lower():
                        staff_tree.insert("", "end", values=(staff_member.name, staff_member.__class__.__name__))

        filter_frame = tk.Frame(view_window, bg=colors['bg_color'])
        filter_frame.pack(fill='x', padx=5, pady=5)

        # First row for filter entry
        filter_row1 = tk.Frame(filter_frame, bg=colors['bg_color'])
        filter_row1.pack(fill='x', pady=5)

        create_label(filter_row1, "Фильтр: | Filter:").pack(side='left')
        filter_entry = tk.Entry(filter_row1)
        filter_entry.pack(side='left', padx=5, fill='x', expand=True)

        # Second row for type selection and apply button
        filter_row2 = tk.Frame(filter_frame, bg=colors['bg_color'])
        filter_row2.pack(fill='x', pady=5)

        # Wider "All" dropdown and "Apply Filter" button
        filter_type_var = tk.StringVar(value="Все | All")
        filter_types = ["Все | All", "Bird | Птица", "Mammal | Млекопитающее", "Reptile | Рептилия",
                        "ZooKeeper | Смотритель", "Veterinarian | Ветеринар"]
        create_label(filter_row2, "Тип: | Type:").pack(side='left')
        filter_menu = create_option_menu(filter_row2, filter_type_var, filter_types, width=25)  # Increased width
        filter_menu.pack(side='left', padx=5)

        # Wider "Apply Filter" button to match bottom buttons
        apply_filter_btn = create_button(filter_row2, "Применить фильтр | Apply Filter", apply_filter, width=30,
                                         font_size=9)
        apply_filter_btn.pack(side='left', padx=5)

        def delete_entity():
            if not authenticate_admin():
                messagebox.showerror("Ошибка | Error",
                                     "Ошибка аутентификации администратора! | Admin authentication failed!")
                return

            current_tab = notebook.index(notebook.select())

            if current_tab == 0:
                selected = animal_tree.selection()
                if not selected:
                    return
                item_data = animal_tree.item(selected[0])
                name = item_data['values'][0]

                if messagebox.askyesno("Подтверждение | Confirm", f"Удалить животное {name}? | Delete animal {name}?"):
                    for animal in zoo.animals[:]:
                        if animal.name == name:
                            zoo.animals.remove(animal)
                            logging.info(f"Животное {name} удалено. | Animal {name} deleted.")
                            break
                    refresh_data()

            elif current_tab == 1:
                selected = staff_tree.selection()
                if not selected:
                    return
                item_data = staff_tree.item(selected[0])
                name = item_data['values'][0]

                if messagebox.askyesno("Подтверждение | Confirm",
                                       f"Удалить сотрудника {name}? | Delete staff member {name}?"):
                    for staff_member in zoo.staff[:]:
                        if staff_member.name == name:
                            zoo.staff.remove(staff_member)
                            logging.info(f"Сотрудник {name} удален. | Staff {name} deleted.")
                            break
                    refresh_data()

        def edit_entity():
            if not authenticate_admin():
                messagebox.showerror("Ошибка | Error",
                                     "Ошибка аутентификации администратора! | Admin authentication failed!")
                return

            current_tab = notebook.index(notebook.select())
            selected = animal_tree.selection() if current_tab == 0 else staff_tree.selection()

            if not selected:
                return

            if current_tab == 0:
                item_data = animal_tree.item(selected[0])
                name, age, animal_class = item_data['values']
                animal = next((a for a in zoo.animals if a.name == name), None)
                if not animal:
                    return

                edit_window = create_toplevel("Редактировать животное | Edit Animal", 300, 150)

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
                    new_name = name_var.get()
                    try:
                        new_age = float(age_var.get())
                        if new_age <= 0:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Ошибка | Error", "Некорректное значение возраста! | Invalid age value!")
                        return

                    animal.name = new_name
                    animal.age = new_age
                    logging.info(f"Животное {name} обновлено: {new_name}, возраст {new_age}")
                    refresh_data()
                    edit_window.destroy()
                    show_success_message("Успех | Success", "Данные животного обновлены! | Animal updated!")

                create_button(edit_window, "Сохранить | Save", save_changes, width=20).pack(pady=10)

            elif current_tab == 1:
                item_data = staff_tree.item(selected[0])
                name = item_data['values'][0]
                staff = next((s for s in zoo.staff if s.name == name), None)
                if not staff:
                    return

                edit_window = create_toplevel("Редактировать сотрудника | Edit Staff", 300, 150)

                create_label(edit_window, "Новое имя: | New Name:").pack(pady=5)
                name_var = tk.StringVar(value=name)
                name_entry_edit = tk.Entry(edit_window, textvariable=name_var, bg=colors['entry_bg'],
                                           fg=colors['text_color'])
                name_entry_edit.pack(pady=5)

                def save_changes():
                    new_name = name_var.get()
                    staff.name = new_name
                    logging.info(f"Сотрудник {name} обновлен: {new_name}")
                    refresh_data()
                    edit_window.destroy()
                    show_success_message("Успех | Success", "Данные сотрудника обновлены! | Staff updated!")

                create_button(edit_window, "Сохранить | Save", save_changes, width=20).pack(pady=10)

        btn_frame = tk.Frame(view_window, bg=colors['bg_color'])
        btn_frame.pack(fill='x', padx=5, pady=5)

        # Buttons with consistent width and font size
        delete_btn = create_button(btn_frame, "Удалить выбранное | Delete Selected", delete_entity, width=28,
                                   font_size=9)
        delete_btn.pack(side='left', padx=2, fill='x', expand=True)

        edit_btn = create_button(btn_frame, "Редактировать выбранное | Edit Selected", edit_entity, width=28,
                                 font_size=9)
        edit_btn.pack(side='left', padx=2, fill='x', expand=True)

        refresh_btn = create_button(btn_frame, "Обновить | Refresh", refresh_data, width=20, font_size=9)
        refresh_btn.pack(side='right', padx=2, fill='x', expand=True)

    def play_animal_sound():
        if not zoo.animals:
            messagebox.showinfo("Информация | Info", "В зоопарке пока нет животных. | No animals in the zoo yet.")
            return

        sound_window = create_toplevel("Воспроизвести звук животного | Play Animal Sound", 350, 180)

        create_label(sound_window, "Выберите животное: | Select an animal:").pack(pady=10)

        animal_var = tk.StringVar()
        animal_names = [animal.name for animal in zoo.animals]
        if not animal_names:
            create_label(sound_window, "Нет животных для воспроизведения звука. | No animals available.").pack()
            return

        animal_menu = create_option_menu(sound_window, animal_var, animal_names)
        animal_menu.pack(pady=5)

        def play_sound():
            selected_name = animal_var.get()
            if not selected_name:
                return

            animal = next((a for a in zoo.animals if a.name == selected_name), None)
            if animal:
                animal.make_sound()
                logging.info(f"Воспроизведен звук животного: {animal.name}")

        create_button(sound_window, "Воспроизвести звук | Play Sound", play_sound, width=30).pack(pady=10)

    def add_animal_gui():
        name = name_entry.get()
        if not name:
            messagebox.showerror("Ошибка | Error", "Введите имя животного! | Enter animal name!")
            return

        try:
            age = float(age_entry.get())
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка | Error",
                                 "Возраст должен быть положительным числом! | Age must be a positive number!")
            return

        selected_type = animal_type_var.get().split(" | ")[0]

        if selected_type == "Птица":
            animal = Bird(name, age)
        elif selected_type == "Млекопитающее":
            animal = Mammal(name, age)
        elif selected_type == "Рептилия":
            animal = Reptile(name, age)
        else:
            messagebox.showerror("Ошибка | Error", "Выберите тип животного! | Select animal type!")
            return

        zoo.add_animal(animal)
        show_success_message("Успех | Success",
                             f"{selected_type} {name} добавлен в зоопарк. | {selected_type} {name} added to zoo.")
        logging.info(f"Добавлено животное: {name} ({selected_type})")

        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)

    def add_keeper():
        name = keeper_entry.get()
        if not name:
            messagebox.showerror("Ошибка | Error", "Введите имя смотрителя! | Enter keeper name!")
            return

        zoo.add_staff(ZooKeeper(name))
        show_success_message("Успех | Success", f"Смотритель {name} добавлен. | ZooKeeper {name} added.")
        logging.info(f"Добавлен сотрудник: {name} (Смотритель)")
        keeper_entry.delete(0, tk.END)

    def add_vet():
        name = vet_entry.get()
        if not name:
            messagebox.showerror("Ошибка | Error", "Введите имя ветеринара! | Enter veterinarian name!")
            return

        zoo.add_staff(Veterinarian(name))
        show_success_message("Успех | Success", f"Ветеринар {name} добавлен. | Veterinarian {name} added.")
        logging.info(f"Добавлен сотрудник: {name} (Ветеринар)")
        vet_entry.delete(0, tk.END)

    def save_zoo():
        save_filename = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
            title="Сохранить зоопарк | Save Zoo"
        )
        if save_filename:
            if zoo.save_zoo(save_filename):
                show_success_message("Успех | Success",
                                     f"Зоопарк сохранен в {os.path.basename(save_filename)} | Zoo saved to {os.path.basename(save_filename)}")
                logging.info(f"Зоопарк сохранен в {save_filename}")
            else:
                messagebox.showerror("Ошибка | Error", "Не удалось сохранить зоопарк! | Failed to save zoo!")

    def load_zoo():
        load_filename = filedialog.askopenfilename(
            filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
            title="Загрузить зоопарк | Load Zoo"
        )
        if load_filename:
            try:
                loaded_zoo = Zoo.load_zoo(load_filename)
                zoo.animals = loaded_zoo.animals
                zoo.staff = loaded_zoo.staff
                zoo.name = loaded_zoo.name
                root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
                show_success_message("Успех | Success",
                                     f"Зоопарк загружен из {os.path.basename(load_filename)} | Zoo loaded from {os.path.basename(load_filename)}")
                logging.info(f"Зоопарк загружен из {load_filename}")
            except Exception as load_exc:
                logging.error(f"Ошибка загрузки зоопарка: {load_exc}")
                if messagebox.askyesno("Ошибка | Error",
                                       "Не удалось загрузить зоопарк. Создать новый? | Failed to load zoo. Create new zoo?"):
                    zoo.animals = []
                    zoo.staff = []
                    zoo.name = "Новый зоопарк | New Zoo"
                    root_window.title(f"Управление зоопарком: {zoo.name} | Zoo Management: {zoo.name}")
                    logging.info("Создан новый зоопарк после ошибки загрузки")

    # Main Interface
    create_label(root_window, "Добавление животных | Add Animals", font_size=11).pack(pady=(10, 5))

    create_label(root_window, "Имя животного: | Animal Name:").pack()
    name_entry = tk.Entry(root_window, width=48, bg=colors['entry_bg'], fg=colors['text_color'])
    name_entry.pack(pady=2)

    create_label(root_window, "Возраст (месяцев): | Age (months):").pack()
    age_entry = tk.Entry(root_window, width=48, bg=colors['entry_bg'], fg=colors['text_color'])
    age_entry.pack(pady=2)

    animal_type_var = tk.StringVar(value="Птица | Bird")
    create_label(root_window, "Тип животного: | Animal Type:").pack(pady=2)

    animal_types = ["Птица | Bird", "Млекопитающее | Mammal", "Рептилия | Reptile"]
    animal_type_menu = create_option_menu(root_window, animal_type_var, animal_types)
    animal_type_menu.pack(pady=2)

    create_button(root_window, "Добавить животное | Add Animal", add_animal_gui).pack(pady=7)

    create_label(root_window, "Добавление персонала | Add Staff", font_size=11).pack(pady=(15, 5))

    create_label(root_window, "Имя смотрителя: | ZooKeeper Name:").pack()
    keeper_entry = tk.Entry(root_window, width=48, bg=colors['entry_bg'], fg=colors['text_color'])
    keeper_entry.pack(pady=2)

    create_button(root_window, "Добавить смотрителя | Add ZooKeeper", add_keeper).pack(pady=7)

    create_label(root_window, "Имя ветеринара: | Veterinarian Name:").pack()
    vet_entry = tk.Entry(root_window, width=48, bg=colors['entry_bg'], fg=colors['text_color'])
    vet_entry.pack(pady=2)

    create_button(root_window, "Добавить ветеринара | Add Veterinarian", add_vet).pack(pady=7)

    create_button(root_window, "Воспроизвести звук животного | Play Animal Sound", play_animal_sound).pack(pady=7)
    create_button(root_window, "Просмотр животных и персонала | View Animals and Staff", view_entities).pack(pady=7)
    create_button(root_window, "Сохранить зоопарк | Save Zoo", save_zoo).pack(pady=7)
    create_button(root_window, "Загрузить зоопарк | Load Zoo", load_zoo).pack(pady=7)
    create_button(root_window, "Сменить пароль администратора | Change Admin Password", change_admin_password).pack(
        pady=7)
    create_button(root_window, "Настройки цветов | Color Settings", configure_colors).pack(pady=7)
    create_button(root_window, "Выход | Exit", root_window.destroy).pack(pady=12)

    apply_colors()
    root_window.mainloop()


if __name__ == "__main__":
    zoo_instance = None

    try:
        zoo_instance = Zoo.load_zoo("last_zoo.pkl")
        logging.info("Автоматически загружено состояние зоопарка")
    except Exception as auto_load_error:
        logging.warning(f"Ошибка автоматической загрузки: {auto_load_error}")
        if messagebox.askyesno("Ошибка загрузки | Load Error",
                               "Не удалось загрузить зоопарк. Создать новый? | Failed to load zoo. Create new zoo?"):
            zoo_instance = Zoo("Новый зоопарк | New Zoo")
            logging.info("Создан новый зоопарк после ошибки загрузки")
        else:
            manual_filename = filedialog.askopenfilename(
                filetypes=[("Файлы pickle | Pickle files", "*.pkl"), ("Все файлы | All files", "*.*")],
                title="Выберите файл зоопарка | Select Zoo File"
            )
            if manual_filename:
                try:
                    zoo_instance = Zoo.load_zoo(manual_filename)
                    logging.info(f"Ручная загрузка зоопарка из {manual_filename}")
                except Exception as manual_load_error:
                    logging.error(f"Ошибка ручной загрузки: {manual_load_error}")
                    messagebox.showerror("Ошибка | Error",
                                         "Не удалось загрузить зоопарк. Создаётся новый. | Failed to load zoo. Creating new one.")
                    zoo_instance = Zoo("Новый зоопарк | New Zoo")
            else:
                zoo_instance = Zoo("Новый зоопарк | New Zoo")

    if zoo_instance:
        run_gui(zoo_instance)

    try:
        zoo_instance.save_zoo("last_zoo.pkl")
        logging.info("Состояние зоопарка сохранено при выходе")
    except Exception as save_exc:
        logging.error(f"Ошибка сохранения при выходе: {save_exc}")