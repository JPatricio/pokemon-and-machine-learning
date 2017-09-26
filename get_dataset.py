import requests
import csv
import sys
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

if len(sys.argv) < 2:
    print("no extraction source argument specified")
    exit(0)

if sys.argv[1] == "gis":
    url = "https://www.google.pt/search?biw=1440&bih=799&tbs=isz%3Aex%2Ciszw%3A128%2Ciszh%3A128&tbm=isch&sa=1&q=pikachu&oq=pikachu&gs_l=psy-ab.3..0i67k1j0l3.157630574.157630574.0.157631022.1.1.0.0.0.0.109.109.0j1.1.0....0...1.1.64.psy-ab..0.1.108....0.Uzdo5HW8EUA"
    # starting pokemon ID in case of restarts.
    progress = 1

    pikachu_family = ["Pikachu", "Raichu", "Pichu", "Plusle", "Minun", "Pachirisu", "Emolga", "Dedenne", "Togedemaru", "Alolan Raichu"]
    with open('Pokemon.csv', newline='') as csvfile:
        pokemon = csv.reader(csvfile, delimiter=',', quotechar='|')
        # Skip first line, the labels
        next(pokemon)
        for row in pokemon:
            if int(row[0]) < progress:
                continue
            if row[1] in pikachu_family:
                r = requests.get(url.replace("pikachu", row[1]))
                data = r.text

                soup = BeautifulSoup(data, "html5lib")
                i = 0
                for link in soup.find_all('img')[1:]:
                    urlretrieve(link.get('src'), "DCGAN-tensorflow-master/data/pika_family/%s_%s.jpg" % (progress, i))
                    i += 1
                progress += 1
                print("%s images downloaded. %s out of %s pokemon completed!" % (row[1], row[0], 721))

    # python main.py --dataset pokemon --input_height=128 --crop --train

if sys.argv[1] == "ss":
    url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/%s.png"
    # starting pokemon ID in case of restarts.
    progress = 1

    with open('Pokemon.csv', newline='') as csvfile:
        pokemon = csv.reader(csvfile, delimiter=',', quotechar='|')
        # Skip first line, the labels
        next(pokemon)
        for row in pokemon:
            if int(row[0]) < progress:
                continue
            if row[3] != "Electric":
                continue
            try:
                urlretrieve(url % row[0].zfill(3), "DCGAN-tensorflow-master/data/electricss/%s.jpg" % row[0])
                print("%s images downloaded. %s out of %s pokemon completed!" % (row[1], row[0], 721))
            except Exception as err:
                print(err)
                print("Pokemon %s failed to download" % row[1])
                print(url % row[0].zfill(3))
                a = input()
        progress += 1

    # python main.py --dataset pokemon --input_height=128 --crop --train

if sys.argv[1] == "cards":
    url = "https://assets.pokemon.com/assets/cms2/img/cards/web/EX%s/EX%s_EN_%s.png"
    # starting pokemon ID in case of restarts.
    ex_number = 1
    card_number = 1

    while True:
        try:
            urlretrieve(url % (ex_number, ex_number, card_number),
                        "DCGAN-tensorflow-master/data/cards/%s_%s.png" % (ex_number, card_number))
            print("Image %s downloaded." % card_number)
            card_number += 1
        except Exception as err:
            if card_number == 1:
                print("finished")
                break
            card_number = 1
            ex_number += 1
            print("This ex is done. Proceeding to EX%s" % ex_number)

        # python main.py --dataset pokemon --input_height=128 --crop --train
