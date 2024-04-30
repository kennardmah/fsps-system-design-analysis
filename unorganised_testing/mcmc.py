import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt

def run_model():
    # Assuming prior distribution parameters for demand
    mu_D = 34.2  # mean demand in kW
    sigma_D = 2.7  # standard deviation of demand in kW

    # Observed supply after deploying 40 kW
    observed_supply = 37  # in kW

    # Setting up the Bayesian model
    with pm.Model() as model:
        # Prior distribution for demand
        demand = pm.Normal('demand', mu=mu_D, sigma=sigma_D)
        
        # Likelihood
        likelihood = pm.Normal('likelihood', mu=demand + 7, sigma=5, observed=observed_supply)
        
        # Running MCMC to sample from the posterior
        trace = pm.sample(3000, return_inferencedata=False)

        # Plotting the posterior distribution of demand
        pm.plot_trace(trace)
        plt.show()

        # Summary of the posterior distribution
        print(pm.summary(trace))

if __name__ == '__main__':
    run_model()
