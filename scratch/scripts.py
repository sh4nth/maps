import pandas as pd
import urllib, json
from concurrent.futures import ThreadPoolExecutor


allDistricts = {}
with open('List_of_Districts.txt') as f:
    for dist in f.read().splitlines():
        allDistricts[dist.split(',')[0]] = dist.replace('_', ' ')

allDistricts['Andamans'] = None
allDistricts['Nicobars'] = None
allDistricts['Lakshadweep'] = None
allDistricts['Lahul_and_Spiti'] = 'Lahul, Himachal Pradesh, India'
allDistricts['Leh_Ladakh'] = 'Leh 194101'
allDistricts['East_Godavari'] = 'Kakinada, Andhra Pradesh, India'
allDistricts['South_Garo_Hills'] = 'Chokpot, Meghalaya, India'
allDistricts['Mayurbhanj'] = 'Baripada, Odisha, India'
allDistricts['Kurung_Kumey'] = 'Aalo 791001'
allDistricts['Upper_Dibang_Valley'] = 'Anini 792101'
allDistricts['Upper_Siang'] = 'Yingkiong 791002'
allDistricts['Upper_Subansiri'] = 'Gengi 791125'
allDistricts['Karbi_Anglong'] = 'Diphu, Assam, India'

def getDirections(address, mode='transit', origin='New Delhi', log=False):
    apiKey = 'your apiKey from https://developers.google.com/maps/documentation/directions/ (Click get a Key)'
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+origin+'&key='+apiKey+'&destination=' + address + '&mode=' + mode
    
    ntries = 5
    response = None
    for _ in range(ntries):
        try:
            response = urllib.urlopen(url)
            break # success
        except IOError as err:
            pass
            # noOp
    else: # all ntries failed 
        raise err # re-raise the last timeout error
    
    data = json.loads(response.read())
    if log:
        print data
    time = data['routes']
    if len(time) != 0:
        time = time[0]['legs'][0]['duration']
        return time
    else:
        return None


mode = 'driving' #,'walking','transit'
executor = ThreadPoolExecutor(max_workers=10)

origins_done = ['Kolkata', 'Delhi', 'Mumbai', 'Bangalore', 'Chennai','Srinagar', 'Kohima', 'Nagpur', 'Gandhinagar']
origins = []

for origin_id in origins:
    times[origin_id] = {}
    origin = allDistricts[origin_id]
    for dest_id in allDistricts:
        dest = allDistricts[dest_id]
        if dest is None or origin is None:
            times[origin_id][dest_id] = None
        else:
            times[origin_id][dest_id] =  executor.submit(getDirections, dest, mode, origin=origin)

    for dest_id in allDistricts:
        if times[origin_id][dest_id] is not None:
            times[origin_id][dest_id] = times[origin_id][dest_id].result()
            if times[origin_id][dest_id] is not None:
                times[origin_id][dest_id] = times[origin_id][dest_id]['value']
            print '.',
        else:
            print 'o',origin_id,'->',dest_id, '(',allDistricts[origin_id],allDistricts[dest_id],')'

with open("/tmp/data.csv","w") as f:
    f.write('origin')
    for dest_id in sorted(allDistricts):
        f.write(',' + dest_id)
    f.write('\n')
    for origin_id in origins_done:
        f.write(origin_id)
        for dest_id in sorted(allDistricts):
            f.write(','+str(times[origin_id][dest_id]))
        f.write('\n')

