import json
from io import BytesIO
from ..models.content import Content, Keyword

find_keys = ['title', 'description', 'keyword', 'value']


def find_content(search_args):
    """
    Find a contents 
    """
    # Check if all search arguments are valids
    if not all(arg in find_keys for arg in search_args):
        return None

    # Find the contents
    if 'keyword' in search_args or 'value' in search_args:
        contents = Content.query.join(Keyword).filter_by(**search_args)
    else:
        contents = Content.query.filter_by(**search_args)
    return contents


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
    if 'keywords' in request_form:
        if not Content.are_valid_keywords(request_form['keywords']):
            return None
        content = Content(title, description, keywords=request_form['keywords'])
    else:
        content = Content(title, description)
    # Store the new content in the database
    content.save()
    return content


def get_content_by_id(content_id):
    return Content.query.get(content_id)


def modify_content(content_id, form):
    content = Content.query.get(content_id)
    if content is None:
        return None
    content.update(form)
    return content


def delete_content_by_id(content_id):
    content = Content.query.get(content_id)
    if content is None:
        return False
    content.delete()
    return True


def get_content_file_by_id(content_id):
    content = get_content_by_id(content_id)
    if not content:
        return None
    content_file = BytesIO()
    content_file.write(json.dumps(content.serialize).encode())
    content_file.seek(0)
    return content_file


def get_all_content_file():
    contents = Content.query.all()
    if not contents:
        return None
    contents_file = BytesIO()
    contents_file.write(json.dumps([content.serialize for content in contents]).encode())
    contents_file.seek(0)
    return contents_file
