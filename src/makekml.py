#!/usr/bin/python
import numpy as np
class kmlclass:
    def __init__(self):
      return

    def begin(self, fname, name, desc, width):
      self.f = open (fname, 'w')
      self.f.write ('<?xml version="1.0" encoding="UTF-8"?>\n')
      self.f.write ('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
      self.f.write ('<Document>\n')
      self.f.write ('<name>%s</name>\n' % (name))
      self.f.write ('<description>%s</description>\n' % (desc))

      self.f.write ('<Style id="red">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff0000ff</color>\n')      
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="green">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff00ff00</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="blue">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ffff0000</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="cyan">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ffffff00</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="yellow">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff00ffff</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="grey">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff888888</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="orange">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff00a5ff</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="purple">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ffal20f0</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="green_poly">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff00aa00</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('  <PolyStyle>\n')
      self.f.write ('    <color>2000cc00</color>\n')
      self.f.write ('  </PolyStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="yellow_poly">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff0000ff</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('  <PolyStyle>\n')
      self.f.write ('    <color>2000ffff</color>\n')
      self.f.write ('  </PolyStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="red_poly">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff0000ff</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('  <PolyStyle>\n')
      self.f.write ('    <color>120000ff</color>\n')
      self.f.write ('  </PolyStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="orange_poly">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ff00a5ff</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('  <PolyStyle>\n')
      self.f.write ('    <color>1200a5ff</color>\n')
      self.f.write ('  </PolyStyle>\n')
      self.f.write ('</Style>\n')

      self.f.write ('<Style id="purple_poly">\n')
      self.f.write ('  <LineStyle>\n')
      self.f.write ('    <color>ffa020f0</color>\n')
      self.f.write ('    <width>%.1f</width>\n' % (width))
      self.f.write ('  </LineStyle>\n')
      self.f.write ('  <PolyStyle>\n')
      self.f.write ('    <color>10a020f0</color>\n')
      self.f.write ('  </PolyStyle>\n')
      self.f.write ('</Style>\n')


    def trksegbegin(self, name, desc, color, altitude):
      self.f.write ('<Placemark>\n')
      self.f.write ('<name>%s</name>\n' % (name))
      self.f.write ('<description>%s</description>\n' % (desc))
      self.f.write ('<styleUrl>#%s</styleUrl>\n' % (color))
      self.f.write ('<LineString>\n')
      if altitude == 'absolute': 
        self.f.write ('<altitudeMode>absolute</altitudeMode>\n')
      elif altitude == 'relativeToGround': 
        self.f.write ('<altitudeMode>relativeToGround</altitudeMode>\n')
      self.f.write ('<coordinates>\n')

    def trksegend(self):
      self.f.write ('</coordinates>\n')
      self.f.write ('</LineString>\n')
      self.f.write ('</Placemark>\n')

    def polybegin(self, name, desc, color, altitude):
      self.f.write ('<Placemark>\n')
      self.f.write ('<name>%s</name>\n' % (name))
      self.f.write ('<description>%s</description>\n' % (desc))
      self.f.write ('<styleUrl>#%s</styleUrl>\n' % (color))
      self.f.write ('<Polygon>\n')
      self.f.write ('<tessellate>1</tessellate>\n')
      self.f.write ('<outerBoundaryIs>\n')
      self.f.write ('<LinearRing>\n')
      if altitude == 'absolute': 
        self.f.write ('<altitudeMode>absolute</altitudeMode>\n')
      elif altitude == 'relativeToGround': 
        self.f.write ('<altitudeMode>relativeToGround</altitudeMode>\n')
      self.f.write ('<coordinates>\n')
  
    def polyend(self):
      self.f.write ('</coordinates>\n')
      self.f.write ('</LinearRing>\n')
      self.f.write ('</outerBoundaryIs>\n')
      self.f.write ('</Polygon>\n')
      self.f.write ('</Placemark>\n')

    def pt(self, lat, lon, ele):
      self.f.write ('%012.8f,%011.8f,%.1f\n' % (lon, lat, ele))

    #New function added to get the tracking of the drone 
    def getPoints(self,lat,lon):
        for i in range(len(lat)):
            self.f.write ('%012.8f,%011.8f,%.1f\n' % (lon[i], lat[i], 0)) #2D plot so height is zero

    def end(self):
      self.f.write ('</Document>\n')
      self.f.write ('</kml>')
      self.f.close ()
      return
        
if __name__ == "__main__":
  print ('Creating kml file')
  kml = kmlclass()

  data = []  

  lines = [line.rstrip() for line in open("../output/gps_pos.txt")] 
  for i in range(len(lines)): # for all lines
    if len(lines[i]) > 0 and lines[i][0] != '#': # if not a comment or empty line
      csv = np.asarray(lines[i].split (' ')) # split into comma separated list
      csv = csv[[22,24,25,26,27,29,30,31]]
      csv[1] = csv[1].split('\'')[0]
      csv[5] = csv[5].split('\'')[0]
      csv[2] = csv[2].split('"')[0]
      csv[6] = csv[6].split('"')[0]
      latitude = float(csv[0]) + (float(csv[1])/60.0) + (float(csv[2])/3600.0)
      if csv[3] == 'S':
        latitude *= -1.0
      longitude = float(csv[4]) + (float(csv[5])/60.0) + (float(csv[6])/3600.0)
      if csv[7] == 'W':
        longitude *= -1.0
      data.append([latitude,longitude])

  data = np.asarray(data)

  minElement = np.argmin(data,0)
  maxElement = np.argmax(data,0)
  print(minElement)
  print(maxElement)

  print(data[minElement[0],0],data[minElement[1],1])
  print(data[maxElement[0],0],data[minElement[1],1])
  print(data[maxElement[0],0],data[maxElement[1],1])
  print(data[minElement[0],0],data[maxElement[1],1])

  kml.begin('../output/flight_path.kml', 'Example', 'Example on the use of kmlclass', 0.7)
  kml.trksegbegin ('', '', 'red', 'absolute') 
  kml.getPoints(data[:,0],data[:,1])
  kml.trksegend()
  kml.end()
