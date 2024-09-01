import urllib.request
from control.models import Satellite

tle_resource_id = "https://celestrak.org/NORAD/elements/gp.php?CATNR={id}&FORMAT=tle"
tle_resource_group = "https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"

f = urllib.request.urlopen(tle_resource_id.format(id = 25544))
page = f.read()
lines = page.decode().split("\r\n")
# print(lines)

obj = Satellite(catNo = lines[2].split(" ")[2],
                name = lines[0].strip(),
                tle1 = lines[1],
                tle2 = lines[2])
obj.save()

print(obj)