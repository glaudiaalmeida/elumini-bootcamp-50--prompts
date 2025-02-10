from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.0-turbo"

def categoriza_produto(nome_produto, lista_categorias_possiveis):
    prompt_sistema = f"""
        Você é um categorizador de produtos.
        Você deve assumir as categorias presentes na lista abaixo.
    
        #Lista de categorias válidas
        {lista_categorias_possiveis.split(", ")}
    
        #Formato de saída
        Produto: Nome do Produto
        categoria: apresente a categoria do produto

        #Exemplo de saída
        Produto: Escova elétrica com recarga solar
        Categoria: Eletrônicos Verdes

    """
    resposta = cliente.chat.completions.create(
        messages = [
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": nome_produto
            }
        ],
        model = modelo,
        temperatura = 0,
        max_tokens = 100
    )

    return resposta.choices[0].message.content

categorias_validas = input("Informe as categorias possíveis separadas por vírgula: ")

while True:
    nome_produto = input("Informe o nome do produto: ")
    texto_resposta = categoriza_produto(nome_produto, categorias_validas)
    print(texto_resposta)
