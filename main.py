import os

#dir = input("Add meg a dirt: ")
dir = "/home/sz0msz3d/Documents/dusza_cluster"

klaszter = open(f'{dir}/.klaszter', 'r')

def menu():
    print("1. Monitoring")
    print("2. Számítógép törlése")
    print("3. Számítógép hozzáadása")
    print("4. Program leállítása")
    print("5. Program adatainak módosítása")
    print("6. Új programpéldány futtatása")
    print("7. Kilépés")
    muvelet = input("Mit akarsz? ")
    if muvelet == "1":
        monitoring()
    elif muvelet == "2":
        torles()
    elif muvelet == "3":
        hozzaadas()
    elif muvelet == "4":
        program_leallitas()
    elif muvelet == "7":
        exit()
    else:
        print("Helytelen")

def monitoring():
    ciklus = 0
    ciklus2 = 0
    max_processor = 0
    max_memoria = 0
    hasznalt_processor = 0
    hasznalt_memoria = 0
    print("-------------------------")
    for i in os.listdir(dir):
        if os.path.isdir(f'{dir}/{i}') and os.path.isfile(f'{dir}/{i}/.szamitogep_config'):
            print(i)
            print("MAX:")
            config = open(f'{dir}/{i}/.szamitogep_config', 'r')
            for j in config:
                ciklus += 1
                if ciklus == 1:
                    max_processor = int(j.replace("\n", ""))
                if ciklus == 2:
                    max_memoria = int(j.replace("\n", ""))
            print(max_processor, max_memoria)
            print("SZABAD:")
            for k in os.listdir(f"{dir}/{i}"):
                if ".szamitogep_config" not in k:
                    #print(k)
                    programok = open(f"{dir}/{i}/{k}")
                    for l in programok:
                        ciklus2 += 1
                        if ciklus2 == 3:
                            hasznalt_processor += int(l.replace("\n", ""))
                        if ciklus2 == 4:
                            hasznalt_memoria += int(l.replace("\n", ""))

                    ciklus2 = 0
            print(max_processor-hasznalt_processor, max_memoria-hasznalt_memoria)
            hasznalt_memoria = 0
            hasznalt_processor = 0
            print("-------------------------")

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

while True:
    menu()