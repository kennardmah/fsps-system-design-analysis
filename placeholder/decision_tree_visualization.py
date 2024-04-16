
from graphviz import Digraph

def generate_decision_tree():
    # Create a new graph for the decision tree
    dtree = Digraph(comment='Lunar Energy System Decision Tree')

    # Define the initial decision nodes for nuclear fission capacity
    nuclear_options = ['Small Nuclear', 'Medium Nuclear', 'Large Nuclear']
    solar_options = ['Small Solar', 'Medium Solar', 'Large Solar']
    chance_nodes = ['No Shortage', 'Shortage']

    # Adding the initial decision node
    dtree.node('A', 'Nuclear Fission Capacity')

    # Adding nodes for nuclear options
    for i, option in enumerate(nuclear_options, start=1):
        dtree.node(f'B{i}', option)
        dtree.edge('A', f'B{i}', label=' ')

        # Adding decision nodes for adding solar panels after X years
        dtree.node(f'C{i}', 'Add Solar Panels?', shape='diamond')
        dtree.edge(f'B{i}', f'C{i}', label='After X years')

        # Adding nodes for solar panel options
        for j, solar_option in enumerate(solar_options, start=1):
            node_id = f'D{i}{j}'
            dtree.node(node_id, solar_option)
            dtree.edge(f'C{i}', node_id, label=' ')

            # Adding chance nodes for energy shortage
            for k, chance_node in enumerate(chance_nodes, start=1):
                chance_id = f'E{i}{j}{k}'
                dtree.node(chance_id, chance_node, shape='ellipse')
                dtree.edge(node_id, chance_id, label=' ')

    # Adjust the path below to where you want to save the decision tree visualization on your local system
    print('hello world')
    output_path = 'lunar_energy_decision_tree'
    dtree.render(output_path, format='png', cleanup=True)
    print(f"Decision tree visualization saved to {output_path}.png")

if __name__ == '__main__':
    generate_decision_tree()
