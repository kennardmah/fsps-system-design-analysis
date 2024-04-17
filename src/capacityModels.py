"""
Lunar Energy Implementation Optimisation - Kennard Mah 2024, Imperial College London
--- capacityModels.py ---
Calculates the energy capacity for Nuclear-based reactors and PV panels
"""

def nuclear_capacity(installed_capacity, efficiency=0.33):
    """
    Calculate output capacity for nuclear energy systems based on installed capacity and efficiency.

    :param installed_capacity: Installed capacity of nuclear system (in MW)
    :param efficiency: Efficiency rate of the nuclear system
    :return: Effective output capacity (in MW)
    """
    return installed_capacity * efficiency

def pv_capacity(installed_capacity, irradiance, conversion_efficiency=0.18):
    """
    Calculate output capacity for PV systems based on installed capacity, irradiance, and conversion efficiency.

    :param installed_capacity: Installed capacity of PV panels (in MW)
    :param irradiance: Solar irradiance (kWh/m^2/day)
    :param conversion_efficiency: Efficiency of the PV panels
    :return: Effective output capacity (in MW)
    """
    # Assuming 5 peak sun hours per day
    return installed_capacity * irradiance * conversion_efficiency * 5

# Example usage
if __name__ == "__main__":
    print("Nuclear Output:", nuclear_capacity(1000))
    print("PV Output:", pv_capacity(500, 5.5))
