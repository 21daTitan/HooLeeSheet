# Política de referências

## Adicionar referência
1. Validar URL (esquema https, host público, sem credenciais embutidas)
2. Canonicalizar (remover tracking params: utm_*, si, fbclid, gclid)
3. Gerar hash SHA-256 do URL canônico como ID
4. Classificar setor: core, sagaz, creator, marketing, hot_creator, security_defensive, finance_organization
5. Registrar com status `queued_not_analyzed` e confiança `0.0`
6. Verificar duplicata pelo ID antes de inserir

## Atualizar referência
1. Nunca sobrescrever automaticamente
2. Gerar Change Proposal com: ID, origem, comparação, impactos, rollback
3. Aguardar autorização explícita do dono
4. Registrar alteração no CHANGELOG com timestamp

## Validar consistência
1. URLs duplicados entre catálogos
2. Referências cruzadas quebradas (repo mencionado em skills que não existe no catálogo)
3. JSON bem formado em todos os arquivos .json
4. Repositórios com scope `research_only` marcados corretamente
5. Todos os MCPs e skills referenciados presentes nas listas

## Remover referência
1. Requer autorização explícita
2. Mover para seção `archived` em vez de deletar
3. Registrar motivo da remoção

## Estado de verificação
- `not_verified`: padrão; nunca tratado como seguro
- `confirmed_public`: confirmado como público via API GitHub
- `not_found`: retornou 404; pode ser privado, removido ou renomeado
- `blocked`: rate limit ou erro de autenticação
- `archived_upstream`: repositório arquivado pelo mantenedor
