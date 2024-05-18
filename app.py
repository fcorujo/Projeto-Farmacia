from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Dados de conexão
dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-SM62DP4\SQLEXPRESS;"
    "Database=FarmaciaSQL;"
    "Trusted_Connection=yes;" 
)

# Conectar ao banco de dados SQL Server
conn = pyodbc.connect(dados_conexao)
c = conn.cursor()


# Rotas...
@app.route('/')
def index():
    # Buscar todos os produtos
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    return render_template('index.html', produtos=produtos)

@app.route('/all_products')
def all_products():
    # Consultar todos os produtos disponíveis
    c.execute("SELECT nome, preco, quantidade FROM produtos")
    produtos = c.fetchall()
    return render_template('all_products.html', produtos=produtos)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        c.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, quantidade))
        conn.commit()
        return redirect('/')
    return render_template('add_product.html')

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        c.execute("UPDATE produtos SET nome = ?, preco = ?, quantidade = ? WHERE id = ?", (nome, preco, quantidade, id))
        conn.commit()
        return redirect('/')
    c.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    produto = c.fetchone()
    return render_template('edit_product.html', produto=produto)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    c.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
