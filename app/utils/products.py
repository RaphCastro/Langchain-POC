import json


products_data = json.load(open("produtos.json"))


def get_product_info(product_name):
    json_base = products_data["produtos"]
    for product in json_base:
        if product_name.lower() in product["nome"].lower():
            return product
    return None


def get_products_by_category(category):
    products = []
    for product in products_data:
        print(category)
        if category.lower() in product["NomeProduto"].lower():
            products.append(product)
    return products


def return_combinations(json_data, nome_produto):
    try:
        produto_encontrado = None
        for produto in json_data["produtos"]:
            if produto["nome"] == nome_produto:
                produto_encontrado = produto
                break
        if produto_encontrado:
            return produto_encontrado["combinacoes-recomendadas"][0]
        else:
            return f"Produto '{nome_produto}' não encontrado no JSON."
    except json.JSONDecodeError as e:
        return f"Erro ao decodificar o JSON: {str(e)}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"


def find_product_with_lowest_price(json_data):
    try:
        products_json = json.loads(json_data)
        if "produtos" not in products_json or not products_json["produtos"]:
            print("No products found.")
            return None
        lowest_price_product = min(products_json["produtos"], key=lambda x: x["preco"])
        return lowest_price_product
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None
