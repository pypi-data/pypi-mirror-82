# TwissGrid

This application performs one- or two-dimensional grid scans of lattice parameters
and visualizes their effect on selected optics functions.

## Installation

The application can be installed from the Python Package Index (PyPI):

```
pip install twissgrid
```

## Usage

The application can be used from the command line in the following way:

```
python -m twissgrid /path/to/script.madx a_param
```

It expects at least two arguments:

1. The file path to a MADX script.
2. The name of a lattice parameter. It needs to be given as `label->attr` where the `->attr` part is optional (it will be inferred from the element type). The corresponding element must be accessible in MADX via the provided `label` (internally the parameter will be updated as `label->attr = value;` so that must be an effective statement).

This example will create a 2D-plot of the beta functions in dependence on that parameter:

![Example1D](./example1d.png)

### 3D Plots

A second parameter can be provided, following the first one, in order to perform a two-dimensional parameter scan
and create a corresponding 3D-plot:

```
python -m twissgrid /path/to/script.madx a_param b_param
```

![Example2D](./example2d.png)

### Customization

The application supports various other arguments for customizing the parameter scan or the resulting plots.
The full set of available parameters can be found via `--help`:

```
$ python -m twissgrid --help
usage: python -m twissgrid [-h] [--p1lb P1LB] [--p1ub P1UB]
                           [--p1delta P1DELTA] [--p1margin P1MARGIN]
                           [--p1n P1N] [--p2lb P2LB] [--p2ub P2UB]
                           [--p2delta P2DELTA] [--p2margin P2MARGIN]
                           [--p2n P2N] [--funcs FUNCS [FUNCS ...]]
                           [--target TARGET] [--beta0 BETA0]
                           [--threshold [THRESHOLD [THRESHOLD ...]]]
                           [--figsize FIGSIZE FIGSIZE]
                           script p1 [p2]

positional arguments:
  script                File path to MADX script
  p1                    Lattice parameter 1 (format: label[->attribute])
  p2                    Lattice parameter 2 (format: label[->attribute])
                        (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --funcs FUNCS [FUNCS ...]
                        Optics functions to plot (default: ('betx', 'bety'))
  --target TARGET       Label of the target element where optics functions are
                        observed (default: #e)
  --beta0 BETA0         Label of BETA0 command (this must be part of the MADX
                        script) (default: None)
  --threshold [THRESHOLD [THRESHOLD ...]]
                        Plot threshold line on each optics plot (default:
                        None)
  --figsize FIGSIZE FIGSIZE
                        Figure size in inches (default: (14, 10))

Parameter 1:
  --p1lb P1LB           Lower boundary for parameter scan (default: None)
  --p1ub P1UB           Upper boundary for parameter scan (default: None)
  --p1delta P1DELTA     Compute missing boundaries as a distance to the
                        current value (i.e. "lb = value - delta" and "ub =
                        value + delta"); --delta takes precedence over
                        --margin (default: None)
  --p1margin P1MARGIN   Compute missing boundaries as a fraction of the
                        current value (i.e. "lb = (1 - margin)*value" and "ub
                        = (1 + margin)*value") (default: 0.01)
  --p1n P1N             Number of grid points for parameter scan (default:
                        100)

Parameter 2:
  --p2lb P2LB           Lower boundary for parameter scan (default: None)
  --p2ub P2UB           Upper boundary for parameter scan (default: None)
  --p2delta P2DELTA     Compute missing boundaries as a distance to the
                        current value (i.e. "lb = value - delta" and "ub =
                        value + delta"); --delta takes precedence over
                        --margin (default: None)
  --p2margin P2MARGIN   Compute missing boundaries as a fraction of the
                        current value (i.e. "lb = (1 - margin)*value" and "ub
                        = (1 + margin)*value") (default: 0.01)
  --p2n P2N             Number of grid points for parameter scan (default:
                        100)
```
