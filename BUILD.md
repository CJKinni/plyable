# Build the package

```bash
python setup.py sdist bdist_wheel
```

# Use Locally

```bash
pip install dist/plyable-VERSION-py3-none-any.whl
```

# Upload to PIP

```bash
python3 -m twine upload --repository plyable dist/*
```