<div align="center">

# Freirinho - Jogo Espacial Educativo

### Navegue pelo universo coletando letras para formar palavras

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Pygame](https://img.shields.io/badge/Pygame-00979D?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org)

</div>

---

## Sobre o Projeto

**Freirinho** e um jogo 2D educativo com tema espacial. O jogador controla uma nave e explora um universo aberto coletando planetas com letras para formar palavras — na ordem correta! Desvie de asteroides, evite letras erradas e complete os 5 niveis.

---

## Preview

### Gameplay
![Gameplay](screenshots/03-gameplay.png)

### Tela de Vitoria
![Vitoria](screenshots/01-vitoria.png)

### Tela de Derrota
![Derrota](screenshots/02-derrota.png)

---

## Funcionalidades

- **Mundo aberto** — mapa 3x maior que a tela com camera que segue a nave
- **5 niveis** com palavras diferentes: MARTE, TEMA, ARTE, TREM, META
- **Coleta em ordem obrigatoria** — precisa pegar as letras na sequencia correta da palavra
- **Seta indicadora** no HUD mostra qual e a proxima letra
- **Letra fora de ordem** — perde vida mas reaparece em outro lugar do mapa
- **Mini-mapa** — mostra posicao da nave, planetas corretos (verde) e errados (vermelho)
- **Dificuldade progressiva** — mais obstaculos a cada nivel
- **Sistema de vidas** com power-up de vida extra
- **Animacoes de explosao** coloridas ao coletar planetas
- **Estrelas de fundo** para sensacao de profundidade
- **Planetas flutuantes** com animacao senoidal
- **Telas finais** desenhadas por codigo (se adaptam a cada nivel)
- **Restart** com ENTER nas telas finais

---

## Controles

| Tecla | Acao |
|-------|------|
| Setas / WASD | Mover a nave |
| ENTER | Proximo nivel / Reiniciar |
| ESC | Sair do jogo |

---

## Regras

1. Colete as letras **na ordem da palavra** (indicada pela seta dourada no HUD)
2. Letra certa na ordem certa = ponto
3. Letra certa fora de ordem = perde vida (a letra reaparece em outro lugar)
4. Letra errada = perde vida
5. 3 vidas — ao perder todas, game over
6. Power-up de borracha restaura 1 vida

---

## Tecnologias

- **Python 3** — linguagem principal
- **Pygame** — engine para renderizacao, sprites, colisoes e animacoes

---

## Como Executar

```bash
# Clone o repositorio
git clone https://github.com/GeozedequeGuimaraes/freirinho-jogo-espacial.git

# Acesse a pasta
cd freirinho-jogo-espacial

# Instale pygame
pip install pygame

# Execute
python main.py
```

---

## Estrutura

```
freirinho-jogo-espacial/
├── main.py              # Codigo principal do jogo
├── assets/              # Sprites, imagens e fonte
│   ├── NaveCima*.png    # Frames da nave
│   ├── M.png, A.png ... # Planetas com letras
│   ├── *_True/False.png # Letras do HUD
│   ├── Laranja*.png ... # Frames de explosao
│   ├── background.png   # Fundo espacial
│   └── GameFont.ttf     # Fonte do jogo
└── screenshots/         # Imagens para o README
```

---

## Contexto

Projeto desenvolvido para a disciplina de **Introducao a Programacao** — CIn-UFPE.

---

## Autor

<div align="center">

**Geozedeque Guimaraes**

Estudante de Ciencia da Computacao — CIn-UFPE

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/GeozedequeGuimaraes)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/geozedeque-guimaraes)

</div>
