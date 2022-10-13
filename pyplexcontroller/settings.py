import numpy

class Settings:
    def __init__(
        self,
        fs: float = 40000
    ):
        self.fs = fs
        self.ps = float(numpy.round(1 / fs, 6))
        return
    
if __name__ == "__main__":
    settings = Settings()
    print("sample rate", settings.fs)
    print(f"sample period {settings.ps}")