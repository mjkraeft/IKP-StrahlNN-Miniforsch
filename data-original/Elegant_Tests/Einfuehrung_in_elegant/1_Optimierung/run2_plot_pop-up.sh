#!/bin/sh  
# \
exec tclsh "$0" "$@"

# Dieses Skript basiert aus "tclsh", das andere auf "bash"

# ============================
# 2D-Plots von 6D-Verteilungen
# ============================

# elegant muss schon ausgeführt worden sein, d.h. die Dateien "optimierung_aus_start.bun", "optimierung_aus_start.w*****" und "optimierung_aus_start.out" müssen schon existieren!

# mit nachfolgendem kann man sich die 6D-Verteilung auf zwei Koordinaten projiziert angucken. Ausgabe in Pop-Up-Fenster. Unter Windows ist "OAG WIN32 Plotter" bzw. "Xming" nötig.
# Das Fragezeichen in ".w?" ist eine Wildcard für EINEN Charakter. Sollte die Laufzahl also mehr Stellen haben muss entsprechend geändert werden:
# .w1, .w2, .w3 => .w?
# .w01, .w02, .w03 => .w??
# die Option "-sep" sorgt dafür, dass die Plots nicht in bloß einen Graphen kommen, sondern in mehrere. Man kann mit der Tastatur über "N" (next) und "P" (previous) durchblättern. Lässt man "-sep" weg, so sind die ersten drei Phasenräume sichtlich überlagert, und der letzte sieht aus wie eine "zeitliche Fortpflanzung".
# mit "-sep"
eval exec sddsplot -column=x,y -graph=dot optimierung_aus_start.bun [glob -nocomplain optimierung_aus_start.w?] optimierung_aus_start.out -sep &
eval exec sddsplot -column=x,xp -graph=dot optimierung_aus_start.bun [glob -nocomplain optimierung_aus_start.w?] optimierung_aus_start.out -sep &
eval exec sddsplot -column=y,yp -graph=dot optimierung_aus_start.bun [glob -nocomplain optimierung_aus_start.w?] optimierung_aus_start.out -sep &
eval exec sddsplot -column=t,p -graph=dot optimierung_aus_start.bun [glob -nocomplain optimierung_aus_start.w?] optimierung_aus_start.out -sep &
# die nachfolgende Zeile funktioniert nur, weil im Skript "run1_plot_png.sh" mit sddsprocess die Spalte "pmevc" in *.bun, *.w1 und *.out erzeugt wurde!
eval exec sddsplot -column=t,pmevc -graph=dot optimierung_aus_start.bun [glob -nocomplain optimierung_aus_start.w?] optimierung_aus_start.out -sep &
# ohne "-sep"
eval exec sddsplot -column=t,p -graph=dot optimierung_aus_start.bun [glob -nocomplain optimierung_aus_start.w?] optimierung_aus_start.out &


# Der Vollständigkeit wegen hier einfach noch mal ein Plot "s vs Sx" im pop-up-Fenster statt in einer png-Datei
eval exec sddsplot -columnnames=s,Sx optimierung_aus_start.sig -graph=line,vary &
