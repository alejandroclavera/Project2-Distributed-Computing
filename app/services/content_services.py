from ..models.content import Content


def find_content(search_args):
    """
    Find a contents 
    """
    contents = Content.query.filter_by(**search_args)
    return contents


def post_new_content(request_form):
    """
    Create a new Content and stored it in the database
    """
    # Check the request form
    if 'title' not in request_form:
        return None
    elif 'description' not in request_form:
        return None
    # Create a new content
    title = request_form['title']
    description = request_form['description']
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
