# Copyright (C) 2016 Simon Biggs
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# http://www.gnu.org/licenses/.

"""Electron insert REST API tornado server."""


import numpy as np
import json

import tornado.escape
import tornado.ioloop
import tornado.web


from electroninserts import (
    parameterise_insert_with_visual_alignment, create_transformed_mesh)


class Parameterise(tornado.web.RequestHandler):
    """REST API for parametering inserts."""

    def post(self):
        """REST API for parametering inserts."""
        # origin = self.request.headers['Origin']
        # allow_origins = np.array([
        #     'http://localhost:8080', 'http://localhost:3000',
        #     'http://localhost:8889', 'http://electrons.simonbiggs.net'])
        # if np.any(origin == allow_origins):
        #     self.set_header('Access-Control-Allow-Origin', origin)

        coordinates = json.loads(self.get_argument('body'))
        x = coordinates['x']
        y = coordinates['y']

        (
            width, length, circle_centre, x_shift, y_shift, rotation_angle
        ) = parameterise_insert_with_visual_alignment(x, y)

        respond = {
            'width': np.round(width, decimals=2),
            'length': np.round(length, decimals=2),
            'circle_centre': np.round(circle_centre, decimals=2).tolist(),
            'x_shift': np.round(x_shift, decimals=2),
            'y_shift': np.round(y_shift, decimals=2),
            'rotation_angle': np.round(rotation_angle, decimals=4)
        }

        self.write(respond)


class Model(tornado.web.RequestHandler):
    """REST API for modelling inserts."""

    def post(self):
        """REST API for modelling inserts."""
        # origin = self.request.headers['Origin']
        # allow_origins = np.array([
        #     'http://localhost:8080', 'http://localhost:3000',
        #     'http://localhost:8889', 'http://electrons.simonbiggs.net'])
        # if np.any(origin == allow_origins):
        #     self.set_header('Access-Control-Allow-Origin', origin)

        coordinates = json.loads(self.get_argument('body'))
        width = np.array(coordinates['width']).astype(float)
        length = np.array(coordinates['length']).astype(float)
        factor = np.array(coordinates['factor']).astype(float)

        x, y, z = create_transformed_mesh(width, length, factor)

        respond = {
            'x': np.round(x, decimals=1).tolist(),
            'y': np.round(y, decimals=1).tolist(),
            'z': np.round(z, decimals=4).tolist()
        }

        self.write(respond)


app = tornado.web.Application([
    ('/parameterise', Parameterise),
    ('/model', Model)
])
app.listen(8888)
tornado.ioloop.IOLoop.current().start()
