# Verificação dos repositórios do catálogo

> Retrato de 2026-11-10. Só metadados públicos pela busca do GitHub; nada foi clonado, instalado ou executado. Existir não significa ser seguro, mantido ou livre para uso. Dados completos em `verificacao-repos.json`.

## Resultado

| Situação | Quantidade |
|---|---|
| No catálogo | 288 |
| Encontrados | 261 |
| Não encontrados | 27 |
| Arquivados pelo mantenedor (entre os encontrados) | 18 |
| Forks (entre os encontrados) | 8 |
| Sem licença declarada ou reconhecida | 59 |

## Limites do método
- A busca não segue redirecionamento: repositório renomeado ou transferido aparece como não encontrado.
- A busca recusa organizações que restringem acesso de aplicativos; três itens da ConsenSys ficaram inconclusivos.
- Para os candidatos abaixo, a existência do nome novo foi conferida. **[INFERIDO]** A equivalência se apoia em descrição, dono e popularidade (base de cada um em `references/aliases.json`), não em redirecionamento oficial. O catálogo guarda o nome original do dono e, ao lado, o nome atual provável.

## Não encontrados

| Repositório do catálogo | Candidato que existe | Observação |
|---|---|---|
| BloodHoundAD/SharpHound | SpecterOps/SharpHound | nome atual provável; ver aliases.json |
| ConsenSys/mythril | ConsenSysDiligence/mythril | nome atual provável; ver aliases.json |
| ConsenSys/scribble | — | inconclusivo: a busca recusa esta organização |
| ConsenSys/surya | — | inconclusivo: a busca recusa esta organização |
| ConsenSys/teku | — | inconclusivo: a busca recusa esta organização |
| IPST/uefi-firmware-parser | theopolis/uefi-firmware-parser | nome atual provável; ver aliases.json |
| LordNoteworthy/al-khaser | ayoubfaouzi/al-khaser | nome atual provável; ver aliases.json |
| NVIDIA/NeMo-Guardrails | NVIDIA-NeMo/Guardrails | nome atual provável; ver aliases.json |
| SecureAuthCorp/impacket | fortra/impacket | nome atual provável; ver aliases.json |
| WithSecureLabs/drozer | ReversecLabs/drozer | nome atual provável; ver aliases.json |
| Zero-Memory/EDR-Blocker | — | sem candidato |
| bensadeh/zenith | — | sem candidato |
| cloudsploit/scans | aquasecurity/cloudsploit | nome atual provável; ver aliases.json |
| deepinstinct/BlockEtw | — | sem candidato |
| elder-plinius/L1B3RT45 | elder-plinius/L1B3RT4S | nome atual provável; ver aliases.json |
| fox-it/BloodHound.py | dirkjanm/BloodHound.py | nome atual provável; ver aliases.json |
| fox-it/mitm6 | dirkjanm/mitm6 | nome atual provável; ver aliases.json |
| google/project-zero | — | sem candidato |
| j00ru/windows-syscall-processing | — | sem candidato |
| leondz/garak | NVIDIA/garak | nome atual provável; ver aliases.json |
| mazzeoia/mazyos-scraper | — | sem candidato |
| nicolo-ribaudo/sourcemap-decoder | — | sem candidato |
| prysmaticlabs/prysm | OffchainLabs/prysm | nome atual provável; ver aliases.json |
| returntocorp/semgrep | semgrep/semgrep | nome atual provável; ver aliases.json |
| snyk/snyk | snyk/cli | nome atual provável; ver aliases.json |
| tandasat/MiniVisor | tandasat/MiniVisorPkg | nome atual provável; ver aliases.json |
| waylan/beautifulsoup | — | sem candidato |

## Arquivados

Sem manutenção pelo próprio autor; usar só como leitura.

- GreatSCT/GreatSCT
- HavocFramework/Havoc
- Rebzzel/kiero
- RikkaApps/Riru
- Shopify/kubeaudit
- byt3bl33d3r/OffensiveNim
- de4dot/de4dot
- google/binnavi
- google/enjarify
- lelinhtinh/de4js
- lifting-bits/mcsema
- notaryproject/notary
- offensive-security/exploitdb
- optiv/Freeze
- protectai/llm-guard
- rovo89/Xposed
- tandasat/HyperPlatform
- tenable/terrascan

## Forks

Conferir se a fonte original é outra antes de usar.

- BC-SECURITY/Empire
- DarkyHArry/Jailbreak-AI
- danielkrupinski/CSGOSimple
- dnSpyEx/dnSpy
- hasherezade/FOLIAGE
- lgandx/Responder
- loneicewolf/koadic
- tandasat/SimpleVisor

## Sem licença declarada ou reconhecida

Sem licença clara, o uso não é permitido por padrão; conferir no repositório.

- Arno0x/DNSExfiltrator
- Cr4sh/KernelForge
- DarkyHArry/Jailbreak-AI
- DarkyHArry/Mythos-Driver
- DarkyHArry/cassandra-agent
- Dr-TSNG/ZygiskNext
- Encryqed/Dumper-7
- FlexingCodes/ChessCheat
- Gallopsled/pwntools
- JonathanSalwan/ROPgadget
- NomicFoundation/hardhat
- OWASP/www-project-top-10-for-large-language-model-applications
- OpenSecurityResearch/hostapd-wpe
- Ridter/noPac
- RikkaApps/Riru
- SECFORCE/SharpWhispers
- Tencent/rapidjson
- TsudaKageyu/minhook
- am0nsec/HellsGate
- anthemtotheego/InlineExecute-Assembly
- bettercap/bettercap
- capstone-engine/capstone
- cheat-engine/cheat-engine
- corca-ai/awesome-llm-security
- curl/curl
- frida/frida
- gabime/spdlog
- gentilkiwi/mimikatz
- hashcat/hashcat
- hasherezade/FOLIAGE
- in-toto/in-toto
- ionescu007/SimpleVisor
- ionescu007/SpecuCheck
- ionescu007/VisualUefi
- its-a-feature/Mythic
- j00ru/windows-syscalls
- kismetwireless/kismet
- liaojack8/AndroidKiller
- longld/peda
- meta-llama/PurpleLlama
- microsoft/binskim
- qemu/qemu
- radareorg/radare2
- rampageX/firmware-mod-kit
- rapid7/metasploit-framework
- rapid7/metasploit-payloads
- rovo89/Xposed
- rwfpl/rewolf-wow64ext
- slsa-framework/slsa
- status-im/nimbus-eth2
- tandasat/SimpleVisor
- thefLink/DeepSleep
- thefLink/Hunt-Sleeping-Beacons
- theopolis/uefi-firmware-parser
- topotam/PetitPotam
- transmissions11/solmate
- trickster0/TartarusGate
- trustedsec/TrevorC2
- x64dbg/x64dbg

## Como repetir

```bash
python3 scripts/quebrador.py check-repos --backend search --all
```
