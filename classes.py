from alg import *
from struct import unpack
from math import acos, atan2, pi


class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, offset_color):
        r = self.r + offset_color.r
        g = self.g + offset_color.g
        b = self.b + offset_color.b

        return color(r, g, b)

    def __mul__(self, other):
        r = self.r * other
        g = self.g * other
        b = self.b * other
        return color(r, g, b)

    def toBytes(self):
        self.r = int(max(min(self.r, 255), 0))
        self.g = int(max(min(self.g, 255), 0))
        self.b = int(max(min(self.b, 255), 0))
        return bytes([self.b, self.g, self.r])


class environment(object):
    def __init__(self, intensity=0, colorarg=color(255, 255, 255)):
        self.intensity = intensity
        self.currcolor = colorarg


class Light(object):
    def __init__(self, position=V3(0, 0, 0), intensity=1):
        self.position = position
        self.intensity = intensity


class Material(object):
    def __init__(self, diffuse=color(255, 255, 255), albedo=(1, 0, 0, 0), spec=0, refractive_index=1, active_texture=None):
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec
        self.refractive_index = refractive_index
        self.active_texture = active_texture


class Texture(object):
    def __init__(self, ifile):
        self.ifile = ifile
        self.load()

    def load(self):
        with open(self.ifile, 'rb') as inputfile:
            inputfile.seek(10)
            header_size = unpack('=l', inputfile.read(4))[0]

            inputfile.seek(14 + 4)
            self.width = unpack('=l', inputfile.read(4))[0]
            self.height = unpack('=l', inputfile.read(4))[0]
            inputfile.seek(header_size)

            self.frame = []

            for y in range(self.height):
                self.frame.append([])
                for x in range(self.width):
                    b = ord(inputfile.read(1)) / 255
                    g = ord(inputfile.read(1)) / 255
                    r = ord(inputfile.read(1)) / 255
                    self.frame[y].append(color(r, g, b))

    def currentcolor(self, texture_x, texture_y):
        if texture_x >= 0 and texture_x <= 1 and texture_y >= 0 and texture_y <= 1:
            x = int(texture_x * self.width - 1)
            y = int(texture_y * self.height - 1)

            return self.frame[y][x]
        else:
            return color(0, 0, 0)


class Intersect(object):
    def __init__(self, distance, point, normal, texture_pos=None):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texture_pos = texture_pos


class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = norm(normal)
        self.material = material

    def ray_intersect(self, origin, direction):
        d = dot(direction, self.normal)

        if abs(d) > 0.001:
            t = dot(self.normal, sub(self.position, origin)) / d
            if t > 0:
                hit = sum(origin, V3(direction.x * t,
                                     direction.y * t, direction.z * t))

                return Intersect(distance=t, point=hit, normal=self.normal)

        return None


class Cube(object):
    def __init__(self, position, planar_dist, material):
        self.position = position
        self.planar_dist = planar_dist
        self.material = material

        self.faces = [
            Plane(sum(position, V3((self.planar_dist / 2), 0, 0)),
                  V3(1, 0, 0), material),
            Plane(sum(position, V3(-(self.planar_dist / 2), 0, 0)),
                  V3(-1, 0, 0), material),
            Plane(sum(position, V3(0, (self.planar_dist / 2), 0)),
                  V3(0, 1, 0), material),
            Plane(sum(position, V3(0, -(self.planar_dist / 2), 0)),
                  V3(0, -1, 0), material),
            Plane(sum(position, V3(0, 0, (self.planar_dist / 2))),
                  V3(0, 0, 1), material),
            Plane(sum(position, V3(0, 0, -(self.planar_dist / 2))),
                  V3(0, 0, -1), material),
        ]

    def ray_intersect(self, origin, dir):
        bb1 = 0.001 + (self.planar_dist / 2)
        minx, miny, minz = (
            self.position.x - bb1), (self.position.y - bb1), (self.position.z - bb1)

        maxx, maxy, maxz = (
            self.position.x + bb1), (self.position.y + bb1), (self.position.z + bb1)

        t0 = float("inf")
        ints = None
        txt = None

        for face in self.faces:
            current_ints = face.ray_intersect(origin, dir)
            if current_ints is not None:
                pix, piy, piz = current_ints.point.x, current_ints.point.y, current_ints.point.z
                distance = current_ints.distance
                if (pix >= minx and pix <= maxx and piy >= miny and piy <= maxy and piz >= minz and piz <= maxz and distance < t0):
                    t0 = current_ints.distance
                    ints = current_ints

                    if abs(face.normal.z) > 0:
                        txt = [(pix - minx) / (maxx - minx),
                               (piy - miny) / (maxy - miny)]

                    elif abs(face.normal.y) > 0:
                        txt = [(pix - minx) / (maxx - minx),
                               (piz - minz) / (maxz - minz)]

                    elif abs(face.normal.x) > 0:
                        txt = [(piy - miny) / (maxy - miny),
                               (piz - minz) / (maxz - minz)]

        if ints is None:
            return None

        return Intersect(
            distance=ints.distance, point=ints.point, normal=ints.normal, texture_pos=txt
        )


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, origin, direction):
        L = sub(self.center, origin)
        tca = dot(L, direction)
        l = length(L)
        d2 = l ** 2 - tca ** 2
        if d2 > self.radius ** 2:
            return None
        thc = (self.radius ** 2 - d2) ** 1 / 2
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        hit = sum(origin, mul(direction, t0))
        normal = norm(sub(hit, self.center))

        return Intersect(distance=t0, point=hit, normal=normal)


class Triangle(object):
    def __init__(self, vertices, material):
        self.vertices = vertices
        self.material = material

    def ray_intersect(self, origin, direction):
        v0, v1, v2 = self.vertices
        normal = cross(sub(v1, v0), sub(v2, v0))
        determinant = dot(normal, direction)

        if abs(determinant) < 0.001:
            return None

        distance = dot(normal, v0)
        t = (dot(normal, origin) + distance) / determinant
        if t < 0:
            return None

        point = sum(origin, mul(direction, t))
        u, v, w = barycentric(v0, v1, v2, point)
        if w < 0 or v < 0 or u < 0:
            return None

        return Intersect(distance=distance, point=point, normal=norm(normal))


class textureprocessor(object):
    def __init__(self, infile):
        self.infile = infile
        self.load()

    def load(self):
        with open(self.infile, 'rb') as inputf:
            inputf.seek(10)
            headers = unpack('=l', inputf.read(4))[0]

            inputf.seek(14 + 4)
            self.width = unpack('=l', inputf.read(4))[0]
            self.height = unpack('=l', inputf.read(4))[0]
            inputf.seek(headers)

            self.frame = []
            for y in range(self.height):
                self.frame.append([])
                for x in range(self.width):
                    b = ord(inputf.read(1))
                    g = ord(inputf.read(1))
                    r = ord(inputf.read(1))
                    self.frame[y].append(color(r, g, b))

    def currentcolor(self, dir):
        dir = norm(dir)
        x = int((atan2(dir.z, dir.z) /
                 (2 * pi) + 0.5) * self.width)
        y = int(acos(-dir.y) / pi * self.height)

        if x < self.width and y < self.height:
            return self.frame[y][x]

        return color(0, 0, 0)


class Pyramid(object):
    def __init__(self, vertices, material):
        self.sides = self.generate_sides(vertices, material)
        self.material = material

    def generate_sides(self, vertices, material):
        if len(vertices) != 4:
            return [None, None, None, None]

        v0, v1, v2, v3 = vertices
        sides = [
            Triangle([v0, v3, v2], material),
            Triangle([v0, v1, v2], material),
            Triangle([v1, v3, v2], material),
            Triangle([v0, v1, v3], material),
        ]
        return sides

    def ray_intersect(self, origin, direction):
        t = float("inf")
        intersect = None

        for face in self.sides:
            local_intersect = face.ray_intersect(origin, direction)
            if local_intersect is not None:
                if local_intersect.distance < t:
                    t = local_intersect.distance
                    intersect = local_intersect

        return intersect
