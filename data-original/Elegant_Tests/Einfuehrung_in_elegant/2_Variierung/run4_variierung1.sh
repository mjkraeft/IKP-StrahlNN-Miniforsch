#!/bin/sh  
# \
exec tclsh "$0" "$@"

# Dieses Skript basiert aus "tclsh"

# Durch die Option "-sep" kann jede Seite einzeln geplottet werden.
# Man kann mit der Tastatur über "N" (next) und "P" (previous) durchblättern.
eval exec sddsplot variierung1.cen -columnnames=s,Cx -split=pages -graph=line,vary -sep
