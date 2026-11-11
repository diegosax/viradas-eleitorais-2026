# Viradas por seção — Eleições 2026

Painel estático em português, adaptado para celular. Os resultados oficiais são carregados automaticamente; não é necessário baixar ou selecionar arquivos. Não há telemetria ou envio de arquivos locais.

## Fonte e reprodução
Fonte: https://dadosabertos.tse.jus.br/dataset/resultados-2026 (TSE, licença Creative Commons Atribuição).
Arquivos originais:
- https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip
- https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_secao/detalhe_votacao_secao_2026.zip

Baixe os dois ZIPs para uma pasta e execute `python3 prepare_data.py /caminho/da/pasta`. A saída `public/data/results.json` inclui os hashes SHA-256 dos arquivos de origem, totais de votos, contagens de exclusão e contagens nas duas direções para cada limite. O arquivo compactado logicamente preserva as contagens municipais de todas as seções comparáveis e as seções com reversão de pelo menos 55/45, suficientes para todos os filtros oferecidos.

UF/município/zona/seção identificam o par. O denominador usa apenas os votos 13 + 22 em cada turno. Limites inclusivos, cálculo sem arredondamento. Excluem-se seções anuladas, não instaladas, sem par com soma positiva ou sem detalhe de apuração nos dois turnos. Comparecimento, brancos e nulos são apresentados separadamente. Uma reversão isolada não demonstra irregularidade.

Render: build `sh build.sh`, publish `public`. Prévia local: `python3 -m http.server --directory public`.

Somente código e resultados públicos agregados integram este repositório. Os ZIPs originais e arquivos de teste não são publicados.
