from . indexed import Indexed


class Wrapper(Indexed):
    """
    Wraps a single Animation.

    ``Wrapper`` is used as a base class for Pytho Animation classes that control
    or process other animations.
    """

    # TODO: No unit tests cover any of this.
    @staticmethod
    def pre_recursion(desc):
        if 'animations' in desc:
            raise ValueError('Cannot specify animations in a Wrapper')
        desc['animations'] = [desc.pop('animation')]
        return Indexed.pre_recursion(desc)

    @property
    def animation(self):
        return self.animations[0]
