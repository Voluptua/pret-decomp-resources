import os
import json

dir = os.getcwd()
for dname, dirs, files in os.walk(dir + "/data/maps"):
    for fname in files:
        if not fname.lower() == 'map.json':
            continue
        fpath = os.path.join(dname, fname)
        with open(fpath) as f:
            data = json.load(f)
            data.pop('object_events', None)
            data.pop('coord_events', None)
            data.pop('bg_events', None)
        s = json.dumps(data, indent=2)
        with open(fpath, "w") as f:
            f.write(s+'\n')
        print('Stripped ' + fpath.replace(dir, ''))
print('Done.')
