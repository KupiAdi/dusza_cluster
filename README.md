# Cluster Manager Dokumentáció

## Készítette a print("Hello World") csapat

## Bevezetés
Ez a program egy klaszter alapú számítógép- és program menedzsment eszköz, amely két fő komponensből áll: egy parancssoros felületből (main.py) és egy grafikus felületből (gui.pyw). A szoftver célja, hogy segítsen a számítógépeken futó programok erőforrásainak nyomon követésében, konfigurálásában, valamint a futó alkalmazások monitorozásában és kezelésében.

## Felhasználói dokumentáció

### Általános áttekintés
A program két felhasználói felülettel rendelkezik:
- **Parancssoros felület (CLI):**  
    - A `main.py` script futtatásával elérhető.
    - Menüpontokon keresztül lehet választani a klaszter monitorozására, számítógépek hozzáadására vagy törlésére, program példányok módosítására, futtatására illetve leállítására.
- **Grafikus felület (GUI):**  
    - A `gui.pyw` script indításával elérhető.
    - Kényelmes gombok, beviteli mezők és vizuális elemek segítik a felhasználót a klaszter állapotának megtekintésében és a műveletek kiválasztásában.

### Használati esetek és lépések

#### 1. Monitoring
- **Művelet:**  
    - A futó processzek és számítógépek erőforrásainak állapotát lehet megtekinteni.
- **Felhasználói lépések:**
    - CLI esetén válasszuk a menüből az "1. Monitoring" opciót.
    - GUI esetén a "Monitoring" gomb kiválasztása után a lekérdezendő program nevét kell megadni.

#### 2. Számítógép törlése
- **Művelet:**  
    - Egy számítógép törlését biztosítja, feltéve, ha nincs rajta futó program.
- **Felhasználói lépések:**
    - CLI: A "2. Számítógép törlése" opció kiválasztása, majd a számítógép nevének megadása.
    - GUI: A "Számítógép törlése" gomb megnyomása a megfelelő számítógép nevének beírásával.

#### 3. Számítógép hozzáadása
- **Művelet:**  
    - Új számítógép felvétele a klaszterbe a szükséges erőforrás paraméterekkel.
- **Felhasználói lépések:**
    - CLI: "3. Számítógép hozzáadása" opció, majd az új számítógép neve, CPU és RAM értékének megadása.
    - GUI: A "Számítógép hozzáadása" gomb használata és a megadandó mezők kitöltése.

#### 4. Program leállítása
- **Művelet:**  
    - Egy adott program leállítása, amely törli a hozzá tartozó konfigurációs bejegyzéseket.
- **Felhasználói lépések:**
    - CLI: "4. Program leállítása" opció választása, majd a törlendő program nevének megadása.
    - GUI: "Program leállítása" gomb kiválasztása a megfelelő program nevének beírásával.

#### 5. Program adatainak módosítása
- **Művelet:**  
    - A klaszter konfigurációs fájljában szereplő program paramétereinek módosítása, ideértve a példányszámot, CPU és RAM értékeket.
- **Felhasználói lépések:**
    - CLI: "5. Program adatainak módosítása" opció, majd a módosítandó program neve és új értékeinek megadása.
    - GUI: "Program adatainak módosítása" gomb, majd a megfelelő beviteli mezők kitöltése.

#### 6. Új programpéldány futtatása
- **Művelet:**  
    - Új példány futtatása egy programból, ellenőrizve a cél számítógép erőforrásait.
- **Felhasználói lépések:**
    - CLI: "6. Új programpéldány futtatása" opció, majd a számítógép neve és a program neve megadása.
    - GUI: "Új programpéldány futtatása" gomb használata, majd a szükséges mezők kitöltése.

#### 7. Adott programpéldány leállítása 
- **Művelet:**  
    - Egy futó programpéldány leállítása a klaszterből.
- **Felhasználói lépések:**
    - CLI: "7. Adott programpéldány leállítása" opció, majd a leállítandó példány azonosítójának megadása.
    - GUI: "Adott programpéldány leállítása" gomb, majd a program nevének beírása.

#### 8. Kilépés
- **Művelet:**  
    - A program bezárása.
- **Felhasználói lépések:**
    - CLI: "8. Kilépés" opció választása.
    - GUI: "Kilépés" gomb megnyomása.

## Fejlesztői dokumentáció

### Program logikai és fizikai szerkezete
A projekt három fő forrásfájlra tagolódik:

1. **main.py:**
    - Feladata a parancssoros felület biztosítása.
    - Tartalmazza a klaszter állapotának lekérdezéséhez, monitorozásához, számítógépek és programok hozzáadásához/törléséhez szükséges függvényeket.
    - Főbb modulok:
        - Menu rendszer és felhasználói interakciók kezelése.
        - Fájlok módosítása, konfigurációs bejegyzések kezelése (`.szamitogep_config`, `.klaszter`).
        - Program példányok futtatásához szükséges logika (pl. erőforrások ellenőrzése, egyedi azonosító generálása).

2. **gui.pyw:**
    - A grafikus felület megvalósítása a CustomTkinter (ctk) modul segítségével.
    - Felépítése több ablakrészre:
        - Kezdőképernyő (InputApp): A klaszter könyvtárának beállítása.
        - Fő ablak (MainApp): Klaszter állapotának vizuális megjelenítése, interaktív gombok és információs dobozok.
    - Feladatok:
        - Dinamikus nyelvi támogatás (hu/en) a `translations` szótár alapján.
        - Különböző műveletek indítása gombnyomásra, amelyek meghívják a megfelelő funkciókat a backend logikából.
        - Értesítések és hibakezelés például messagebox-ok segítségével.

3. **translations.py**
    - Tartalmazza a fordításokat `hu/en` (magyar, angol) nyelvekre, amiket a `gui.pyw` fájlban importálunk.

### A fájlok értelmezése

1. **.klaszter:**
    - A klaszter konfigurációs fájlja, amely tartalmazza a programok adatait.
    - Fájl szerkezete: a sorokat újsor (\n) karakter választja el, egy adatot 4 egymást követő sor ír le.
        - első sor: a program neve
        - második sor: a példányok száma
        - harmadik sor: processzor használat
        - negyedik sor: memória használat

2. **.szamitogep_config:**
    - Egy adott számítógép konfigurációs fájlja, amely tartalmazza a számítógép processzor és memória erőforrás kapacitásait.
    - Fájl szerkezete: a sorokat újsor (\n) karakter választja el.
        - első sor: a processzor erőforrás kapacitása millimagban
        - második sor: a memória erőforrás kapacitása MB-ban

3. **programnev-abcdef:**
    - Egy adott program, ami éppen fut a számítógépen.
    - Fájlnév felépítése: a kötőjel előtt a program neve, utána egy 6 random karakterből álló egyedi azonosító.
    - Fájl szerkezete: a sorokat újsor (\n) karakter választja el.
        - első sor: a folyamat indításának ideje
        - második sor: A folyamat állapota
        - harmadik sor: a program által használt processzor erőforrás
        - negyedik sor: a program által használt memória erőforrás

### Használt technológiák és választásuk indoklása
- **Python:**  
    - Magas szintű nyelv, amely lehetővé teszi a gyors fejlesztést és karbantartást.
- **Tkinter és CustomTkinter (ctk):**  
    - A beépített modulok egyszerű grafikus felület létrehozására.
    - CustomTkinter biztosít modern megjelenést, testreszabható stílusokat és könnyebb kezelhetőséget.
- **OS, datetime, random, string:**  
    - Alapvető könyvtárak az operációs rendszer szintű műveletekhez, időbélyegek és azonosítók generálásához.
- **Regular Expressions (re):**  
    - A felhasználói bemenetek validálására, például számítógép nevek ellenőrzése.

### Telepítési és futtatási útmutató
1. **Követelmények:**
     - Python 3.12 vagy magasabb.
     - Operációs rendszer: Windows, Linux vagy macOS.
     - A szükséges könyvtárak telepíthetők a `pip install -r requirements.txt` paranccsal.

2. **Futtatás:**
     - **Parancssoros verzió futtatása:**
         - Navigáljunk a projekt könyvtárába.
         - Futtassuk a `main.py` scriptet a parancssorból:  
             `python main.py`
     - **Grafikus felület futtatása:**
         - Navigáljunk a projekt könyvtárába.
         - Futtassuk a `gui.pyw` scriptet:  
             `python gui.pyw`
