import numpy
import requests
from PIL import Image
from io import BytesIO

layouts = "https://mintercat.com/generator/"


class Cat:
    def __init__(self, config):
        self.eyes = config['eyes']
        self.bg1 = config['bg1']
        self.bg2 = config['bg2']
        self.bg2color = hex_to_rgb(config['bg2color'])
        self.circuit = config['circuit']
        self.spot = config['spot']
        self.spotcolor = hex_to_rgb(config['spotcolor'])
        self.create_cat()

    def get_cat(self):
        return self.cat

    def create_cat(self):
        cat = Image.alpha_composite(self.get_eyes(), self.get_bg1())
        cat = Image.alpha_composite(cat, self.get_bg2())
        cat = Image.alpha_composite(cat, self.get_circuit())
        cat = Image.alpha_composite(cat, self.get_spot())
        self.cat = cat

    def change_color(self, img, from_color, to_color):
        img = img.convert("RGBA")
        arr = numpy.array(img)
        arr[..., :-1][from_color.T] = to_color
        return Image.fromarray(arr)

    def get_eyes(self):
        response = requests.get(layouts + "eyes/" + str(self.eyes) + ".webp")
        img = Image.open(BytesIO(response.content))
        return img

    def get_bg1(self):
        response = requests.get(layouts + "bg1/" + str(self.bg1) + ".webp")
        img = Image.open(BytesIO(response.content))
        return img

    def get_bg2(self):
        response = requests.get(layouts + "bg2/" + str(self.bg2) + ".webp")
        img = Image.open(BytesIO(response.content))
        red, green, blue, alpha = numpy.array(img).T
        default_color = (red != 255) & (green != 255) & (blue != 255)
        img = self.change_color(img, default_color, self.bg2color)
        return img

    def get_circuit(self):
        response = requests.get(layouts + "circuit/" + str(self.circuit) + ".webp")
        img = Image.open(BytesIO(response.content))
        return img

    def get_spot(self):
        response = requests.get(layouts + "spot/" + str(self.spot) + ".webp")
        img = Image.open(BytesIO(response.content))
        red, green, blue, alpha = numpy.array(img).T
        default_color = (red != 255) & (green > 250) & (blue != 255)
        img = self.change_color(img, default_color, self.spotcolor)
        return img
    

def hex_to_rgb(hex):
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return rgb
    

def test_cat():
    out_path = "C:\\Users\\"
    test_config = {
        "eyes": 1,
        "bg1": 1,
        "bg2": 1,
        "bg2color": "8240FF",
        "circuit": 1,
        "spot": 1,
        "spotcolor": "FFFF00"
    }

    random_cat = Cat(test_config)
    out = random_cat.get_cat()
    out.save(out_path + "out.png", "png")
    out.save(out_path + "out.webp", "webp")

test_cat()