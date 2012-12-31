# Spickey The Game - Projekt zaliczeniowy

Gra platformowa polegająca na pokonaniu planszy naszpikowanej zabójczymi półapkami w jak najkrótszym czasie. 

![Screenshot](http://eros.vlo.gda.pl/~spiroz/projekt/screen.png)


## Uwagi

Jest to wczesna wersja projektu. Kolizja zrealizowana jest z wykorzystaniem techniki bounding box, w zwiazku z czym  
obiekty reagują ze sobą wcześniej niż wynika to z bitmapy.


## Instalacja

Projekt napisany został w języku Python z wykorzystaniem biblioteki pyglet. 
Wymaga interpretera Python w wersji 2.7.3. Pod gałęzią 3.x gra nie była testowana.

### Linux (dystrybucje oparte na debianie)

1. Zainstaluj Python z gałęzi 2.7.x 
    
    	$ sudo apt-get install python
    
2. Zainstaluj bibliotekę pyglet
    
    	$ sudo apt-get install python-pyglet
    
3. [Pobierz] i rozpakuj projekt
4. Nadaj uprawnienia uruchomiania dla pliku game/main.py
    
    	$ chmod +x scieżka_do_projektu/game/main.py

5. Uruchom aplikacje
		
		$ cd scieżka_do_projektu/game/
		$ ./main.py
    
[Pobierz]: https://github.com/jmietki/Projekt/archive/master.zip

### Windows 

Obecnie platforma Windows nie jest wspierana.

Oficjalna wersja do oceny zostanie wydana w wersji na Windows, prawdopodobnie w formie paczki .exe
przygotowanej z pomocą py2exe.

## Znane problemy

Pomijając liczne problemy związane z wczesną wersją, może wystąpić problem z bardzo niską wydajnością w trybie okienkowym pod Ubuntu Unity.
W takim przypadku należy przełączyć grę w tryb pełnoekranowy. 

W pliku game/game.xml należy zmienić linijkę
	
		<fullscreen value="false"/>

na 

		<fullscreen value="true"/>


## Główne TO-DO

- Kolizja per pixel
- Rozliczanie wygranej/przegranej
- Proste menu
