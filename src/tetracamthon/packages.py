import math


class Package(object):
    """Define various package types.
    p250sq = Package(250, 'Square', 43, 41.5, 126.8, 5, 185)
    p100b = Package(100, 'Base', 47, 32, 69.3, 4, 113.33)
    p125s = Package(100, 'Slim', 47, 32, 86, 4, 130.00)
    p1000b = Package(1000, 'Base', 94, 63, 166, 5, 245.00)
    p1000sq = Package(1000, 'Square', 72, 71, 198, 5, 285.00)
    print(p1000b)
    print(p125s.get_pulling_velocity(cycle_time=0.9))
        # 411.1111111111111
    p330sq = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
    print(p330sq)
    print(p330sq.get_pulling_velocity(cycle_time=0.9))
        # 422.22222222222223
    print(p330sq.get_x_when_touching_tube())
        # 24.25
    p200m = Package(200, "Mini", 53, 38, 106, 6, 160)
    print(p200m)
    print(p200sq.get_pulling_velocity(cycle_time=0.9))
        # Package of 250 of shape Square
        # Width: 43
        # Depth: 41.5
        # Height: 126.8
        # Tube diameter: 53.79
        # Horizental Sealing: 16
    """

    def __init__(self, volumn, shape, width, depth, height,
                 ls_overlap, web_repeated_length, top_slim=1):
        self.volumn = volumn
        self.shape = shape
        self.width = width
        self.depth = depth
        self.height = height
        self.ls_overlap = ls_overlap
        self.slim = top_slim
        self.web_repeated_length = web_repeated_length
        self.web_width = 2 * (self.width + self.depth) + self.ls_overlap
        self.hs_sealing_length = self.web_repeated_length - \
                                 (self.height + self.depth)
        self.hs_sealing_width = (self.web_width - self.ls_overlap) / 2
        self.tube_diameter = round(
            (self.web_width - self.ls_overlap) / math.pi, 2)

    def __str__(self):
        return ("Package of " + str(self.volumn) +
                " of shape " + self.shape + "\n" +
                "Width: " + str(self.width) + "\n" +
                "Depth: " + str(self.depth) + "\n" +
                "Height: " + str(self.height) + "\n" +
                "Tube diameter: " + str(self.tube_diameter) + "\n" +
                "Horizental Sealing length and width: " +
                str(round(self.hs_sealing_length, 2)) + ' and ' +
                str(self.hs_sealing_width))

    def get_pulling_velocity(self, cycle_time=0.9):
        return -self.web_repeated_length / cycle_time * 2

    def get_x_when_touching_tube(self):
        return self.depth / 2.0

    def get_hs_sealing_length(self):
        return self.hs_sealing_length

    def get_height(self):
        return self.height

if __name__ == "__main__":
    pass
