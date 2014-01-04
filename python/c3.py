from itertools import chain


def c3(cls, *mro_lists):
    # Make a copy so we don't change existing content
    mro_lists = [list(mro_list[:]) for mro_list in mro_lists]
    # Set up the new MRO with the class itself
    mro = [cls]
    while True:
        candidate_found = False
        for mro_list in mro_lists:
            if len(mro_list):
                # Get the first item as a potential candidate for the MRO.
                candidate = mro_list[0]
                if candidate_found:
                    # Candidates prompted to the MRO are no longer of user.
                    if candidate in mro:
                        mro_list.pop(0)
                elif candidate not in chain(*(x[1:] for x in mro_lists)):
                    # The candidate is valid and should be promted to the MRO.
                    mro.append(candidate)
                    mro_list.pop(0)
                    candidate_found = True
        if not sum(len(mro_list) for mro_list in mro_lists):
            # There are no MROs to cycle through, so we're all done.
            break
        if not candidate_found:
            raise TypeError('Inconsistent MRO')
    return mro


def mro(cls):
    bases = cls.__bases__
    mro_list = [mro(b) for b in bases]
    mro_list.append(bases)
    return c3(cls, *mro_list)

# test code


class A(object):
    def test(self):
        return 'A'


class B(A):
    def test(self):
        return 'B->' + super(B, self).test()


class C(A):
    def test(self):
        return 'C'


class D(B, C):
    pass
