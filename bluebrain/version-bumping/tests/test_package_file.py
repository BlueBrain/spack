def version(*args, **kwargs):
    pass


class TestPackage:
    version("stable", branch="main")
    version("1.2.4", tag="test-v1.2.3")
    version(
        "3.4.5.6", sha256sum="339382b6452a93c07d5bdcb0b5a941acbff78e7218b61570e7eba29572db5b96"
    )
    version("1.2.3", tag="test-v1.2.3")
    version("1.2.3a", tag="alpha-1.2.3")
