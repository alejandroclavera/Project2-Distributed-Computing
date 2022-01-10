import json
from io import BytesIO
from ..models.content import Content, Keyword
from flask import g
from app.models.user import User
from app.models.node import Node

valid_search_args = ['title', 'description', 'keyword', 'value', 'partial']


def find_content(search_args):
    """
    Find a contents 
    """
    # Check if all search arguments are valids
    if not all(arg in valid_search_args for arg in search_args):
        return None
    
    query = Content.query

    # Check the search it is partial by description
    if 'partial' in search_args:
        # Check if the search args have the keyword description
        if 'description' not in search_args:
            return None
        # Convert search_args to mutable dic
        args = {}
        args.update(search_args)
        search_args = args
        # Check must apply a partial search by description
        if search_args['partial'] == 'true':
            query = query.filter(Content.description.contains(search_args['description']))
            search_args.pop('description')
        # Remove the partial arg from the search_args
        search_args.pop('partial')

    # Filter the contents 
    if 'keyword' in search_args or 'value' in search_args:
        # Case the filter contain keyword filtering
        content_args, keyword_args = {}, {}
        for arg in search_args.items():
            # Split the search arguments in content search args and keyword search args
            if arg[0] == 'keyword' or arg[0] == 'value':
                keyword_args[arg[0]] = arg[1]
            else:
                content_args[arg[0]] = arg[1]
        query = query.filter_by(**content_args).join(Keyword).filter_by(**keyword_args)
    else:
        query = query.filter_by(**search_args)
    
    return query


def post_new_content(request_form):
    """
    Create a new Content and stored it in the database
    """
    if request_form is None:
        return None
    # Check the request form
    if 'title' not in request_form:
        return None
    elif 'description' not in request_form:
        return None
    # Create a new content
    title = request_form['title']
    description = request_form['description']
    user = User.get_user_by_id(g.user.get('id'))
    node = None if 'node' not in request_form else Node.query.get(request_form['node'])
    if 'keywords' in request_form:
        if not Content.are_valid_keywords(request_form['keywords']):
            return None
        content = Content(title, description, user, node, keywords=request_form['keywords'])
    else:
        content = Content(title, description, user, node)
    # Store the new content in the database
    content.save()
    return content


def get_content_by_id(content_id):
    return Content.query.get(content_id)


def modify_content(content_id, form):
    """
    Modify the content information from a dict form
    """
    content = Content.query.get(content_id)
    if content is None:
        return None, 404
    
    # Check if the user is the owner of the content
    if g.user.get('id') != content.owner:
        return None, 403
    content.update(form)
    return content, 200


def delete_content_by_id(content_id):
    """
    Delete the content
    """
    content = Content.query.get(content_id)
    if content is None:
        return 404
    # Check if the user is the owner of the content
    if g.user.get('id') != content.owner:
        return 403
    content.delete()
    return 200


def get_content_file_by_id(content_id):
    """
    Generate a file with the information of a content
    """
    content = get_content_by_id(content_id)
    if not content:
        return None
    content_file = BytesIO()
    content_file.write(json.dumps(content.serialize).encode())
    content_file.seek(0)
    return content_file


def get_all_content_file():
    """
    Generate a file with information of all contents of the WS
    """
    contents = Content.query.all()
    if not contents:
        return None
    contents_file = BytesIO()
    contents_file.write(json.dumps([content.serialize for content in contents]).encode())
    contents_file.seek(0)
    return contents_file
