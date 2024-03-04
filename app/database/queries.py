import sqlite3


def insert_conversation(step_conversation="greet", db_name="main.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = "INSERT INTO conversations (step_conversation) VALUES (?);"
    cursor.execute(query, (step_conversation,))
    conn.commit()
    id_conversation = cursor.lastrowid
    conn.close()
    return id_conversation


def get_step(id_conversation=1, db_name="main.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = "SELECT step_conversation FROM conversations WHERE id_conversation = ?;"
    cursor.execute(query, (id_conversation,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


def update_step(new_step, id_conversation=1, db_name="main.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = f"UPDATE conversations SET step_conversation = '{new_step}' WHERE id_conversation = ?;"
    cursor.execute(query, (id_conversation,))
    conn.commit()
    conn.close()


def get_conversation(id_conversation, db_name="main.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = "SELECT * FROM conversations WHERE id_conversation = ?;"
    cursor.execute(query, (id_conversation,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def insert_sale_choice(
    discounted_product,
    discounted_product_price,
    chosen_product,
    chosen_product_price,
    nome_banco="main.db",
):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    query = """
    INSERT INTO sale_choice (
        discounted_product, discounted_product_price, chosen_product, chosen_product_price
    ) VALUES (?, ?, ?, ?);
    """
    cursor.execute(
        query,
        (
            discounted_product,
            discounted_product_price,
            chosen_product,
            chosen_product_price,
        ),
    )
    conn.commit()
    id_sale_choice = cursor.lastrowid
    conn.close()
    return id_sale_choice


def update_chosen_product(
    id_sale_choice,
    new_chosen_product,
    new_chosen_product_price,
    nome_banco="main.db",
):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    query = """
    UPDATE sale_choice
    SET chosen_product = ?, chosen_product_price = ?
    WHERE id = ?;
    """
    cursor.execute(
        query, (new_chosen_product, new_chosen_product_price, id_sale_choice)
    )
    conn.commit()
    conn.close()


def select_all_sale_choices(nome_banco="main.db"):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    query = "SELECT * FROM sale_choice;"
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado[0]
