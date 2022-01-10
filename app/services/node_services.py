from app.models.node import Node

def register_node(request_form):
    """
    Register a new node and store it in the data base
    """
    # Check the request form
    if 'public_key' not in request_form:
        return None, 400
        
    # Creata and store the node in the data base
    node = Node('plk')
    node.save()

    return node.serialize, 201

