"""
Lunar Energy Implementation Optimisation - Kennard Mah 2024, Imperial College London
--- config.py ---
Store all constants and parameters in one centralized location
"""

"""
CONSTANTS
"""
# COST RELATED
C_penalty = 5000000
r_eos = 0 # economies of scale (?)

# POWER OUTPUT RELATED
r_decay = 0.0159

# DEMAND RELATED

# MISC
time = 20

"""
PARAMETERS
"""
# COST RELATED
M_nf_40 = 3929
M_components_40 = 1621
M_total_40 = M_nf_40 + M_components_40

C_launch = 2720
C_produce = 43000
C_payload = 3500

# POWER OUTPUT RELATED
EOPM = 40/3969 # Energy output per mass (kW/kg)
capacities = [60, 50, 40] # 60kW, 50kW, 40kW

# DEMAND RELATED
ECLSS_p1 = [6, 4.2]
OPERATIONS_p1 = [('ISRU Operations', 7), ('Rover Operations', 1), ('Some other stuff', 1)]

# MISC.