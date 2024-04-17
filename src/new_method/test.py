from pyomo.environ import *
from pyomo.opt import SolverFactory

# Define the Concrete Model
model = ConcreteModel()

# Stage 1 Variables: Nuclear base-load capacity
model.X = Var(domain=NonNegativeReals, initialize=100)

# Stage 2 Variables: PV capacity in the future (a dictionary of PV capacities per scenario)
model.P = Var(['scenario1', 'scenario2'], domain=NonNegativeReals, initialize=0)

# Parameters for costs and demands
model.CostNuclear = Param(initialize=1000)  # Cost per MW for nuclear
model.CostPV = Param(['scenario1', 'scenario2'], initialize={'scenario1': 500, 'scenario2': 450})  # Cost per MW for PV
model.DemandBase = Param(initialize=100)  # Base demand in MW
model.DemandPeak = Param(['scenario1', 'scenario2'], initialize={'scenario1': 150, 'scenario2': 200})  # Peak demand scenarios
model.Probability = Param(['scenario1', 'scenario2'], initialize={'scenario1': 0.5, 'scenario2': 0.5})  # Scenario probabilities

# Objective Function: Minimize total expected cost
def objective_rule(model):
    return (model.CostNuclear * model.X +
            sum(model.CostPV[sc] * model.P[sc] * model.Probability[sc] for sc in ['scenario1', 'scenario2']))

model.TotalCost = Objective(rule=objective_rule, sense=minimize)

# Constraints

# Constraint: Nuclear must meet base demand
def base_demand_rule(model):
    return model.X >= model.DemandBase

model.BaseDemandConstraint = Constraint(rule=base_demand_rule)

# Constraint: Total energy must meet or exceed demand in all scenarios
def peak_demand_rule(model, scenario):
    return model.X + model.P[scenario] >= model.DemandPeak[scenario]

model.PeakDemandConstraint = Constraint(['scenario1', 'scenario2'], rule=peak_demand_rule)

# Solve the model
solver = SolverFactory('glpk')
result = solver.solve(model, tee=True)

# Print the results
print("Optimal Nuclear Base-Load Capacity (MW):", model.X.value)
for sc in ['scenario1', 'scenario2']:
    print(f"Optimal PV Capacity for {sc} (MW):", model.P[sc].value)
print("Total Cost:", model.TotalCost())

