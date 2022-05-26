import _helpers
import euklides
import lattice_points
import optim_reduce
import skracanie_ulamkow
import find_min_max

if __name__ == '__main__':
    _helpers.menu('# Menu', [
        _helpers.MenuLabel("Zajęcia 2022-05-15"),
        _helpers.MenuItem("Sklejanie par liczb", optim_reduce.run),
        _helpers.MenuItem("Punkty kratowe", lattice_points.run),

        _helpers.MenuLabel("Zajęcia 2022-04-10"),
        _helpers.MenuItem("Znajdowanie min/max w ciągu", find_min_max.run),

        _helpers.MenuLabel("Zajęcia 2022-04-04"),
        _helpers.MenuItem("Algorytm Euklidesa – iteracyjnie oraz rekurencyjnie", euklides.run),
        _helpers.MenuItem("Skracanie ułamków", skracanie_ulamkow.run),

    ])
