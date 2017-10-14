python setup.py sdist
twine upload dist/*
rd /S /Q hse_ruz.egg-info
rd /S /Q dist
del MANIFEST
del setup.cfg
