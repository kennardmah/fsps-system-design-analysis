from graphviz import Digraph

# Create a new graph for the decision tree, with 'LR' orientation
dtree = Digraph(comment='Lunar Energy System Decision Tree', graph_attr={'rankdir': 'LR'})

# Define the initial decision nodes for nuclear fission capacity
nuclear_options = ['Small', 'Medium', 'Large']
solar_options = ['Small', 'Medium', 'Large']
chance_nodes = ['No Shortage', 'Shortage']

# Adding the initial decision node
dtree.node('A', 'Nuclear Fission Capacity', shape='box')

# Adding nodes for nuclear options
for i, option in enumerate(nuclear_options, start=1):
    nuc_node_id = f'B{i}'
    dtree.node(nuc_node_id, option, shape='box')
    dtree.edge('A', nuc_node_id, label=' ')
    
    # Adding chance nodes for energy shortages between nuclear decision and solar panel decision
    for sc, chance in enumerate(chance_nodes, start=1):
        shortage_node_id = f'SC{i}{sc}'
        dtree.node(shortage_node_id, chance, shape='ellipse')
        dtree.edge(nuc_node_id, shortage_node_id, label='')

        # Adding decision nodes for adding solar panels after X years
        sol_node_id = f'C{i}{sc}'
        dtree.node(sol_node_id, 'PV Panel Expansion', shape='box')
        dtree.edge(shortage_node_id, sol_node_id, label='After 10 years')
    
        # Adding nodes for solar panel options
        for j, solar_option in enumerate(solar_options, start=1):
            solar_option_node_id = f'D{i}{sc}{j}'
            dtree.node(solar_option_node_id, solar_option, shape='box')
            dtree.edge(sol_node_id, solar_option_node_id, label=' ')

            # Add an outcome node for each path
            outcome_id = f'Outcome{i}{sc}{j}'
            dtree.node(outcome_id, f'Outcome {i}{sc}{j}', shape='box')
            dtree.edge(solar_option_node_id, outcome_id, label='Outcome')

# Visualize the decision tree
output_path = '/Users/kennardmah/Documents/GitHub/masters-thesis-sustainable-lunar-energy/lunar_energy_decision_tree'
dtree.render(output_path, format='png', cleanup=True)
print(f"Decision tree visualization saved as {output_path}.png")
