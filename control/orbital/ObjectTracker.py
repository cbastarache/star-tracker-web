import orekit
vm = orekit.initVM()

from orekit.pyhelpers import setup_orekit_curdir, absolutedate_to_datetime
from pathlib import Path

d = Path(__file__).parent / "orekit-data.zip"
setup_orekit_curdir(str(d))

from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.time import TimeScalesFactory, AbsoluteDate
from org.orekit.utils import IERSConventions, Constants

from org.orekit.propagation.analytical.tle import TLE, TLEPropagator

from math import radians, pi
import matplotlib.pyplot as plt

from datetime import datetime, timezone

class ObjectTracker:

    def __init__(self, lat, lon, alt, latency):
        #iss by default
        tle_line1 = "1 25544U 98067A   24240.52549514  .00031224  00000+0  54981-3 0  9998"
        tle_line2 = "2 25544  51.6410 321.8942 0005709 275.6085 165.4630 15.50147074469617"

        self.latency = latency

        ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        self.earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, 
                                Constants.WGS84_EARTH_FLATTENING, 
                                ITRF)
        
        self.init(lat, lon, alt)
        self.setTLE(tle_line1, tle_line2)

    def init(self, lat, lon, alt):
        self.latitude = lat
        self.longitude= lon
        self.altitude  = alt

        self.station = GeodeticPoint(self.latitude, self.longitude, self.altitude)
        self.station_frame = TopocentricFrame(self.earth, self.station, "Esrange")

        self.inertialFrame = FramesFactory.getEME2000()
        
    def setTLE(self, tle1, tle2):
        self.tle_line1 = tle1
        self.tle_line2 = tle2
        self.mytle = TLE(self.tle_line1, self.tle_line2)
        self.propagator = TLEPropagator.selectExtrapolator(self.mytle)
        self.pv = self.propagator.getPvProvider()


    def getPrediction(self):
        el=[]
        az=[]
        pos=[]
        time=[]

        dt = datetime.now(timezone.utc)
        extrapDate = AbsoluteDate(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0.0, TimeScalesFactory.getUTC())
        finalDate = extrapDate.shiftedBy(60.0*60*24) #seconds

        while (extrapDate.compareTo(finalDate) <= 0.0):  
            pv = self.propagator.getPvProvider().getPVCoordinates(extrapDate, self.inertialFrame)
            pos_tmp = pv.getPosition()
            pos.append((pos_tmp.getX(),pos_tmp.getY(),pos_tmp.getZ()))
            
            el_tmp = self.station_frame.getElevation(pv.getPosition(),
                            self.inertialFrame,
                            extrapDate)*180.0/pi
            az_tmp = self.station_frame.getAzimuth(pv.getPosition(),
                            self.inertialFrame,
                            extrapDate)*180.0/pi
            el.append(el_tmp)
            az.append(az_tmp)
            time.append(extrapDate)
            extrapDate = extrapDate.shiftedBy(10.0)
        return {"el": el,"az": az, "timestamp": time}
    
    def nextVisible(self):
        data = self.getPrediction()
        for i in range(len(data["el"])):
            if data["el"][i] > 10.0:
                return {"el": data["el"][i],"az": data["az"][i], "timestamp": data["timestamp"][i]}

    def getPos(self, pollTime):
        dt = datetime.now(timezone.utc)
        extrapDate = AbsoluteDate(dt.year, dt.month, dt.day, dt.hour, dt.minute, float(dt.second) + (dt.microsecond / 1000000), TimeScalesFactory.getUTC())
        extrapDate = extrapDate.shiftedBy(self.latency)
        
        pv_now = self._pos(extrapDate)
        extrapDate = extrapDate.shiftedBy(pollTime)
        pv_next = self._pos(extrapDate)

        return { "now": pv_now, "next": pv_next }

    def _pos(self, t):
        pv = self.pv.getPVCoordinates(t, self.inertialFrame)
        el = self.station_frame.getElevation(pv.getPosition(),
                        self.inertialFrame,
                        t)*180.0/pi
        az = self.station_frame.getAzimuth(pv.getPosition(),
                        self.inertialFrame,
                        t)*180.0/pi
        return { "el": el, "az": az }



if __name__ == "__main__":

    latitude = radians(43.227246) 
    longitude= radians(-79.851980)
    altitude  = 205.0
    latency = 6.0

    "AAUSAT-II"               
    tle1 = "1 32788U 08021F   24243.18838656  .00043348  00000+0  18643-2 0  9994"
    tle2 = "2 32788  97.5978 223.8950 0001016 210.3762 149.7415 15.22504497889660"
    tr = ObjectTracker(latitude, longitude, altitude, latency)
    tr.setTLE(tle1,tle2)
    print(tr.getPos(1.0))
    
    next = tr.nextVisible()
    ad = absolutedate_to_datetime(next["timestamp"])
    ad = ad.replace(tzinfo=timezone.utc)
    print(ad.astimezone())

    prediction = tr.getPrediction()
    plt.plot(prediction["el"])
    plt.ylim(-90,90)
    plt.title('Elevation')
    plt.grid(True)

    # plt.plot(az)
    # plt.ylim(0,360)
    # plt.title('Azimuth')
    # plt.grid(True)

    plt.show()