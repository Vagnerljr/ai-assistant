from langchain_community.document_loaders import (WebBaseLoader,CSVLoader, PyPDFLoader, TextLoader)

def carregaSite(url):
    loader = WebBaseLoader(url)
    listaDocumentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in listaDocumentos])
    return documento

def carregaCSV(caminho):
    loader = CSVLoader(caminho)
    listaDocumentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in listaDocumentos])
    return documento

def carregaPDF(caminho):
    loader = PyPDFLoader(caminho)
    listaDocumentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in listaDocumentos])
    return documento

def carregaTXT(caminho):
    loader = TextLoader(caminho)
    listaDocumentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in listaDocumentos])
    return documento