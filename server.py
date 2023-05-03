import uuid

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'title': 'Milch', 'content': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'title': 'Arbeitsblätter ausdrucken', 'content': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'title': 'Kinokarten kaufen', 'content': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'title': 'Eier', 'content': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def check_for_and_get_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if list_item:
        return list_item
    else:
        abort(404)


def check_for_and_get_entry(entry_id):
    # find todo entry depending on given entry id
    entry_item = None
    for t in todos:
        if t['id'] == entry_id:
            entry_item = t
            break
    # if the given entry id is invalid, return status code 404
    if entry_item:
        return entry_item
    else:
        abort(404)


# define endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE', 'PATCH'])
def handle_list(list_id):
    list_item = check_for_and_get_list(list_id)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id]), 200
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200
    elif request.method == 'PATCH':
        new_list_data = request.get_json(force=True)
        # edit name of given list
        for item in new_list_data:
            if item == 'name':
                list_item['name'] = new_list_data['name']
        # update list with given id
        print('Updating todo list...')
        return '', 200


# define endpoint for returning all existing lists
@app.route('/todo-list', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200


# define endpoint for adding a new list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 200


# define endpoint for adding a list entry
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    # make JSON from POST data (even if content type is not set correctly)
    new_entry = request.get_json(force=True)
    # add list_id to new entry
    new_entry['list'] = list_id
    print('Got new list entry to be added: {}'.format(new_entry))
    # create id for new entry, save it and return the entry with id
    new_entry['id'] = str(uuid.uuid4())
    todos.append(new_entry)
    return jsonify(new_entry), 200


# define endpoint for updating or deleting a list entry
@app.route('/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def handle_list_entry(entry_id):
    entry_item = check_for_and_get_entry(entry_id)
    if request.method == 'DELETE':
        # delete entry with given id
        print('Deleting todo list entry...')
        todos.remove(entry_item)
        return '', 200
    elif request.method == 'PATCH':
        new_entry_data = request.get_json(force=True)
        # edit given entry
        for item in new_entry_data:
            entry_item[item] = new_entry_data[item]
        print('Updating todo list entry...')
        return jsonify(entry_item), 200


if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
