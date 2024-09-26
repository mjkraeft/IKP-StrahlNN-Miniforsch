#!/bin/bash

# Dieses Skript basiert aus "bash", das andere auf "tclsh"

# =========================================================================================
# Erstmal eine Einführung in die wichtigsten Befehle, weiter unten dann weiteres relevantes
# =========================================================================================

# das nachfolgende führt elegant aus und schreibt die Ausgabe nicht in die Konsole, sondern in eine Log-Datei.
# Der Optimierungsalgorithmus gibt eine Meldung aus, wenn er (in einem Teilschritt) terminiert.
# Diese Meldung beginnt mit "error: divide-by-zero in fractional tolerance evaluation".
# Dies ist ein gutes Zeichen und keine Fehlermeldung. Die Ausgabe dieser Meldungen erfolgt trotzdem im Terminal, auch wenn man die Ausgabe alles übrigen in eine Datei weitergeleitet hat.
elegant optimierung_aus_start.ele > optimierung_aus_start.log # exportiere Ausgabe von elegant in eine Log-Datei, um keine Konsolenausgabe zu erhalten. Ist man an dem Log nicht interessiert, kann man ihn auch einfach nach "/dev/null" pipen: "elegant optimierung_aus_start.ele > /dev/null". Da wir im Rahmen dieses Beispiels aber explizit in die Log-Dateien reinschauen wollen, sollen sie explizit erstellt werden.

# Ausgabe der Größe "Sx" entlang der Strahlführung "s"
sddsplot -columnnames=s,Sx optimierung_aus_start.sig -graph=line,vary -device=png -output=sigmaX_test.png

# Ausgabe der Größen "Sx" und "Sy" entlang der Strahlführung "s" zusammen in einem Plot
sddsplot -columnnames=s,'(Sx,Sy)' optimierung_aus_start.sig -graph=line,vary -device=png -output=sigmaX_und_sigmaY_test.png

# Ausgabe einzelner Parameter in eine Textdatei. Hier: Absolute Anzahl vorhandener Elektronen am Ende der Strahlführung
sddsprintout optimierung_aus_start.fin -parameter=Particles finale_absolute_teilchenzahl.txt

# Ausgabe einzelner Parameter in die Konsole. Hier: Absolute Anzahl vorhandener Elektronen am Ende der Strahlführung
sdds2stream optimierung_aus_start.fin -parameter=Particles

# Ausgabe einzelner Parameter in die Konsole. Hier: optisch schöner mit Shell-Befehl "echo"
echo "Die absolute Anzahl vorhandener Elektronen am Ende der Strahlführung ist:"
sdds2stream optimierung_aus_start.fin -parameter=Particles

# Erzeugen neuer Parameter oder Spalten in SDDS-Dateien ist mit "sddsprocess" möglich. Hier: Angabe der relativen Anzahl vorhandener Elektronen am Ende der Strahlführung (durch Rechnen mit der Reverse Polish Notation, Angenommen die Anzahl vorhandener Elektronen am Anfang der Strahlführung sei 1000).
sddsprocess optimierung_aus_start.fin -define=parameter,relativeParticles,"Particles 1000 /",units=1
# Es wird eine Meldung in der Konsole ausgegeben, dass die Datei "optimierung_aus_start.fin" überschrieben wird. Diese Meldung kommt, weil kein output angegeben wurde und dann output=input ist. Man kann Warnungen mit der Option "-noWarnings" unterdrücken:
# sddsprocess optimierung_aus_start.fin -define=parameter,relativeParticles,"Particles 1000 /",units=1 -noWarnings
echo "Die relative Anzahl vorhandener Elektronen am Ende der Strahlführung ist:"
sdds2stream optimierung_aus_start.fin -parameter=relativeParticles


# mit dem nachfolgenden kann man die 6D-Verteilung auf zwei Koordinaten projiziert angucken. Ausgabe in png-Datei:
sddsplot -column=x,y  -graph=dot optimierung_aus_start.bun -device=png -output=x_vs_y_test.png


# ===============================================================================================================================================================================================================================
# Ausgabe weiterer relevanter Größen (y,xp,yp, etc.) sowie Skalierung von m auf mm. Modifizierung von Achsen. Plotten des Lattices, etc. folgt nun bei der Ausführung des Optimierungsalgorithmus ("elegant optimierung_an.ele"):
# ===============================================================================================================================================================================================================================

# Nun wird jenes elegant-File ausgeführt, bei dem die entscheidende Zeile bzgl. des Optimierungsalgorithmus (Zeile mit "&optimize &end") nicht auskommentiert ist. Der Optimierungsprozess dauert bei mir ca. 20 Sekunden. Auch die Zeile mit "&alter_elements" wurde getoggelt, damit nicht sinnlos die Festplatte zugemüllt wird. Toggelt man nicht, hat die Datei "optimierung_an.w1" am Ende 37 MB. Man kann also sagen: Pro Watch-Element werden ca. 2 MB pro Sekunde auf die Festplatte geschrieben. Bei einem Optimierungsprozess, der Stunden laufen kann und eine zweistellige Zahl an Watch-Elementen hat, ist die Festplatte voll.
elegant optimierung_an.ele > optimierung_an.log

# Pro Durchlauf entsteht ein verbessertes Lattice, mit dem Namen "optimierung_an.new". Dieses wird pro Schritt überschrieben. Zum Schluss bleibt also nur das finale, optimale Lattice.
# Nachfolgend wird elegant noch mal ausgeführt, ohne Optimierung, dafür auf diesem finalen Lattice (Option "lattice=optimierung_an.new").
elegant optimierung_aus_ende.ele > optimierung_aus_ende.log

# Und nachfolgend wird viel geplottet. Über die Datei "bildbetrachter.html" kann man die Ergebnisse leicht vergleichen.
# v1
sddsplot -columnnames=s,Sx  optimierung_aus_start.sig -graph=line,vary -device=png -output=sigmaX_v1.png
sddsplot -columnnames=s,Sy  optimierung_aus_start.sig -graph=line,vary -device=png -output=sigmaY_v1.png
sddsplot -columnnames=s,Sxp optimierung_aus_start.sig -graph=line,vary -device=png -output=sigmaXp_v1.png
sddsplot -columnnames=s,Syp optimierung_aus_start.sig -graph=line,vary -device=png -output=sigmaYp_v1.png
# v2
sddsplot -columnnames=s,Sx  optimierung_aus_ende.sig -graph=line,vary -device=png -output=sigmaX_v2.png
sddsplot -columnnames=s,Sy  optimierung_aus_ende.sig -graph=line,vary -device=png -output=sigmaY_v2.png
sddsplot -columnnames=s,Sxp optimierung_aus_ende.sig -graph=line,vary -device=png -output=sigmaXp_v2.png
sddsplot -columnnames=s,Syp optimierung_aus_ende.sig -graph=line,vary -device=png -output=sigmaYp_v2.png
# v3
sddsplot -columnnames=s,Sx  optimierung_aus_start.sig optimierung_aus_ende.sig -graph=line,vary -legend -device=png -output=sigmaX_v3.png
sddsplot -columnnames=s,Sy  optimierung_aus_start.sig optimierung_aus_ende.sig -graph=line,vary -legend -device=png -output=sigmaY_v3.png
sddsplot -columnnames=s,Sxp optimierung_aus_start.sig optimierung_aus_ende.sig -graph=line,vary -legend -device=png -output=sigmaXp_v3.png
sddsplot -columnnames=s,Syp optimierung_aus_start.sig optimierung_aus_ende.sig -graph=line,vary -legend -device=png -output=sigmaYp_v3.png
# v4
sddsplot -columnnames=s,'(Sx,Sy)'   optimierung_aus_ende.sig -graph=line,vary -legend -device=png -output=sigmaXY_v4.png
sddsplot -columnnames=s,'(Sxp,Syp)' optimierung_aus_ende.sig -graph=line,vary -legend -device=png -output=sigmaXpYp_v4.png
# v5
sddsplot optimierung_aus_ende.sig -columnNames=s,'(Sx,Sy)' -graph=line,vary -legend -yScalesGroup=id=XY -columnNames=s,'(Sxp,Syp)' -graph=line,vary -legend -yScalesGroup=id=XpYp -device=png -output=sigmaXYXpYp_v5.png
# v6
sddsprocess optimierung_aus_ende.sig -define=column,Sx_in_mm,"Sx 1000 *",units=mm optimierung_aus_ende.sig
sddsprocess optimierung_aus_ende.sig -define=column,Sy_in_mm,"Sy 1000 *",units=mm optimierung_aus_ende.sig
sddsprocess optimierung_aus_ende.sig -define=column,Sxp_in_mrad,"Sxp 1000 *",units=mrad optimierung_aus_ende.sig
sddsprocess optimierung_aus_ende.sig -define=column,Syp_in_mrad,"Syp 1000 *",units=mrad optimierung_aus_ende.sig
sddsplot optimierung_aus_ende.sig -columnNames=s,'(Sx_in_mm,Sy_in_mm)' -ylabel='$gs$r$bx$n\,$gs$r$by$n' -graph=line,vary -legend -yScalesGroup=id=XY -columnNames=s,'(Sxp_in_mrad,Syp_in_mrad)' -ylabel='$gs$r$bdx/ds$n\,$gs$r$bdy/ds$n' -graph=line,vary -legend -yScalesGroup=id=XpYp -device=png -output=sigmaXYXpYp_v6.png
# v7
sddsplot optimierung_aus_ende.sig -columnNames=s,'(Sx_in_mm,Sy_in_mm)' -ylabel='$gs$r$bx$n\,$gs$r$by$n' -graph=line,vary -legend -yScalesGroup=id=XY -columnNames=s,'(Sxp_in_mrad,Syp_in_mrad)' -ylabel='$gs$r$bdx/ds$n\,$gs$r$bdy/ds$n' -graph=line,vary -legend -yScalesGroup=id=XpYp -columnNames=s,Profile optimierung_aus_ende.mag -overlay=yfactor=0.05,xmode=norm -device=png -output=sigmaXYXpYp_v7.png
# v8
sddsplot optimierung_aus_ende.sig -columnNames=s,'(Sx,Sy)' -graph=line,vary -legend -columnNames=s,Profile optimierung_aus_ende.mag -overlay=yfactor=0.05,xmode=norm -columnNames=s,xAperture optimierung_aus_ende.twi -device=png -output=sigmaXY_v8.png
# v9
sddsprocess optimierung_aus_ende.sig -define=column,Sx_mal_3,"Sx 3 *",units=m optimierung_aus_ende.sig
sddsprocess optimierung_aus_ende.sig -define=column,Sy_mal_3,"Sy 3 *",units=m optimierung_aus_ende.sig
sddsplot optimierung_aus_ende.sig -columnNames=s,'(Sx_mal_3,Sy_mal_3)' -ylabel='3$gs$r$bx$n\,3$gs$r$by$n' -graph=line,vary -legend -columnNames=s,Profile optimierung_aus_ende.mag -overlay=yfactor=0.05,xmode=norm -columnNames=s,xAperture optimierung_aus_ende.twi -device=png -output=sigmaXY_v9.png



# =============================================
# Plot der 2D-Projektionen der 6D-Verteilungen:
# =============================================

# Startverteilung
sddsplot -column=x,y     -graph=dot optimierung_aus_start.bun -device=png -output=x_vs_y_v1.png
sddsplot -column=x,xp    -graph=dot optimierung_aus_start.bun -device=png -output=x_vs_xp_v1.png
sddsplot -column=y,yp    -graph=dot optimierung_aus_start.bun -device=png -output=y_vs_yp_v1.png
sddsplot -column=t,p     -graph=dot optimierung_aus_start.bun -device=png -output=t_vs_p_v1.png
sddsprocess optimierung_aus_start.bun -define=column,pmevc,"p 0.51099895 *",units=MeV_per_c
sddsplot -column=t,pmevc -graph=dot optimierung_aus_start.bun -device=png -output=t_vs_pmevc_v1.png
# An der Stelle des watch-Elements
sddsplot -column=x,y  -graph=dot optimierung_aus_start.w1 -device=png -output=x_vs_y_v2.png
sddsplot -column=x,xp -graph=dot optimierung_aus_start.w1 -device=png -output=x_vs_xp_v2.png
sddsplot -column=y,yp -graph=dot optimierung_aus_start.w1 -device=png -output=y_vs_yp_v2.png
sddsplot -column=t,p  -graph=dot optimierung_aus_start.w1 -device=png -output=t_vs_p_v2.png
sddsprocess optimierung_aus_start.w1 -define=column,pmevc,"p 0.51099895 *",units=MeV_per_c
sddsplot -column=t,pmevc -graph=dot optimierung_aus_start.w1 -device=png -output=t_vs_pmevc_v2.png
# finale Verteilung
sddsplot -column=x,y  -graph=dot optimierung_aus_start.out -device=png -output=x_vs_y_v3.png
sddsplot -column=x,xp -graph=dot optimierung_aus_start.out -device=png -output=x_vs_xp_v3.png
sddsplot -column=y,yp -graph=dot optimierung_aus_start.out -device=png -output=y_vs_yp_v3.png
sddsplot -column=t,p  -graph=dot optimierung_aus_start.out -device=png -output=t_vs_p_v3.png
sddsprocess optimierung_aus_start.out -define=column,pmevc,"p 0.51099895 *",units=MeV_per_c
sddsplot -column=t,pmevc -graph=dot optimierung_aus_start.out -device=png -output=t_vs_pmevc_v3.png




# ======================================
# Erzeugung von groben und glatten Plots
# ======================================

# Die Ergebnisse sind in "bildbetrachter.html" ganz unten zu sehen. Dort findet sich auch die Bedeutung zu den Plots. 
elegant normaler_run_grob_schwach.ele > normaler_run_grob_schwach.log
elegant normaler_run_glatt_schwach.ele > normaler_run_glatt_schwach.log
elegant normaler_run_grob_mittel.ele > normaler_run_grob_stark.log
elegant normaler_run_glatt_mittel.ele > normaler_run_glatt_stark.log
elegant normaler_run_grob_stark.ele > normaler_run_grob_stark.log
elegant normaler_run_glatt_stark.ele > normaler_run_glatt_stark.log

sddsplot -columnnames=s,Sx  normaler_run_grob_schwach.sig  normaler_run_glatt_schwach.sig  -graph=line,vary -legend -columnNames=s,Profile normaler_run_grob_schwach.mag  -overlay=yfactor=0.05,xmode=norm -device=png -output=sigmaX_grob_vs_glatt_schwach.png
sddsplot -columnnames=s,Sx  normaler_run_grob_mittel.sig   normaler_run_glatt_mittel.sig   -graph=line,vary -legend -columnNames=s,Profile normaler_run_grob_mittel.mag   -overlay=yfactor=0.05,xmode=norm -device=png -output=sigmaX_grob_vs_glatt_mittel.png
sddsplot -columnnames=s,Sx  normaler_run_grob_stark.sig    normaler_run_glatt_stark.sig    -graph=line,vary -legend -columnNames=s,Profile normaler_run_grob_stark.mag    -overlay=yfactor=0.05,xmode=norm -device=png -output=sigmaX_grob_vs_glatt_stark.png

