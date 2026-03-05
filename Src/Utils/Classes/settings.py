class Settings:
    """
    Centralized system-wide settings for per-unit calculations.

    This class defines the global base quantities used across the
    power system model.
    """

    def __init__(self, freq: float = 60.0, sbase: float = 100.0):
        """
        Initialize a Settings instance.

        Args:
            freq: System frequency in hertz (Hz). Default is 60 Hz.
            sbase: System base apparent power in megavolt-amperes (MVA).
                   Default is 100 MVA.
        """
        self.freq = freq
        self.sbase = sbase

    def __repr__(self):
        return f"Settings(freq={self.freq}, sbase={self.sbase})"


if __name__ == "__main__":
    # Simple validation test
    print("=== Settings Class Validation ===\n")

    # Default settings
    default_settings = Settings()
    print("Default Settings:")
    print(f"Frequency (Hz): {default_settings.freq}")
    print(f"Sbase (MVA): {default_settings.sbase}")
    print(f"Representation: {repr(default_settings)}\n")

    # Custom settings
    custom_settings = Settings(freq=50.0, sbase=200.0)
    print("Custom Settings:")
    print(f"Frequency (Hz): {custom_settings.freq}")
    print(f"Sbase (MVA): {custom_settings.sbase}")
    print(f"Representation: {repr(custom_settings)}")

