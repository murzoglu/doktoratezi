import importlib.util, pathlib

spec = importlib.util.spec_from_file_location("ex", pathlib.Path(__file__).parents[1]/"scripts/util/extract_triadic_matrix.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

def test_role_map():
    assert ex.ROLE["ANNE"] == "mother"
    assert ex.ROLE["HASTA"] == "t1dm_child"
    assert ex.ROLE["KARDEŞ"] == "healthy_sibling"

def test_family_pad():
    assert ex.pad_family("11") == "011"
    assert ex.pad_family("201") == "201"

def test_axis_slugs_8():
    assert len(ex.AXIS_SLUGS) == 8
