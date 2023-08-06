def test_version_is_correct():
    import configparser
    from pathlib import Path
    import mbf_fileformats

    c = configparser.ConfigParser()
    c.read(Path(__file__).parent.parent / "setup.cfg")
    version = c["metadata"]["version"]
    assert version == mbf_fileformats.__version__
