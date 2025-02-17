import os, sys
import requests
# Lock file to tell conky that the script is running
lock_file = "/tmp/script_eq.lock"
try:
    # Check for file lock
    open(lock_file, 'w').close()
    #   number of rows
    rows = 30
    ################################ get your HOME name automatically
    homepath = os.environ['HOME']
    homename = homepath
    homename = homename[6:]
    ###################################                  website url
    url = "https://www.seismicportal.eu/fdsnws/event/1/query?callback=angular.callbacks._0&format=jsonp&limit=" + str(rows) + "&offset=1&orderby=time"
    res = requests.get(url)
    data = res
    ###################################                  file paths
    home = '/home/'
    conkypath = "/.conky/"
    filepathtxt = home + homename + conkypath + 'earthquakes/eq.txt'
    #filepathjson = '/home/hiro/.conky/earthquakes/eq.json'
    filepathconky = home + homename + conkypath + 'earthquakes/eqconky.txt'
    filepathconkyfin = home + homename + conkypath + 'earthquakes/eqconkyfin.txt'
    ###################################                  get the HTML page source code in a txt file named eq.txt
    with open(filepathtxt, 'w') as f:
        f.write(data.text)
    # first get all lines from file
    with open(filepathtxt, 'r') as f:
        lines = f.readlines()
    # # remove spaces
    # lines = [line.replace(' ', '') for line in lines]
    # remove comma
    lines = [line.replace(',', '') for line in lines]
    # remove quotes
    lines = [line.replace('"', '') for line in lines]
    # finally, write lines in the file
    with open(filepathtxt, 'w') as f:
        f.writelines(lines)
    ###################################                  write conky statements
    #   mag color
    maggreen = '${color6}'
    magorange = '${color3}'
    magred = '${color4}'
    j = 24
    delta = 0
    time = 600
    with open(filepathconky, 'w') as fo:
        for i in range(0, rows):
            temp = j + delta - 1
            #   select mag color
            fomag = open(filepathtxt, 'r')
            eqtxt = fomag.readlines()
            string = (eqtxt[temp - 1])
            rest, n = string.rsplit(':', 1)
            value = float(n)
            fomag.close()
            if (value >= 0 and value < 4):
                row1_1 = maggreen + "${execpi " + str(time) + " sed -n '" + str(temp + 1) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c14-16} "
                row1_2 = maggreen + "${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c10-12}${color}"
            elif (value >= 4 and value < 6):
                row1_1 = magorange + "${execpi " + str(time) + " sed -n '" + str(temp + 1) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c14-16} "
                row1_2 = magorange + "${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c10-12}${color}"
            elif (value >= 6):
                row1_1 = magred + "${execpi " + str(time) + " sed -n '" + str(temp + 1) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c14-16} "
                row1_2 = magred + "${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c10-12}${color}"
            fo.write('{}\n'.format(row1_1))
            fo.write('{}\n'.format(row1_2))
            #   end mag color
            temp = j + delta - 8
            row1_3 = "${GOTO 50}${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c11-20}"
            fo.write('{}\n'.format(row1_3))
            temp = j + delta - 6
            row1_4 = "${GOTO 120}${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c10-14}"
            fo.write('{}\n'.format(row1_4))
            temp = j + delta - 5
            row1_5 = "${GOTO 160}${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c10-14}"
            fo.write('{}\n'.format(row1_5))
            temp = j + delta - 4
            row1_6 = "${GOTO 210}${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c12-16}"
            fo.write('{}\n'.format(row1_6))
            temp = j + delta - 2 
            row1_7 = "${GOTO 265}${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c11-16}"
            fo.write('{}\n'.format(row1_7))
            temp = j + delta - 7
            row1_8 = "${GOTO 310}${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eq.txt | cut -c19-50}"
            fo.write('{}\n'.format(row1_8))
            delta = delta + 26
    ###################################                  write conky final statements to copy in conky file
    last = rows * 8 + 1
    with open(filepathconkyfin, 'w') as fo:
        for i in range(1, last):
            temp = i
            rowconky = "${execpi " + str(time) + " sed -n '" + str(temp) + "p' $HOME" + conkypath + "earthquakes/eqconky.txt}"
            fo.write('{}\n'.format(rowconky))
except Exception as e:
    # Manage exceptions (optional)
    filelockerror = (f"Error during script execution: {e}")
finally:
    # remove lock file
    try:
        os.remove(lock_file)
    except FileNotFoundError:
        pass  # file already removed