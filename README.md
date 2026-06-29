# Computer-Architecture---IAS-Computer-Simulation
# English🇺🇸
# Português🇧🇷

# Simulador IAS - Guia de Instalação e Execução

## Requisitos

* Python 3.14 ou superior
* Biblioteca CustomTkinter
* Ambiente virtual Python (recomendado)

---
e
## Passo 1: Copiar o projeto para o computador

O projeto deve ser executado em um diretório do próprio sistema operacional.

Evite executar diretamente de:

* Pendrives
* Cartões SD
* Partições FAT32 ou exFAT

---

## Passo 2: Verificar a instalação do Python

Linux:

```bash
python3 --version
```

Windows:

```cmd
python --version
```

Caso o Python não esteja instalado, faça a instalação antes de prosseguir.

---

## Passo 3: Instalar suporte a ambientes virtuais (somente Linux)

sudo apt install python3.14-venv

Observação:
Usuários Windows podem pular este passo.

## Passo 3.1: Criar o ambiente virtual

Windows:
python -m venv venv

Linux:
python3 -m venv venv

## Passo 4: Ativar o ambiente virtual

Linux:

```bash
source venv/bin/activate
```

Windows:

```cmd
venv\Scripts\activate
```

Após a ativação, o terminal deverá exibir:

```text
(venv)
```

no início da linha de comando.

---

## Passo 5: Instalar as dependências

Com o ambiente virtual ativado:

```bash
pip install customtkinter
```

---

## Passo 6: Executar o programa

Com o ambiente virtual ativado:

Linux:

```bash
python3 Main.py
```

Windows:

```cmd
python Main.py
```

---

## Problemas Comuns

### Erro: ModuleNotFoundError: No module named 'customtkinter'

O ambiente virtual não está ativado ou a biblioteca não foi instalada.

Ative novamente o ambiente virtual:

```bash
source venv/bin/activate
```

e execute:

```bash
pip install customtkinter
```

### Erro ao criar o ambiente virtual

Verifique se o pacote de suporte ao venv está instalado:

```bash
sudo apt install python3.14-venv
```

### Erro ao executar diretamente de pendrive

Copie o projeto para uma pasta local do computador antes de criar o ambiente virtual.

---

## Autor

Projeto desenvolvido para a disciplina de Arquitetura de Computadores.

Simulador da arquitetura IAS com interface gráfica desenvolvida em Python utilizando CustomTkinter.

