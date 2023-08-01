from flask import Flask, jsonify

app = Flask(__name__)

books = [
    {
    'id' : 1,
    'title' : 'El señor de los anillos',
    'author' : 'J. R. R. Tolkien'
    },
    {
    'id' : 2,
    'title' : '1984',
    'author' : 'George Orwell'
    }
]

# Creamos una ruta para la API
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books' : books})

if __name__ == '__main__':
    app.run(debug=True)
