# Sistema de Identificação e Autenticação Biométrica

Este projeto é um sistema de identificação e autenticação biométrica utilizando impressões digitais para restringir o acesso a informações sensíveis. Ele foi desenvolvido como parte da atividade prática supervisionada (APS) da disciplina de Processamento de Imagem e Visão Computacional (PIVC) no curso de Ciência da Computação da Universidade Paulista – UNIP.

## 📌 Funcionalidades

- Captura e processamento de imagens de impressões digitais.
- Extração de características e comparação com um banco de dados de usuários.
- Autenticação baseada em níveis de acesso.
- Interface web para login e gerenciamento de usuários.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Frameworks e Bibliotecas:**
  - Flask (para a interface web)
  - OpenCV (para processamento de imagens)
  - NumPy (para manipulação de matrizes)
  - Face Recognition (para reconhecimento biométrico)

## 📦 Dependências

Antes de rodar o projeto, instale as dependências listadas no arquivo `requirements.txt`.  

Para instalá-las, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

Aqui estão as dependências do projeto:

```txt
blinker==1.9.0
certifi==2025.1.31
charset-normalizer==3.4.1
click==8.1.8
colorama==0.4.6
filelock==3.17.0
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
fsspec==2025.2.0
greenlet==3.1.1
idna==3.10
imageio==2.37.0
imageio-ffmpeg==0.6.0
itsdangerous==2.2.0
Jinja2==3.1.5
lazy_loader==0.4
llvmlite==0.44.0
MarkupSafe==3.0.2
more-itertools==10.6.0
mpmath==1.3.0
networkx==3.4.2
numba==0.61.0
numpy==2.1.3
openai-whisper @ git+https://github.com/openai/whisper.git@517a43ecd132a2089d85f4ebc044728a71d49f6e
opencv-python-headless==4.11.0.86
packaging==24.2
pillow==11.1.0
psutil==6.1.1
regex==2024.11.6
requests==2.32.3
scikit-image==0.25.1
scipy==1.15.2
setuptools==75.8.0
SQLAlchemy==2.0.38
sympy==1.13.1
tifffile==2025.1.10
tiktoken==0.8.0
torch==2.6.0
torchaudio==2.6.0
torchvision==0.21.0
tqdm==4.67.1
typing_extensions==4.12.2
urllib3==2.3.0
Werkzeug==3.1.3
wheel==0.45.1
```

## 🚀 Como Executar o Projeto

### 🔧 Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado e de que todas as dependências do `requirements.txt` foram instaladas corretamente.

### ▶️ Executando a aplicação

1. Clone este repositório:
   ```bash
   git clone https://github.com/galdino013/APS2024.git
   cd APS2024
   ```

2. Execute o servidor Flask:
   ```bash
   python run.py
   ```

3. Acesse no navegador:
   ```
   http://127.0.0.1:5000
   ```

## 👥 Autores

- **Igor Galdino dos Santos**
- **Leonardo Marana**
- **Lukas Andrade Nascimento**
- **Pedro Henrique de Souza Putinatti**


## 📜 Créditos e Licença

Este projeto utiliza código do repositório [Fingerprint-Enhancement-Python](https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python), desenvolvido por Utkarsh Deshmukh.  

O código original está licenciado sob a **BSD 2-Clause License**, disponível [aqui](https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python/blob/master/LICENSE).
---
Desenvolvido como parte do projeto acadêmico da Universidade Paulista – UNIP 🎓
