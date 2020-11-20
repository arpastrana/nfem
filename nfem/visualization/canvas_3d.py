import json
import numpy as np
import html
import os
from IPython.display import display, HTML


class Canvas3D:
    def __init__(self, height=600):
        self.data = dict()
        self.data['height'] = height
        self.data['frame'] = 0
        self.data['frames'] = []

    def next_frame(self):
        self.data['frames'].append({"items": []})

    @property
    def frame(self):
        return self.data['frame']

    @frame.setter
    def frame(self, value):
        self.data['frame'] = value

    def line(self, a, b, color='red', layer=0):
        items = self.data['frames'][-1]['items']

        a = np.asarray(a)
        b = np.asarray(b)

        items.append({
            "type": "line",
            "points": [
                {"x": float(a[0]), "y": float(a[1]), "z": float(a[2])},
                {"x": float(b[0]), "y": float(b[1]), "z": float(b[2])},
            ],
            "color": color,
            "layer": layer,
        })

    def polyline(self, points, color='red', layer=0):
        items = self.data['frames'][-1]['items']

        points = np.asarray(points)

        items.append({
            "type": "line",
            "points": [{"x": point[0], "y": point[1], "z": point[2]} for point in points],
            "color": color,
            "layer": layer,
        })

    def point(self, location, color='red', layer=0):
        items = self.data['frames'][-1]['items']

        location = np.asarray(location)

        items.append({
            "type": "point",
            "location": {"x": float(location[0]), "y": float(location[1]), "z": float(location[2])},
            "color": color,
            "layer": layer,
        })

    def arrow(self, location, direction, color='red', layer=0):
        items = self.data['frames'][-1]['items']

        location = np.asarray(location)
        direction = np.asarray(direction)

        items.append({
            "type": "arrow",
            "location": {"x": float(location[0]), "y": float(location[1]), "z": float(location[2])},
            "direction": {"x": float(direction[0]), "y": float(direction[1]), "z": float(direction[2])},
            "color": color,
            "layer": layer,
        })

    def text(self, text, location, color='red', layer=0):
        items = self.data['frames'][-1]['items']

        location = np.asarray(location)

        items.append({
            "type": "text",
            "text": text,
            "location": {"x": float(location[0]), "y": float(location[1]), "z": float(location[2])},
            "color": color,
            "layer": layer,
        })

    def support(self, direction, location, color='red', layer=0):
        items = self.data['frames'][-1]['items']

        location = np.asarray(location)

        items.append({
            "type": "support",
            "direction": direction,
            "location": {"x": float(location[0]), "y": float(location[1]), "z": float(location[2])},
            "color": color,
            "layer": layer,
        })

    def _embed_js(self, template, filename):
        path = os.path.join(os.path.dirname(__file__), 'html', 'js', filename)
        with open(path, 'r', encoding='UTF-8') as file:
            content = file.read()
            template = template.replace(f'<script type="text/javascript" src="js/{filename}"></script>', f'<script type="text/javascript">{content}</script>')
        return template

    def show(self, height):
        template_path = os.path.join(os.path.dirname(__file__), 'html', 'canvas_3d.html')
        with open(template_path, 'r', encoding='UTF-8') as file:
            template = file.read()

        template = self._embed_js(template, 'three.min.js')
        template = self._embed_js(template, 'OrbitControls.js')
        template = self._embed_js(template, 'd3.min.js')
        template = self._embed_js(template, 'guify.min.js')
        template = self._embed_js(template, 'screenfull.min.js')

        content = template.replace("{} /* [data] */", json.dumps(self.data))
        element = HTML(f'<iframe seamless frameborder="0" allowfullscreen width="100%" height="{height}" srcdoc="{html.escape(content)}"></iframe>')
        display(element)