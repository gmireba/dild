import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.file_name = "trainings.json"
        self.data = self.load_data()

        # --- Поля ввода ---
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(root, text="Тип тренировки:").grid(row=1, column=0)
        self.type_entry = tk.Entry(root)
        self.type_entry.grid(row=1, column=1)

        tk.Label(root, text="Длительность (мин):").grid(row=2, column=0)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=2, column=1)

        # --- Кнопки ---
        tk.Button(root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Фильтры ---
        tk.Label(root, text="Фильтр (Тип/Дата):").grid(row=4, column=0)
        self.filter_entry = tk.Entry(root)
        self.filter_entry.grid(row=4, column=1)
        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=5, column=0, columnspan=2)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Дата", "Тип", "Длительность"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Длительность", text="Мин.")
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.update_table(self.data)

    def validate(self, date_str, duration_str):
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            if int(duration_str) <= 0:
                raise ValueError
            return True
        except ValueError:
            return False

    def add_training(self):
        date = self.date_entry.get()
        t_type = self.type_entry.get()
        dur = self.duration_entry.get()

        if self.validate(date, dur):
            new_item = {"date": date, "type": t_type, 

"duration": dur}
            self.data.append(new_item)
            self.save_data()
            self.update_table(self.data)
            messagebox.showinfo("Успех", "Тренировка добавлена!")
        else:
            messagebox.showerror("Ошибка", "Неверный формат даты (ДД.ММ.ГГГГ) или длительности!")

    def update_table(self, display_data):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in display_data:
            self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def apply_filter(self):
        query = self.filter_entry.get().lower()
        filtered = [i for i in self.data if query in i["type"].lower() or query in i["date"]]
        self.update_table(filtered)

    def save_data(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
