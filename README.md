# hse_ruz
Python wrapper for HSE RUZ API

### Requirements
* Python Python 3.3+
* PyPy3

### Installation
```bash
    pip install hse_ruz
```

### Usage
**Note:** add ruz api url throw `API_RUZ_URL` environment variable.
```python
    from ruz import RUZ

    api = RUZ()
    assert api.v == 2
    assert api.get("buildings")
```

### ToDo
* [ ] add separate method for each endpoint
* [ ] update tests
