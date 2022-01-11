from app.models.node import Node

def register_node():
    """
    Register a new node and store it in the data base
    """
    
    # Creata and store the node in the data base
    node = Node('plk')
    node.save()

    return node.serialize, 201

