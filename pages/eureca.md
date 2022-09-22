---
layout: Post
title: EuReCa 3 🇸🇮
permalink: /eureca/
content-type: eg
---
<style>
  hr {
    border: inherit;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  }
  table, thead, tr, th {
    color: var(--text-main);
  }
</style>

This subpage is in Slovenian language and is intended for use by Slovenian healthcare professionals in order to use SiOHCA.

> **Vsem sodelujočim se bi radi zahvalili za pripravljenost sodelovati in angažiranost za sledenje podatkom.** Veselimo se že rezultatov, ki jih bomo dobili. Upamo tudi, da bo naš produkt postavil standard prijazne uporabniške izkušnje v zdravstvu.

<div style="padding:30pt 40pt 30pt 40pt;" id="collab-banner"></div>


| status sistema        | delujoč                                                |
| začetek študije       | 1. september 2022                                      |
| mail za podporo       | luka.petravic@student.um.si                            |
| link do baze          | [baza](https://local.siohca.um.si)                     |
| link za vpis podatkov | [vpis podatkov](https://test-api.siohca.local) |
| link do obrazca za tisk | <a href="https://github.com/SterArcher/OHCA-registry-Slovenia/raw/gh-pages/assets/pdf/siohca-v280822.pdf" download>obrazec </a>|
| pogosta vprašanja     | [FAQ](https://siohca.um.si/faq/)                       |

___
- [Kaj je SiOHCA](#kaj-je-siohca)
- [Kaj je EuReCa 3](#kaj-je-eureca-3)
- [Navodila za uporabo](#navodila-za-uporabo)
  - [Prošnja za dostop](#prošnja-za-dostop)
  - [Namestitev VPN](#namestitev-vpn)
    - [Operacijski sistem Windows](#operacijski-sistem-windows)
    - [Operacijski sistem Apple](#operacijski-sistem-apple)
      - [Kako namestiti VPN certifikat?](#kako-namestiti-vpn-certifikat)
      - [Kako aktivirati VPN?](#kako-aktivirati-vpn)
      - [Kako dodati bližnjico do nastavitev za VPN v zgornjo vrstico operacijskega sistema?](#kako-dodati-bližnjico-do-nastavitev-za-vpn-v-zgornjo-vrstico-operacijskega-sistema)
    - [Drugi operacijski sistemi](#drugi-operacijski-sistemi)
  - [Vpisovanje podatkov](#vpisovanje-podatkov)
    - [Ročno](#ročno)
    - [Avtomatizirano (trenutno samo preko Computela)](#avtomatizirano-trenutno-samo-preko-computela)
  - [Dostop do podatkov](#dostop-do-podatkov)
    - [Analiziranje](#analiziranje)
    - [Izvoz](#izvoz)
  - [Pravila uporabe](#pravila-uporabe)
  
____

# Kaj je SiOHCA
SiOHCA je interdisciplinaren študentski projekt, ki deluje z namenom digitalizacije zbiranja podatkov o predbolnišničnih srčnih zastojih (*ang. OHCA*). Končni cilj je vzpostavitev nacionalnega OHCA registra, ki predstavlja zlati standard za raziskave na področju tovrstnih kardiovaskularnih dogodkov. 


# Kaj je EuReCa 3
EuReCa 3 je evropska študija v kateri sodeluje 28 držav.

Podrobni rezultati EuReCa 2 študije in ostale informacije so spisane v [naši objavi na blogu](https://siohca.um.si/posts/EuReCa-3-and-SiOHCA).

# Navodila za uporabo
## Prošnja za dostop
Za dostop do registra SiOHCA je zaradi varnosti potrebno izpolniti prošnjo. Podatki so namenjeni za izdelavo osebno-specifičnega dostopa do spletnih strani, potrebnih za sodelovanje v registru SiOHCA ter študiji EuReCa 3.

> Po prijavi v sodelovanje preko e-maila vam bomo poslali prošnjo za dostop.

## Namestitev VPN
### Operacijski sistem Windows
Na mail, ki ste ga vpisali v obrazcu, boste prejeli povezavo do enkriptiranega odložišča. Zraven povezave je priložena tudi koda za dekodiranje datotek na povezavi in geslo certifikata.

Za namestitev sledite spodnjim korakom:
<style>
  img {
    margin-top: 20px;
    margin-bottom: 20px;
  }
</style>
1. Odpremo shranjeno datoteko “SiOHCA VPN.zip”
   
2. Vse datoteke v ZIP arhivu ekstrahiramo v enako mapo z orodjem po izbiri (na sliki prikazana Drag&Drop metoda z uporabo Windows Explorer-ja):  
![ekstrahiranje podatkov](https://siohca.um.si/assets/img/EuReCa/windows/ekstrahiranje.png)

3. V mapi, kamor smo ekstrahirali datoteke, zaženemo program “SiOHCA VPN.exe”: 
![prikaz po ekstrahiranju](https://siohca.um.si/assets/img/EuReCa/windows/ekstrahirano.png)

4.	Odpre se pojavno okno s prošnjo za administratorske pravice, ki jih za pravilno delovanje programa moramo odobriti:
![odobritev administratorskih pravic](https://siohca.um.si/assets/img/EuReCa/windows/admin.png)

5.	Pojavi se program za namestitev VPN omrežja in nas prosi za geslo certfikata. Geslo VTIPKAJTE in ne kopirajte, <ins>saj bo kopiranje povzročilo napako</ins>! Po vtipkanem geslu pritisnite tipko ENTER:
![geslo certifikata](https://siohca.um.si/assets/img/EuReCa/windows/geslo.png)

6.	Počakajte nekaj sekund, da se namestitev zaključi. Namestitev je uspešna, če se v oknu izpiše podobno besedilo:
![zakljucek](https://siohca.um.si/assets/img/EuReCa/windows/zakljucek.png)

7.	Po uspešni namestitvi vam svetujemo, da vse ekstrahirane datoteke zbrišete z računalnika.

### Operacijski sistem Apple
Na v obrazcu vpisan mail boste prejeli povezavo do enkriptiranega odložišča. Zraven povezave je priložena tudi koda za dekodiranje datotek na povezavi in geslo certifikata.

#### Kako namestiti VPN certifikat?
Za namestitev sledite spodnjim korakom:
1. Odprite .mobileconfig datoteko tako, da nanjo dvakrat kliknete:
![.mobileconfig datoteka](https://siohca.um.si/assets/img/EuReCa/ios/odprtje_config.png)

2. Sistem vas obvesti, da je certifikat potrebno potrditi v nastavitvah:
![obvestilo sistema](https://siohca.um.si/assets/img/EuReCa/ios/obvestilo_sistema.png)

3. Odprite **System Preferences**:
![nastavitve](https://siohca.um.si/assets/img/EuReCa/ios/nastavitve.png)

4.	Izberite **Profiles**:
![Profiles](https://siohca.um.si/assets/img/EuReCa/ios/profiles.jpg)

5.	Z rdečim napisom **Unverified** vas sistem obvesti, da certifikat še ni dokončno naložen. Klikinte »**Install...**«:
![instalacija](https://siohca.um.si/assets/img/EuReCa/ios/instalacija.png)

6.	Izberite možnost **Continue**:
![nadaljevanje instalacije](https://siohca.um.si/assets/img/EuReCa/ios/nadaljevanje_instalacije.png)

7.	Vnesite geslo in vnos potrdite s klikom na **Install**:
![vnos gesla](https://siohca.um.si/assets/img/EuReCa/ios/geslo.png)

8.	Zelen napis Verified je potrditev, da je bil certifikat uspešno nameščen:
![oznaka verified](https://siohca.um.si/assets/img/EuReCa/ios/verified.png)

#### Kako aktivirati VPN?
1.	V **System Preferences** izberite **Network**:
![Network](https://siohca.um.si/assets/img/EuReCa/ios/network.png)

2.	V levem stolpcu izberite **SiOHCA**, na desni strani pa klikinte **Connect**:
![siohca netwrok](https://siohca.um.si/assets/img/EuReCa/ios/siohca_network.png)

3. **Status: Connected** je znak, da je bila povezava uspešna:
![status connected](https://siohca.um.si/assets/img/EuReCa/ios/connected.png)

#### Kako dodati bližnjico do nastavitev za VPN v zgornjo vrstico operacijskega sistema?
1. V **System Preferences** izberite **Network**:
![Network](https://siohca.um.si/assets/img/EuReCa/ios/network.png)

2. V levem stolpcu izberite **SiOHCA**. Obkljukajte »**Show VPN status in menu bar.**«:
![show VPN status](https://siohca.um.si/assets/img/EuReCa/ios/siohca_network.png)

3.	Sedaj je bližnjica za aktivacijo VPN na voljo v opravilni vrstici:
![bliznjica](https://siohca.um.si/assets/img/EuReCa/ios/bliznjica.png)

### Drugi operacijski sistemi
Če uporabljate drug operacijski sistem, pišite na [luka.petravic@student.um.si](mailto:luka.petravic@student.um.si). Z veseljem vam bomo pomagali.


## Vpisovanje podatkov
### Ročno
Za ročno vpisovanje podatkov je potrebno imeti nameščen in aktiviran VPN.

> Za odprtje obrazca za vpisovanje podatkov kliknite [tukaj](https://test-api.siohca.local) .

### Avtomatizirano (trenutno samo preko Computela)

Za vse NMP enote, ki uporabljajo informacijski sistem podjetja Computel, smo se z njimi povezali in ustvarili direktno povezavo znotraj njihove informacijskega sistema.

Funkcija je trenutno v razvoju, dostopna bo kot del *⍺ verzije*.


## Dostop do podatkov
Za dostop do podatkov je potrebno imeti nameščen in aktiviran VPN.

> Za dostop do baze kliknite [**tukaj**](https://local.siohca.um.si).


### Analiziranje
Za dostop do podatkov uporabljamo [MetaBase](https://www.metabase.com). Zaradi omejitve financ projekta uporabljamo osnovno verzijo. Vseeno je funkcionalnosti za analiziranje podatkov ogromno.

Uporabniški vmesnik je preprost in prijazen do uporabnika. V angleščini pa so na voljo tudi uporabna navodila, do njih lahko dostopate preko povezave [**tukaj**](https://www.metabase.com/docs/latest/).

### Izvoz
Podatki, ki jih zbirate so zmeraj na voljo za prenos. Odločite se lahko, da prenesete samo podatke povezane z vašimi vprašanji, glej [analiziranje](#Analiziranje).

Podatke prenesete s klikom na ikono spodaj desno:

![slika ikone spodaj desno](/assets/img/EuReCa/metabase_download.png)

Izberete si lahko tudi v kakšnem formatu bi radi imeli podatke
- csv
- xls
- json

## Pravila uporabe
Pozor podatki EuReCa tri študije ne smejo biti objavljeni pred objavljenim članom delovne skupine!

Podatki vsebujejo zaupne informacije, ki morajo biti varovane v skladu s pravili in dobro prakso medicinske etike ter GDPR zakonodaje, zato baze ne fotografirajte/objavljajte prosto.

Željene data sete vam bomo izvozili mi.
<script src="https://siohca.um.si/assets/js/eureca.js"></script>
