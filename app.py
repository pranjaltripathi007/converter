import os
from flask import Flask, request, render_template, send_file, jsonify,redirect,url_for
import convertapi

app = Flask(__name__)

# Set the API key here
convertapi.api_credentials = 'secret_qwxF9qOrsrnCZdqW'  # Replace with your actual API key

# Set the upload folder
UPLOAD_FOLDER = ' UPLOAD_FOLDER'  # Folder where uploaded files will be saved
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/', methods=['GET', 'POST'])
def index():
    # Render the main page with the "Convert Now" button
    return render_template('index.html')
@app.route('/tools')
def tools():
    return render_template('tools.html')


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        # Get the file and output format from the form
        file = request.files['file']
        output_format = request.form['output_format']

        if file:
            # Save the uploaded file
            input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(input_file_path)

            try:
                # Convert the file using ConvertAPI
                result = convertapi.convert(output_format, {'File': input_file_path})

                # Save the converted file
                output_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], f"converted.{output_format}")
                result.file.save(output_file_path)

                # Return the converted file as a downloadable response
                return send_file(output_file_path, as_attachment=True)
            except Exception as e:
                # Handle conversion errors
                return jsonify({"error": str(e)}), 500

    # Render the conversion form (convert.html) for GET requests
    return render_template('convert.html')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Get the file and the desired output format from the form
#         file = request.files['file']
#         output_format = request.form['output_format']

#         if file:
#             # Save the uploaded file
#             input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(input_file_path)

#             try:
#                 # Convert the file using ConvertAPI
#                 result = convertapi.convert(output_format, {'File': input_file_path})
                
#                 # Save the converted file
#                 output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"converted.{output_format}")
#                 result.file.save(output_file_path)

#                 # Return the converted file as a response
#                 return send_file(output_file_path, as_attachment=True)
#             except Exception as e:
#                 # Catch any exceptions and return the error message
#                 return jsonify({"error": str(e)}), 500

#     # Render the upload form if it's a GET request
#     return render_template('index.html')
# @app.route('/convert', methods=['GET', 'POST'])
# def convert():
#     if request.method == 'POST':
#         # Handle the file upload and conversion logic here
#         file = request.files['file']
#         output_format = request.form['output_format']

#         # Simulate a conversion process
#         # Save the file or send it to an external API for conversion
#         # Example: conversion_logic(file, output_format)

#         # For now, redirect back to the form after submission
#         return redirect(url_for('index'))
#     return render_template('convert.html')

if __name__ == '__main__':
    app.run(debug=True)

