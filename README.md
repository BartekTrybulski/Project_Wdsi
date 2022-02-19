# Projekt WDSI
Ponieżej opisano działanie najważniejszych funkcji progamu.
## load_data
Funkcja ta wczytuje dane z pilku xml takie jak:
- nazwa obrazka
- ścieżka do obrazka  
- wymiary obrazka: szerokość i wysokość
- obszar występowania znaku  
- klasa obrazka.

Następnie obrazek jest przyciany i jeśli jego wymiary są przynajminej wielkości 10% wysokości i szerokości całego obrazka to
paramtery zapisywane są w zmiennej data.

Najważniejsze wykorzystane funkcje:
- ***os.listdir(path)*** - wyszukiwanie pilków w podnej ścieżce
- ***et.parse()*** - wczytywanie plików
- ***getroot()*** - pobieranie korzenia
- ***findall(label)*** - wyszukiwanie korzeni o podanej nazwie
- ***find(label).text*** - znajdowanie danego elementu i zwracanie go jako tekst
- ***image[int(y_min) : int(y_max), int(x_min) : int(x_max)]*** - wycięcie fragmentu obrazka
- ***class_id_to_new_class_id*** - zmania nazwy klasy na numer 
- ***os.getcwd()*** - zwracenie ścieżki do pliku
- ***os.path.join(path, filename)*** - połączenie ścieżki z nazwą pliku
- ***cv2.imread()*** - wczytywanie obrazka


## learn_bovw
Funkcja ta tworzy słownik przy pomocy charakterystycznych punktów ze zdjęć.

Najważniejsze wykorzystane funkcje:
- ***cv2.BOWKMeansTrainer()*** - tworzy zbiór treningowy, określa jego rozmiar (w programie zmienna bow)
- ***cv2.SIFT_create()*** - tworzy klasę do wyodrębnienia kluczowych punktów i deskryptorów
- ***sift.detect()*** - znajduje kluczowe punkty na obrazkach
- ***sift.compute()*** - oblicza deskryptory dla znalezionych punktów
- ***bow.add(desc)*** - dodaje opis do zbioru 
- ***bow.cluster()*** - tworzy słownik
- ***np.save()*** - zapisuje słownik do pliku
## extract features
Funkcja ta odpowiada za wyodrębnianie cech zawartych w słowniku dla poszczególnych próbek wczytanego zbioru.


Najważniejsze wykorzystane funkcje:
- ***cv2.FlannBasedMatcher_create()***  - tworzy moduł dopasowania
- ***cv2.BOWImgDescriptorExtractor(sift, flann)*** - tworzy moduł dla opisów
- ***bow.setVocabulary(vocabulary)*** - zwraca wizualny słownik

## train
Funkcja odpowiadająca ze trenowanie klasyfikatora Random Forest.

Najważniejsze wykorzystane funkcje:
- ***squeeze(0)*** - usuwanie osi
- ***RandomForestClassifier()*** - tworzy klasyfikator Random Forest (w programie rf)
- ***rf.fit(descs, labels)*** - tworzy "las drzew" z zestawu treningowego
## predict
Przewiduje etykiete danego modelu i zapisuje jako wpis „label_pred” dla każdej próbki:

Najważniejsze wykorzystane funkcje:
- ***rf.predict(sample['desc'])*** - przewidywanie klasy z opisu 

## evaluate
Ocena wyników klasyfikacji. Funkcja sprawdza poprawność klasyfikacji z opisami z plików xml.
Następnie oblicza i wyświetla procentowy wynik poprawności klasyfikacji miary mAP oraz macierz pomyłek.
Odpowiada także za wypisywanie nazw zdjęć na których znajdują się znaki przejść dla pieszych.
## display_dataset_stats
Funkcja ta wyświetla ilość obrazów każdego zbioru.
## balance_dataset
Balansuje próbki zgodnie z podanym współczynnikiem (zakres od 0 do 1)
W zależności od jego wartości wczytywany jest odpowiedni procent danych.

Najważniejsze wykorzystane funkcje:
- ***random.sample(data, amount)*** - wybór losowych próbek 
## main
Wywołuje wszystkie wcześniej opisane funkcje, a także wyświetla która z funkcji aktualnie jest wykonywana.

Funkcję learn_bovw można zakomentować po pierwszym uruchomieniu programu.
W takim przypadku słownik będzie wczytywany z pliku voc.npy.
