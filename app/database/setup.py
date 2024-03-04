import sqlite3


def generate_database(nome_banco='main.db'):
    # Conectar ao banco de dados (será criado se não existir)
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS conversations (
        id_conversation INTEGER PRIMARY KEY,
        step_conversation INTEGER,
        answer TEXT,
        prompt TEXT,
        messages TEXT
    );
    '''
    create_sale_choice_table_query = '''
    CREATE TABLE IF NOT EXISTS sale_choice (
        id INTEGER PRIMARY KEY,
        discounted_product TEXT,
        discounted_product_price REAL,
        chosen_product TEXT,
        chosen_product_price REAL
    );
    '''
    cursor.execute(create_table_query)
    cursor.execute(create_sale_choice_table_query)

    conn.commit()
    conn.close()

generate_database()