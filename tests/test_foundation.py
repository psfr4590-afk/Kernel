from kernel import __version__


def test_kernel_package_imports():
    assert __version__ == "0.1.0"
