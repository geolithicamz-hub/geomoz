# GeoMoz: proveniência e catálogo de fontes externas

Esta documentação refere-se **à biblioteca** GeoMoz (Python e R), nunca à
aplicação GeoMoz-Explorer.

## O que foi implementado

`geomoz.list_source_datasets()` e `geomoz.get_source_dataset("...")`
expõem um catálogo **apenas de metadados**. Esta alteração não incorpora,
descarrega nem redistribui qualquer dado do MIS/MIREME ou da DataPortal.
O acesso público a um serviço não constitui autorização de redistribuição.
`redistribution="permission_unverified"` e
`access="reference_only"` são intencionais.

Exemplo:

```python
import geomoz
for source in geomoz.list_source_datasets(category="geology"):
    print(source["title"], source["producer"], source["url"])
print(geomoz.get_source_dataset("data4moz_soils_1995")["year"])
```

## Proveniência original da geologia

O produtor/fonte original indicado pelo mantenedor para o dataset geológico
GeoMoz é **MIS/MIREME**, não a GEOLÍTHICA. A biblioteca é software para acesso,
processamento e exploração. A camada pública Seamless Geology 250K expõe
`code2006`, `Legend`, `ERA`, `SUITE`, `Formation`, compatíveis com o leitor
GeoMoz. *Esta correspondência de atributos não demonstra que os ficheiros
sejam exactamente os mesmos.* Confirmar IDs, geometrias, datas e linhagem
da cópia antes de usar uma afirmação de equivalência no artigo.

O serviço MIS/MIREME reporta **EPSG:4130 (Moznet/ITRF94)**. Não atribuir
simplesmente EPSG:4326 aos dados de origem. Guardar CRS original, parâmetros
de transformação e CRS de saída durante a conversão.

- Geologia 250K: https://mis.mireme.gov.mz/server/rest/services/Website/Map/MapServer/4
- Estruturas 250K: https://mis.mireme.gov.mz/server/rest/services/Website/Map/MapServer/3
- Ocorrências minerais: https://mis.mireme.gov.mz/server/rest/services/Website/GeoEconomic_Data/MapServer/0

## Fontes externas DataPortal

- Solos INIA (1995): https://dataportal.co.mz/dataset/116
- Bacias DNGRH (2015): https://dataportal.co.mz/dataset/118
- Distritos CENACARTA (2017): https://dataportal.co.mz/dataset/3
- Bairros INE (2016): https://dataportal.co.mz/dataset/25
- Estradas ANE (2010): https://dataportal.co.mz/dataset/6
- Aeroportos IACM (2020): https://dataportal.co.mz/dataset/5
- Precipitação INAM atribuída pelo portal (2024): https://dataportal.co.mz/dataset/219

A camada distrital no DataPortal anuncia **162 feições**, enquanto a documentação
actual da biblioteca indica **161 distritos**. Não alterar contagens até
comparar os IDs e a definição de unidade administrativa. Para a precipitação
2024, o próprio portal assinala fonte ainda não verificada. Os valores das
capitais não devem ser descritos como medições espaciais em toda a província.

## Protocolo de integração científica

1. Determinar a licença **de cada dataset**, incluindo redistribuição no
   PyPI/Hugging Face e eventual uso comercial. Pedir confirmação às fontes.
2. Obter apenas por vias autorizadas, guardar origem, data e checksum SHA-256.
3. Inspeccionar CRS, datum, géneros de geometria e atributos.
4. Corrigir e registar geometrias inválidas e nulos, sem alterar silenciosamente
   os dados oficiais.
5. Harmonizar os nomes e códigos administrativos, com registos de diferenças.
6. Criar testes reproduzíveis com exemplos de dados e emitir relatório de
   qualidade e metadados de citação.
7. Criar release imutável com DOI e bibliografia da fonte original.

## Estratégia de publicação

**JOSS:** descrever a biblioteca, API, instalação, testes, casos de investigação
e contribuição perante alternativas.

**MDPI:** propor um estudo **distinto**, com análise original e resultados
quantitativos sobre harmonização ou validação geoespacial em Moçambique.
Evitar submissão duplicada de conteúdo substancialmente idêntico.
