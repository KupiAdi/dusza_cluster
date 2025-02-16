import customtkinter as ctk
import os
import random
import string
from datetime import datetime
from tkinter import messagebox
import re

dir = ""
lang = "hu"
appearance_mode = "System"
update = True

translations = {
    "hu": {
        "input_labels": {
            "computer_name": "Számítógép neve",
            "enter_dir": "Add meg a könyvtárat:",
            "program_name": "Program neve",
            "new_computer_name": "Új számítógép neve",
            "cpu": "Proccesszor erőforrás",
            "ram": "Memóriakapacítás",
            "number_of_copies": "Példányok száma"
        },
        "button_labels": {
            "monitoring": "Monitoring",
            "delete_computer": "Számítógép törlése",
            "add_computer": "Számítógép hozzáadása",
            "stop_program": "Program leállítása",
            "modify_program": "Program adatainak módosítása",
            "run_new_instance": "Új programpéldány futtatása",
            "stop_instance": "Adott programpéldány leállítása",
            "exit": "Kilépés",
            "cancel": "Mégse",
            "back": "Vissza",
            "dark": ["Sötét", "Dark"],
            "light": ["Világos", "Light"],
            "system": ["Rendszer", "System"]
        },
        "messages": {
            "cluster_not_found": "A .klaszter fájl nem található!",
            "all_running_processes": "Összes futó folyamat:",
            "active": "AKTÍV",
            "inactive": "INAKTÍV",
            "cluster_status_correct": "A klaszter állapota helyes",
            "cluster_status_not_correct": "A klaszter állapota NEM helyes",
            "error_state": "Hibás állapot:",
            "expected_instances": "esetén várva",
            "actual_instances": ", valós példány:",
            "computer": "Számítógép",
            "id": "Azonosító",
            "resource_requirements": "Erőforrásigény",
            "status": "Státusz",
            "total_running_instances": "Összes futó példány száma",
            "no_running_instance_with_this_name": "Nincs futó példány ezzel a névvel",
            "running_instances": "futó példányai",
            "computer_not_empty": "A számítógép nem üres",
            "running_programs": "Futó programok:",
            "no_computer_found": "Nincs ilyen számítógép!",
            "computer_already_exists": "Ez a számítógép már létezik!",
            "no_program_found": "Nincs ilyen program!",
            "invalid_computer_program_name": "Nem megfelelő a számítógép/program neve!",
            "invalid_resource_value": "Nem megfelelő erőforrás érték!",
            "invalid_computer_name": "Nem megfelelő számítógép név!",
            "free": "Szabad",
            "language": "Nyelv:",
            "theme": "Téma:"
        }
    },
    "en": {
        "input_labels": {
            "computer_name": "Computer name",
            "enter_dir": "Enter the directory:",
            "program_name": "Program name",
            "new_computer_name": "New computer name",
            "cpu": "Processor resource",
            "ram": "Memory capacity",
            "number_of_copies": "Number of copies"
        },
        "button_labels": {
            "monitoring": "Monitoring",
            "delete_computer": "Delete computer",
            "add_computer": "Add computer",
            "stop_program": "Stop program",
            "modify_program": "Modify program",
            "run_new_instance": "Run new instance",
            "stop_instance": "Stop specific instance",
            "exit": "Exit",
            "cancel": "Cancel",
            "back": "Back",
            "dark": "Dark",
            "light": "Light",
            "system": "System"
        },
        "messages": {
            "cluster_not_found": "The .klaszter file not found!",
            "all_running_processes": "All running processes:",
            "active": "ACTIVE",
            "inactive": "INACTIVE",
            "cluster_status_correct": "The cluster status is correct",
            "cluster_status_not_correct": "The cluster status is NOT correct",
            "error_state": "Error state: For",
            "expected_instances": "expected",
            "actual_instances": " instance(s), actual instance(s):",
            "computer": "Computer",
            "id": "ID",
            "resource_requirements": "Resource Requirements",
            "status": "Status",
            "total_running_instances": "Total Running Instances",
            "no_running_instance_with_this_name": "No running instance with this name",
            "running_instances": "running instances of",
            "computer_not_empty": "The computer is not empty",
            "running_programs": "Running programs:",
            "no_computer_found": "No such computer!",
            "computer_already_exists": "This computer already exists!",
            "no_program_found": "No such program!",
            "invalid_computer_program_name": "Invalid computer/program name!",
            "invalid_resource_value": "Invalid resource value!",
            "invalid_computer_name": "Invalid computer name!",
            "free": "Free",
            "language": "Language:",
            "theme": "Theme:"
        }
    }
}

def update_language(new_lang, app):
    global lang
    lang = new_lang
    refresh_ui(app)

def refresh_ui(app):
    if isinstance(app, InputApp):
        app.label.configure(text=translations[lang]["input_labels"]["enter_dir"])
        app.lang_label.configure(text=translations[lang]["messages"]["language"])
    elif isinstance(app, MainApp):
        for widget in app.header_frame.winfo_children():
            widget.destroy()
        app.create_header()
        for widget in app.main_frame.winfo_children():
            widget.destroy()
        app.create_boxes(app.status())
        for button in app.button_frames:
            button.grid_forget()
        app.create_buttons()

ctk.set_appearance_mode(appearance_mode)
ctk.set_default_color_theme("blue")

class InputApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cluster manager")
        self.geometry("400x200")

        self.header_frame = ctk.CTkFrame(self, height=50, fg_color="gray20")
        self.header_frame.pack(side="top", fill="x")

        ctk.CTkLabel(self.header_frame, text="Cluster manager", font=("Arial", 18)).pack(side="left", padx=10 ,pady=10)
        self.lang_dropdown = ctk.CTkOptionMenu(self.header_frame, values=["hu", "en"], command=lambda new_lang: update_language(new_lang, self))
        self.lang_label = ctk.CTkLabel(self.header_frame, text=translations[lang]["messages"]["language"])

        self.lang_dropdown.pack(side="right", padx=10, pady=10)
        self.lang_label.pack(side="right", pady=10)

        self.label = ctk.CTkLabel(self, text=translations[lang]["input_labels"]["enter_dir"])
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="OK", command=self.open_main_app)
        self.button.pack(pady=10)

    def open_main_app(self):
        global dir
        input = self.entry.get()
        if input:
            if os.path.isfile(f"{input}/.klaszter"):
                dir = input
                self.withdraw()
                self.main_app = MainApp()
                self.main_app.mainloop()
            else:
                messagebox.showerror(title="Error", message=translations[lang]["messages"]["cluster_not_found"])

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        global klaszter
        klaszter = open(f'{dir}/.klaszter', 'r')

        self.title("Cluster manager")
        self.geometry("800x600")

        self.header_frame = ctk.CTkFrame(self, height=50, fg_color="gray20")
        self.header_frame.pack(side="top", fill="x")

        self.create_header()

        self.footer_frame = ctk.CTkFrame(self, height=150, fg_color="gray30")
        self.footer_frame.pack(side="bottom", fill="x")

        self.button_frames = []

        self.create_buttons()

        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(expand=True, fill="both")

        self.start()

        self.protocol("WM_DELETE_WINDOW", self.exit_program)

    def create_boxes(self, results):
        cols = 3
        total_boxes = len(results)
        for i in range(total_boxes):
            row = i // cols
            col = i % cols
            box = ctk.CTkFrame(self.main_frame, fg_color="gray40", corner_radius=5)
            box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            self.main_frame.grid_columnconfigure(col, weight=1)
            self.main_frame.grid_rowconfigure(row, weight=1)

            title = ctk.CTkLabel(box, text=results[i]["pc"], font=("Arial", 22))
            title.pack(side="top", fill="x", padx=5)

            ctk.CTkLabel(box, text=f"Max CPU: {results[i]["max_cpu"]} Max RAM: {results[i]["max_ram"]}").pack(fill="x", padx=5)
            ctk.CTkLabel(box, text=f"{translations[lang]["messages"]["free"]} CPU: {results[i]["free_cpu"]} {translations[lang]["messages"]["free"]} RAM: {results[i]["free_ram"]}").pack(fill="x", padx=5)
            for j in range(len(results[i]["active_programs"])):
                ctk.CTkLabel(box, text=results[i]["active_programs"][j]).pack(fill="x", padx=5)

    def create_header(self):
        ctk.CTkLabel(self.header_frame, text="Cluster manager", font=("Arial", 22)).pack(side="left", padx=10 ,pady=10)
        self.lang_dropdown = ctk.CTkOptionMenu(self.header_frame, values=["hu", "en"], command=lambda new_lang: update_language(new_lang, self))
        self.lang_dropdown.pack(side="right", padx=10, pady=10)
        self.lang_dropdown.set(lang)

        ctk.CTkLabel(self.header_frame, text=translations[lang]["messages"]["language"]).pack(side="right", pady=10)

        if lang == "hu":
            self.appearance_mode_dropdown = ctk.CTkOptionMenu(self.header_frame, values=[translations[lang]["button_labels"]["dark"][0], translations[lang]["button_labels"]["light"][0], translations[lang]["button_labels"]["system"][0]], command=self.change_appearance_mode_event)
            self.appearance_mode_dropdown.set(translations[lang]["button_labels"][appearance_mode.lower()][0])
            self.appearance_mode_dropdown.pack(side="right", padx=10, pady=10)
        elif lang == "en":
            self.appearance_mode_dropdown = ctk.CTkOptionMenu(self.header_frame, values=[translations[lang]["button_labels"]["dark"], translations[lang]["button_labels"]["light"], translations[lang]["button_labels"]["system"]], command=self.change_appearance_mode_event)
            self.appearance_mode_dropdown.set(appearance_mode)
            self.appearance_mode_dropdown.pack(side="right", padx=10, pady=10)
            
        ctk.CTkLabel(self.header_frame, text=translations[lang]["messages"]["theme"]).pack(side="right", pady=10)

    def create_buttons(self):
        button_labels = translations[lang]["button_labels"]

        buttons = [
            (button_labels["monitoring"], self.monitoring_btn),
            (button_labels["delete_computer"], self.delete_computer_btn),
            (button_labels["add_computer"], self.add_computer_btn),
            (button_labels["stop_program"], self.stop_program_btn),
            (button_labels["modify_program"], self.modify_program_btn),
            (button_labels["run_new_instance"], self.run_new_instance_btn),
            (button_labels["stop_instance"], self.stop_instance_btn),
            (button_labels["exit"], self.exit_program)
        ]

        for index, (button_text, command) in enumerate(buttons):
            button = ctk.CTkButton(self.footer_frame, text=button_text, command=command)
            button.grid(row=index//4, column=index%4, padx=5, pady=5, sticky="ew")
            self.button_frames.append(button)

        for col in range(4):
            self.footer_frame.grid_columnconfigure(col, weight=1)

        self.footer_frame.grid_rowconfigure(0, weight=1)
        self.footer_frame.grid_rowconfigure(1, weight=1)

    def show_input(self, function_name, input_keys):
        input_labels = translations[lang]["input_labels"]
        button_labels = translations[lang]["button_labels"]
        input_names = [input_labels[key] for key in input_keys]

        for button in self.button_frames:
            button.grid_forget()

        self.input_frame = ctk.CTkFrame(self.footer_frame)
        self.input_frame.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        self.input_entries = []

        for input_name in input_names:
            input_entry = ctk.CTkEntry(self.input_frame, placeholder_text=input_name)
            input_entry.pack(pady=10)
            self.input_entries.append(input_entry)

        self.ok_button = ctk.CTkButton(self.input_frame, text="OK", command=lambda: self.on_ok_button(function_name))
        self.ok_button.pack(pady=10, padx=10)

        self.cancel_button = ctk.CTkButton(self.input_frame, text=button_labels["cancel"], command=self.cancel_input)
        self.cancel_button.pack(pady=10, padx=10)

    def on_ok_button(self, function_name):
        correct = True
        all_inputs_filled = True
        global input_texts
        input_texts = []

        for input_entry in self.input_entries:
            input_text = input_entry.get()
            if not input_text:
                all_inputs_filled = False
                break
            input_texts.append(input_text)

        if all_inputs_filled:
            match function_name:
                case "monitoring":
                    self.monitoring(input_texts[0])
                case "delete_computer":
                    self.delete_computer(input_texts[0])
                case "add_computer":
                    if re.fullmatch(r'^[^\sÁÉÍÓÖŐÚÜŰáéíóöőúüű]+$', input_texts[0]):
                        if re.fullmatch(r'\d+', input_texts[1]) and re.fullmatch(r'\d+', input_texts[2]):
                            self.add_computer(input_texts[0], input_texts[1], input_texts[2])
                        else:
                            messagebox.showerror(title="Error", message=translations[lang]["messages"]["invalid_resource_value"])
                            correct = False
                    else:
                        messagebox.showerror(title="Error", message=translations[lang]["messages"]["invalid_computer_name"])
                        correct = False
                case "stop_program":
                    self.stop_program(input_texts[0])
                case "modify_program":
                    self.modify_program(input_texts[0], input_texts[1], input_texts[2], input_texts[3])
                case "run_new_instance":
                    self.run_new_instance(input_texts[0], input_texts[1])
                case "stop_instance":
                    self.stop_instance(input_texts[0])

            if correct:
                self.input_frame.destroy()
                self.create_buttons()

    def refresh_main_view(self):
        if update == True:
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            self.create_boxes(self.status())

            self.after(2500, self.refresh_main_view)

    def cancel_input(self):
        self.input_frame.destroy()
        self.create_buttons()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        global appearance_mode
        if lang == "hu":
            if new_appearance_mode == "Világos":
                appearance_mode = translations[lang]["button_labels"]["light"][1]
                ctk.set_appearance_mode(appearance_mode)
            elif new_appearance_mode == "Sötét":
                appearance_mode = translations[lang]["button_labels"]["dark"][1]
                ctk.set_appearance_mode(appearance_mode)
            elif new_appearance_mode == "Rendszer":
                appearance_mode = translations[lang]["button_labels"]["system"][1]
                ctk.set_appearance_mode(appearance_mode)
        elif lang == "en":
            appearance_mode = new_appearance_mode
            ctk.set_appearance_mode(new_appearance_mode)

    def monitoring_btn(self):
        self.show_input(function_name="monitoring", input_keys=["program_name"])

    def delete_computer_btn(self):
        self.show_input(function_name="delete_computer", input_keys=["computer_name"])

    def add_computer_btn(self):
        self.show_input(function_name="add_computer", input_keys=["new_computer_name", "cpu", "ram"])

    def stop_program_btn(self):
        self.show_input(function_name="stop_program", input_keys=["program_name"])

    def modify_program_btn(self):
        self.show_input(function_name="modify_program", input_keys=["program_name", "number_of_copies", "cpu", "ram"])

    def run_new_instance_btn(self):
        self.show_input(function_name="run_new_instance", input_keys=["computer_name", "program_name"])

    def stop_instance_btn(self):
        self.show_input(function_name="stop_instance", input_keys=["program_name"])

    def exit_program(self):
        exit()

    def set_update_true(self):
        global update
        update = True
        
    def modify_line(self, file_path, line_number, new_content):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if 0 <= line_number < len(lines):
            lines[line_number] = new_content + '\n'
        else:
            return

        with open(file_path, 'w') as file:
            file.writelines(lines)

    def status(self):
        results = []
    
        for pc in os.listdir(dir):
            pc_path = os.path.join(dir, pc)
            if os.path.isdir(pc_path) and os.path.isfile(os.path.join(pc_path, ".szamitogep_config")):
                with open(os.path.join(pc_path, ".szamitogep_config"), "r", encoding="utf-8") as conf_file:
                    config_lines = conf_file.readlines()
                    max_cpu = int(config_lines[0].strip()) if config_lines else 0
                    max_ram = int(config_lines[1].strip()) if len(config_lines) > 1 else 0

                used_cpu = 0
                used_ram = 0
                active_programs = []

                for item in os.listdir(pc_path):
                    if item == ".szamitogep_config":
                        continue
                    file_path = os.path.join(pc_path, item)
                    if os.path.isfile(file_path):
                        with open(file_path, "r", encoding="utf-8") as prog_file:
                            lines = prog_file.readlines()
                            if len(lines) >= 4:
                                status = lines[1].strip()
                                cpu_needed = int(lines[2].strip())
                                ram_needed = int(lines[3].strip())
                                if status == "AKTÍV":
                                    used_cpu += cpu_needed
                                    used_ram += ram_needed
                                    active_programs.append(item)

                free_cpu = max_cpu - used_cpu
                free_ram = max_ram - used_ram

                results.append({
                    "pc": pc,
                    "max_cpu": max_cpu,
                    "max_ram": max_ram,
                    "free_cpu": free_cpu,
                    "free_ram": free_ram,
                    "active_programs": active_programs
                })

        return results

    def start(self):
        total_active = 0
        total_inactive = 0
        cluster_consistent = True
        program_instances = {}

        for pc in os.listdir(dir):
            pc_path = os.path.join(dir, pc)
            if os.path.isdir(pc_path) and os.path.isfile(os.path.join(pc_path, ".szamitogep_config")):
                for item in os.listdir(pc_path):
                    if item == ".szamitogep_config":
                        continue
                    file_path = os.path.join(pc_path, item)
                    if os.path.isfile(file_path):
                        with open(file_path, "r", encoding="utf-8") as prog_file:
                            lines = prog_file.readlines()
                            if len(lines) >= 4:
                                status = lines[1].strip()
                                prog_name = item.split('-')[0]
                                if status == "AKTÍV":
                                    total_active += 1
                                    if prog_name not in program_instances:
                                        program_instances[prog_name] = []
                                    program_instances[prog_name].append((pc, item, status))
                                elif status == "INAKTÍV":
                                    total_inactive += 1
        
        with open(f"{dir}/.klaszter", "r", encoding="utf-8") as f:
            lines = f.readlines()

            for i in range(0, len(lines), 4):
                prog = lines[i].strip()
                expected_instances = int(lines[i+1].strip())
                actual_instances = len(program_instances.get(prog, []))
                if expected_instances != actual_instances:
                    cluster_consistent = False
                    ctk.CTkLabel(self.main_frame, text=f"{translations[lang]["messages"]["error_state"]} {prog} {translations[lang]["messages"]["expected_instances"]} {expected_instances}{translations[lang]["messages"]["actual_instances"]} {actual_instances}", font=("Arial", 16)).pack()
        if cluster_consistent:
            ctk.CTkLabel(self.main_frame, text=translations[lang]["messages"]["cluster_status_correct"], font=("Arial", 16)).pack(pady=20)
        else:
            ctk.CTkLabel(self.main_frame, text=translations[lang]["messages"]["cluster_status_not_correct"], font=("Arial", 16)).pack(pady=20)

        ctk.CTkLabel(self.main_frame, text=translations[lang]["messages"]["all_running_processes"], font=("Arial", 16)).pack()
        ctk.CTkLabel(self.main_frame, text=f"{translations[lang]["messages"]["active"]}: {total_active} {translations[lang]["messages"]["inactive"]}: {total_inactive}", font=("Arial", 16)).pack()

        ctk.CTkButton(self.main_frame, text="OK", command=self.refresh_main_view).pack(pady=20)

    def monitoring(self, query):
        global update
        total_active = 0
        total_inactive = 0
        program_instances = {}

        for pc in os.listdir(dir):
            pc_path = os.path.join(dir, pc)
            if os.path.isdir(pc_path) and os.path.isfile(os.path.join(pc_path, ".szamitogep_config")):
                used_cpu = 0
                used_ram = 0

                for item in os.listdir(pc_path):
                    if item == ".szamitogep_config":
                        continue
                    file_path = os.path.join(pc_path, item)
                    if os.path.isfile(file_path):
                        with open(file_path, "r", encoding="utf-8") as prog_file:
                            lines = prog_file.readlines()

                            if len(lines) >= 4:
                                status = lines[1].strip()
                                cpu_needed = int(lines[2].strip())
                                ram_needed = int(lines[3].strip())
                                if status == "AKTÍV":
                                    used_cpu += cpu_needed
                                    used_ram += ram_needed

                                prog_name = item.split('-')[0]
                                if status == "AKTÍV":
                                    total_active += 1
                                    if prog_name not in program_instances:
                                        program_instances[prog_name] = []
                                    program_instances[prog_name].append((pc, item, cpu_needed, ram_needed, status))
                                elif status == "INAKTÍV":
                                    total_inactive += 1

        if query in program_instances:
            update = False
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            if lang == "hu":
                ctk.CTkLabel(self.main_frame, text=f"{query} {translations[lang]["messages"]["running_instances"]}:", font=("Arial", 16)).pack(pady=10)
            elif lang == "en":
                ctk.CTkLabel(self.main_frame, text=f"{translations[lang]["messages"]["running_instances"]} {query}:", font=("Arial", 16)).pack(pady=10)
            for instance in program_instances[query]:
                comp, unique_id, cpu_needed, ram_needed, status = instance
                ctk.CTkLabel(self.main_frame, text=f"{translations[lang]["messages"]["computer"]}: {comp}, {translations[lang]["messages"]["id"]}: {unique_id}, {translations[lang]["messages"]["resource_requirements"]}: CPU {cpu_needed}, RAM {ram_needed}, {translations[lang]["messages"]["status"]}: {status}", font=("Arial", 16)).pack()
            ctk.CTkLabel(self.main_frame, text=f"{translations[lang]["messages"]["total_running_instances"]}: {len(program_instances[query])}", font=("Arial", 16)).pack(pady=10)
            ctk.CTkButton(self.main_frame, text="OK", command=lambda: [self.set_update_true(), self.refresh_main_view()]).pack(pady=10)
        else:
            messagebox.showerror(title="Error", message=translations[lang]["messages"]["no_running_instance_with_this_name"])

    def delete_computer(self, pc):
        cycle = 0
        global update
        if pc in os.listdir(dir) and os.path.isfile(f'{dir}/{pc}/.szamitogep_config'):
            update = False
            if os.listdir(f"{dir}/{pc}") != ['.szamitogep_config']:
                for widget in self.main_frame.winfo_children():
                    widget.destroy()
                ctk.CTkLabel(self.main_frame, text=translations[lang]["messages"]["computer_not_empty"], font=("Arial", 16)).pack(pady=10)
                ctk.CTkLabel(self.main_frame, text=translations[lang]["messages"]["running_programs"], font=("Arial", 16)).pack()
                for k in os.listdir(f"{dir}/{pc}"):
                    if ".szamitogep_config" not in k:
                        ctk.CTkLabel(self.main_frame, text=k, font=("Arial", 16)).pack()
                        programok = open(f"{dir}/{pc}/{k}", encoding="utf-8")
                        for l in programok:
                            if cycle < 2:
                                cycle += 1
                                ctk.CTkLabel(self.main_frame, text=l.replace("\n", ""), font=("Arial", 16)).pack()
                    ctk.CTkLabel(self.main_frame, text="-------------------------", font=("Arial", 16)).pack()
                    cycle = 0
                ctk.CTkButton(self.main_frame, text="OK", command=lambda: [self.set_update_true(), self.refresh_main_view()]).pack(pady=10)
            else:
                os.remove(f"{dir}/{pc}/.szamitogep_config")
                os.rmdir(f"{dir}/{pc}")
        else:
            messagebox.showerror(title="Error", message=translations[lang]["messages"]["no_computer_found"])

    def add_computer(self, new_pc, performance1, performance2):
        if new_pc in os.listdir(dir):
            messagebox.showerror(title="Error", message=translations[lang]["messages"]["computer_already_exists"])
        else:
            os.mkdir(f"{dir}/{new_pc}")
            open(f"{dir}/{new_pc}/.szamitogep_config", "w")
            with open(f"{dir}/{new_pc}/.szamitogep_config", "w") as f:
                f.write(str(performance1)+"\n"+str(performance2)+"\n")

    def stop_program(self, program):
        found = False

        with open(f"{dir}/.klaszter", "r") as f:
            lines = f.readlines()
        new_lines = []
        skip_count = 0
        for i in range(len(lines)):
            if skip_count > 0:
                skip_count -= 1
                continue
            if lines[i].strip() == program:
                skip_count = 3
                found = True
                continue
            new_lines.append(lines[i])
        with open(f"{dir}/.klaszter", "w") as f:
            f.writelines(new_lines)

        for i in os.listdir(dir):
            path = f"{dir}/{i}"
            if os.path.isdir(path):
                for j in os.listdir(path):
                    if program in j:
                        os.remove(f"{path}/{j}")
        if not found:
            messagebox.showerror(title="Error", message=translations[lang]["messages"]["no_program_found"])

    def modify_program(self, program, copies, cpu_perf, ram_perf):
        n = -1
        with open(f'{dir}/.klaszter', 'r') as f:
            rows = f.readlines()

        for i in rows:
            n += 1
            exists = False
            if i.strip() == program:
                exists = True
                break
        
        if exists == True:
            self.modify_line(f"{dir}/.klaszter", n+1, copies)
            self.modify_line(f"{dir}/.klaszter", n+2, cpu_perf)
            self.modify_line(f"{dir}/.klaszter", n+3, ram_perf)
        else:
            messagebox.showerror(title="Error", message=translations[lang]["messages"]["no_program_found"])

    def stop_instance(self, program):
        exists = False

        with open(f'{dir}/.klaszter', 'r', encoding="utf-8") as f:
            rows = f.readlines()
        n = -1
        for i in os.listdir(dir):
            if os.path.isdir(f'{dir}/{i}') and os.path.isfile(f'{dir}/{i}/.szamitogep_config') and os.listdir(f'{dir}/{i}') != ['.szamitogep_config']:
                for j in os.listdir(f"{dir}/{i}"):
                    if program == j:
                        os.remove(f"{dir}/{i}/{program}")
                        for k in rows:
                            n += 1
                            if k.strip() == program.split('-')[0]:
                                self.modify_line(f"{dir}/.klaszter", n+1, str(int(rows[n+1])-1))
                        exists = True
                        break
        if exists == False:
            messagebox.showerror(title="Error", message=translations[lang]["messages"]["no_program_found"])

    def run_new_instance(self, new_pc, new_program):
        def generate_unique_id(program_name):
            unique_id = program_name + '-' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            return unique_id

        def get_program_resources(program_name):
            with open(f"{dir}/.klaszter", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for i in range(0, len(lines), 4):
                    if lines[i].strip() == program_name:
                        instances = int(lines[i + 1].strip())
                        cpu = int(lines[i + 2].strip())
                        ram = int(lines[i + 3].strip())
                        return instances, cpu, ram, i + 1
            return None, None, None, None

        def update_instances_count(program_name, instances_index):
            with open(f"{dir}/.klaszter", "r", encoding="utf-8") as file:
                lines = file.readlines()
            
            lines[instances_index] = str(int(lines[instances_index].strip()) + 1) + "\n"
            
            with open(f"{dir}/.klaszter", "w", encoding="utf-8") as file:
                file.writelines(lines)

        def get_computer_resources(new_pc):
            config_path = os.path.join(f"{dir}/{new_pc}", ".szamitogep_config")
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as file:
                    cpu_available = int(file.readline().strip())
                    ram_available = int(file.readline().strip())
                    return cpu_available, ram_available
            return None, None

        def check_resources_and_create_file(program_name, new_pc):
            if not os.path.exists(f"{dir}/{new_pc}"):
                return False

            instances, cpu_needed, ram_needed, instances_index = get_program_resources(program_name)
            
            if cpu_needed is None or ram_needed is None:
                return False

            cpu_available, ram_available = get_computer_resources(new_pc)

            if cpu_available is None or ram_available is None:
                return False

            if cpu_needed > cpu_available or ram_needed > ram_available:
                return False

            unique_id = generate_unique_id(program_name)
            file_path = os.path.join(f"{dir}/{new_pc}", unique_id)
            
            with open(file_path, "w", encoding="utf-8") as file:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{current_time}\n")
                file.write("AKTÍV\n")
                file.write(f"{cpu_needed}\n")
                file.write(f"{ram_needed}\n")

            update_instances_count(program_name, instances_index)
            
            return True

        if check_resources_and_create_file(new_program, new_pc) == False:
            messagebox.showerror(title="Error", message=translations[lang]["messages"]["invalid_computer_program_name"])

if __name__ == "__main__":
    input_app = InputApp()
    input_app.mainloop()