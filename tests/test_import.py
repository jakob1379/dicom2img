import dicom2img


def test_import():
    """
    Test that the package can be imported.
    """
    dir(dicom2img)
    assert True  # If the import succeeds, this test passes
