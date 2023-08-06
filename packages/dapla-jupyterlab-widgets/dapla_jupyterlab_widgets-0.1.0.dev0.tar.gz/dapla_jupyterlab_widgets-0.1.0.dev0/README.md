
# dapla-jupyterlab-widgets

A collection of custom Jupyterlab widgets for the Dapla platform.
These are extensions with backend (i.e. server) and frontend parts.

## Installation

Install Jupyterlab using `pip`:

```bash
pip install jupyterlab
```

Then you can install the extensions:

```bash
pip install dapla_jupyterlab_widgets
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

## Development Installation

```bash
# First install the python package. This will also build the JS packages.
pip install -e ".[test, examples]"
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:

```
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
jupyter labextension install .
```

### How to see your changes
#### Typescript:
To continuously monitor the project for changes and automatically trigger a rebuild, start Jupyter in watch mode:
```bash
jupyter lab --watch
```
And in a separate session, begin watching the source directory for changes:
```bash
npm run watch
```

After a change wait for the build to finish and then refresh your browser and the changes should take effect.

#### Python:
If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.

#### Publishing

The packages needs to be published to npm and PyPi.
To publish to npm you need a user and a membership in the statisticsnorway organization on npm. The user must also have 2FA authentication enabled. Steps to follow:

- Login into your npm account in a terminal with npm login
- Make sure all tests work (test components in the example application as well, if you made a new one)
- Bump version in package.json
- Run `npm package`
- Dry run a release with `npm pack`
- Publish with `npm publish --access public --otp=<code>` 
  (where \<code> is your 2FA code, without <>)
  
To publish to PyPi, use:
```bash
# Clean all build artifacts
rm -rf *.egg-info
rm -rf dist
# Build dist
python setup.py sdist bdist_wheel
# Validate that a distribution will render properly on PyPI
twine check dist/*.gz
# Release a new version, uploading it to PyPI
twine upload dist/*
```
