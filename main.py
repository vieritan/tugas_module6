from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)

def load_staffs():
    if os.path.exists('staffs.json'):
        with open('staffs.json', 'r') as file: # r untuk menulis data
            return json.load(file)
    return []

def save_staffs(staffs): 
    with open('staffs.json', 'w') as file: # w untuk write data
        json.dump(staffs, file, indent=4)

# Load existing animal data from JSON file or initialize an empty list
def load_animals():
    if os.path.exists('animals.json'):
        with open('animals.json', 'r') as file: # r untuk menulis data
            return json.load(file)
    return []

# Save animals data to the JSON file
def save_animals(animals): 
    with open('animals.json', 'w') as file: # w untuk write data
        json.dump(animals, file, indent=4)

@app.route('/', methods=['GET'])
def home():
    return '<p> hello world </p>'

# Retrieve all animals
@app.route('/animals', methods=['GET'])
def get_animals():
    animals = load_animals()
    return jsonify(animals)

# Retrieve a specific animal by ID
@app.route('/animals/<int:id>', methods=['GET'])
def get_animal_by_id(id):
    animals = load_animals()
    animal = next((a for a in animals if a['id'] == id), None) # id yg ijo db dan id yg kuning postman(req)
    if animal is None:
        abort(404, description="Animal not found")
    return jsonify(animal)

# Add a new animal
@app.route('/animals', methods=['POST'])
def add_animal():
    if not request.json or 'species' not in request.json:
        abort(400, description="Invalid request. 'species' is required")
    
    species = request.json.get('species')
    
    animals = load_animals()
    for animal in animals:
        if animal['species'] == species:
            return jsonify({"message": "animal already exist"})
    new_animal = {
        'id': animals[-1]['id'] + 1 if animals else 1,
        'species': request.json.get('species'),
        'age': request.json.get('age', 0),
        'gender': request.json.get('gender', 'Unknown'),
        'special_requirements': request.json.get('special_requirements', '')
    }
    animals.append(new_animal)
    save_animals(animals)
    return jsonify(new_animal), 201

# Update an existing animal
@app.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    animals = load_animals()
    animal = next((a for a in animals if a['id'] == id), None)
    if animal is None:
        abort(404, description="Animal not found")
    
    if not request.json:
        abort(400, description="Invalid request format")

    animal['species'] = request.json.get('species', animal['species'])
    animal['age'] = request.json.get('age', animal['age'])
    animal['gender'] = request.json.get('gender', animal['gender'])
    animal['special_requirements'] = request.json.get('special_requirements', animal['special_requirements'])

    save_animals(animals)
    return jsonify(animal)

# Delete an animal
@app.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animals = load_animals()
    animal = next((a for a in animals if a['id'] == id), None)
    if animal is None:
        abort(404, description="Animal not found")
    
    animals.remove(animal)
    save_animals(animals)
    return jsonify({'result': 'Animal deleted'})


    
###########################################################################################################      
# staff

# GET
@app.route('/employees', methods=['GET'])
def get_staffs():
    staffs = load_staffs()
    return jsonify(staffs)

# Retrieve a specific animal by ID
@app.route('/employees/<int:id>', methods=['GET'])
def get_staff_by_id(id):
    staffs = load_staffs()
    staff = next((a for a in staffs if a['id'] == id), None) # id yg ijo db dan id yg kuning postman(req)
    if staff is None:
        abort(404, description="ID not found")
    return jsonify(staff)

# POST
@app.route('/employees', methods=['POST'])
def add_staff():
    if not request.json or 'name' not in request.json:
        abort(400, description="Invalid request. 'name' is required")
    
    name = request.json.get('name')
    
    staffs = load_staffs()
    for staff in staffs:
        if staff['name'] == name:
            return jsonify({"message": "name already exist"}), 400
    new_staff = {
        'id': staffs[-1]['id'] + 1 if staffs else 1,
        'name': request.json.get('name'),
        'email': request.json.get('email', ''),
        'phone_number': request.json.get('phone_number', 'Unknown'),
        'role': request.json.get('role', ''),
        'schedule': request.json.get('schedule'),
    }
    staffs.append(new_staff)
    save_staffs(staffs)
    return jsonify(new_staff), 201

# PUT
@app.route('/employees/<int:id>', methods=['PUT'])
def update_staff(id):
    staffs = load_staffs()
    staff = next((a for a in staffs if a['id'] == id), None)
    if staff is None:
        abort(404, description="staff not found")
    
    if not request.json:
        abort(400, description="Invalid request format")

    staff['id'] = request.json.get('id', staff['id'])
    staff['name'] = request.json.get('name', staff['name'])
    staff['email'] = request.json.get('email', staff['email'])
    staff['phone_number'] = request.json.get('phone_number', staff['phone_number'])
    staff['role'] = request.json.get('role', staff['role'])
    staff['schedule'] = request.json.get('schedule', staff['schedule'])

    save_staffs(staffs)
    return jsonify(staff)

# Delete an animal
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_staff(id):
    staffs = load_staffs()
    staff = next((a for a in staffs if a['id'] == id), None)
    if staff is None:
        abort(404, description="staff not found")
    
    staffs.remove(staff)
    save_staffs(staffs)
    return jsonify({'result': 'staff deleted'})


# Error handlers
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)