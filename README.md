# AutoZap

**AutoZap** é uma automação web desenvolvida em Python para facilitar o envio de mensagens de texto ou arquivos em massa para uma lista de contatos previamente definida. Diferente da função de listas de transmissão do WhatsApp, o **AutoZap** permite o envio mesmo que o contato destinatário não tenha o número de origem salvo.

---

## 📋 Funcionalidades

- **Envio em Massa de Mensagens de Texto (AutoZap Text):**

  - Envia mensagens de texto personalizadas para cada número contido em uma planilha Excel.

- **Encaminhamento de Arquivos (AutoZap Arquivos):**
  - Encaminha arquivos ou mensagens anexadas a um grupo do WhatsApp para contatos contidos na planilha Excel, em lotes de 5 contatos por vez.

---

## ✅ Requisitos

Para utilizar o **AutoZap**, é necessário:

- **Planilha em Excel:** No formato adequado, contendo os contatos dos destinatários.
- **Navegador Chrome:** Deve estar instalado no computador.
- **Smartphone:** Para login no WhatsApp Web.
- **Grupo do WhatsApp:** Necessário para o envio de arquivos (mais detalhes abaixo).

---

## ⚙️ Configuração e Instalação

Para facilitar o uso por outros membros da equipe, o programa foi disponibilizado como executável. Siga as instruções abaixo:

### Passo a Passo de Uso

1. **Preparar a Planilha de Contatos:**

   - Crie uma planilha no Excel com os contatos no formato específico:
     - **AutoZap - Arquivos:** Coluna "A" com os números **sem o DDD e sem o dígito 9 adicional** (ex.: `80808080`).
       Exemplo de como deve ficar:
       ![Exemplo Planilha AutoZap Arquivos](prints/PlanArq.png)
     - **AutoZap - Texto:** Coluna "A" com os números **com DDD e o dígito 9** (ex.: `61980808080`).
       Exemplo de como deve ficar:
       ![Exemplo Planilha AutoZap Arquivos](prints/PlanText.png)
   - Certifique-se de que a primeira linha da coluna "A" contém o cabeçalho `Celular`.

2. **AutoZap - Arquivos:**

   - No WhatsApp do celular, crie um grupo chamado `Robô` (exatamente como está escrito) e envie a mensagem/arquivo que será encaminhado.
   - Exemplo de grupo:
     <img src="prints/GroupExample.png.png" alt="Exemplo de grupo" width="250" style="vertical-align: middle; margin-top: 10px; margin-bottom: 10px;">
   - Exclua mensagens anteriores no grupo, deixando apenas a última que será enviada.

3. **Executar o Programa:**

   - Localize o executável (`AutoZap_arquivosV2.exe` ou `AutoZap_text.exe`).
   - Clique duas vezes para iniciar.
   - Selecione a planilha de contatos quando solicitado.
   - Faça login no WhatsApp Web escaneando o QR Code.
   - O envio será iniciado automaticamente.

4. **Finalizar:**
   - Ao final, o programa exibirá uma mensagem de conclusão. Verifique se todos os contatos receberam a mensagem.
     - Tela final:
       <img src="prints/Conclusion.png" alt="Exemplo Planilha AutoZap Arquivos" width="250" style="vertical-align: middle; margin-top: 10px; margin-bottom: 10px;">

---

## 🗂 Estrutura de Arquivos

O projeto contém os seguintes arquivos principais:

- `AutoZap_arquivosV2.py`: Automação para envio de arquivos.
- `autoZap_text.py`: Automação para envio de mensagens de texto.

---

## 🛠 Tecnologias Utilizadas

- **Python:** Linguagem principal para o desenvolvimento.
- **Bibliotecas:** Selenium, pandas, entre outras.
- **Navegador Chrome:** Para acesso ao WhatsApp Web.

---

## 📝 Licença

Este projeto está sob a **Licença de Uso Restrito**. O uso comercial é proibido sem autorização prévia. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para sugestões ou melhorias, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

---

## 📞 Contato

Dúvidas ou solicitações podem ser enviadas para:  
**Erick Cezar**  
erickcezar07@gmail.com

---
