# 🧾 Extrator de Dados XML

Projeto desenvolvido em Python para facilitar a filtragem e extração de informações de arquivos XML de Nota Fiscal Eletrônica (NFe), com uma interface moderna e amigável.

## 🚀 Funcionalidades

- Leitura automática de arquivos XML de NFe;
- Extração dos seguintes dados do **destinatário**:
  - Nome Fantasia;
  - CNPJ;
  - Número da Nota;
- Filtros personalizáveis para localizar arquivos XML com base nesses dados;
- Cópia automática dos arquivos filtrados para uma **pasta de destino**;
- Interface gráfica intuitiva para facilitar o uso, mesmo sem conhecimento técnico.

## 🛠 Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- `tkinter` (interface gráfica)
- `xml.etree.ElementTree` (manipulação XML)
- `os`, `shutil`, `re`, `pathlib` e outras bibliotecas padrão

## 📦 Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/extrator-de-dados-xml.git
   cd extrator-de-dados-xml
   ```

2. Instale os requisitos (se houver):
   > ⚠️ Nenhuma dependência externa necessária — apenas Python instalado.

3. Execute o programa:
   ```bash
   python extrator.py
   ```

4. Use a interface para:
   - Escolher a pasta com os XMLs;
   - Inserir os filtros desejados (Nome Fantasia, CNPJ, Número da Nota);
   - Definir a pasta de destino;
   - Clicar em "Filtrar" para iniciar a extração.

## 📁 Estrutura do Projeto

```
extrator-de-dados-xml/
├── visuais.py
├── utils.py
├── filtro_xml.py
├── interface_grafica.py
├── README.md
```

## 📌 Observações

- O projeto foi feito com foco em simplicidade e produtividade.
- Ideal para empresas ou usuários que precisam organizar grandes quantidades de XMLs de NFe.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

💡 **Sugestões e melhorias são bem-vindas!**
