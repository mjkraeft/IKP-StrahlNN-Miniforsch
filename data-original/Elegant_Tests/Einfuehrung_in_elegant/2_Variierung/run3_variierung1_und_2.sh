#!/bin/bash

# Dieses Skript basiert aus "bash"

# elegant ausführen
elegant variierung1.ele > variierung1.log

# Arbeitet man mit "&vary_element" erhält man als Ergebnis SDDS-Dateien mit mehreren Seiten.
# Um die Ergebnisse besser zu verarbeiten, gibt es den Befehl "sddscollapse".
# Damit werden von alle Parametern aller Seiten Spalten erzeugt und das Ergebnis pro Seite wird zu einer Zeile umgewandelt.
# Es entspricht quasi einer Transponierung:
# m Seiten, n Parameter, 1 Wert pro Parameter
# =>
# 1 Seite, n Spalten, m Zeilen
# So sind alle Ergebnisse übersichtlich auf einer SDDS-Seite und lassen sich leider postprocessen.
# Das ganze klappt nur für Paramater (1 x 1), nicht für Spalten (m x 1).
sddscollapse variierung1.fin variierung1.fin.collapse

# jetzt lassen sich die Ergebnis-Parameter in abhängigkeit der variierten Parameter plotten:
sddsplot variierung1.fin.collapse -columnnames=MAL.DX,Cx -device=png -output=DX_vs_Cx.png
# geplottet wird also die Abweichung des Schwerpunkts der x-Koordinate vom Sollorbit am Ende der Strahlführung (Daten aus *.fin) in Abhängigkeit des variierten Parameters DX des Elements MAL (also der Variation des Schwerpunkts der x-Koordinate an der Stelle des Elements MAL (=am Anfang der Strahlführung)).

# auch eine gewollte überlagerung von plots ist möglich.
# wie gesagt bleiben ergebnisse die vorher schon spalten waren, "spalten auf verschiedenen seiten" und lassen sich nicht per "sddscollapse" transponieren.
# ein überlagert plot, bei dem jede Seite geplottet wird ("-split=pages") sieht z.B. wie folgt aus:
sddsplot variierung1.cen -columnnames=s,Cx -split=pages -graph=line,vary -columnNames=s,Profile variierung1.mag -overlay=yfactor=0.05,xmode=norm -device=png -output=s_vs_Cx_vs_iteration_101.png
# geplottet wird also die Abweichung des Schwerpunkts der x-Koordinate vom Sollorbit am Ende der Strahlführung (Daten aus *.fin) in Abhängigkeit des variierten Parameters DX des Elements MAL (also der Variation des Schwerpunkts der x-Koordinate an der Stelle des Elements MAL (=am Anfang der Strahlführung)) entlang der Strahlführung. Auf diese Weise werden die Trajektorieren des Schwerpunkts sichtbar!

# Die Datei "variierung1.fin.collapse" kann auch zur Orientierung genutzt werden:
# Die (nicht mit "sddscollapse" erzeugten) Ergebnis-Dateien besitzten nur Seiten.
# Es ist unklar, welche Seite zu welchem Parameter-Set gehören.
# Die Zeilen in der Datei "variierung1.fin.collapse" entsprechen den Seitenzahlen.
# Über die entsprechende Zeile lässt sich also in den Spalten der Parameter (MAL.DX, MAL.DY, etc.) ermitteln, welches Parameter-Set zu den Ergebnissen geführt hat.
# Vergleiche auch die Spalte "PageNumber"

# Und nochmal mit nur 10 statt 101 Problemstellungen:

elegant variierung2.ele > variierung2.log
sddscollapse variierung2.fin variierung2.fin.collapse
sddsplot variierung2.cen -columnnames=s,Cx -split=pages -graph=line,vary -columnNames=s,Profile variierung2.mag -overlay=yfactor=0.05,xmode=norm -device=png -output=s_vs_Cx_vs_iteration_10.png