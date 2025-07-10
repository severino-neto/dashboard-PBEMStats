# Dashboard - Ensino Médio da Paraíba

## 📊 Sobre o Projeto

Este dashboard interativo apresenta uma análise abrangente dos dados educacionais do ensino médio nos municípios da Paraíba, integrando informações do ENEM, SAEB, IDEB, PIB municipal e infraestrutura escolar para o período de 2017 a 2023.

## 🎯 Funcionalidades

### 📈 Visualizações Interativas
- **Médias por Área de Conhecimento**: Análise das médias do ENEM em Ciências da Natureza, Ciências Humanas, Linguagens e Códigos, Matemática e Redação
- **Comparação por Gênero**: Desempenho comparativo entre estudantes femininos e masculinos
- **PIB vs Desempenho**: Correlação entre PIB per capita municipal e desempenho educacional
- **IDEB vs Taxa de Aprovação**: Relação entre o Índice de Desenvolvimento da Educação Básica e taxa de aprovação
- **Infraestrutura Tecnológica**: Análise da infraestrutura tecnológica das escolas

### 🔍 Filtros Dinâmicos
- **Ano**: Seleção de dados de 2017 a 2023
- **Dependência Administrativa**: Federal, Estadual, Municipal ou Privada
- **Municípios**: Seleção múltipla de municípios específicos

### 📋 Ranking e Estatísticas
- Top 10 municípios por desempenho
- Cards com estatísticas resumo
- Tabela interativa com dados detalhados

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Dash**: Framework para aplicações web interativas
- **Plotly**: Biblioteca para visualizações interativas
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica

## 📁 Estrutura do Projeto

```
pb_ensino_medio_dashboard/
├── app.py                          # Aplicação principal (desenvolvimento local)
├── index.py                        # Aplicação configurada para Vercel
├── PB_EnsinoMedio_Stats.csv        # Dataset principal
├── requirements.txt                # Dependências Python
├── vercel.json                     # Configuração do Vercel
├── README.md                       # Documentação
└── .gitignore                      # Arquivos ignorados pelo Git
```

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pb-ensino-medio-dashboard.git
cd pb-ensino-medio-dashboard
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

4. Acesse no navegador:
```
http://localhost:8050
```

## 🌐 Deploy no Vercel

### Configuração Automática

1. Faça fork deste repositório
2. Conecte sua conta do Vercel ao GitHub
3. Importe o projeto no Vercel
4. O deploy será feito automaticamente

### Configuração Manual

1. Instale a CLI do Vercel:
```bash
npm i -g vercel
```

2. Faça login:
```bash
vercel login
```

3. Deploy:
```bash
vercel --prod
```

## 📊 Sobre os Dados

### Fontes de Dados
- **ENEM**: Médias por área de conhecimento e gênero
- **SAEB**: Notas de Matemática e Linguagens e Códigos
- **IDEB**: Índice de Desenvolvimento da Educação Básica
- **PIB Municipal**: Dados econômicos dos municípios
- **Censo Escolar**: Infraestrutura e recursos tecnológicos das escolas

### Período Coberto
2017 - 2023

### Granularidade
- Municipal
- Por dependência administrativa (Federal, Estadual, Municipal, Privada)
- Por gênero (quando aplicável)

## 🔍 Análises Possíveis

### Perguntas que o Dashboard Responde

1. **Qual a relação entre PIB municipal e desempenho no ENEM?**
2. **Municípios com melhor infraestrutura apresentam melhores resultados no SAEB?**
3. **Quais municípios apresentam maior crescimento no IDEB ao longo dos anos?**
4. **Existe correlação entre investimento público e qualidade da educação?**
5. **Qual dependência administrativa se destaca em desempenho?**
6. **Há desigualdade educacional entre os municípios?**

### Tipos de Análise Suportados

- **Análise Descritiva**: Estatísticas sobre desempenho escolar e infraestrutura
- **Análise Comparativa**: Comparação entre municípios e dependências administrativas
- **Análise Temporal**: Evolução dos indicadores ao longo dos anos
- **Análise de Correlação**: Relações entre variáveis socioeconômicas e educacionais

## 📈 Indicadores Principais

### Desempenho Educacional
- Médias do ENEM por área de conhecimento
- Notas do SAEB (Matemática e Linguagens)
- IDEB (Índice de Desenvolvimento da Educação Básica)
- Taxa de aprovação do 3º ano do ensino médio

### Indicadores Socioeconômicos
- PIB municipal
- PIB per capita
- Valor da administração pública

### Infraestrutura Escolar
- Acesso à internet
- Laboratórios de informática
- Equipamentos para alunos (desktop, portátil, tablet)
- Atendimento educacional especializado
- EJA no ensino médio

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Márcia Cristina Rafael de Lima**
- **Severino Pereira das Chagas Neto**

**Instituição**: Instituto Federal da Paraíba (IFPB)  
**Programa**: Mestrado Profissional em Tecnologia da Informação  
**Disciplina**: Ciência de Dados  

## 📞 Contato

Para dúvidas ou sugestões, entre em contato através dos issues do GitHub ou pelos emails institucionais.

---

**Desenvolvido com ❤️ para a educação paraibana**

