import _helpers
import euklides

if __name__ == '__main__':
    _helpers.menu('# Menu', [
        _helpers.MenuLabel("Zajęcia 2022-04-04"),
        _helpers.MenuItem("Algorytm Euklidesa – iteracyjnie oraz rekurencyjnie", euklides.run),
    ])
