@echo off
CLS
:: Replace line breaks with spaces inside double quotes using mlr
:: https://miller.readthedocs.io/en/latest/
:: Rename original file
ren Wrecks_and_Obstructions_in_AWOIS.csv Wrecks_and_Obstructions_in_AWOIS_original.csv
:: Clean line breaks and save to original filename
mlr --csv -N clean-whitespace Wrecks_and_Obstructions_in_AWOIS_original.csv > Wrecks_and_Obstructions_in_AWOIS.csv