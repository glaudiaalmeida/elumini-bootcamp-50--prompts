from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
Modelo = "gpt-4"

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")
        
def salva(nome_do_arquivo, dados):
    try:
        with open(nome_do_arquivo, "w", enconding="utf-8") as arquivo:
            arquivo.write(dados)
    except IOError as e:
        print(f"Erro: {e}")

def analisador_sentimentos(produto):
    prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados nas avaliações.
        
        #Formato de Saída
        Nome do produto:
        Resumo das avaliações:
        Sentimento geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Pontos fortes: lista com 3 bullets
        Pontos fracos: lista com 3 bullets
    """
    
prompt_usuario = carrega(f"./dados/avaliacoes-{produto}.txt")
print(f"Analisando as avaliações do produto {produto}...")

lista_mensagens = [
    {
        "role": "system",
        "content": prompt_sistema
    },
    {
        "role": "user",
        "content": prompt_usuario
    }
]

try:
    resposta = client.chat.completions.create(
        messages=lista_mensagens,
        model=Modelo
    )


    texto_resposta = resposta.choices[0].message.content
    salva(f"./dados/analise-{produto}.txt", texto_resposta)
except openai.AutenticationError as e:
    print(f"Erro de Autenticação: {e}")
except openai.APIError as e:
    print(f"Erro de API: {e}")

lista_de_produtos = ["smartphone", "notebook", "tablet", "smartwatch", "fones de ouvido"]
for um_produto in lista_de_produtos:
    analisador_sentimentos(um_produto)