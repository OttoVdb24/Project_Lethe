# Raspberry Pi code

De interface van de slimme kapstok werd ontwikkeld in Python met behulp van Pygame. De applicatie draait op een Raspberry Pi 4 en biedt gebruikers een eenvoudige manier om hun planning te bekijken en een tas samen te stellen op basis van geplande activiteiten.

Het startpunt van de applicatie is [`Homescreen.py`](./Homescreen.py). Vanuit dit startscherm kan de gebruiker:

- Een overzicht van de geplande activiteiten bekijken.
- De **zak-maak**-interface openen via [`ZakMaakApp_Kleuren.py`](./ZakMaakApp_Kleuren.py).
- De **planning-maak**-interface openen via [`PlanningApp.py`](./PlanningApp.py).

## Planning-maak interface

Tijdens develop 2 werd de planning-maak interface ontworpen en verder uitgewerkt. Hierbij lag de focus op gebruiksvriendelijkheid en usability goals, zodat gebruikers op een intuïtieve manier activiteiten kunnen toevoegen en beheren.

Meer informatie hierover is terug te vinden in de documentatie: [Develop 2 – App](../docs/develop2.md#app).

## Zak-maak interface

Tijdens develop 3 werd de zak-maak interface verder ontwikkeld. Hierbij werd bijzondere aandacht besteed aan emotional design om de interactie aantrekkelijker en speelser te maken voor de gebruiker.

Verschillende varianten van de interface werden onderzocht en geïmplementeerd. Zo zijn er versies waarbij gebruikers:

- Benodigdheden kunnen aantikken om ze te selecteren [`ZakMaakApp_Tikken.py`](./ZakMaakApp_Kleuren.py).
- Objecten naar een tas kunnen slepen [`ZakMaakApp_Slepen.py`](./ZakMaakApp_Slepen.py).
- Benodigdheden kunnen inkleuren om de interactie persoonlijker en visueel aantrekkelijker te maken [`ZakMaakApp_Kleuren.py`](./ZakMaakApp_Kleuren.py).

Alle code en prototypes van deze varianten zijn terug te vinden in deze map.