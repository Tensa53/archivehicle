# ArchiVehicle

ArchiVehicle è un progetto realizzato per il corso di Basi di Dati 2. L’obiettivo è quello di semplificare e digitalizzare la gestione relative alle
informazioni del parco veicoli di un concessionario. Questo software è destinato all’utenza
di un’attività commerciale che si occuperà di recuperare le informazioni dei veicoli e di
memorizzarle nel sistema, attraverso un’interfaccia grafica fornita da un applicazione web
client/server. ArchiVehicle supporta le seguenti funzionalità:
1. Inserimento, modifica, cancellazione delle informazioni di un veicolo;
2. Inserimento, modifica, cancellazione delle informazioni di un produttore di
veicoli;
3. Ricerca di un veicolo mediante l’applicazione di alcuni filtri;
4. Visualizzazione rapida del numero di veicoli da parte di ogni produttore, sulla
base di varie caratteristiche per veicolo.

# Installazione di ArchiVehicle
Per installare e utilizzare ArchiVehicle è sufficiente seguire questi passaggi:
1. Importare tramite MongoDB Compass le due collezioni di documenti:
    >archiVehicle.manufacturer.json <br>
     archiVehicle.vehicle.json
2. Posizionarsi nella cartella root del progetto;
3. Creare un virtual environment con il seguente comando:
    > python -m venv .venv
4. Attivare il virtual environment
5. Installare le dipendenze necessarie con il seguente comando:
    > pip install flask pymongo
6. Lanciare l’esecuzione del server flask con il seguente comando:
    > flask run