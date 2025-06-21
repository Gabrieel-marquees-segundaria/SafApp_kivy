# Leitor de Arquivos - SAF App

Um aplicativo Android desenvolvido com Kivy que demonstra o uso do Storage Access Framework (SAF) para acesso seguro ao armazenamento externo.

## 📱 Sobre o App

Este aplicativo permite ao usuário selecionar pastas no dispositivo Android e realizar operações básicas de arquivo (criar, ler) respeitando as políticas de segurança modernas do Android através do SAF.

## 🚀 Funcionalidades

- **Seleção de Pasta**: Utiliza o seletor nativo do Android para escolher uma pasta
- **Criação de Arquivo**: Cria um arquivo de texto (`exemplo.txt`) na pasta selecionada
- **Leitura de Arquivo**: Lê e exibe o conteúdo do arquivo criado
- **Interface Simples**: Interface minimalista com botões para cada ação

## 🛠️ Tecnologias Utilizadas

- **Kivy**: Framework Python para desenvolvimento de aplicativos multiplataforma
- **PyJNIus**: Biblioteca para interação com classes Java do Android
- **Storage Access Framework (SAF)**: API nativa do Android para acesso seguro a arquivos
- **Buildozer**: Ferramenta para compilação e empacotamento do app Android

## 📋 Pré-requisitos

- Python 3.x
- Buildozer instalado
- Android SDK configurado
- Dispositivo Android com API 21+ (Android 5.0+)

## 🔧 Instalação e Build

1. **Clone ou baixe os arquivos do projeto**

2. **Instale as dependências:**
   ```bash
   pip install buildozer kivy kivymd
   ```

3. **Build do APK:**
   ```bash
   buildozer android debug
   ```

4. **Instalar no dispositivo:**
   ```bash
   buildozer android deploy
   ```

## 📱 Como Usar

1. **Abra o aplicativo** no seu dispositivo Android

2. **Selecionar Pasta**: 
   - Toque em "Selecionar pasta"
   - Use o seletor nativo do Android para escolher uma pasta
   - O app solicitará permissão persistente para acessar a pasta

3. **Salvar Arquivo**:
   - Após selecionar uma pasta, toque em "Salvar arquivo"
   - O app criará um arquivo `exemplo.txt` com o conteúdo "Olá do Kivy via SAF!"

4. **Ler Arquivo**:
   - Toque em "Ler arquivo" para visualizar o conteúdo do arquivo criado
   - O texto será exibido na tela

## 🔒 Permissões

O app solicita as seguintes permissões:
- `READ_EXTERNAL_STORAGE`: Para leitura de arquivos
- `WRITE_EXTERNAL_STORAGE`: Para escrita de arquivos
- `INTERNET`: Permissão padrão do Kivy

## 📁 Estrutura do Projeto

```
projeto/
├── main.py              # Código principal do aplicativo
├── buildozer.spec       # Configurações de build do Buildozer
└── README.md           # Este arquivo
```

## 🔍 Detalhes Técnicos

### Storage Access Framework (SAF)

O app utiliza o SAF que é a abordagem recomendada pelo Google para acesso a arquivos no Android moderno. Principais vantagens:

- **Segurança**: O usuário controla explicitamente quais pastas o app pode acessar
- **Compatibilidade**: Funciona com provedores de armazenamento diversos (Drive, Dropbox, etc.)
- **Persistência**: As permissões são mantidas entre execuções do app

### Arquitetura do Código

#### Estrutura Principal (`main.py`)

```python
# Importações essenciais
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from jnius import autoclass, cast
from android import activity
```

**Classes Java Utilizadas:**
- `Intent`: Para comunicação entre atividades Android
- `Uri`: Para manipulação de URIs de recursos
- `PythonActivity`: Acesso à atividade principal do app
- `DocumentFile`: Manipulação de arquivos através do SAF

#### Fluxo de Funcionamento

1. **Seleção de Pasta (`select_folder`):**
   ```python
   intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
   self.activity.startActivityForResult(intent, REQUEST_CODE)
   ```
   - Cria um Intent para seleção de pasta
   - Inicia a atividade nativa do Android
   - Aguarda retorno através de `onActivityResult`

2. **Callback de Resultado (`on_activity_result`):**
   ```python
   uri = data.getData()
   self.activity.getContentResolver().takePersistableUriPermission(uri, flags)
   ```
   - Recebe a URI da pasta selecionada
   - Solicita permissão persistente para acesso
   - Armazena a URI para uso posterior

3. **Salvamento de Arquivo (`save_file`):**
   ```python
   DocumentFile = autoclass('androidx.documentfile.provider.DocumentFile')
   docFolder = DocumentFile.fromTreeUri(self.ctx, self.folderUri)
   newFile = docFolder.createFile("text/plain", "exemplo.txt")
   ```
   - Utiliza DocumentFile para criar novo arquivo
   - Especifica tipo MIME e nome do arquivo
   - Escreve conteúdo através de OutputStream

4. **Leitura de Arquivo (`load_file`):**
   ```python
   for f in docFolder.listFiles().toArray():
       if f.getName() == "exemplo.txt":
           fis = self.activity.getContentResolver().openInputStream(f.getUri())
   ```
   - Lista arquivos na pasta selecionada
   - Localiza arquivo específico por nome
   - Lê conteúdo através de InputStream

### Configuração do Build (`buildozer.spec`)

**Dependências Críticas:**
```ini
requirements = python3,kivy,kivymd,android,pyjnius
android.gradle_dependencies = androidx.documentfile:documentfile:1.0.1
```

**Configurações Android:**
- `android.api = 31`: API level para compatibilidade
- `android.archs = arm64-v8a, armeabi-v7a`: Arquiteturas suportadas
- Permissões necessárias para acesso ao armazenamento

### Padrões de Design Utilizados

#### Observer Pattern
```python
activity.bind(on_activity_result=self.on_activity_result)
```
O app utiliza binding de eventos para responder a resultados de atividades Android.

#### Callback Pattern
```python
btn_select.bind(on_press=lambda _: self.select_folder())
```
Botões utilizam callbacks para executar ações específicas.

### Tratamento de Erros

- **Verificação de Pasta Selecionada**: Antes de operações de arquivo
- **Validação de Resultado**: Verificação de `RESULT_OK` em callbacks
- **Controle de Fluxo**: Mensagens informativas para o usuário

### Limitações e Considerações

- **Dependência de Permissões**: Requer concessão de permissões pelo usuário
- **API Level**: Funciona apenas em Android 5.0+ (API 21+)
- **Tipo de Arquivo**: Exemplo limitado a arquivos de texto
- **Encoding**: Utiliza UTF-8 para leitura/escrita

## 🐛 Troubleshooting

### Problemas de Compilação

**App não compila**
- Verifique se todas as dependências estão instaladas: `pip install buildozer kivy kivymd`
- Certifique-se de que o Android SDK está configurado corretamente
- Verifique se a dependência `androidx.documentfile:documentfile:1.0.1` está no buildozer.spec

**Erro de PyJNIus**
```bash
# Se encontrar erros relacionados ao PyJNIus, tente:
buildozer android clean
buildozer android debug
```

### Problemas de Execução

**Permissões negadas**
- O app precisa de permissões de armazenamento nas configurações do Android
- Verifique se `READ_EXTERNAL_STORAGE` e `WRITE_EXTERNAL_STORAGE` estão concedidas
- Em Android 11+, pode ser necessário habilitar "Acesso a todos os arquivos"

**"Nenhuma pasta selecionada" não muda**
- Verifique se o callback `on_activity_result` está sendo chamado
- Teste em dispositivo físico (emulador pode ter limitações SAF)
- Confirme se o REQUEST_CODE está consistente (12345)

**Arquivo não encontrado**
- Certifique-se de ter selecionado uma pasta primeiro
- Tente salvar um arquivo antes de tentar ler
- Verifique se o nome do arquivo está correto: "exemplo.txt"

### Problemas Específicos do Código

**Erro ao acessar DocumentFile**
```python
# Se encontrar erro: androidx.documentfile not found
# Verifique se está no buildozer.spec:
android.gradle_dependencies = androidx.documentfile:documentfile:1.0.1
```

**Problemas de Encoding**
```python
# Para caracteres especiais, certifique-se do encoding:
fos.write("Texto com acentos: ção, ã".encode('utf-8'))
content = data.decode('utf-8')
```

**URI Permissions perdidas**
```python
# As permissões SAF podem ser perdidas. Para verificar:
resolver = self.activity.getContentResolver()
persistedUris = resolver.getPersistedUriPermissions()
# Implemente verificação se necessário
```

## 💡 Melhorias Possíveis

### Funcionalidades Adicionais

**Seletor de Tipo de Arquivo**
```python
# Implementar seleção de diferentes tipos de arquivo
def create_file_with_type(self, mime_type, filename):
    newFile = docFolder.createFile(mime_type, filename)
```

**Listagem de Arquivos**
```python
# Mostrar todos os arquivos da pasta
def list_all_files(self):
    files = []
    for f in docFolder.listFiles().toArray():
        files.append(f.getName())
    return files
```

**Operações Avançadas**
- Renomear arquivos
- Deletar arquivos  
- Criar subpastas
- Copiar/mover arquivos

### Melhorias de Interface

**Progress Bar**
```python
from kivy.uix.progressbar import ProgressBar
# Para operações de arquivo longas
```

**Dialogs Nativos**
```python
# Para confirmações e alertas
from kivy.uix.popup import Popup
```

**Lista de Arquivos**
```python
from kivy.uix.listview import ListView
# Para exibir arquivos da pasta
```

### Tratamento de Erros Avançado

**Try-Catch para Operações SAF**
```python
def safe_file_operation(self, operation):
    try:
        return operation()
    except Exception as e:
        self.label.text = f"Erro: {str(e)}"
        return None
```

**Validação de Permissões**
```python
def check_permissions(self):
    # Verificar se ainda temos acesso à pasta
    try:
        docFolder.listFiles()
        return True
    except:
        return False
```

## 📊 Exemplo de Uso Avançado

### Trabalhando com Diferentes Tipos de Arquivo

```python
# Salvar arquivo JSON
import json
data = {"nome": "João", "idade": 30}
json_content = json.dumps(data, ensure_ascii=False)
newFile = docFolder.createFile("application/json", "dados.json")

# Salvar imagem (se tiver dados binários)
newFile = docFolder.createFile("image/jpeg", "foto.jpg")
```

### Implementando Busca de Arquivos

```python
def find_files_by_extension(self, extension):
    found_files = []
    for f in docFolder.listFiles().toArray():
        if f.getName().endswith(extension):
            found_files.append(f)
    return found_files
```

## 📄 Licença

Este projeto é disponibilizado como exemplo educacional. Use livremente para aprender e desenvolver seus próprios projetos.

## 📚 Recursos Adicionais

- [Documentação oficial do Kivy](https://kivy.org/doc/stable/)
- [Guia do Storage Access Framework](https://developer.android.com/guide/topics/providers/document-provider)
- [PyJNIus Documentation](https://pyjnius.readthedocs.io/)
