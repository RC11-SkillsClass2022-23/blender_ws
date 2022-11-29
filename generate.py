import bpy
import math
import re
import os.path
f = open("C:\\Users\\joris\\OneDrive\\Documenten\\bartlett_blender_ws\\5\\data.txt","r")


#COORDINATEN CODE
class TransverseMercator:
    radius = 6378137

    def __init__(self, **kwargs):
        # setting default values
        self.lat = 0 # in degrees
        self.lon = 0 # in degrees
        self.k = 1 # scale factor
        
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        self.latInRadians = math.radians(self.lat)

    def fromGeographic(self, lat, lon):
        lat = math.radians(lat)
        lon = math.radians(lon-self.lon)
        B = math.sin(lon) * math.cos(lat)
        x = 0.5 * self.k * self.radius * math.log((1+B)/(1-B))
        y = self.k * self.radius * ( math.atan(math.tan(lat)/math.cos(lon)) - self.latInRadians )
        return (x,y)

    def toGeographic(self, x, y):
        x = x/(self.k * self.radius)
        y = y/(self.k * self.radius)
        D = y + self.latInRadians
        lon = math.atan(math.sinh(x)/math.cos(D))
        lat = math.asin(math.sin(D)/math.cosh(x))

        lon = self.lon + math.degrees(lon)
        lat = math.degrees(lat)
        return (lat, lon)

C = bpy.context
D = bpy.data
scene = bpy.context.scene

#COORDINATEN FORMAT
projection = TransverseMercator(lat=scene["lat"], lon=scene["lon"])

def dms2dd(degrees, minutes, seconds):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60*100);
    return dd;


def parse_dms(dms):
    parts = re.split('[^\d\w]+', dms)
    lat = dms2dd(parts[0], parts[2], parts[4])

    return (lat)

#KLEUR CREATIE
def makeMaterial(name, diffuse, specular, alpha):

    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (0.37,0.15,0.02,0.8)
    return mat

def setMaterial(ob, mat):

    me = ob.data
    me.materials.append(mat)


#OBJECT CREATIE


for i in range(1361,1399):
    loc = "C:\\Users\\joris\\OneDrive\\Documenten\\bartlett_blender_ws\\5\\IMAG"
    loc += str(i)
    loc += ".jpg"
    if os.path.isfile(loc) :
        
        # converting from the geographical coordinates to the Blender global coordinate system:
        (x, y) = projection.fromGeographic(parse_dms(f.readline()), parse_dms(f.readline()))
        
        #install the inmages as plane addon
        plane = bpy.ops.import_image.to_plane(shader='SHADELESS', files=[{'name':loc}])
        ob = bpy.context.object
        ob.rotation_euler[0] = math.radians(90)
        ob.rotation_euler[1] = math.radians(90)
        ob.location = ( x/100, y/100, 15 )
        ob.scale = (10,10,10)
        
        red = makeMaterial("Red",(1,0,0),(1,1,1),1)
        #bpy.ops.mesh.primitive_uv_sphere_add(location=(x,y,35))
        #bpy.ops.transform.translate(value=(1,0,0))
        # setMaterial(bpy.context.object, red)


f.close



#grab kmz files from google maps
#https://timeline.google.com/maps/timeline?pli=1&rapt=AEjHL4NHQpAaBgAWkKBmnCYJyTIFvJ21kMxKvD39Rdhx_fQqORz_GUCQfrF1MTN6DDv2QsKzvi1dTGL8zk3vhDiQkyMbJL-bBw&pb=!1m2!1m1!1s2021-05-23
#right click gear icon, export kmz
#kmz to gpx
#https://kml2gpx.com/
#load in with bledner_osm