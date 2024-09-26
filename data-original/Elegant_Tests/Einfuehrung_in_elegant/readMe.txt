Stand: 2020-04-02

=============================================================
Einführung in die Funktionsweise des Tracking-Tools "elegant"
=============================================================

elegant ("ELEctron Generation ANd Tracking") kann nicht nur Tracken, sondern hat
auch ein Optimierungsalgorithmus implementiert. Dieser sowie eine generelle Einführung
in elegant ist im Ordner "1_Optimierung" erläutert.
Im Ordner "2_Variierung" wird Parameter-Sweeping behandelt.
Die Manuals für elegant und SDDS sowie "GettingStartedWithSDDS" sind beigefügt und sollten
später oder parallel zu den Einführungsbeispielen ebenfalls gelesen werden.

elegant funktioniert wie folgt: in einer *.lte-Datei wird der Beschleuniger definiert,
in einer *.ele-Datei wird dieser definierte Beschleuniger eingelesen sowie weitere
Optionen festgelegt, die für das Tracking relevant sind.

Das Tracking kann dann durch eine Konsole mittels "elegant Datei_Name.ele" ausgeführt werden.
Smartes Ausführen sowie erstes Postprocessing mit SDDS-Befehlen gelingt über bash-/tclsh-Skripte.

Beim Ausführen der Skripte könnte aufgrund der Ausgabe im Terminal der Eindruck entstehen, dass ein Fehler vorliegt,
weil u.a. "warnings" und "errors" ausgegeben werden. Dies ist aber korrekt. Wird alles in den Kommentaren der oben
erwähnten Dateien erklärt! Die zu erwartenden Terminal-Ausgaben sind unten aufgeführt.

Darüber hinaus dauern die Skripte einen Moment. Einige ca. 20-30 Sekunden, abhängig von der Rechenleistung. Einfach warten
bis der Prompt wieder erscheint. 

Auf die parallele Version von elegant (=Pelegant) wird in den Beispielen nicht eingegangen. Es ist unter 
http://ikpweb.ikp.physik.tu-darmstadt.de/mediawiki/index.php/Elegant#Benutzung_von_Pelegant
erklärt. Ich habe die Erfahrung gemacht, dass es kaum einen Vorteil bringt. Zeitgewinn ist in der Regel maximal Faktor 2
(egal wie viele Prozessoren oder Threads), eventuell ist es bei mir aber auch nicht richtig kompiliert.
Der Nachteil von Pelegant ist, dass man keinerlei Infos über die Konvergenz bzw. die Konvergenzgeschwindigkeit erhält,
wenn man den Optimierungsalgorithmus nutzt.
Das Manual für Pelegant ist ebenfalls in dieser Beispielsammlung enthalten.

Im Ordner "Formelsammlung" sind ein paar Formeln aufgeführt, die beim Rechnen helfen können. Auch für die Definition des
Bunches über Twiss-Parameter kann sie hilfreich sein. Ferner finden sich dort Zitate aus dem elegant-Forum, wo es über
die Definition von R56 und damit im Zusammenhang stehende Größen geht.

Alle Dateien im Ordner sind mit ausführlichen Kommentaren versehen, um die Funktionsweisen zu verstehen.
Es empfiehlt sich folgende Reihenfolge:

0)  Sollte man Notepad++ verwenden, kann man über "Sprachen/Eigene Sprache definieren .../Importieren"
    die "elegant_sprache_notepad++.xml" importieren, was u.a. Kommentare farblich hervorhebt. Wem die Farben
    nicht zusagen, kann sie natürlich über "Sprachen/Eigene Sprache definieren .../" editieren.
   
1)  Gehe in den Ordner "1_Optimierung".
2)  Lies mit einem Texteditor die ASCII-Datei "s-dalinac.lte". Dort wird der Beschleuniger definiert.
    Hier findet sich nur ein kurzer Pseudo-Beschleuniger sowie die echte T-Rezirkulation des S-DALINAC.
	Für den vollständigen S-DALINAC siehe das IKP-Git:
    http://gitlab.ikp.physik.tu-darmstadt.de/users/sign_in
	und dort "/Strahldynamik-Simulationen/elegant/"
	Es sollte aus dem IKP-Netzwerk für jeden mit einem Linux-IKP-Account zugänglich sein.
	Falls nicht, in der Beschleuniger-Gruppe (Büro 101) nach Berechtigungen fragen.
3)  Lies mit einem Texteditor die ASCII-Datei "optimierung_aus_start.ele".
    Dort wird das Tracking definiert und der Optimierungsalgorithmus erklärt.
4)  Vergleiche die Unterschiede dieser Datei zu den Dateien "optimierung_an.ele" und "optimierung_aus_ende.ele".
    Es sind nur ein paar Zeilen auskommentiert bzw. getoggelt.
5)  Lies mit einem Texteditor die ASCII-Datei "normaler_run_grob_schwach.ele" und vergleiche mit den anderen "normaler_run_....ele"
    Es sind jeweils nur andere Beamlines aus dem Lattice "s-dalinac.lte" eingelesen.
6)  Lies mit einem Texteditor die ASCII-Datei "run1_plot_png.sh"
7)  Führe über "./run1_plot_png.sh" in der Konsole (ohne Anführungszeichen) das Skript aus.
8)  Überfliege mal schnell mit einem Texteditor die nach der Ausführung des Skripts erstellte
    Log-Datei "optimierung_aus_start.log". 
    Die Struktur ist: Lies alles ein, werte Reverse Polish Notations aus, platztiere temporär weitere
	Elemente im Lattice ("&insert_elements"), führe das eigentliche Tracking aus, speichere Ergebnisse in
	entsprechende Dateien.
9)  Überfliege mal schnell mit einem Texteditor die Log-Datei "optimierung_an.log".	
    Dort ist der Log des Optimierungsalgorithmus. Im Prinzip wird da Tracking nacheinander ausgeführt
	und die Ergebnisse jedes mal ausgegeben. Man findet Zwischenergebnisse wie:
		-->			equation evaluates to   6.138420713609010e+03
					Terms of equation: 
					10*(IP#1.Sx  1e-3 0.1e-3 segt ):   1.474491911117888e+03
					10*(IP#1.Sxp 1e-4 0.1e-4 segt ):   0.000000000000000e+00
					10*(IP#1.Sy  1e-3 0.1e-3 segt ):   7.045931271842454e+02
					10*(IP#1.Syp 1e-4 0.1e-4 segt ):   3.187487039537300e+03
					1*(M111#1.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#2.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#3.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#4.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#5.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#6.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#7.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#8.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#9.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#10.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#11.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#1.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#2.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#3.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#4.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#5.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#6.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#7.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#8.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#9.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#10.Sy 3e-3 0.1e-3 segt):   2.879202187792449e+02
					1*(M111#11.Sy 3e-3 0.1e-3 segt):   4.839284169903308e+02
					15*(IP#1.Particles 900 1 selt ):   0.000000000000000e+00
	Interessant ist der Zwischenwert der Zielfunktion "equation evaluates to".
	Am Ende des Optimierungsalgorithmus, also am Ende der Log-Datei, sollte der
	finale Wert der Zielfunktion idealerweise Null sein. Insbesondere wenn man mit
	"kleiner als", "größer als", "gleich wie" gearbeitet hat. Bei "maximiere" oder
	"minimiere" resultiert in der Regel keine Null.
	Tatsächlich ist in unserem Beispiel am Ende folgendes zu finden:
		-->			equation evaluates to   0.000000000000000e+00
					Terms of equation: 
					10*(IP#1.Sx  1e-3 0.1e-3 segt ):   0.000000000000000e+00
					10*(IP#1.Sxp 1e-4 0.1e-4 segt ):   0.000000000000000e+00
					10*(IP#1.Sy  1e-3 0.1e-3 segt ):   0.000000000000000e+00
					10*(IP#1.Syp 1e-4 0.1e-4 segt ):   0.000000000000000e+00
					1*(M111#1.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#2.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#3.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#4.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#5.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#6.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#7.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#8.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#9.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#10.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#11.Sx 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#1.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#2.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#3.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#4.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#5.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#6.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#7.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#8.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#9.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#10.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					1*(M111#11.Sy 3e-3 0.1e-3 segt):   0.000000000000000e+00
					15*(IP#1.Particles 900 1 selt ):   0.000000000000000e+00
					Dumping output beam data...done.
					Dumping centroid data...done.
					Dumping sigma data...done.
					Dumping final properties data...done.
					Post-tracking output completed.
					Completed post-tracking output
					Optimization results:
		-->			  optimization function has value 0
					Terms of equation: 
					IP#1.Sx  1e-3 0.1e-3 segt :   0.000000000000000e+00
					IP#1.Sxp 1e-4 0.1e-4 segt :   0.000000000000000e+00
					IP#1.Sy  1e-3 0.1e-3 segt :   0.000000000000000e+00
					IP#1.Syp 1e-4 0.1e-4 segt :   0.000000000000000e+00
					M111#1.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#2.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#3.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#4.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#5.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#6.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#7.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#8.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#9.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#10.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#11.Sx 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#1.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#2.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#3.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#4.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#5.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#6.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#7.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#8.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#9.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#10.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					M111#11.Sy 3e-3 0.1e-3 segt:   0.000000000000000e+00
					IP#1.Particles 900 1 selt :   0.000000000000000e+00
	Also "equation evaluates to   0.000000000000000e+00", d.h. es resultiert die gewünschte Null
	im letzten Schritt und dann erfolgt nochmal die Zusammenfassung: "optimization function has value 0".
	Ferner findet man ganz am Ende der Log-Datei:
					Optimum values of variables and changes from initial values:
		-->			 T1QU01.K1:  -1.959540068344301e+00    4.924022935125554e-01 (was  -2.451942361856856e+00) 
		-->			 T1QU02.K1:   2.424394216289607e+00   -7.240227479079464e-01 (was   3.148416964197553e+00) 
		-->			 T1QU03.K1:  -3.082285854405391e+00   -1.094772786437852e+00 (was  -1.987513067967539e+00) 
		-->			 T1QU04.K1:   4.463704000175681e-01   -8.790438715172959e-01 (was   1.325414271534864e+00) 
		-->			 T1QU05.K1:  -2.898546403425257e-01   -5.043427067013545e-01 (was   2.144880663588288e-01) 
		-->			 T1QU06.K1:   2.743134813266507e+00   -5.498391877934616e-01 (was   3.292974001059969e+00) 
		-->			 T1QU07.K1:  -1.802317913708511e+00   -2.804101057532744e-01 (was  -1.521907807955237e+00)
    Da steht also, wie die finalen Fokussierstärken der sieben Quadrupole sind, die variiert werden durften,
	um das optimale Ergebnis (klein(st)e Strahlausdehnung) zu erhalten.
	Da in der "optimierung_an.ele" die Option "&save_lattice filename=%s.new &end" gesetzt wurde,
	befinden sich die Ergebnisse bereits auf das Lattice angewendet in der Datei "optimierung_an.new",
	was eine Lattice-Datei ist (egal ob *.new oder *.lte).
10) Überfliege mal schnell mit einem Texteditor die Datei "optimierung_an.new".
    Es ist ein kompaktes Lattice. Alle Kommentare wurden gelöscht und alle Reverse Polish Notations
	und Variablen wurden ausgewertet und den Parametern direkt zugeschrieben.
11) Öffne die Datei "bildbetrachter.html" mit einem Browser und schau dir die Ergebnisse an.

Alternativ kann man auch direkt das Skript ausführen, sich "bildbetrachter.html" ansehen und dann hat man direkt die
Ergebnisse vor Augen, von denen in den Dateien gesprochen wird.

12) Lies mit einem Texteditor die ASCII-Datei "run2_plot_pop.sh"
13) Führe über "./run2_plot_pop-up.sh" in der Konsole (ohne Anführungszeichen) das Skript aus.
    Klicke auf der Tastatur N (next) oder P (previous) um durch die Seiten zu blättern.
14) Man sollte sich die erzeugten, binären Ausgabedateien mal ansehen: *.sig, *.cen, *.mag, *.mat, *.twi, *.bun, *.w1, *.out
    Um sich den Inhalt anzusehen benötigt man den SDDS-Editor (unter Linux der Befehl "jsddsEdit", unter Windows
    im Ordner "C:\Program Files (x86)\APS\SDDS Java\SDDSedit.jar" zu finden), den man im Rahmen der elegant-Installation
	mit installieren sollte, siehe die Installationsanleitungen unter
	http://ikpweb.ikp.physik.tu-darmstadt.de/mediawiki/index.php/Elegant
	Öffnet man die binären Ergebnisdateien mit einem Texteditor statt mit dem SDDS-Editor, sieht man zwar nicht den Inhalt,
	aber dafür einen Header-Bereich, in dem der Inhalt bzw. die dort genannten Parameter und Größen definiert sind!
	Öffnet man z.B. "optimierung_aus_start.sig" mit einem Texteditor, erhält man:
					SDDS1
					!# little-endian
					&description text="sigma matrix--input: optimierung_aus_start.ele  lattice: s-dalinac.lte", contents="sigma matrix", &end
					&parameter name=Step, description="Simulation step", type=long, &end
					&parameter name=SVNVersion, description="SVN version number", type=string, fixed_value=25318:25321M, &end
		-->			&column name=s, units=m, description=Distance, type=double,  &end
					&column name=ElementName, description="Element name", format_string=%10s, type=string,  &end
					&column name=ElementOccurence, description="Occurence of element", format_string=%6ld, type=long,  &end
					&column name=ElementType, description="Element-type name", format_string=%10s, type=string,  &end
					&column name=s1, symbol="$gs$r$b1$n", units=m, description="sqrt(<x*x>)", type=double,  &end
					&column name=s12, symbol="$gs$r$b12$n", units=m, description="<x*xp'>", type=double,  &end
					&column name=s13, symbol="$gs$r$b13$n", units="m$a2$n", description="<x*y>", type=double,  &end
					&column name=s14, symbol="$gs$r$b14$n", units=m, description="<x*y'>", type=double,  &end
					...
					...
					...
		-->			&column name=Sx, symbol="$gs$r$bx$n", units=m, description=sqrt(<(x-<x>)^2>), type=double,  &end
					&column name=Sxp, symbol="$gs$r$bx'$n", description=sqrt(<(x'-<x'>)^2>), type=double,  &end
					&column name=Sy, symbol="$gs$r$by$n", units=m, description=sqrt(<(y-<y>)^2>), type=double,  &end
					&column name=Syp, symbol="$gs$r$by'$n", description=sqrt(<(y'-<y'>)^2>), type=double,  &end
					&column name=Ss, symbol="$gs$r$bs$n", units=m, description=sqrt(<(s-<s>)^2>), type=double,  &end
					&column name=Sdelta, symbol="$gs$bd$n$r", description=sqrt(<(delta-<delta>)^2>), type=double,  &end
					&column name=St, symbol="$gs$r$bt$n", units=s, description=sqrt(<(t-<t>)^2>), type=double,  &end
					...
					...
					...
	Zum Beispiel: "s" ist die Distanz zum Urpsrung des gekrümmten Koordinatensystems in Meter. Wichtig: elegant rechnet nicht
	mit einem Sollteilchen, sondern ermittelt für alles die Strecken und lässt dann die Teilchen fliegen. Für jedes Teilchen
	wird dann die Zeit bemessen, die es auf seinem individuellen Orbit benötigt.
	Oder zum Beispiel: "Sx" (sigma_x) ist definiert als "sqrt(<(x-<x>)^2>)" mit <x>="Arithmetisches Mittel von x" und hat die Einheit Meter.
	Mit symbol="$gs$r$bx$n" ist die grafische Darstellung von "Sx" definiert, wichtig für den Plot. Details siehe SDDS Manual.
	Im Beispiel des Ordners "2_Variierung" wird erklärt, wie man die Ergebnisse in CSV-Dateien umwandeln kann und somit deutlich leichter
	zugänglichere ASCII-Dateien erhält, die sich auch angenehmer postprocessen lassen.

Danach entsprechend die Beispiele im Ordner "2_Variierung" durchgehen:

15) Gehe in den Ordner "2_Variierung".
16) Lies mit einem Texteditor die ASCII-Datei "test-lattice_fuer_variierung.lte". Dort wird der Beschleuniger definiert.
17) Lies mit einem Texteditor die ASCII-Datei "variierung1.ele". Dort wird das Parameter-Sweeping erklärt.
18) Vergleiche die Unterschiede dieser Datei mit der Datei "variierung2.ele". 
    Der Unterschied ist "101" vs. "10" und "element_divisions = 20" vs. "keine Option gesetzt"
19) Lies mit einem Texteditor die ASCII-Datei "run3_variierung1_und_2.sh"
20) Führe über "./run3_variierung1_und_2.sh" in der Konsole (ohne Anführungszeichen) das Skript aus.
21) Überfliege mal schnell mit einem Texteditor die Datei "variierung1.log".
    Es werden eben so viele Trackings durchgeführt, wie man im Parameter-Sweep angegeben hat.
22) Öffne die Datei "bildbetrachter.html" mit einem Browser und schau dir die Ergebnisse an.
23) Lies mit einem Texteditor die ASCII-Datei "run4_variierung1.sh"
24) Führe über "./run4_variierung1.sh" in der Konsole (ohne Anführungszeichen) das Skript aus.
    Klicke auf der Tastatur N (next) oder P (previous) um durch die Seiten zu blättern.
25) Lies mit einem Texteditor die ASCII-Datei "variierung3.ele". Dort wird weiteres Parameter-Sweeping erklärt.
26) Lies mit einem Texteditor die ASCII-Datei "run5_variierung3.sh". Dort wird u.a. der Export zu CSV-Dateien erklärt.
27) Führe über "./run5_variierung3.sh" in der Konsole (ohne Anführungszeichen) das Skript aus.
28) Sieh dir die erstellte CSV-Datei "variierung3.fin.collapse.csv" an.

Danach entsprechend die Beispiele im Ordner "3-externe_Bunch-Verteilung" durchgehen:

29) Gehe in den Ordner "3-externe_Bunch-Verteilung".
30) Lies mit einem Texteditor die ASCII-Datei "run6_umwandeln_zu_sdds.sh"
31) Führe über "./run6_umwandeln_zu_sdds.sh" in der Konsole (ohne Anführungszeichen) das Skript aus.
32) Öffne die erzeugten Bunch-Verteilungen im ASCII-Format sowohl mit einem Texteditor als auch mit dem SDDS-Editor.
33) Öffne die erzeugten Bunch-Verteilungen im Binärformat  sowohl mit einem Texteditor als auch mit dem SDDS-Editor.

Es gibt die Möglichkeit den Output von elegant für andere Tracking-Tools aufzubereiten, sodass er dort als Input
verwendet werden kann. Bzw. auch andersrum: Es gibt die Möglichkeit den Output von anderen Tracking-Tools für elegant
aufzubereiten, sodass er dort als Input verwendet werden kann.
Details dazu befinden sich im elegant Manual.
Für das Tracking-Tool ASTRA extieren z.B. die Befehle "elegant2astra" und "astra2elegant".



===============================================================================================================================
zu erwartende Terminal-Ausgaben:

1)
$ ./run1_plot_png.sh
1000
Die absolute Anzahl vorhandener Elektronen am Ende der Strahlführung ist:
1000
warning: existing file optimierung_aus_start.fin will be replaced (sddsprocess)
Die relative Anzahl vorhandener Elektronen am Ende der Strahlführung ist:
1.000000000000000e+00
error: divide-by-zero in fractional tolerance evaluation (simplexMinimization)
error: divide-by-zero in fractional tolerance evaluation (simplexMinimization)
error: divide-by-zero in fractional tolerance evaluation (simplexMin)
error: divide-by-zero in fractional tolerance evaluation (simplexMinimization)
error: divide-by-zero in fractional tolerance evaluation (simplexMin)
error: divide-by-zero in fractional tolerance evaluation (simplexMinimization)
error: divide-by-zero in fractional tolerance evaluation (simplexMin)
error: divide-by-zero in fractional tolerance evaluation (simplexMinimization)
error: divide-by-zero in fractional tolerance evaluation (simplexMin)
error: divide-by-zero in fractional tolerance evaluation (simplexMinimization)
error: divide-by-zero in fractional tolerance evaluation (simplexMin)
error: divide-by-zero in fractional tolerance evaluation (simplexMinimization)
error: divide-by-zero in fractional tolerance evaluation (simplexMin)
warning: existing file optimierung_aus_ende.sig will be replaced (sddsprocess)
warning: existing file optimierung_aus_ende.sig will be replaced (sddsprocess)
        1 Datei(en) kopiert.
warning: existing file optimierung_aus_ende.sig will be replaced (sddsprocess)
        1 Datei(en) kopiert.
warning: existing file optimierung_aus_ende.sig will be replaced (sddsprocess)
        1 Datei(en) kopiert.
warning: (s, Profile) does not appear in optimierung_aus_ende.sig
1 of 1 datanames absent from file optimierung_aus_ende.sig
warning: no datanames in request found for file optimierung_aus_ende.sig
warning: (s, Profile) does not appear in optimierung_aus_ende.sig
1 of 1 datanames absent from file optimierung_aus_ende.sig
warning: no datanames in request found for file optimierung_aus_ende.sig
warning: (s, xAperture) does not appear in optimierung_aus_ende.sig
1 of 1 datanames absent from file optimierung_aus_ende.sig
warning: no datanames in request found for file optimierung_aus_ende.sig
Warning: not all y quantities have the same units
warning: existing file optimierung_aus_ende.sig will be replaced (sddsprocess)
        1 Datei(en) kopiert.
warning: existing file optimierung_aus_ende.sig will be replaced (sddsprocess)
        1 Datei(en) kopiert.
warning: (s, Profile) does not appear in optimierung_aus_ende.sig
1 of 1 datanames absent from file optimierung_aus_ende.sig
warning: no datanames in request found for file optimierung_aus_ende.sig
warning: (s, xAperture) does not appear in optimierung_aus_ende.sig
1 of 1 datanames absent from file optimierung_aus_ende.sig
warning: no datanames in request found for file optimierung_aus_ende.sig
warning: existing file optimierung_aus_start.bun will be replaced (sddsprocess)
warning: existing file optimierung_aus_start.w1 will be replaced (sddsprocess)
warning: existing file optimierung_aus_start.out will be replaced (sddsprocess)

2)
$ ./run2_plot_pop-up.sh

3)
$ ./run3_variierung1_und_2.sh
warning: (s, Profile) does not appear in variierung1.cen
1 of 1 datanames absent from file variierung1.cen
warning: no datanames in request found for file variierung1.cen
warning: (s, Profile) does not appear in variierung2.cen
1 of 1 datanames absent from file variierung2.cen
warning: no datanames in request found for file variierung2.cen

4)
$ ./run4_variierung1.sh

5)
$ ./run5_variierung3.sh
warning: existing file variierung3.fin.collapse will be replaced (sddsprocess)

