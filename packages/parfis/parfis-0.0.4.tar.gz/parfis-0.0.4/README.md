# PARFIS

PARticles and FIeld Simulator

Wiki: http://www.parfis.com

## Testing

We have two types of tests, googletest for the c++ code and python scripts as an examples and testing of the python interface.

### Python unittest

We use `unittest` module for testing python functionality. To run all tests:

```python
import parfis.tests
parfis.tests.run_all_tests()
```
