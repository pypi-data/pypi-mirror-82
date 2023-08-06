from . import wrapper
from .. util.image import movie_writer as _movie_writer


class MovieWriter(wrapper.Wrapper):
    """
    An animation that writes animated GIFs for each frame in the contained
    animation."""

    def __init__(self, *args, filename='output.gif', render=None,
                 divide=1, frames=128, time=0, scale=1.0, options=None,
                 gif_dir=None, **kwds):
        """
        :param str filename: Base filename to write the animated GIF file

        :param dict render: Parameters to the renderer function -
            see ``bibliopixel.util.image.render.renderer``

        :param int divide: If greater than 1, only rendered one in ``divide``
            frames

        :param int frames: Number of frames to write

        :param float time: Total time to write.  If non-zero, takes precedence
            over `frames`

        :param float speed: the speed of the GIF is scaled up by this factor,
            so if speed=2 then a 2 second animation will become a 1 second GIF.

        :param dict options: Options to
            ``bibliopixel.util.image.gif.write_animation``

        :param str gif_dir: If set, write individual GIF frame files to this
            directory, and do not delete them when done.  For testing purposes.
        """
        super().__init__(*args, **kwds)
        self.movie_writer = _movie_writer.MovieWriter(
            filename, render, divide, frames, time, scale, options, gif_dir)

    def set_project(self, project):
        super().set_project(project)
        self.movie_writer.set_project(project)

    def step(self, amt=1):
        super().step(amt)
        if self.movie_writer.step(self.cur_step):
            self.completed = True

    def cleanup(self, clean_layout=True):
        super().cleanup(clean_layout)
        self.movie_writer.cleanup()
