from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    from . circle import Circle
    from . matrix import Matrix
    from . cube import Cube
    from . strip import Strip
    from . geometry.matrix import make_matrix_coord_map
    from . geometry.circle import make_circle_coord_map
    from . geometry.cube import make_cube_coord_map
    from . geometry.rotation import Rotation

    LEDCircle, LEDCube, LEDMatrix, LEDStrip = Circle, Cube, Matrix, Strip
