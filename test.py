import difflib
import sys
import os
import re

#busqueda de la vacante que se de como parametro
if len(sys.argv) > 1:
    id_vac = int(sys.argv[1])
    curl = "curl \'https://empleosti.com.mx/api/v2/applicants?token=RfUXApjKLI&vacancy_id=" + str(id_vac)
    os.system(curl + "&favorites=false\' > aplicantes.html")
    os.system(curl + "&favorites=true\' > favoritos.html")

#lectura de favoritos
file = open('favoritos.html', 'r')
linea = file.read()
favorites = re.split('\"updated_at\":\"\d+-\d+-\d+ \d+:\d+:\d+\"},.', linea)
#\d+-\d+-\d+ \d+:\d+:\d+
#[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:
#file.close()
#lectura de aplicantes
file = open('aplicantes.html', 'r')
linea = file.read()
applicants = re.split('\"updated_at\":\"\d+-\d+-\d+ \d+:\d+:\d+\"},.', linea)
#file.close()

matches = []

print '\n\nAnalizando, espere por favor...'

for app in applicants:
    dif = difflib.SequenceMatcher(lambda x: x == " ", app, favorites[0])
    best_match = dif.ratio()
    for fav in favorites:
        if len(app) < len(fav):
            if (len(app)/len(fav))>.55:
                dif = difflib.SequenceMatcher(lambda x: x == " ", app, fav)
            else:
                continue
        else:   
            dif = difflib.SequenceMatcher(lambda x: x == " ", fav, app)     
        if best_match < dif.ratio():
            best_match = dif.ratio()
    p = app.find(',')
    matches.append((best_match, app[0:p]))

#se tienen que ordenar los aplicantes con respecto a los matches
matches.sort()
matches.reverse()
print 'Coincidencias'
for match in matches:
    print match