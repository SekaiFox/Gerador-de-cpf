# 👨‍💻 Gerador de CPF para Ambientes de Teste

Uma aplicação web (Python + Streamlit) que gera números de CPF sinteticamente válidos para uso exclusivo em ambientes de teste e desenvolvimento.

---
### ⚠️ AVISO IMPORTANTE: USO EXCLUSIVO PARA TESTES
**Este projeto foi desenvolvido para fins acadêmicos e de teste de software (sandbox).**

Os CPFs gerados são **100% fictícios** e aleatórios. Eles **não** correspondem a pessoas reais. O objetivo é apenas gerar dados que passem em validações de formulário. O uso indevido desses dados é de responsabilidade exclusiva do usuário.
---

![Gerador_de_CPF_IF9pieYwTK](https://github.com/user-attachments/assets/5c45c85e-bac9-4a45-82ad-bc9db8fa9d12)


## 🎯 O Problema (Contexto de Desenvolvimento)

Ao testar formulários de cadastro, precisamos de dados que passem na validação do sistema. Usar CPFs de pessoas reais é uma violação grave da **LGPD (Lei Geral de Proteção de Dados)**. Inserir números aleatórios (ex: 123456789-00) falha, pois os sistemas modernos validam os dígitos verificadores.

## 💡 A Solução (Habilidade Técnica)

Este gerador cria números de CPF que passam na validação porque ele implementa corretamente o **Algoritmo de Módulo 11** para calcular os dois dígitos verificadores.

O processo:
1.  Gera 9 dígitos aleatórios.
2.  Calcula o primeiro dígito verificador (DV1) com base nos 9 iniciais.
3.  Calcula o segundo dígito verificador (DV2) com base nos 9 iniciais + DV1.
4.  Concatena e formata o resultado (XXX.XXX.XXX-XX).
5.  Permite a exportação em massa para Excel.

## 🛠️ Tecnologias Utilizadas
* **Python**
* **Streamlit**
* **Pandas** (para exportação para Excel)

## 🏁 Como Executar o Projeto

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/SekaiFox/Gerador-de-cpf.git](https://github.com/SekaiFox/Gerador-de-cpf.git)
    cd Gerador-de-cpf
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  Instale as dependências (crie um arquivo `requirements.txt`):
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o app Streamlit:
    ```bash
    streamlit run gerador_cpf.py
    ```

**Arquivo `requirements.txt`:**
