import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from loader import *
import tempfile
from langchain.prompts import ChatPromptTemplate

# Tipos e modelos disponíveis
tipoArquivoValido = ['PDF', 'CSV', 'WebSite']
modelosConfig = {
    'Groq': {
        'modelos': ['llama3-70b-8192', 'llama3-8b-8192', 'mixtral-8x7b-32768'],
        'chat': ChatGroq,
    },
}

# Inicializa memória no session_state
if 'memoria' not in st.session_state:
    st.session_state['memoria'] = ConversationBufferMemory()

# Carrega o conteúdo do arquivo
def carregaArquivo(tipoArquivo, arquivo):
    if tipoArquivo == 'WebSite':
        documento = carregaSite(arquivo)
    elif tipoArquivo == 'CSV':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nomeTemp = temp.name
        documento = carregaCSV(nomeTemp)
    elif tipoArquivo == 'PDF':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nomeTemp = temp.name
        documento = carregaPDF(nomeTemp)
    else:
        documento = "Tipo de arquivo não suportado."
    return documento


# Carrega o modelo e prepara a cadeia de conversação
def carregaModelo(provedor, modelo, apiKey, tipoArquivo, arquivo):
    try:
        documento = carregaArquivo(tipoArquivo, arquivo)

        if "Just a moment..." in documento:
            st.warning("O conteúdo do site não pôde ser carregado corretamente. Tente novamente.")
            return

        system_message = f'''Você é um assistente amigável chamado VagnerGPT. Você possui acesso às seguintes informações vindas de um documento do tipo {tipoArquivo}:
        ####
        {documento}
        ####
        Utilize as informações fornecidas para basear as suas respostas.
        Sempre que houver $ em sua saída, substitua por S.

        Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue", sugira ao usuário carregar novamente o modelo.
        '''

        template = ChatPromptTemplate.from_messages([
            ('system', system_message),
            ('placeholder', '{chat_history}'),
            ('user', '{input}')
        ])

        chat = modelosConfig[provedor]['chat'](model=modelo, api_key=apiKey)
        chain = template | chat
        st.session_state['chain'] = chain

    except Exception as e:
        st.error(f"Erro ao carregar modelo ou documento: {e}")


# Página principal do chat
def pagina_chat():
    st.header('🤖 Welcome to VagnerGPT', divider=True)
    chain = st.session_state.get('chain')

    if chain is None:
        st.error('Carregue o modelo antes de conversar.')
        st.stop()

    memoria = st.session_state['memoria']

    # Exibe o histórico
    for mensagem in memoria.buffer_as_messages:
        chat_msg = st.chat_message(mensagem.type)
        chat_msg.markdown(mensagem.content)

    input_usuario = st.chat_input('Talk to me')

    if input_usuario:
        st.chat_message('human').markdown(input_usuario)

        # Executa o modelo e escreve a resposta em streaming
        resposta_stream = chain.stream({'input': input_usuario, 'chat_history': memoria.buffer_as_messages})
        resposta_chat = st.chat_message('ai')
        resposta_completa = resposta_chat.write_stream(resposta_stream)

        # Salva no histórico da memória
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta_completa)

        st.session_state['memoria'] = memoria


# Sidebar de configuração
def sidebar():
    tabs = st.tabs(['📁 File Upload', '⚙️ Model Selection'])

    with tabs[0]:
        tipoArquivo = st.selectbox('Select source type', tipoArquivoValido)
        if tipoArquivo == 'WebSite':
            arquivo = st.text_input('Enter website URL')
        elif tipoArquivo == 'CSV':
            arquivo = st.file_uploader('Upload CSV file', type=['.csv'])
        elif tipoArquivo == 'PDF':
            arquivo = st.file_uploader('Upload PDF file', type=['.pdf'])
        else:
            arquivo = None

    with tabs[1]:
        provedor = st.selectbox('Select provider', list(modelosConfig.keys()))
        modelo = st.selectbox('Select model', modelosConfig[provedor]['modelos'])
        apiKey = st.text_input('Enter your API key', type='password')

    if st.button('🚀 Load Model'):
        if not arquivo:
            st.warning("Você precisa fornecer um arquivo ou URL.")
        else:
            with st.spinner("Carregando modelo e documento..."):
                carregaModelo(provedor, modelo, apiKey, tipoArquivo, arquivo)


# Função principal
def main():
    with st.sidebar:
        sidebar()
    pagina_chat()


if __name__ == '__main__':
    main()
