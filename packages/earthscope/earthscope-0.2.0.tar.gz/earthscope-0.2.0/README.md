# GeoTIFF Viewer for JupyterLab

`earthscope` allows GeoTIFF files (even large onces) to be browser from within JupyterLab.

## Installing earthscope

You'll need both the JupyterLab widget, as well as the python library:

```
jupyter labextension install @ceresimaging/earthscope
pip install earthscope
```

## Developing earthscope
Follow all the setup steps below in order.

### Create virtualenv, and install dependencies:
```bash
# note that this block of pip installs must happen in the root dir
cd ../..
python3 -m venv env
. env/bin/activate
pip install -r requirements.icin.txt
pip install -r requirements.txt
pip install -r requirements.ceres.txt
pip install -e .
```
If you have issues trying to install `Rtree` on a mac, try running `brew install spatialindex`
Then install eaerthscope dependencies:
```bash
cd icin/earthscope
pip install -r requirements.txt
```

### Download sample imagery (from `icin/earthscope`):
`npm run local-flights-setup`

### Install python-mapnik (directions for mac OSX only, see @jake for help on linux):
`npm run tile-server-build-python-mapnik`

### Setup Jupyterlab
```bash
pip install -r requirements.txt && pip install -e . && \
jupyter nbextension enable --py widgetsnbextension && \
jupyter labextension install --no-build @jupyter-widgets/jupyterlab-manager && \
npm install
```

## Running earthscope
Make sure that your python virtual env is activated before running each command.

### First: Run a tile server
In one terminal: `npm run tileserver`

### (Option 1) Run outside JupyterLab for faster dev iteration:

If you're working on a feature/bug that doesn't require jupyterlab, you
may prefer to develop inside `webpack`'s hot-reloading app mode. To do this:
In a separate terminal: `npm run start`

### (Option 2) Run inside JupyterLab to validate integration:

Most of earthscope is written in Javascript/React, which is then accessed through a thin python library.
Development will mostly take place inside the context of JupyterLab, so its nice to set things
up so every time you save a file, the JupyterLab extension is updated:

1. In one terminal: `npm run watch`
2. In another terminal: `npm run jupyterlab`

Now from within JupyterLab you can try something like:
```python
from earthscope import view, setup
# if you're not running on improc.ceresimaging.net, you may have to run setup first, eg.:
#   setup(base_url='http://localhost:9090/flights')
#   setup(base_url='https://improc-dev.ceresimaging.net/hub/user-redirect/tileserver/flights')
v = view([
  '/Flight 11290/field borders/56968 Overman.shp',
  '/Flight 11290/registered/2020-07-27 56968 Overman VNIR.tif',
  '/Flight 11290/registered/2020-07-27 56968 Overman Jenoptik.tif',
  '/Flight 11290/color merged/2020-07-27 56968 Overman TR.tif',
  '/Flight 11290/color merged/2020-07-27 56968 Overman WSC.tif'
])
v
```
You can modify the existing earthscope widget instance, and it will re-render:
```python
widget = v.children[0]
source_id = '/Flight 11290/color merged/2020-07-27 56968 Overman CIR.tif'
widget.add_source(source_id)
```

Which should start a earthscope widget instance viewing a tile on your local
tile server instance (see above if you aren't running one) in `~/flights/Flight 5158/color merged/2018-07-23 8585 Oakes 69 Boundary WSC.tif`