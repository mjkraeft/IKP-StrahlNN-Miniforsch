#!/bin/bash

# elegant ausführen
elegant variierung3.ele > variierung3.log

# Arbeitet man mit "&vary_element" erhält man als Ergebnis SDDS-Dateien mit mehreren Seiten.
# Um die Ergebnisse besser zu verarbeiten, gibt es den Befehl "sddscollapse".
# Damit werden von alle Parametern aller Seiten Spalten erzeugt und das Ergebnis pro Seite wird zu einer Zeile umgewandelt.
# Es entspricht quasi einer Transponierung:
# m Seiten, n Parameter, 1 Wert pro Parameter
# =>
# 1 Seite, n Spalten, m Zeilen
# So sind alle Ergebnisse übersichtlich auf einer SDDS-Seite und lassen sich leider postprocessen.
# Das ganze klappt nur für Paramater (1 x 1), nicht für Spalten (m x 1).
sddscollapse variierung3.fin variierung3.fin.collapse

# Da wir am Impuls in MeV/c interessiert sind, erzeugen wir zunächst die entsprechende Zeile:
sddsprocess variierung3.fin.collapse -define=column,pmevc,"pCentral 0.51099895 *",units=MeV_per_c variierung3.fin.collapse

# zum postprocessen exportieren wir die Daten in eine CSV Datei:
sdds2plaindata variierung3.fin.collapse variierung3.fin.collapse.csv -outputMode=ascii -separator='\,' -noRowCount -column=MAL.DX -column=MAL.DY -column=CAVITY1.VOLT -column=DIPOL1.ANGLE -column=pmevc
# leider werden keine Spalten-Namen in die CSV-Datei mitgeschrieben. Dies sollte man manuel nachholen, damit man die Daten zuordnen kann. Hier bequemlichkeitshalber in die letzte Zeile:
echo "MAL.DX in m,MAL.DY in m,CAVITY1.VOLT in eV,DIPOL1.ANGLE in rad,finaler Schwerpunktsimpuls in MeV/c" >> variierung3.fin.collapse.csv