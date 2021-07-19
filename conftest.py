# Empty conftest.py for running the pytests rekursive from within the root directory.
# The empty conftest.py is needed, because when pytest discovers a conftest.py,
# it modifies sys.path so it can import stuff from the conftest module.
# So, since now an empty conftest.py is found in rootdir, pytest will be
# forced to append it to sys.path.
# Source -> https://stackoverflow.com/questions/49028611/pytest-cannot-find-module
