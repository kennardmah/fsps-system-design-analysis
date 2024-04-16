from graphviz import Digraph

def create_cost_decision_tree():
    dtree = Digraph(comment='Lunar Energy System Cost Decision Tree', graph_attr={'rankdir': 'LR'})

    # Styles for the decision tree
    decision_style = {'shape': 'rect'}
    chance_style = {'shape': 'circle'}
    cost_style = {'shape': 'rect'}

    # Initial decision node for nuclear fission capacity
    dtree.node('A', 'Nuclear Fission Capacity\nInitial Cost', **decision_style)

    nuclear_costs = {'Flexible Small': '20', 'Flexible Medium': '50', 'Inflexible Large': '100'}
    solar_costs = {'Small': '20', 'Medium': '40', 'Large': '60'}
    shortage_costs = {'No Shortage': '0', 'Shortage': '50'}

    # Adding nodes for nuclear options with their costs
    for i, (option, cost) in enumerate(nuclear_costs.items(), start=1):
        nuc_node_id = f'B{i}'
        dtree.node(nuc_node_id, f'{option} Nuclear\n{cost}', **decision_style)
        dtree.edge('A', nuc_node_id, label=' ')

        # Chance nodes for energy shortages with their costs
        for sc, (chance, shortage_cost) in enumerate(shortage_costs.items(), start=1):
            chance_node_id = f'SC{i}{sc}'
            dtree.node(chance_node_id, f'{chance}\n{shortage_cost}', **chance_style)
            dtree.edge(nuc_node_id, chance_node_id, label=' ')

            # Decision nodes for adding solar panels with their costs
            for j, (solar_option, solar_cost) in enumerate(solar_costs.items(), start=1):
                solar_node_id = f'D{i}{sc}{j}'
                dtree.node(solar_node_id, f'{solar_option} Solar\n{solar_cost}', **decision_style)
                dtree.edge(chance_node_id, solar_node_id, label=' ')

                # Cost outcomes
                outcome_id = f'Outcome{i}{sc}{j}'
                final_cost = 'FinalCost'  # Placeholder for final cost calculation
                dtree.node(outcome_id, f'Outcome\n{final_cost}', **cost_style)
                dtree.edge(solar_node_id, outcome_id, label=' ')

    # Render the decision tree
    output_path = 'lunar_energy_cost_decision_tree'
    dtree.render(output_path, format='png', cleanup=True)
    print(f"Decision tree visualization saved as {output_path}.png")

create_cost_decision_tree()
