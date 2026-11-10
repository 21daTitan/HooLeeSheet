# Estudo — Página de pré-venda e página de obrigado com pixel

- **URL**: https://www.youtube.com/watch?v=hEBmmSCZODg
- **Rótulo do dono**: sem título
- **Setor informado**: core
- **Evidência**: nível 2, somente legendas (português), obtidas em 2026-11-10 via vidIQ. Tela e código **não analisados**.
- **Duração aproximada**: 29min30 | **Confiança**: média; a transcrição automática tem muitos erros em termos técnicos
- **Status**: pendente_de_revisao

## Resumo [OBSERVADO]
Tutorial sem slides: editar duas páginas HTML prontas (uma página intermediária antes da oferta e uma página de obrigado), inserir o pixel de anúncios, publicar em hospedagem estática gratuita por arrastar e soltar, e apontar o anúncio para a página intermediária em vez do bot de vendas no Telegram. Há um bloco de venda da comunidade paga do autor.

## Estrutura por tempo
| Tempo | O que é dito | Função |
|---|---|---|
| 0:03 | Parte 2 de um vídeo anterior sobre bot de vendas | Gancho de continuação |
| 0:37–1:10 | Instalação do editor de código | Preparação |
| 1:10–3:01 | Oferta: vagas com 50% de desconto pelos 1.000 inscritos | Venda própria |
| 3:17–7:39 | Abrir o HTML; trocar cores pedindo a um assistente de IA gratuito | Tutorial |
| 8:12–11:13 | Inserir o identificador do pixel e o link de destino | Tutorial |
| 11:13–15:06 | Publicar a pasta em hospedagem estática; renomear o site | Tutorial |
| 15:06–15:54 | Conferir o disparo do evento com extensão do navegador | Verificação |
| 17:03–22:17 | Página de obrigado com evento de compra | Tutorial |
| 22:17–27:15 | Variante com imagem | Tutorial |

## Técnicas transferíveis
1. **Página estática simples publicada por arrastar e soltar**: caminho barato para página de captura ou de obrigado.
2. **Página de obrigado como ponto de medição**: o evento de compra dispara nela; uma página por etapa (venda principal e venda adicional) melhora a medição.
3. **Conferir o evento antes de anunciar**, com a extensão do pixel ou no painel.
4. **Editar HTML com assistente de IA**: colar o arquivo inteiro e pedir uma alteração de cada vez.
5. **Republicar a cada alteração**: a hospedagem não atualiza sozinha.
6. **Oferta de comemoração**: desconto atrelado a um marco real (1.000 inscritos) dá motivo à promoção.

## Não aplicar / cuidado [CONTRADITÓRIO]
- O autor diz que a página intermediária serve para a plataforma de anúncios não ver o destino real e não bloquear o anúncio (16:11): é burlar a revisão de anúncios.
- O evento de compra com valor fixo, sem relação com o valor pago (19:10), entrega dado falso à plataforma e distorce a própria medição. Usar o valor real.
- A pergunta "você é maior de 18?" leva ao mesmo destino com "sim" ou "não" (9:35): não é verificação de idade. Conteúdo adulto exige verificação de verdade.
- Coleta por pixel exige aviso de privacidade e consentimento (LGPD).

## Observação de classificação
Marcado como "core", mas o conteúdo é funil de anúncio. Sugestão: reclassificar para marketing.

## Aplicação original sugerida
Página de obrigado do dSantCreator com evento de conversão de valor real, aviso de privacidade e destino declarado no anúncio. Teste: conferir o evento em ambiente de teste antes de qualquer campanha.

## Lacunas [PENDENTE]
- Os arquivos HTML citados não foram baixados nem lidos.
- Parte 1 da série.
