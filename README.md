# Bazy danych 1 - projekt
## Adam Paleczny, Informatyka stosowana, grudzień 2023

Aplikacja bazodanowa obsługująca zawody inżynierskie Formula Student Polska. Jej zadaniem jest rejestracja nowych uczestników na zawody oraz oferuje niezbędne informacje potrzebne na zawodach.

## Struktura aplikacji
- **sql** - katalog zawierający potrzebne pliki sql do przykładowej bazy danych
- **dataset** - folder zawierający przykładowe dane do wprowadzenia
- **app** - folder ze programem napisanym w języku Python do obsługi aplikacji 
- **docs** - katalog zawierający dokumentację do projektu

## Aplikacja
### Wymagania:
- Python 🐍
- Linux 🖥️

Instalowanie potrzebnych bibliotek:
``` bash
pip install -r requirements.txt
```

### Uruchomienie aplikacji
```bash
python3 app/main.py
```

## Konfiguracja przykładowej bazy danych
W celu sprawdzenia działania programu nie jest wymagana konfiguracja bazy danych, gdyż wstępna konfiguracja została już zrobiona. Jednak w przypadku konfiguracji własniej bazy danych trzeba wykonać pare zmian:

- Zmiana danych w pliku app/main.py w metodzie **connect_to_database()** - zmiana bazy danych
- W swojej bazie danych należy wykonać pliki z katalogu **sql** w odpowiedniej kolejności:
1. ***create_table.sql*** -> Tworzy tabele potrzebne do instnienia projektu w schemacie *projekt*
2. ***insert.sql*** -> Przykładowe dane
3. ***trigger.sql*** -> Tworzy trigery potrzebne do działania bazy danych we współpracy z aplilkacją
4. ***view.sql*** -> tworzy widok potrzebny do działania aplikacji

## Dokumentacja
Dokumentacja do projektu znajduje się w katalogu docs. Tam również znajdują się szczegóły co do implementacji oraz struktury bazy danych.