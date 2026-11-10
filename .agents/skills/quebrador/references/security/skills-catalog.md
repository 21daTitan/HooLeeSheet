# Catálogo de Skills de Segurança

> **AVISO**: Nenhuma skill está instalada ou ativada. Nomes listados são rótulos de referência fornecidos pelo operador, não confirmação de disponibilidade. Ativação requer verificação, dependências satisfeitas e autorização explícita de dSanT.

**Total**: 32 skills listadas | **Instaladas**: 0 | **Ativas**: 0

---

## Engenharia Reversa (12)

| Nome | Domínio | Propósito | MCPs relacionados | Nível |
|---|---|---|---|---|
| assembly-internals | RE / Baixo nível | Fundamentos de Assembly x86, estruturas de dados em memória, calling conventions | — | Iniciante |
| assembly-x64 | RE / Baixo nível | Assembly x86-64, registradores, instruções SIMD, análise de binários 64-bit | — | Intermediário |
| ghidra | RE / Descompilação | Uso avançado do Ghidra: scripts, plugins, análise de malware, patching | ghidra-mcp | Intermediário |
| ida-pro | RE / Descompilação | IDA Pro: navegação, IDAPython, Hex-Rays, tipos, structs, enums | ida-pro-mcp | Avançado |
| ida-ghidra | RE / Comparativo | Integração e comparação IDA + Ghidra, exportação/importação de análises | ghidra-mcp, ida-pro-mcp | Avançado |
| x64dbg | RE / Debug | Depuração dinâmica com x64dbg: breakpoints, patches, scripts, plugins | x64dbg-mcp | Intermediário |
| windbg | RE / Kernel debug | WinDbg: comandos, extensões, análise de crash dumps, kernel debugging | windbg-mcp, kernel-debug-mcp | Avançado |
| live-debugging | RE / Debug | Técnicas de depuração em tempo real, anti-anti-debug, trace | x64dbg-mcp, windbg-mcp | Intermediário |
| manual-unpacking | RE / Proteção | Desempacotamento manual de executáveis protegidos, reconstrução de IAT | x64dbg-mcp | Avançado |
| detect-it-easy | RE / Triagem | Identificação de compiladores, packers, linkers, criptografia em binários | — | Iniciante |
| reclass | RE / Memória | ReClass.NET: reconstrução de classes e structs em memória de processos | — | Intermediário |
| scylla | RE / Imports | Reconstrução de tabelas de importação, dump de processos, fixup de PE | x64dbg-mcp | Intermediário |

## Kernel e Internals (6)

| Nome | Domínio | Propósito | MCPs relacionados | Nível |
|---|---|---|---|---|
| kernel-dev | Kernel / Dev | Desenvolvimento de drivers Windows, modelos WDM/WDF, callbacks | kernel-debug-mcp | Avançado |
| windows-internals | OS / Internals | Estruturas internas do Windows: PEB, TEB, EPROCESS, handles, tokens | windbg-mcp | Avançado |
| syscalls | OS / Baixo nível | System calls Windows: ntdll, SSDT, direct/indirect syscalls | — | Avançado |
| hooks | OS / Interceptação | Inline hooks, IAT hooks, VTable hooks, detours, trampolines | — | Intermediário |
| obfuscation | Proteção / Ofuscação | Técnicas de ofuscação de código: control flow, string encryption, VM | — | Avançado |
| antidebug | Proteção / Anti-análise | Técnicas anti-debug e anti-VM: timing, PEB flags, hardware breakpoints | x64dbg-mcp | Avançado |

## Linguagens (5)

| Nome | Domínio | Propósito | MCPs relacionados | Nível |
|---|---|---|---|---|
| cpp-core | Dev / C++ | C++ moderno para segurança: templates, smart pointers, ABI, linking | — | Intermediário |
| csharp-unity | Dev / C#/Unity | C# e Unity: IL2CPP, Mono, manipulação de assemblies, modding | — | Intermediário |
| rust-cheats | Dev / Rust | Rust para ferramentas de segurança: unsafe, FFI, WinAPI, injeção | — | Avançado |
| python-re | Dev / Python | Python para RE: struct, ctypes, frida bindings, automação de análise | frida-mcp | Intermediário |
| dotnet-deobfuscation | RE / .NET | Desofuscação de assemblies .NET: de4dot, dnSpy, dnlib, ConfuserEx | — | Intermediário |

## Mobile (1)

| Nome | Domínio | Propósito | MCPs relacionados | Nível |
|---|---|---|---|---|
| android-reverse | Mobile / Android | RE de APKs: jadx, Apktool, Frida, Xposed, smali, bypass SSL | frida-mcp, jadx-mcp | Intermediário |

## Malware e Game Hacking (2)

| Nome | Domínio | Propósito | MCPs relacionados | Nível |
|---|---|---|---|---|
| malware-keygen-triage | RE / Malware | Triagem de malware: análise estática e dinâmica, indicadores, relatórios | ghidra-mcp, virustotal-mcp | Avançado |
| cheat-engine | Game / Memória | Cheat Engine: busca de valores, ponteiros, scripts Lua, estruturas | — | Intermediário |

## Cloud e Supply Chain (4)

| Nome | Domínio | Propósito | MCPs relacionados | Nível |
|---|---|---|---|---|
| cloud-security | Cloud / Auditoria | Auditoria AWS/Azure/GCP: IAM, storage, rede, logs, conformidade | aws-mcp, azure-mcp, gcp-mcp | Intermediário |
| supply-chain-security | DevSecOps | Segurança de supply chain: SBOM, assinatura, proveniência, SLSA | codeql-mcp, semgrep-mcp | Intermediário |
| blockchain-security | Smart Contracts | Auditoria de contratos Solidity/Vyper: reentrancy, overflow, access | foundry-mcp, slither-mcp | Avançado |
| llm-security | AI / Segurança | Segurança de LLMs: prompt injection, jailbreak, guardrails, red teaming | garak-mcp, prompt-injection-tester-mcp | Intermediário |

## Ferramentas (2)

| Nome | Domínio | Propósito | MCPs relacionados | Nível |
|---|---|---|---|---|
| codegraph | Dev / Análise | Visualização de dependências e grafos de chamadas em codebase | — | Iniciante |
| repomix | Dev / Contexto | Empacotamento de repositórios para análise por LLM, limites de token | — | Iniciante |

---

## Combinações recomendadas

| Cenário | Skills | MCPs |
|---|---|---|
| RE de binário Windows | assembly-x64 + ghidra + x64dbg + manual-unpacking | ghidra-mcp, x64dbg-mcp |
| Análise de malware | malware-keygen-triage + windows-internals + antidebug | ghidra-mcp, virustotal-mcp |
| Pentest AD | windows-internals + syscalls | metasploit-mcp, nmap-mcp |
| Segurança mobile | android-reverse + python-re | frida-mcp, jadx-mcp |
| Auditoria de smart contracts | blockchain-security | foundry-mcp, slither-mcp |
| Red teaming de LLM | llm-security | garak-mcp, prompt-injection-tester-mcp |
