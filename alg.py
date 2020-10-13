class V3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def sum(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)


def sub(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
    return V3(v0.x * k, v0.y * k, v0.z * k)


def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z


def length(v0):
    return (v0.x ** 2 + v0.y ** 2 + v0.z ** 2) ** 0.5


def norm(v0):
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x / v0length, v0.y / v0length, v0.z / v0length)


def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]

    xs.sort()
    ys.sort()

    xmin = xs[0]
    xmax = xs[-1]
    ymin = ys[0]
    ymax = ys[-1]

    return xmin, xmax, ymin, ymax


def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y, v1.z * v2.x -
        v1.x * v2.z, v1.x * v2.y - v1.y * v2.x,
    )


def barycentric(A, B, C, P):
    res = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y),
    )
    cx, cy, cz = res.x, res.y, res.z

    if abs(cz) < 1:
        return -1, -1, -1

    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz

    return w, v, u


def reflect(I, N):
    Lm = mul(I, -1)
    n = mul(N, 2 * dot(Lm, N))
    return norm(sub(Lm, n))


def refract(I, N, refractive_index):  # Implementation of Snell's law
    cosi = -max(-1, min(1, dot(I, N)))
    etai = 1
    etat = refractive_index

    if cosi < 0:  # if the ray is inside the object, swap the indices and invert the normal to get the correct result
        cosi = -cosi
        etai, etat = etat, etai
        N = mul(N, -1)

    eta = etai/etat
    k = 1 - eta**2 * (1 - cosi**2)
    if k < 0:
        return V3(1, 0, 0)

    return norm(sum(
        mul(I, eta),
        mul(N, (eta * cosi - k**(1/2)))
    ))
