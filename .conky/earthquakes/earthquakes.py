import os
import requests

# Set how many earthquakes you want to see in the list (e.g. 10, 15, 20...)
rows = 30 
homepath = os.environ['HOME']
filepathconky = os.path.join(homepath, '.conky/earthquakes/eqconky.txt')
filepath_tmp = filepathconky + '.tmp'

url = f"https://www.seismicportal.eu/fdsnws/event/1/query?format=json&limit={rows}&orderby=time"

try:
    res = requests.get(url)
    data = res.json()
    events = data.get('features', [])
    
    output_lines = []
    
    for event in events:
        props = event.get('properties', {})
        
        try:
            value = float(props.get('mag', 0.0))
        except:
            value = 0.0
        magtype = props.get('magtype', 'ML').lower() # minuscolo come l'originale
        
        # Color selection based on magnitude
        if value < 4.0:
            color_tag = '${color6}'   # Verde
        elif value < 6.0:
            color_tag = '${color3}'   # Arancione
        else:
            color_tag = '${color4}'   # Rosso
            
        # Time (HH:MM:SS). If you prefer the date (YYYY-MM-DD) change [11:19] to [0:10]
        time_iso = props.get('time', '')
        eq_time = time_iso[11:19] if len(time_iso) > 19 else "00:00:00"
        
        lat = f"{float(props.get('lat', 0.0)):.2f}"
        lon = f"{float(props.get('lon', 0.0)):.2f}"
        depth = f"{float(props.get('depth', 0.0)):.1f}"
        auth = props.get('auth', 'UNK')
        region = props.get('flynn_region', 'Unknown Region').upper() # Maiuscolo come l'originale
        
        # THE KEY TO THE SOLUTION: Everything concatenated into a single string/line
        single_line = f"{color_tag}{magtype} {value:.1f}${{color}} ${{GOTO 50}}{eq_time} ${{GOTO 120}}{lat} ${{GOTO 160}}{lon} ${{GOTO 210}}{depth} ${{GOTO 265}}{auth} ${{GOTO 310}}{region}"
        output_lines.append(single_line)
        
    # Writing to file
    with open(filepath_tmp, 'w') as fo:
        for line in output_lines:
            fo.write(f"{line}\n")
            
    os.replace(filepath_tmp, filepathconky)

except Exception as e:
    with open(filepathconky, 'w') as fo:
        fo.write(f"${{color4}}Error: {e}${{color}}\n")