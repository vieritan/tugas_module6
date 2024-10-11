from flask import Flask, jsonify, request, abort
from supabase import create_client, Client
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET'])
def home():
    return '<p> hello world </p>'

# Get all animals from Supabase
@app.route('/animals', methods=['GET'])
def get_animals():
    response = supabase.table('animals').select('*').execute()
    animals = response.data
    return jsonify(animals)

# Get specific animal by ID from Supabase
@app.route('/animals/<int:id>', methods=['GET'])
def get_animal_by_id(id):
    response = supabase.table('animals').select('*').eq('id', id).execute()
    animals = response.data
    if not animals:
        abort(404, description="Animal not found")
    return jsonify(animals[0])


# Add a new animal to Supabase
@app.route('/animals', methods=['POST'])
def add_animal():
    if not request.json or 'species' not in request.json:
        abort(400, description="Invalid request. 'species' is required")

    new_animal = {
        'species': request.json.get('species'),
        'age': request.json.get('age', 0),
        'gender': request.json.get('gender', 'Unknown'),
        'special_requirements': request.json.get('special_requirements', '')
    }

    response = supabase.table('animals').insert(new_animal).execute()
    return jsonify(response.data[0]), 201


# Update existing animal in Supabase
@app.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    response = supabase.table('animals').select('*').eq('id', id).execute()
    animal = response.data
    if not animal:
        abort(404, description="Animal not found")

    updated_animal = {
        'species': request.json.get('species', animal[0]['species']),
        'age': request.json.get('age', animal[0]['age']),
        'gender': request.json.get('gender', animal[0]['gender']),
        'special_requirements': request.json.get('special_requirements', animal[0]['special_requirements'])
    }

    supabase.table('animals').update(updated_animal).eq('id', id).execute()
    return jsonify(updated_animal)


# Delete an animal from Supabase
@app.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    response = supabase.table('animals').select('*').eq('id', id).execute()
    animal = response.data
    if not animal:
        abort(404, description="Animal not found")

    supabase.table('animals').delete().eq('id', id).execute()
    return jsonify({'result': 'Animal deleted'})

# Error handlers
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)

#########################################################################################################################
@app.route('/employees', methods=['GET'])
def get_employees():
    response = supabase.table('employees').select('*').execute()
    employees = response.data
    return jsonify(employees)



@app.route('/employees/<int:id>', methods=['GET'])
def get_employees_by_id(id):
    response = supabase.table('employees').select('*').eq('id', id).execute()
    employees = response.data
    if not employees:
        abort(404, description="employee not found")
    return jsonify(employees[0])

@app.route('/employees', methods=['POST'])
def add_employees():
    if not request.json or 'name' not in request.json:
        abort(400, description="Invalid request. 'name' is required")

    new_employee = {
        'name': request.json.get('name'),
        'email': request.json.get('email'),
        'phone_number': request.json.get('phone_number'),
        'role': request.json.get('role'),
        'schedule': request.json.get('schedule')
    }

    response = supabase.table('employees').insert(new_employee).execute()
    return jsonify(response.data[0]), 201

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    response = supabase.table('employees').select('*').eq('id', id).execute()
    employee = response.data
    if not employee:
        abort(404, description="employee not found")

    updated_employee = {
        'name': request.json.get('name', employee[0]['name']),
        'email': request.json.get('email', employee[0]['email']),
        'phone_number': request.json.get('phone_number', employee[0]['phone_number']),
        'role': request.json.get('role', employee[0]['role']),
        'schedule': request.json.get('schedule', employee[0]['schedule']),
    }

    supabase.table('employees').update(updated_employee).eq('id', id).execute()
    return jsonify(updated_employee)

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    response = supabase.table('employees').select('*').eq('id', id).execute()
    employee = response.data
    if not employee:
        abort(404, description="employee not found")

    supabase.table('employees').delete().eq('id', id).execute()
    return jsonify({'result': 'employee deleted'})

from unittest.mock import patch

# Get all employees from Supabase
# @app.route('/employees', methods=['GET'])
# def get_employees():
#     response = supabase.table('employees').select('*').execute()
#     employees = response.data
#     return jsonify(employees)


# # Get specific employee by ID from Supabase
# @app.route('/employees/<int:id>', methods=['GET'])
# def get_employee_by_id(id):
#     response = supabase.table('employees').select('*').eq('id', id).execute()
#     employees = response.data
#     if not employees:
#         abort(404, description="Employee not found")
#     return jsonify(employees[0])


# # Add a new employee to Supabase
# @app.route('/employees', methods=['POST'])
# def add_employee():
#     if not request.json or 'name' not in request.json:
#         abort(400, description="Invalid request. 'name' is required")

#     new_employee = {
#         'name': request.json.get('name'),
#         'email': request.json.get('email', ''),
#         'phone_number': request.json.get('phone_number', 'Unknown'),
#         'role': request.json.get('role', ''),
#         'schedule': request.json.get('schedule', '')
#     }

#     response = supabase.table('employees').insert(new_employee).execute()
#     return jsonify(response.data[0]), 201


# # Update existing employee in Supabase
# @app.route('/employees/<int:id>', methods=['PUT'])
# def update_employee(id):
#     response = supabase.table('employees').select('*').eq('id', id).execute()
#     employee = response.data
#     if not employee:
#         abort(404, description="Employee not found")

#     updated_employee = {
#         'name': request.json.get('name', employee[0]['name']),
#         'email': request.json.get('email', employee[0]['email']),
#         'phone_number': request.json.get('phone_number', employee[0]['phone_number']),
#         'role': request.json.get('role', employee[0]['role']),
#         'schedule': request.json.get('schedule', employee[0]['schedule'])
#     }

#     supabase.table('employees').update(updated_employee).eq('id', id).execute()
#     return jsonify(updated_employee)


# # Delete an employee from Supabase
# @app.route('/employees/<int:id>', methods=['DELETE'])
# def delete_employee(id):
#     response = supabase.table('employees').select('*').eq('id', id).execute()
#     employee = response.data
#     if not employee:
#         abort(404, description="Employee not found")

#     supabase.table('employees').delete().eq('id', id).execute()
#     return jsonify({'result': 'Employee deleted'})


# # Error handlers
# @app.errorhandler(404)
# def resource_not_found(e):
#     return jsonify(error=str(e)), 404

# @app.errorhandler(400)
# def bad_request(e):
#     return jsonify(error=str(e)), 400


# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, jsonify, request, abort
# import json
# import os

# app = Flask(__name__)

# def load_staffs():
#     if os.path.exists('staffs.json'):
#         with open('staffs.json', 'r') as file: # r untuk menulis data
#             return json.load(file)
#     return []

# def save_staffs(staffs): 
#     with open('staffs.json', 'w') as file: # w untuk write data
#         json.dump(staffs, file, indent=4)

# # Load existing animal data from JSON file or initialize an empty list
# def load_animals():
#     if os.path.exists('animals.json'):
#         with open('animals.json', 'r') as file: # r untuk menulis data
#             return json.load(file)
#     return []

# # Save animals data to the JSON file
# def save_animals(animals): 
#     with open('animals.json', 'w') as file: # w untuk write data
#         json.dump(animals, file, indent=4)

# @app.route('/', methods=['GET'])
# def home():
#     return '<p> hello world </p>'

# # Retrieve all animals
# @app.route('/animals', methods=['GET'])
# def get_animals():
#     animals = load_animals()
#     return jsonify(animals)

# # Retrieve a specific animal by ID
# @app.route('/animals/<int:id>', methods=['GET'])
# def get_animal_by_id(id):
#     animals = load_animals()
#     animal = next((a for a in animals if a['id'] == id), None) # id yg ijo db dan id yg kuning postman(req)
#     if animal is None:
#         abort(404, description="Animal not found")
#     return jsonify(animal)

# # Add a new animal
# @app.route('/animals', methods=['POST'])
# def add_animal():
#     if not request.json or 'species' not in request.json:
#         abort(400, description="Invalid request. 'species' is required")
    
#     species = request.json.get('species')
    
#     animals = load_animals()
#     for animal in animals:
#         if animal['species'] == species:
#             return jsonify({"message": "animal already exist"})
#     new_animal = {
#         'id': animals[-1]['id'] + 1 if animals else 1,
#         'species': request.json.get('species'),
#         'age': request.json.get('age', 0),
#         'gender': request.json.get('gender', 'Unknown'),
#         'special_requirements': request.json.get('special_requirements', '')
#     }
#     animals.append(new_animal)
#     save_animals(animals)
#     return jsonify(new_animal), 201

# # Update an existing animal
# @app.route('/animals/<int:id>', methods=['PUT'])
# def update_animal(id):
#     animals = load_animals()
#     animal = next((a for a in animals if a['id'] == id), None)
#     if animal is None:
#         abort(404, description="Animal not found")
    
#     if not request.json:
#         abort(400, description="Invalid request format")

#     animal['species'] = request.json.get('species', animal['species'])
#     animal['age'] = request.json.get('age', animal['age'])
#     animal['gender'] = request.json.get('gender', animal['gender'])
#     animal['special_requirements'] = request.json.get('special_requirements', animal['special_requirements'])

#     save_animals(animals)
#     return jsonify(animal)

# # Delete an animal
# @app.route('/animals/<int:id>', methods=['DELETE'])
# def delete_animal(id):
#     animals = load_animals()
#     animal = next((a for a in animals if a['id'] == id), None)
#     if animal is None:
#         abort(404, description="Animal not found")
    
#     animals.remove(animal)
#     save_animals(animals)
#     return jsonify({'result': 'Animal deleted'})


    
# ###########################################################################################################      
# # staff

# # GET
# @app.route('/employees', methods=['GET'])
# def get_staffs():
#     staffs = load_staffs()
#     return jsonify(staffs)

# # Retrieve a specific animal by ID
# @app.route('/employees/<int:id>', methods=['GET'])
# def get_staff_by_id(id):
#     staffs = load_staffs()
#     staff = next((a for a in staffs if a['id'] == id), None) # id yg ijo db dan id yg kuning postman(req)
#     if staff is None:
#         abort(404, description="ID not found")
#     return jsonify(staff)

# # POST
# @app.route('/employees', methods=['POST'])
# def add_staff():
#     if not request.json or 'name' not in request.json:
#         abort(400, description="Invalid request. 'name' is required")
    
#     name = request.json.get('name')
    
#     staffs = load_staffs()
#     for staff in staffs:
#         if staff['name'] == name:
#             return jsonify({"message": "name already exist"}), 400
#     new_staff = {
#         'id': staffs[-1]['id'] + 1 if staffs else 1,
#         'name': request.json.get('name'),
#         'email': request.json.get('email', ''),
#         'phone_number': request.json.get('phone_number', 'Unknown'),
#         'role': request.json.get('role', ''),
#         'schedule': request.json.get('schedule'),
#     }
#     staffs.append(new_staff)
#     save_staffs(staffs)
#     return jsonify(new_staff), 201

# # PUT
# @app.route('/employees/<int:id>', methods=['PUT'])
# def update_staff(id):
#     staffs = load_staffs()
#     staff = next((a for a in staffs if a['id'] == id), None)
#     if staff is None:
#         abort(404, description="staff not found")
    
#     if not request.json:
#         abort(400, description="Invalid request format")

#     staff['id'] = request.json.get('id', staff['id'])
#     staff['name'] = request.json.get('name', staff['name'])
#     staff['email'] = request.json.get('email', staff['email'])
#     staff['phone_number'] = request.json.get('phone_number', staff['phone_number'])
#     staff['role'] = request.json.get('role', staff['role'])
#     staff['schedule'] = request.json.get('schedule', staff['schedule'])

#     save_staffs(staffs)
#     return jsonify(staff)

# # Delete an animal
# @app.route('/employees/<int:id>', methods=['DELETE'])
# def delete_staff(id):
#     staffs = load_staffs()
#     staff = next((a for a in staffs if a['id'] == id), None)
#     if staff is None:
#         abort(404, description="staff not found")
    
#     staffs.remove(staff)
#     save_staffs(staffs)
#     return jsonify({'result': 'staff deleted'})


# # Error handlers
# @app.errorhandler(404)
# def resource_not_found(e):
#     return jsonify(error=str(e)), 404

# @app.errorhandler(400)
# def bad_request(e):
#     return jsonify(error=str(e)), 400

# if __name__ == '__main__':
#     app.run(debug=True)