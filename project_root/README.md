Projekt sa skladá z dvoch častí:

    1. ETL
    - načítanie dát zo vstupných .csv súborov, detekcie chýb, oprava chýb
    načítanie do databázy

    2. Visualization
    - GUI, cez ktoré sa používateľ pripojí k databáze, z ktorej je možné načítať a vizualizovať
    dáta, ktoré sú výsledkom spracovania pomocou ETL pipeline

Priečinok project_root obsahuje okrem iného nasledujúce priečinky:
    - elt - časť projektu ETL pipeline s vlastným main.py
    - Visualization - časť projektu Vizualizácia s vlastným main.py
    - shared - obsahuje súbor config.json, ktorý slúži ako kontrakt medzi ELL a Visualization

Následne osobitne podrobnejšie popíšem obidve časti projektu.

## Visualization

Pre spustenie GUI je potrebné spustiť project_root/visualization/main.py.
Po vyplnení správnych prihlasovacích údajov do databázy v connection window a úspešnom pripojení k
databáze sa otvorí main window. Najprv je potrebné v časti Fact table selection vybrať jednu z 
ponúkaných faktových tabuliek a kliknúť na tlačidlo Show. Následne sa v časti Plot configuration
zobrazia všetky senzory a metriky prítomné vo vybranej faktovej tabuľke. Pre zobrazenie grafu je potrebné:
    - zvoliť začiatočný a konečný dátum,
    - zvoliť senzory a metriky v kombináciách 1. aspoň jeden senzor a od jedna po desať metrík, 2. aspoň 
    jeden senzor a práve jedna metrika,
    - stlačiť tlačidlo Load.
Pre zmenu spojenia ku databáze je potrebné stlačiť tlačidlo Set connection. Aplikácia sa ukončuje klasicky stlačním krížika v pravom hornom rohu okna.

## ETL

## Running the aplication
- po správnom nastavení .env a .config (vid nizsie) spustite main.py
- v main.py sa najprv vytvorí inštancia transformer triedy Transformer následne sa príkazom:
    - transformer.apply_trans_all() - spustia všetky transformácie
    - transformer.apply_trans_regularize() - spustí iba trasformácia regularize_timestamps
    - transformer.apply_trans_correct() - spustí iba trasformácia correct_measurements, podmienkou pre toto spustenie však je, že všetky timestampy musia prichádzať na celú hodinu, lebo implementácia correct_measurements si to vyžaduje, ale rieši to transformácia regularize_timestamps
- všetky parametre sa čítajú zo súboru .config
- po spustení sa vykonajú transformácie a dáta sa načítajú do databázy

## Credentials to database

Vytvorte .env súbor v project_root na základe .env.example:

DB_HOST = ""
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""

## config.json
- "chunk_size" - veľkosť jedného chunku
- "max_approximated" - maximálny počet aproximovateľných hodnôt za sebou
- "active_measurement" - id slovníka z measurements
- "measurements" - zoznam slovníkov, každý popisuje jeden .csv súbor určený na transformáciu
    - "id" - id merania
    - "type" - typ merania, v našom prípade Water alebo Weather 
    - "path" - cesta od project_root ku csv. súboru
    - "target_facts"
        - "target_table" - názov výstupnej tabuľky v databáze
        - "source_columns"
            - zoznam slovníkov, každý slovník zodpovedá jednému MERANÉMU atribútu zo   vstupnej tabuľky, teda stĺpce s menom senzora a timestampom tu nejdú, stĺpce meraní, ktoré nebudú tu, transfomátor odignoruje
            - v každom slovníku je meno senzora, minimálna a maximálna možná hodnota, podľa toho sa budú identifikovať nekorektné hodnoty
    - "target_dimensions"
        - slovník s "accumulator": "yes"
            - "join_column_measurements" - názov stĺpce, podľa ktorého sa záznamy rozdeľujú do akumulátorov, v našom prípade ide o stĺpec s názvom senzora
            - "join_column_codelist" - názov stĺpca z codelistu, v ktorom sa nachádza informácia o type senzora
            - "sensor_name_column_codelist" - názov stĺpca z codelistu s menami senzorov
        - slovník s "time_dimension": "yes"
            - "source_column" - meno stĺpca s timestampom vo vstupnej tabuľke
- "codelists"
    - zoznam slovníkov, každý zodpovedá jednému codelistu, obsahuje id a cestu ku codelistu, v codeliste musia byť práve tie senzory, pre ktoré chceme robiť tranformácie, zvyšné senzory bude transformátor ignorovať

## Comments
- Transformácie nakoniec sú dve:
    - 1. regularize_timestamps - Najprv zaokrúhli timestampy na celé hodiny. Následne odstráni takto vzniknuté duplicity spolu s duplicitami, ktoré tam už boli. Táto transformácie teda rieši nasledovné chyby:
        - dáta prišli v iných časoch, ako je pravidlom, v riadnom pritom neprišli
        - dáta prišli v iných časoch, ako je pravidlom, ale pritom prišli aj v riadnom čase
        - duplicitné záznamy - rovnaké hodnoty
        - duplicitné záznamy - rôzne hodnoty
    - 2. correct_measurements - Doplní chýbajúce riadky do limitu max_aproximated z .config. Potom aproximuje tie chýbajúce hodnoty a nekorektné hodnoty, ktoré podľa max_aproximated môže aproximovať. Chýbajúce hodnoty sú označené hodnotou None. Skok v čase je označený riadkom s menom senzora, timestampom a hodnotami nan z knižnice numpy. Aktuálna verzia rieši zatiaľ skôr klasické prípady a tie okrajovejšie ešte nie sú ošetrené. Do piatku by som chcel ošetriť aj tieto okrajové prípady a implementovať dvojbufferový akumulátor. Táto transformácie teda rieši nasledovné chyby:
        - nekorektné hodnoty (mimo bežného rozsahu)
        - chýbajúce hodnoty pre niektoré atribúty
        - chýbajúce celé záznamy pre niektoré timestampy
- Načítanie do databázy je hotové