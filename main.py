import os
import random
import string
from datetime import datetime

dir = input("Add meg a dirt: ")

klaszter = open(f'{dir}/.klaszter', 'r')

def menu():
    print("1. Monitoring")
    print("2. Számítógép törlése")
    print("3. Számítógép hozzáadása")
    print("4. Program leállítása")
    print("5. Program adatainak módosítása")
    print("6. Új programpéldány futtatása")
    print("7. Adott programpéldány leállítása")
    print("8. Kilépés")
    muvelet = input("Mit akarsz? ")
    if muvelet == "1":
        monitoring()
    elif muvelet == "2":
        torles()
    elif muvelet == "3":
        hozzaadas()
    elif muvelet == "4":
        program_leallitas()
    elif muvelet == "5":
        modositas()
    elif muvelet == "6":
        uj_program_futtatasa()
    elif muvelet == "7":
        programpeldany_leallitas()
    elif muvelet == "8":
        exit()
    else:
        print("Helytelen")

def modify_line(file_path, line_number, new_content):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if 0 <= line_number < len(lines):
        lines[line_number] = new_content + '\n'
    else:
        print(f"A megadott sor száma ({line_number}) kívül esik a fájl sorainak tartományán.")
        return

    with open(file_path, 'w') as file:
        file.writelines(lines)

def monitoring():
    total_active = 0
    total_inactive = 0
    cluster_consistent = True
    program_instances = {}
    print("Klaszter Állapotának Áttekintése:\n")
    print("-------------------------")

    for pc in os.listdir(dir):
        pc_path = os.path.join(dir, pc)
        if os.path.isdir(pc_path) and os.path.isfile(os.path.join(pc_path, ".szamitogep_config")):

            with open(os.path.join(pc_path, ".szamitogep_config"), "r", encoding="utf-8") as conf_file:
                config_lines = conf_file.readlines()
                max_cpu = int(config_lines[0].strip()) if config_lines else 0
                max_ram = int(config_lines[1].strip()) if len(config_lines) > 1 else 0
            used_cpu = 0
            used_ram = 0
            print("Számítógép:", pc)
            print("Max CPU:", max_cpu, "Max RAM:", max_ram)

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
                            used_cpu += cpu_needed
                            used_ram += ram_needed

                            prog_name = item.split('-')[0]
                            if prog_name not in program_instances:
                                program_instances[prog_name] = []
                            program_instances[prog_name].append((pc, item, cpu_needed, ram_needed, status))
                            if status == "AKTÍV":
                                total_active += 1
                            elif status == "INAKTÍV":
                                total_inactive += 1
            free_cpu = max_cpu - used_cpu
            free_ram = max_ram - used_ram
            if free_ram >= 0 and free_cpu >= 0:
                print("Szabad erőforrások: CPU:", free_cpu, "RAM:", free_ram)
            else:
                cluster_consistent = False
                if free_ram < 0:
                    print("Az alkalmazás több RAM-ot használ mint amennyi elérhető")              
                if free_cpu < 0:
                    print("Az alkalmazás több CPU-t használ mint amennyi elérhető")
            print("-------------------------")

    print("\nÖsszes futó folyamat:")
    print("AKTÍV:", total_active, "INAKTÍV:", total_inactive)
    
    with open(f"{dir}/.klaszter", "r", encoding="utf-8") as f:
        lines = f.readlines()

        for i in range(0, len(lines), 4):
            prog = lines[i].strip()
            expected_instances = int(lines[i+1].strip())
            actual_instances = len(program_instances.get(prog, []))
            if expected_instances != actual_instances:
                cluster_consistent = False
                print(f"Hibás állapot: {prog} esetén várva {expected_instances}, valós példány: {actual_instances}")
    if cluster_consistent:
        print("A klaszter állapota helyes.")
    else:
        print("A klaszter állapota NEM helyes.")
        
    query = input("\nAdja meg a program nevét a részletes lekérdezéshez (üresen hagyva kilép): ").strip()
    if query:
        if query in program_instances:
            print(f"\n{query} futó példányai:")
            for instance in program_instances[query]:
                comp, unique_id, cpu_needed, ram_needed, status = instance
                print(f"Számítógép: {comp}, Azonosító: {unique_id}, Erőforrásigény: CPU {cpu_needed}, RAM {ram_needed}, Státusz: {status}")
            print("Összes példányok száma:", len(program_instances[query]))
        else:
            print("Nincs futó példány ezzel a névvel.")

def torles():
    ciklus = 0
    print("-------------------------")
    szamito = input("Számítógép neve: ")
    if szamito in os.listdir(dir) and os.path.isfile(f'{dir}/{szamito}/.szamitogep_config'):
        gepszam = os.listdir(f"{dir}/{szamito}")
        if gepszam != ['.szamitogep_config']:
            print("A számítógép nem üres")
            print("Futó programok:")
            for k in os.listdir(f"{dir}/{szamito}"):
                if ".szamitogep_config" not in k:
                    print(k)
                    programok = open(f"{dir}/{szamito}/{k}")
                    for l in programok:
                        if ciklus < 2:
                            ciklus += 1
                            print(l.replace("\n", ""))
                print("-------------------------")
                ciklus = 0
        else:
            os.remove(f"{dir}/{szamito}/.szamitogep_config")
            os.rmdir(f"{dir}/{szamito}")
            print("A számítógép törölve")
            print("-------------------------")
    else:
        print("Nincs ilyen számítógép")
        print("-------------------------")

def hozzaadas():
    print("-------------------------")
    new_pc = input("Új számítógép neve: ")
    if new_pc in os.listdir(dir):
        print("Ez a számítógép már létezik")
        print("-------------------------")
    else:
        teljesitmeny1 = int(input("Proccesszor erőforrás: "))
        teljesitmeny2 = int(input("Memóriakapacítás: "))
        os.mkdir(f"{dir}/{new_pc}")
        open(f"{dir}/{new_pc}/.szamitogep_config", "w")
        with open(f"{dir}/{new_pc}/.szamitogep_config", "w") as f:
            f.write(str(teljesitmeny1)+"\n"+str(teljesitmeny2)+"\n")
        print("Számítógép létrehozva")
        print("-------------------------")

def program_leallitas():
    program = input("Melyik programot akarod törölni? ")
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
                    print("Program törölve:", j)
                    print("-------------------------")

    if not found:
        print("Nincs ilyen program")
        print("-------------------------")

def modositas():
    n = -1
    program = input("Program neve: ")
    with open(f'{dir}/.klaszter', 'r') as f:
        sorok = f.readlines()

    for i in sorok:
        n += 1
        van = False
        if i.strip() == program:
            van = True
            break
    
    if van == True:
        x = input("Példányok száma: ")
        y = input("Processzor erőforrás: ")
        z = input("Memória erőforrás: ")
        modify_line(f"{dir}/.klaszter", n+1, x)
        modify_line(f"{dir}/.klaszter", n+2, y)
        modify_line(f"{dir}/.klaszter", n+3, z)
        print("Sikeresen módosítva!")
    else:
        print("Nincs ilyen program!")

def programpeldany_leallitas():
    for i in os.listdir(dir):
        if os.path.isdir(f'{dir}/{i}') and os.path.isfile(f'{dir}/{i}/.szamitogep_config') and os.listdir(f'{dir}/{i}') != ['.szamitogep_config']:
            print(i+":")
            for j in os.listdir(f"{dir}/{i}"):
                if ".szamitogep_config" not in j:
                    print("\t" + j)

    x = input("Melyik programot akarod leállítani: ")

    van = False

    with open(f'{dir}/.klaszter', 'r', encoding="utf-8") as f:
        sorok = f.readlines()
    n = -1
    for i in os.listdir(dir):
        if os.path.isdir(f'{dir}/{i}') and os.path.isfile(f'{dir}/{i}/.szamitogep_config') and os.listdir(f'{dir}/{i}') != ['.szamitogep_config']:
            for j in os.listdir(f"{dir}/{i}"):
                if x == j:
                    os.remove(f"{dir}/{i}/{x}")
                    for k in sorok:
                        n += 1
                        if k.strip() == x.split('-')[0]:
                            modify_line(f"{dir}/.klaszter", n+1, str(int(sorok[n+1])-1))
                    van = True
                    print("Programpéldány sikeresen leállítva!")
                    break

    if van == False:
        print("Nincs ilyen program!")

def uj_program_futtatasa():

    def generate_unique_id(program_name):
        unique_id = program_name + '-' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        return unique_id

    def get_program_resources(program_name):
        with open(".klaszter", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):
                if lines[i].strip() == program_name:
                    instances = int(lines[i + 1].strip())
                    cpu = int(lines[i + 2].strip())
                    ram = int(lines[i + 3].strip())
                    return instances, cpu, ram, i + 1
        return None, None, None, None

    def update_instances_count(program_name, instances_index):
        with open(".klaszter", "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        lines[instances_index] = str(int(lines[instances_index].strip()) + 1) + "\n"
        
        with open(".klaszter", "w", encoding="utf-8") as file:
            file.writelines(lines)

    def get_computer_resources(new_pc):
        config_path = os.path.join(new_pc, ".szamitogep_config")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as file:
                cpu_available = int(file.readline().strip())
                ram_available = int(file.readline().strip())
                return cpu_available, ram_available
        return None, None

    def check_resources_and_create_file(program_name, new_pc):
        if not os.path.exists(f"./{new_pc}"):
            print("A megadott számítógép nem létezik.")
            return False

        instances, cpu_needed, ram_needed, instances_index = get_program_resources(program_name)
        
        if cpu_needed is None or ram_needed is None:
            print("A program nem szerepel a klaszter fájlban.")
            return False

        cpu_available, ram_available = get_computer_resources(new_pc)

        if cpu_available is None or ram_available is None:
            print("A számítógép konfigurációs fájl nem található vagy érvénytelen.")
            return False

        if cpu_needed > cpu_available or ram_needed > ram_available:
            print("Nincs elég erőforrás a program futtatásához.")
            return False

        unique_id = generate_unique_id(program_name)
        file_path = os.path.join(new_pc, unique_id)
        
        with open(file_path, "w", encoding="utf-8") as file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{current_time}\n")
            file.write("AKTÍV\n")
            file.write(f"{cpu_needed}\n")
            file.write(f"{ram_needed}\n")

        update_instances_count(program_name, instances_index)
        
        print(f"A program új példánya futtatható és a fájl létrejött: {file_path}")
        return True

    new_pc = input("Számítógép neve: ")
    new_program = input("Mi a program neve?")

    if check_resources_and_create_file(new_program, new_pc):
        print("Minden feltétel teljesült.")
    else:
        print("Nem teljesültek a feltételek.")


total_active = 0
total_inactive = 0
cluster_consistent = True
program_instances = {}
print("Klaszter Állapotának Áttekintése:\n")
print("-------------------------")

for pc in os.listdir(dir):
    pc_path = os.path.join(dir, pc)
    if os.path.isdir(pc_path) and os.path.isfile(os.path.join(pc_path, ".szamitogep_config")):

        with open(os.path.join(pc_path, ".szamitogep_config"), "r", encoding="utf-8") as conf_file:
            config_lines = conf_file.readlines()
            max_cpu = int(config_lines[0].strip()) if config_lines else 0
            max_ram = int(config_lines[1].strip()) if len(config_lines) > 1 else 0
        used_cpu = 0
        used_ram = 0
        print("Számítógép:", pc)
        print("Max CPU:", max_cpu, "Max RAM:", max_ram)

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
                        used_cpu += cpu_needed
                        used_ram += ram_needed

                        prog_name = item.split('-')[0]
                        if prog_name not in program_instances:
                            program_instances[prog_name] = []
                        program_instances[prog_name].append((pc, item, cpu_needed, ram_needed, status))
                        if status == "AKTÍV":
                            total_active += 1
                        elif status == "INAKTÍV":
                            total_inactive += 1
        free_cpu = max_cpu - used_cpu
        free_ram = max_ram - used_ram
        if free_ram >= 0 and free_cpu >= 0:
            print("Szabad erőforrások: CPU:", free_cpu, "RAM:", free_ram)
        else:
            cluster_consistent = False
            if free_ram < 0:
                print("Az alkalmazás több RAM-ot használ mint amennyi elérhető")              
            if free_cpu < 0:
                print("Az alkalmazás több CPU-t használ mint amennyi elérhető")
        print("-------------------------")

print("\nÖsszes futó folyamat:")
print("AKTÍV:", total_active, "INAKTÍV:", total_inactive)

with open(f"{dir}/.klaszter", "r", encoding="utf-8") as f:
    lines = f.readlines()

    for i in range(0, len(lines), 4):
        prog = lines[i].strip()
        expected_instances = int(lines[i+1].strip())
        actual_instances = len(program_instances.get(prog, []))
        if expected_instances != actual_instances:
            cluster_consistent = False
            print(f"Hibás állapot: {prog} esetén várva {expected_instances}, valós példány: {actual_instances}")
if cluster_consistent:
    print("A klaszter állapota helyes.")
else:
    print("A klaszter állapota NEM helyes.")
print("-------------------------")

while True:
    menu()