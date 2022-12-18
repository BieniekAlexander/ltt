read -r -d '' TEXT <<EOF
​Czy powinienem zostać, czy powinienem coś zmienić? 96% osób rozważałoby odejście z pracy, gdyby pojawiła się lepsza okazja. Czemu nie? Zła renoma zmian pracy odchodzi powoli w zapomnienie, a na jej miejsce pojawia się nowe przedświadczenie, że pracownicy powinni zmieniać pracę nie rzadziej niż co 3-5 lat.
Powody zmiany pracy są różne dla wszystkich, ale korzyści z przestawiania się co kilka lat są często takie same – bez względu na to, jaką ścieżką kariery wybrałeś.

​

Rozwijasz nowe umiejętności
Zmiana pracy utrzymuje Cię w ryzach i pomaga rozwinąć cenne umiejętności zawodowe. Kiedy rozpoczynasz nową pracę, jesteś poza strefą komfortu i zmuszony jesteś do nauczenia się nowych systemów, nowej codzienności, nowych nazwisk i nowych umiejętności. Bez względu na to, jak dobra jest Twoja obecna praca, są to rzeczy, których można się nauczyć dopiero po wejściu w nową sytuację zawodową. Praca z różnymi firmami daje także doświadczenie w różnych strukturach biznesowych, co jest pomocne, jeśli kiedykolwiek planujesz rozpocząć własną działalność.

​

Zarobisz więcej pieniędzy
Według Forbesa pracownicy, którzy przebywają w firmie dłużej niż dwa lata, zarabiają o 50% mniej niż pracownicy na podobnych stanowiskach, którzy zmieniają pracę. Jako że roczne podwyżki są zwykle oparte na procentach twojej podstawowej pensji, trudno jest dokonać dużego skoku w skali płac, będąc cały czas w tej samej firmie. Rozwijanie umiejętności i zdobywanie doświadczenia w różnych miejscach pracy oznacza, że ​​pracodawcy mają większe szanse na zaoferowanie wyższej pensji.

​

Praca jest ciekawsza
Kiedy wybieramy studia, czy pierwszą pracę, rzadko wiemy, co tak naprawdę chcemy robić w życiu. I jest to normalne. Zmiana pracy pozwala wypróbować różne role, nawet różne gałęzie przemysłu i dowiedzieć się, co jest dla Ciebie najlepsze. Może to oznaczać oczywiście, że po drodze trafisz na pracę, która Ci nie odpowiada, ale dzięki temu doświadczeniu, będziesz ciągle bliżej znalezienia tej idealnej.

​

Posiądziesz umiejętność adaptacji
Postęp technologiczny i innowacyjne myślenie zmieniają sposób, w jaki pracujemy. Teraz, bardziej niż kiedykolwiek wcześniej, ważne jest, aby pracownicy byli elastyczni i chcieli rzucić się w nieznane. Zmiana pracy zmusza Cię do przystosowania się i przygotowania się do nowych strategii, projektów i osób związanych z każdą rolą. Dzięki temu jesteś bardzo cenny dla firm, które wymagają mobilnych, elastycznych pracowników.

​

Masz kontrolę nad swoją karierą
Trzeba wiele odwagi i samoświadomości, aby podjąć nową pracę, a nie zostać w miejscu, które wydaje się bezpieczne. Poszukiwanie pracy buduje pewność siebie i niezależność, gdy aktywnie poszukujesz możliwości, których pragniesz. Masz własną ścieżkę karierę i nie czekajsz, aż firmy dadzą ci to, na co zasługujesz.

​

Rozwijasz relacje z nowymi osobami
Pozostawienie znajomych z pracy może być trudne, ale zmieniając pracę co kilka lat, będziesz miał możliwość budowania nowych relacji. Nowi koledzy nauczą Cię nowych rzeczy, przedstawią Ci nowych ludzi, a nawet staną się twoimi najlepszymi przyjaciółmi w pracy. Jak to osiągniesz, jesli nie dokonasz zmiany?

​
EOF

echo $TEXT

curl 'http://localhost:5000/annotate' \
  -H 'Content-Type: application/json' \
  -X POST \
  -d "{\"language\": \"polish\", \"user_id\": \"62a57d5bfa96028f59ac1d75\", \"text\": \"$TEXT\"}"


Czy powinienem zostać, czy powinienem coś zmienić? 96% osób rozważałoby odejście z pracy, gdyby pojawiła się lepsza okazja. Czemu nie? Zła renoma zmian pracy odchodzi powoli w zapomnienie, a na jej miejsce pojawia się nowe przedświadczenie, że pracownicy powinni zmieniać pracę nie rzadziej niż co 3-5 lat.
Powody zmiany pracy są różne dla wszystkich, ale korzyści z przestawiania się co kilka lat są często takie same - bez względu na to, jaką ścieżką kariery wybrałeś.

Rozwijasz nowe umiejętności
Zmiana pracy utrzymuje Cię w ryzach i pomaga rozwinąć cenne umiejętności zawodowe. Kiedy rozpoczynasz nową pracę, jesteś poza strefą komfortu i zmuszony jesteś do nauczenia się nowych systemów, nowej codzienności, nowych nazwisk i nowych umiejętności. Bez względu na to, jak dobra jest Twoja obecna praca, są to rzeczy, których można się nauczyć dopiero po wejściu w nową sytuację zawodową. Praca z różnymi firmami daje także doświadczenie w różnych strukturach biznesowych, co jest pomocne, jeśli kiedykolwiek planujesz rozpocząć własną działalność.

Zarobisz więcej pieniędzy
Według Forbesa pracownicy, którzy przebywają w firmie dłużej niż dwa lata, zarabiają o 50% mniej niż pracownicy na podobnych stanowiskach, którzy zmieniają pracę. Jako że roczne podwyżki są zwykle oparte na procentach twojej podstawowej pensji, trudno jest dokonać dużego skoku w skali płac, będąc cały czas w tej samej firmie. Rozwijanie umiejętności i zdobywanie doświadczenia w różnych miejscach pracy oznacza, że pracodawcy mają większe szanse na zaoferowanie wyższej pensji.

Praca jest ciekawsza
Kiedy wybieramy studia, czy pierwszą pracę, rzadko wiemy, co tak naprawdę chcemy robić w życiu. I jest to normalne. Zmiana pracy pozwala wypróbować różne role, nawet różne gałęzie przemysłu i dowiedzieć się, co jest dla Ciebie najlepsze. Może to oznaczać oczywiście, że po drodze trafisz na pracę, która Ci nie odpowiada, ale dzięki temu doświadczeniu, będziesz ciągle bliżej znalezienia tej idealnej.

Posiądziesz umiejętność adaptacji
Postęp technologiczny i innowacyjne myślenie zmieniają sposób, w jaki pracujemy. Teraz, bardziej niż kiedykolwiek wcześniej, ważne jest, aby pracownicy byli elastyczni i chcieli rzucić się w nieznane. Zmiana pracy zmusza Cię do przystosowania się i przygotowania się do nowych strategii, projektów i osób związanych z każdą rolą. Dzięki temu jesteś bardzo cenny dla firm, które wymagają mobilnych, elastycznych pracowników.

Masz kontrolę nad swoją karierą
Trzeba wiele odwagi i samoświadomości, aby podjąć nową pracę, a nie zostać w miejscu, które wydaje się bezpieczne. Poszukiwanie pracy buduje pewność siebie i niezależność, gdy aktywnie poszukujesz możliwości, których pragniesz. Masz własną ścieżkę karierę i nie czekajsz, aż firmy dadzą ci to, na co zasługujesz.

Rozwijasz relacje z nowymi osobami
Pozostawienie znajomych z pracy może być trudne, ale zmieniając pracę co kilka lat, będziesz miał możliwość budowania nowych relacji. Nowi koledzy nauczą Cię nowych rzeczy, przedstawią Ci nowych ludzi, a nawet staną się twoimi najlepszymi przyjaciółmi w pracy. Jak to osiągniesz, jesli nie dokonasz zmiany?