

# Run Tests


Command to run from the main folder:

```bash
#python 3.6
# All test
pytest tests/

# one test, ex
pytest tests/test_classorder.py 

# stop after first failure
pytest -x          

# run a specific test within a module:
pytest test_mod.py::test_func

# run slow tests
pytest tests/ -m slow

# run not slow tests
pytest tests/  -m 'not slow'

# get coverage
python pytest --cov=. tests/
```
