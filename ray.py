from datamodifiers import *
from classes import *
from alg import *
from math import tan, pi


class Raytracer(object):
    def __init__(self, width, height, camera, background, light, environment, background_color):
        self.width = width
        self.height = height
        self.camera = camera
        self.scene = []
        self.background = background
        self.light = light
        self.environment = environment
        self.background_color = background_color
        self.setframe()

    def setframe(self):
        self.frame = [
            [self.background_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def cast_ray(self, orig, direction, recursion=0):
        material, intersect = self.scene_intersect(orig, direction)

        # break recursion of reflections after n iterations
        if material is None or recursion >= 3:
            if self.background:
                return self.background.currentcolor(direction)
            return self.background_color

        light_dir = norm(sub(self.light.position, intersect.point))
        light_distance = length(sub(self.light.position, intersect.point))

        if self.environment:
            ambient_color = self.environment.currcolor * self.environment.intensity
        else:
            ambient_color = self.background_color

        offset_normal = mul(intersect.normal, 1.1)
        shadow_orig = (
            sub(intersect.point, offset_normal)
            if dot(light_dir, intersect.normal) < 0
            else sum(intersect.point, offset_normal)
        )
        shadow_material, shadow_intersect = self.scene_intersect(
            shadow_orig, light_dir)
        shadow_intensity = 0

        if (
            shadow_material
            and length(sub(shadow_intersect.point, shadow_orig)) < light_distance
        ):
            shadow_intensity = 0.9

        intensity = (
            self.light.intensity
            * max(0, dot(light_dir, intersect.normal))
            * (1 - shadow_intensity)
        )

        reflection = reflect(light_dir, intersect.normal)
        specular_intensity = self.light.intensity * (
            max(0, -dot(reflection, direction)) ** material.spec
        )

        if material.albedo[2] > 0:
            reverse_direction = mul(direction, -1)
            reflect_dir = reflect(reverse_direction, intersect.normal)
            reflect_orig = (
                sub(intersect.point, offset_normal)
                if dot(reflect_dir, intersect.normal) < 0
                else sum(intersect.point, offset_normal)
            )
            reflect_color = self.cast_ray(
                reflect_orig, reflect_dir, recursion + 1)
        else:
            reflect_color = self.background_color

        if material.albedo[3] > 0:
            refract_dir = refract(
                direction, intersect.normal, material.refractive_index
            )
            refract_orig = (
                sub(intersect.point, offset_normal)
                if dot(refract_dir, intersect.normal) < 0
                else sum(intersect.point, offset_normal)
            )
            refract_color = self.cast_ray(
                refract_orig, refract_dir, recursion + 1)
        else:
            refract_color = self.background_color

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * \
            specular_intensity * material.albedo[1]
        reflection = reflect_color * material.albedo[2]
        refraction = refract_color * material.albedo[3]

        if material.active_texture and intersect.texture_pos is not None:
            text_color = material.active_texture.currentcolor(
                intersect.texture_pos[0], intersect.texture_pos[1])
            diffuse = text_color * 255

        return ambient_color + diffuse + specular + reflection + refraction

    def scene_intersect(self, orig, direction):
        zbuffer = float("inf")

        material = None
        intersect = None

        for obj in self.scene:
            hit = obj.ray_intersect(orig, direction)
            if hit is not None:
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = obj.material
                    intersect = hit

        return material, intersect

    def render(self, ofile):
        print("Rendering...")
        fov = int(pi / 2)
        for y in range(self.height):
            for x in range(self.width):
                i = (
                    (2 * (x + 0.5) / self.width - 1)
                    * tan(fov / 2)
                    * self.width
                    / self.height
                )
                j = (2 * (y + 0.5) / self.height - 1) * tan(fov / 2)
                direction = norm(V3(i, j, -1))
                self.frame[y][x] = self.cast_ray(self.camera, direction)

        writebmp(ofile, self.width, self.height, self.frame)
