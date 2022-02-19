# Projekt WDSI
Ponieżej opisano działanie najważniejszych funkcji progamu.
## load_data
Funkcja ta wczytuje dane z pilku xml takie jak:
- nazwa obrazka
- ścieżka do obrazka  
- wymiary obrazka: szerokosć i wysokość
- obszar występowania znaku  
- klasa obrazka.

Następnie obrazek jest przyciany i jeśli jego wymiary są przynajminej wielkości 10% wyskości i szerokości całego obrazka to
jego paramtery zapisywane są w zmiennej data.

Najważniejsze wykorzystane funkcje:
- ***os.listdir(path)*** - wyszukianie pilków w podnej ścieżce
- ***et.parse()*** - wczytywanie plików
- ***getroot()*** - pobieranie korzenia
- ***findall(label)*** - wyszukiwanie korzeni o podanej nazwie
- ***find(label).text*** - znajdowanie danego elementu i zwracanie go jako tekst
- ***image[int(y_min) : int(y_max), int(x_min) : int(x_max)]*** - wycięcie fragmentu obrazka
- ***class_id_to_new_class_id*** - zmania słowna na numer klasy 
- ***os.getcwd()*** - zwracenie ścieżki do pliku
- ***os.path.join(path, filename)*** - połączenie ścieżki z nazwą pliku
- ***cv2.imread()*** - wczytywanie obrazka


## learn_bovw

Najważniejsze wykorzystane funkcje:
- ***cv2.BOWKMeansTrainer()*** - podstawowa klasa do trenowania, określa wielkość słownika
- ***cv2.SIFT_create()*** - klasa do wyodrębnienia kluczowych punktów i deskryptorów
- ***sift.detect()*** - znajduje kluczowe punkty na obrazkach
- ***sift.compute()*** - oblicz deskryptory z znalenionych punktów
- ***bow.cluster()*** - tworzy słownik
- ***np.save()*** - zapis do pliku
## extract features
Wyodrębnianie cech i zapis opisów:

- ***cv2.FlannBasedMatcher_create()*** 
- ***cv2.BOWImgDescriptorExtractor(sift, flann)***
- ***bow.setVocabulary(vocabulary)*** 
## train
Trenowanie klasyfikatora Random Forest:

- ***RandomForestClassifier()*** -
- ***rf.fit(descs, labels)*** -
## predict
Przewiduje etykiete danego modelu i zapise jako wpis „label_pred” dla każdej próbki:

- ***rf.predict(sample['desc'])*** - przewidywanie klasy z opisu 

## evaluate
Ocena wyników klasyfikacji:

Funckja sprawdza poprawność klasyfikacji z opisami z plików xml.
Następnie oblicza i wyświetla procentowy wynik poprawności klasyfikacji miary mAP oraz macierz pomyłek.

## display_dataset_stats
Wyświetlanie satystyk zestawu danych:
## balance_dataset
Balanusje próbki zgodnie z podanym współczynnikiem
## main
Wywłoanie fukncji w odpoiedniej kolejności.
Funkcję learn_bovw można zakomentować po pierwszym urchomieniu programu.
W takim przypadku słownik będzie wczytywany z pliku voc.npy.
