# Viradas por seção — 2026
Painel estático em português, adaptado para celular. Abra o site e pressione Carregar base nacional. Nenhuma contagem é exibida antes do processamento. Não há servidor de análise, telemetria ou envio dos arquivos selecionados.

Dados: https://votosecreto.com/dados/ — fornecedor atribui os dados ao TSE. Atribuição não constitui auditoria independente. SHA-256 do GZIP: 261f83fdc2a17ff4dcece9d2bcceced3a34dafb1a4507d3f283a89814463f1d2.

Os turnos são ligados por UF/município/zona/seção. Percentuais usam votos 13 + 22 como denominador. O filtro aplica o mesmo limite inclusivo nos dois sentidos. Duplicatas geram erro; seções sem par positivo são excluídas. Comparecimento/brancos/nulos são exibidos separadamente. O arquivo nacional é público; arquivos pessoais não fazem parte deste repositório.

Render: build `echo Static site`, publish `public`. Para servir localmente: `python3 -m http.server --directory public`.
