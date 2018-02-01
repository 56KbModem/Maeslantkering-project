# IDP-Project Maeslantkering Groep 1 V1J

In deze README vindt u de technische documentatie
en gebruikte bronnen voor het IDP project.

## Index
* [Requirementsanalyse](https://github.com/56KbModem/Maeslantkering-project#requirementsanalyse)
* [Technische documentatie](https://github.com/56KbModem/Maeslantkering-project#technische-documentatie)
  * [Model Maeslantkering](https://github.com/56KbModem/Maeslantkering-project#model-maeslantkering)
  * [Watermeting](https://github.com/56KbModem/Maeslantkering-project#watermeting)
  * [Serieel protocol](https://github.com/56KbModem/Maeslantkering-project#serieel-protocol)
  * [De Client](https://github.com/56KbModem/Maeslantkering-project#de-client)
  * [INIT script](https://github.com/56KbModem/Maeslantkering-project#init-script)
* [Schakeldiagram kering](https://github.com/56KbModem/Maeslantkering-project#schakeldiagram-kering)
* [Bronnen](https://github.com/56KbModem/Maeslantkering-project#bronnen)

## Requirementsanalyse

Het product moet aan de volgende eisen voldoen:
*	Waterhoogte meten op twee punten
  *	Oplossing: Er is meermaals getest met een analoge watersensor, de analoge input is vertaald naar een waarde in centimeters, via een serieel protocol kan van meetpunt gewisseld worden. Er kan dus op twee punten gemeten worden maar er was op de microcontroller nog maar plaats voor 1 sensor. Er is gekozen voor een Arduino omdat de aansturing makkelijker is, er draait maar 1 programma en er is geen operating system. Tevens heeft de Arduino een ingebouwde ADC (analoog naar digitaal converter), deze mist op bijvoorbeeld de Raspberry Pi.
  *	Voldaan?: JA

*	Kering openen, sluiten.
  *	Oplossing: Voor het openen/sluiten van de kering is gebruik gemaakt van stappermotoren. In tegenstelling tot servo motoren hebben stappermotoren meer koppel maar een lagere snelheid, omdat nauwkeurigheid belangrijker is dan snelheid heb ik voor stappermotoren gekozen. De kering sluit bijna volledig (er is ruimte zodat deze niet kapot gaat) en wanneer hij open gaat neemt hij dezelfde positie weer in. De kering opent of sluit pas na commando van de controleposten (servers, ontwikkeld door SIE).
  *	Voldaan?: JA

*	Redundantie
  *	Oplossing: Eigenlijk een opdracht voor SIE, maar ik heb deze op mij genomen omdat het makkelijker te implementeren was van het model af richting de netwerk infrastructuur. Er wordt gebruik gemaakt van een Raspberry Pi die contact legt met een van de twee controleposten (servers). Als hij met de ene geen connectie krijgt of de connectie valt weg, dan schakelt hij automatisch over naar het volgende IP-adres. Er moet natuurlijk wel 1 van de twee servers klaar zijn om de connectie te verwerken anders schakelt de client uit.
  *	Voldaan?: JA

## Technische documentatie

#### Model Maeslantkering

Het model van de Maeslantkering is gebouwd op een
Arduino UNO (ATMega328p) als microcontroller die twee
unipolaire steppermotoren aandrijft van het type 28BYJ-48
door middel van twee ULN2003A Darlington arrays (1 per motor),
deze worden gebruikt als driver.

De ULN2003 wordt gebruikt om de stroomsterkte te reguleren
voor de steppermotoren door middel van 7 interne weerstanden.

De steppermotoren (28BYJ-48) bestaan uit een magnetische rotor
en een elektromagnetische stator bestaande uit 32 'tanden'. Intern
doet de motor er dus 32 stappen over om rond te gaan. De buitenste
as van de motor zit aan de rotor vast met tandwielen die tezamen
een tandwiel verhouding van 1 op 64 geven. De motor kan dus in
(32 * 64 =) 2048 stappen een rotatie maken, wat hem zeer nauwkeurig
maakt.

De Arduino, drivers en motoren zitten geassembleerd in een
houten kist met een opening voor de stroom en seriële verbinding.
De motoren zijn vastgeschroefd op de onderkant van de deksel van
de kist zodat op de bovenkant van de deksel de armen en deuren van 
de Maeslantkering gemonteerd zijn.

De waterhoogte wordt gemeten door middel van een sensor met 
ingebouwde magnetische weerstand. door het spanningsverschil over de
plus- en minpool te meten kan de waterhoogte op schaal berekend worden.

Door het gebruik van een zelf ontworpen protocol kan het meetpunt
gewisseld worden, deze begint in Rotterdam waar de kering dicht gaat
bij een waterstand van 3 meter boven NAP. Het andere meetpunt, Dordrecht,
zal de kering dicht laten gaan bij een waterstand van 2,9 meter boven NAP

#### Watermeting

De watersensor heeft een weerstand die afhankelijk van de hoogte van het waterpeil
de weerstand verhoogt. Door een pool van de sensor op +5 volt te zetten en de
signaalingang op een analoge input van de Arduino kunnen we het verschil in spanning
en dus de waterhoogte aflezen.

Omdat de microcontroller natuurlijk digitaal is zal er op de analoge input
een meting tussen de 0 en 1023 binnenkomen afhankelijk van het voltage. Dankzij
de in de Arduino softwarebibliotheek ingebouwde `map()` functie kunnen we deze 
waardes omzetten naar een schaal tussen de 280 en 310. Deze schaal van 100 stappen
beschouwen wij als centimeters.

Een serieel commando bepaald de 'plek' waar de meting plaatsvindt. Wat deze
eigenlijk doet is een variabele aanpassen die aangeeft of er bij Rotterdam of bij
Dordrecht gemeten wordt. De waarde van deze variabele wordt meegezonden over de
seriële verbinding samen met de gemeten waterstand.

#### Serieel protocol

De communicatie tussen de Arduino in de waterkering en de controleposten
verloopt via een tussenstation (de client). De client en de controleposten
zijn allen Raspberry Pi's die via een Ethernet netwerk met elkaar in verbinding
staan.

Omdat er op de Arduino te weinig pinnen zijn om een Ethernet module aan
te sluiten is gekozen voor een oplossing waarbij de Arduino met de client
een seriële verbinding heeft en zo commando's kan ontvangen en zijn meetwaarden
kan versturen.

De seriële verbinding heeft de volgende eigenschappen:
*	Snelheid: 9600 baud
*	databits: 8
*	pariteitsbit: geen
*	stopbits: 1

Dit is de meest voorkomende configuratie (9600-8N1).

Omdat zo een verbinding zijn karakters bit per bit verzend is het veilig
om de uit te wisselen berichten zo kort mogelijk te houden. Het commando om
de kering te sluiten is een ASCII karakter `A`. Om hem te openen het ASCII
karakter `B`. De waterstand wordt doorgegeven als `XX YYY` waarbij `XX` de
meetplek aangeeft (RD of DD) en `YYY` de waterhoogte in centimeters. Het
ASCII karakter `C` geeft aan dat er van meetplek gewisseld moet worden

Voorbeeld:

```text
RD 271 (waterhoogte 2,71 meter boven NAP. Meetpunt Rotterdam)
DD 296 (waterhoogte 2,96 meter boven NAP. Meetpunt Dordrecht)
```

Omdat de controleposten geprogrammeerd worden in Python 3 zullen deze ASCII 
karakters gedecodeerd worden naar UTF-8 strings, de interne stringrepresentatie
in Python 3.

Als er een sluiting plaats vindt zal het controlewoord `CLOSE` meegestuurd worden,
bij openen is dat `OPEN`. Aan de hand van deze controlewoorden weten de controleposten
de status van de kering.

Een bericht wordt afgesloten met een carriage return (`\r`) gevolgd
door een newline (`\n`).

#### De Client

De client, het tussenstation tussen de Arduino en de servers dient er voor
de data van de Arduino die over de seriële lijn binnenkomt door te geven aan
de servers. Daarna zal hij bij het ontvangen van een commando deze doorzetten
naar de Arduino. 

De client kijkt ook of de hoofd server te bereiken is. Als
dit niet zo is dan zal hij proberen contact te maken met de failover server.
Als de failover server ook wegvalt dan probeert hij de eerste weer enzovoort.

Het is wel belangrijk dat de client de eerste keer dat hij verbinding
probeert te maken een verbinding met een van de twee servers krijgt.
Als er helemaal geen verbinding gemaakt kan worden dan treed er een timeout op.

De client houdt ook loggegevens bij.

#### INIT script

Op de client en servers draaien ook UNIX init scripts, door deze scripts
kan de client en server als UNIX daemon gebruikt worden. dat wil zeggen
dat zowel client als server nu een service zijn die beheerd kunnen worden
met het `service` commando.

De client en server init scripts kunnen drie parameters verwerken,
`start` om de service te starten, `stop` om de service te stoppen en
`restart` om te herstarten.

Dankzij deze scripts worden de python scripts `client.py` en `server.py`
ook gestart zodra de Raspberry Pi's aangezet worden.

## Schakeldiagram kering
![Diagram](https://github.com/56KbModem/Maeslantkering-project/blob/master/src/img/kering_diagram.png?raw=true)

*	Blauw: controller
*	Rood: +5 Volt
*	Zwart: Aarde
*	Geel: Analoge input

## Bronnen

* [serial reference](https://www.arduino.cc/reference/en/language/functions/communication/serial/)

	Deze referentiegids is gebruikt voor de Arduino Serial.h softwarebibliotheek.

* [The C Programming Language](https://en.wikipedia.org/wiki/The_C_Programming_Language)

	De tweede editie van dit boek is gebruikt door Nick als referentie voor het programmeren in C.
	Auteurs: Brian Kernighan & Dennis Ritchie.

* [PySerial documentation](http://pyserial.readthedocs.io)

	Deze documentatie is gebruikt als naslagwerk voor de PySerial softwarebibliotheek.
