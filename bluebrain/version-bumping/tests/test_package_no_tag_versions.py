def version(*args, **kwargs):
    pass


class TestPackage:
    version("stable", branch="main")
    version("1.2.4", sha256sum="f18acf71becf1d9eb1340a7f00468c8d2586778b33021abed9b6c884f9da2a04")
    version(
        "3.4.5.6", sha256sum="339382b6452a93c07d5bdcb0b5a941acbff78e7218b61570e7eba29572db5b96"
    )
