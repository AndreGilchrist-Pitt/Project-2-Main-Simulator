from Src.Utils.Classes.bus import Bus

if __name__ == "__main__":
    bus = Bus("bus1")
    print(bus.v)
    bus.set_bus_v(100)
    print(bus.v)
    print(bus)