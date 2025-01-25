from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from aryn_sdk.partition import partition_file
from werkzeug.utils import secure_filename

# Flask app setup
app = Flask(__name__)
CORS(app)

# Configure Aryn API key
os.environ['ARYN_API_KEY'] = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsiZW1sIjoibXVoaXJ3ZWpAdWNpLmVkdSIsImFjdCI6IjQ3ODQyODE0MDcyMiJ9LCJpYXQiOjE3Mzc3ODIxNDB9._tnOlKs7grs-UccASlKHIUCT3ew8MYIA8u_ut6cuggY2nY6Gc5KSF7Ek9LQLWLeK1RCmQF-flkUUNNLlgD73DA"

# Allowable file extensions
ALLOWED_EXTENSIONS = {'pdf'}

# Check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_with_aryn(file_path):
    """
    Process a file with Aryn SDK and return the results
    
    Args:
        file_path (str): Path to the file to be processed
        
    Returns:
        dict: Results from Aryn processing
        
    Raises:
        Exception: If processing fails
    """
    try:
        result = partition_file(file_path)
        
        # Print the results for debugging
        print("Aryn Processing Results:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        return result
    except Exception as e:
        print(f"Error in Aryn processing: {str(e)}")
        raise

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    # Check for username in request
    username = request.form.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    
    print(f"Received username: {username}")
    '''

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save the file temporarily
            filename = secure_filename(file.filename)
            temp_path = os.path.join('temp', filename)
            os.makedirs('temp', exist_ok=True)
            file.save(temp_path)
            
            # Process with Aryn using helper function
            # result = process_with_aryn(temp_path)
            
            # Clean up temp file
            os.remove(temp_path)
            
            # Include username in response
            return jsonify({
                'message': 'File processed successfully',
                'username': username,
                # 'result': result
            }), 200
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return jsonify({'error': 'Error processing file'}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400
    '''
@app.route('/api/retrieve_loans', methods=['GET'])
def retrieve_loans():
    try:
        # Get username from query parameters
        username = request.args.get('username')
        
        # Connect to the database
        conn = sqlite3.connect('loandb.db')
        cursor = conn.cursor()
        
        # Modify query to filter by username if provided
        if username and username.lower() != 'admin':
            cursor.execute("SELECT * FROM loan WHERE username = ?", (username,))
        else:
            cursor.execute("SELECT * FROM loan")  # Admin sees all loans
        
        # Get column names from cursor description
        columns = [description[0] for description in cursor.description]
        
        # Fetch all rows
        loans = cursor.fetchall()
        
        # Convert to list of dictionaries for JSON serialization
        loans_list = []
        for loan in loans:
            loan_dict = dict(zip(columns, loan))
            loans_list.append(loan_dict)
            
        conn.close()

        return jsonify({
            'message': 'Loans retrieved successfully',
            'loans': loans_list
        }), 200
        
    except Exception as e:
        print(f"Error retrieving loans: {str(e)}")
        return jsonify({'error': 'Error retrieving loans'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    

    
