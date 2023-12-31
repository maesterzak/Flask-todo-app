from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from models import db, Todo, Category



app = Flask(__name__)
app.config.from_object('config')
app.app_context().push()
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    category_param = request.args.get('category')  # Retrieves the 'category' parameter from the request URL query string
    global todos  # Declares 'todos' as a global variable to be accessed and modified within the function
    global current_category  # Declares 'current_category' as a global variable

    if category_param:  # Checks if a 'category' parameter exists in the request URL
        todos = Todo.query.filter_by(category=category_param).all()  # Retrieves all Todo items filtered by the category parameter
        current_category = int(category_param)  # Sets the current category to the integer value of the category parameter
    else:  # Executes if no 'category' parameter is present in the request URL
        todos = Todo.query.all()  # Retrieves all Todo items
        current_category = "All"  # Sets the current category to "All"

    categories = Category.query.all()  # Retrieves all categories from the database

    # Renders the 'index.html' template with the retrieved data (todos, categories, current_category)
    return render_template('index.html', todos=todos, categories=categories, current_category=current_category)


@app.route('/todos', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        description = request.form['description']
        category = request.form['category']
        new_entry = Todo(description=description, category=category)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/categories', methods=['POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['categoryname']
        new_entry = Category(name=name)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
    


@app.route('/todos/<int:id>', methods=['PATCH'])
def update_todo(id):
    try:
        # Fetch the todo with the specified ID from the database
        todo = Todo.query.get(id)
        
        # Check if the todo exists
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404  # Return a 404 error if todo not found
        
        # Assuming your request body contains JSON data with the 'description' field to update
        data = request.json
        
        # Check if the 'description' field is present in the request data
        if 'description' in data:
            # Update the description of the todo with the new value
            todo.description = data['description']
        
        db.session.commit()  # Commit changes to the database
        
        # Return a success message upon successful update
        return jsonify({'message': 'Todo updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()  # Rollback changes if an exception occurs
        return jsonify({'error': str(e)}), 500  # Return an error response with status code 500 for any exceptions
    
 
@app.route('/categories/<int:id>', methods=['PATCH'])
def update_category(id):
    try:     
        category = Category.query.get(id)
        if not category:
          
            return jsonify({'error': 'Category not found'}), 404
        
        # Assuming your request body contains JSON data with the 'description' field to update
        data = request.json
        if 'name' in data:
            category.name = data['name']
        
        db.session.commit()
        return jsonify({'message': 'Category updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()  # Rollback changes if an exception occurs
        return jsonify({'error': str(e)}), 500  # Return an error response with status code 500    
    

@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    try:
        # Fetch the todo with the specified ID from the database
        todo = Todo.query.get(id)
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404  # Return a 404 error if todo not found
        
        # Delete the fetched todo from the database
        db.session.delete(todo)
        
        # Commit the changes to the database
        db.session.commit()
        
    
        # Return a success message with status code 204 (No Content)
        return jsonify({'message': 'Success!'}), 204
    
    except Exception as e:
        db.session.close()  # Close the session in case of an exception
        # Optionally, abort with a 404 error code or handle the exception as needed
        # abort(404)


@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    try:
        # Retrieve the category using the provided ID from the URL
        category = Category.query.get(id)
        
        # Check if the category exists
        if category:
            # Delete the category from the database
            db.session.delete(category)
            db.session.commit()
            
            # Return a success message and status code 204 (no content)
            return jsonify({'message': 'Category deleted successfully'}), 204
        else:
            # If category does not exist, return a 404 error
            return jsonify({'error': 'Category not found'}), 404
    except Exception as e:
        # Rollback changes if any exception occurs
        db.session.rollback()
        
        # Return an error message and status code 500 (server error)
        return jsonify({'error': str(e)}), 500        


if __name__ == '__main__':
    app.run()