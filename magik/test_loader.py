import os
from magik.sys_exec import read_from_file
import importlib.util


# Loads a test suite from the test directory
class TestLoader:
    def __init__(self, test_dir):
        self.test_dir = test_dir

    def _load_prompt(self, test_name):
        test_file_path = f"{self.test_dir}/{test_name}/prompt.txt"
        absolute_path = os.path.abspath(test_file_path)
        return read_from_file(absolute_path)

    def _load_attr_from_test_file(self, test_name, attr_name, default_value=None):
        test_file_path = f"{self.test_dir}/{test_name}/assertions.py"
        # Get the absolute path by resolving against the current working directory
        absolute_path = os.path.abspath(test_file_path)

        # Get the directory path and module name from the absolute path
        directory, module_name = os.path.split(absolute_path)
        module_name = os.path.splitext(module_name)[0]

        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, absolute_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Access the `tests` array from the module
        return getattr(module, attr_name, default_value)

    def _load_define_tests_fn(self, test_name):
        return self._load_attr_from_test_file(
            test_name=test_name, attr_name="define_tests", default_value=lambda _: []
        )

    def _load_context(self, test_name):
        return self._load_attr_from_test_file(
            test_name=test_name, attr_name="test_context", default_value=None
        )

    def _load_test_suite(self, test_name, test_context):
        define_tests_fn = self._load_define_tests_fn(test_name)
        return define_tests_fn(test_context)
