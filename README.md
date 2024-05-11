# AIGeminiBot - Um Chatbot inteligente alimentado pela API do Gemini 1.5 Pro
AIGeminiBot é um projeto que demonstra o poder da API Gemini Pro da Google para criar um chatbot super inteligente.

## Características:
 - Conversas Naturais: AIGeminiBot utiliza o modelo de linguagem avançado do Gemini Pro para gerar respostas de texto que parecem naturais e humanas.
 - Personalizável: Você pode personalizar o AIGeminiBot para ter diferentes personalidades, tons e estilos de conversação.
 - Fácil de Usar: O código é bem documentado e fácil de entender, tornando simples a integração com outras aplicações ou a criação de novos bots.

## Como Funciona:
O código Python utiliza a biblioteca da API Gemini Pro por meio de comando POST e GET para enviar prompts de texto ao modelo. O modelo de linguagem do Gemini processa o prompt e gera uma resposta textual.
A resposta é então exibida para o usuário.

## Utilização:
AIGeminiBot pode ser usado para uma variedade de propósitos, incluindo:
- Entretenimento: Criar bots divertidos para interação casual.
- Educação: Desenvolver bots que podem responder a perguntas e fornecer informações.
- Atendimento ao Cliente: Automatizar respostas a perguntas frequentes de clientes.

## Instalação das dependências

1. Realize o clone do repositório em alguma pasta <path> ou baixe o .zip:
```shell
cd <path>
git https://github.com/Machally/AIGeminiBot.git
```

2. Crie um ambiente virtual python 
```shell
python -m venv venv
```
e em seguida ative o venv:
```shell
source venv/bin/activate
```
3. Instale as dependências do projeto
```shell
pip install -r requirements.txt
```

4. Instalar o ngrok (via chocolatey)
Verifique a instalação do chocolatey:
```shell
choco -v
```
Caso não esteja instalado, um cmd (prompt de comando) do windows como administrador e execute o comando:
```shell
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```

Crie uma conta no site da [ngrok](https://ngrok.com/) e siga as instruções para instalação em [get-started/setup](https://dashboard.ngrok.com/get-started/setup/windows), onde <ngrok_token> é o token da sua conta ngrok:

```shell
choco install ngrok
```
```shell
ngrok config add-authtoken <ngrok_token>
```
## Criação de um Bot Telegram com @BotFather

1. No telegram busque por @BotFather (verifique se tem o selo de verificado ao lado da foto). 
2. Crie um novo Bot com o comando /newbot
3. Especifique um nome para o Bot
4. Especifique um username para o bot. O nome deve terminar em 'bot'. Ex.: AIGeminiEx_bot
5. Copie o token para acesso HTTP API. Crie um arquivo .env na pasta app e adicione a entrada substituindo <token> pela código obtido no @BotFather e <bot_user_name> pelo username especificado:

```shell
bot_token=<token>
bot_user_name=<bot_user_name>
```
Obtenha uma API key para o Gemini no [Google AI Studio](https://aistudio.google.com/) em Get API key e adicione também a entrada no arquivo .env, substituindo <Google_api_key> pela chave gerada:

```shell
GOOGLE_API_KEY=<Google_api_key>
```
6. Abra a conversa com o Bot clicando no link fornecido pelo @BotFather t.me/<bot_user_name> e inicie a conversa clicando em 'start'

## Inicialização da aplicação ngrok 
em um terminal execute o comando:
```shell
ngrok http 5000
```
Neste terminal será apresentado uma url da aplicação ngrok. Copie a url e substitua no comando a seguir em <ngrok_url> e substitua <bot_token> pelo respectivo token salvo no arquivo .env:
```shell
curl -X POST "https://api.telegram.org/bot<bot_token>/setWebhook?url=<ngrok_url>"
```
Caso não seja reconhecido o comando curl no windows, veja como instalar o comando [aqui](https://ramonduraes.net/2021/04/25/como-instalar-o-curl/), ou execute a url completa em uma janela do navegador web.

## Executar o a aplicação com o Flask
em um terminal com o venv habilitado, execute o comando:

```shell
python main.py
```

