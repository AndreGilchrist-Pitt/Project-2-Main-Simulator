import pandas as pd


class TransmissionLine:
    """
    Represents a transmission line in a power system network.

    A transmission line connects two buses and has series impedance (r + jx)
    and shunt admittance (g + jb).
    """

    def __init__(self, name: str, bus1_name: str, bus2_name: str,
                 r: float, x: float, g: float, b: float):
        """
        Initialize a TransmissionLine instance.

        Args:
            name: The name/identifier of the transmission line
            bus1_name: Name of the first bus
            bus2_name: Name of the second bus
            r: Series resistance in per-unit or ohms
            x: Series reactance in per-unit or ohms
            g: Shunt conductance in per-unit or siemens
            b: Shunt susceptance in per-unit or siemens
        """
        self.name = name
        self.bus1_name = bus1_name
        self.bus2_name = bus2_name
        self.r = r
        self.x = x
        self.g = g
        self.b = b
        # Series admittance: Yseries = 1/(r + jx), per-unit values
        self.Yseries = 1 / (r + 1j * x)
        # Shunt admittance: Yshunt = g + jb, per-unit values
        self.Yshunt = g + 1j * b

    def calc_yprim(self) -> pd.DataFrame:
        """
        Return the 2×2 primitive admittance matrix for the transmission line
        pi-model (Yseries with Yshunt/2 at each bus).

        Returns:
            pandas.DataFrame: Yprim with bus1_name and bus2_name as row/column labels.
        """
        labels = [self.bus1_name, self.bus2_name]
        Y11 = self.Yseries + self.Yshunt / 2
        Y12 = -self.Yseries
        Yprim = pd.DataFrame(
            [[Y11, Y12], [Y12, Y11]],
            index=labels,
            columns=labels,
        )
        return Yprim

    def __repr__(self):
        return (f"TransmissionLine(name='{self.name}', bus1='{self.bus1_name}', "
                f"bus2='{self.bus2_name}', r={self.r}, x={self.x}, g={self.g}, b={self.b})")


if __name__ == "__main__":
    # Milestone 3 validation: Yseries, Yshunt, and Yprim only outputted
    print("=== TransmissionLine Class Validation ===\n")

    line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)

    print("Series and shunt admittances:")
    print(line1.Yseries, line1.Yshunt)

    print("\nPrimitive admittance matrix:")
    print(line1.calc_yprim())
