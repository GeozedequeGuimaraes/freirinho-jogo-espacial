import pygame
import random
import sys
import math
import os
import urllib.request

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_WIDTH = 2400
WORLD_HEIGHT = 1800

# Baixar fonte tematica se nao existir
FONT_PATH = './assets/GameFont.ttf'

def get_font(size):
    if os.path.exists(FONT_PATH):
        return pygame.font.Font(FONT_PATH, size)
    return pygame.font.SysFont('Arial', size, bold=True)

# Niveis: palavra + letras erradas extras
NIVEIS = [
    {'palavra': 'MARTE', 'erradas': ['G', 'I', 'N']},
    {'palavra': 'TEMA',  'erradas': ['G', 'I', 'N', 'R']},
    {'palavra': 'ARTE',  'erradas': ['G', 'I', 'N', 'M']},
    {'palavra': 'TREM',  'erradas': ['G', 'I', 'N', 'A']},
    {'palavra': 'META',  'erradas': ['G', 'I', 'N', 'R']},
]

# Cores de explosao por letra
CORES_PLANETA = {
    'M': 'Laranja', 'A': 'Rosa', 'R': 'Azul',
    'T': 'Vermelho', 'E': 'Amarelo',
    'G': 'Laranja', 'I': 'Roxo', 'N': 'Verde',
}


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def follow(self, target_rect):
        self.x = target_rect.centerx - SCREEN_WIDTH // 2
        self.y = target_rect.centery - SCREEN_HEIGHT // 2
        self.x = max(0, min(self.x, WORLD_WIDTH - SCREEN_WIDTH))
        self.y = max(0, min(self.y, WORLD_HEIGHT - SCREEN_HEIGHT))

    def apply(self, rect):
        return rect.move(-self.x, -self.y)


class EstrelasBackground:
    def __init__(self):
        self.stars = []
        for _ in range(200):
            x = random.randint(0, WORLD_WIDTH)
            y = random.randint(0, WORLD_HEIGHT)
            brilho = random.randint(100, 255)
            tamanho = random.choice([1, 1, 1, 2])
            self.stars.append((x, y, brilho, tamanho))

    def draw(self, surface, camera):
        for x, y, brilho, tamanho in self.stars:
            sx = x - camera.x
            sy = y - camera.y
            if -2 <= sx <= SCREEN_WIDTH + 2 and -2 <= sy <= SCREEN_HEIGHT + 2:
                cor = (brilho, brilho, brilho)
                if tamanho == 1:
                    surface.set_at((int(sx), int(sy)), cor)
                else:
                    pygame.draw.circle(surface, cor, (int(sx), int(sy)), tamanho)


class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(f'./assets/NaveCima{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self.current_image = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 6
        self.vida = 3
        self.score = 0

    def update(self, obstaculo_groups, game_active):
        self.current_image = (self.current_image + 1) % 4
        self.image = self.images[self.current_image]

        if not game_active:
            return

        dx, dy = 0, 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            dx = -self.speed
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            dx = self.speed
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            dy = -self.speed
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            dy = self.speed

        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.rect.x += int(dx)
        self.rect.y += int(dy)

        for grupo in obstaculo_groups:
            if pygame.sprite.spritecollideany(self, grupo):
                self.rect.x -= int(dx)
                self.rect.y -= int(dy)
                break

        self.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class PlanetaLetra(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.base_y = y
        self.float_offset = random.uniform(0, 6.28)

    def update(self, ticks):
        self.rect.centery = self.base_y + int(math.sin(ticks / 500 + self.float_offset) * 6)


class LifeUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/Borracha_True.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_on = True
        self.end_showing = pygame.time.get_ticks() + 5000
        self.start_showing = 0


class Explosao(pygame.sprite.Sprite):
    def __init__(self, cor, x, y, size=2):
        pygame.sprite.Sprite.__init__(self)
        sizes = {1: (70, 70), 2: (90, 90), 3: (140, 140)}
        dim = sizes.get(size, (90, 90))
        self.images = []
        for num in range(1, 7):
            img = pygame.image.load(f'./assets/{cor}{num}.png')
            img = pygame.transform.scale(img, dim)
            self.images.append(img)
        self.index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= 3 and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= 3:
            self.kill()


class LetraHUD(pygame.sprite.Sprite):
    def __init__(self, name, x, on=False):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.x = x
        self.is_on = on
        path = f'./assets/{name}_True.png' if on else f'./assets/{name}_False.png'
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 20)

    def ativar(self):
        self.is_on = True
        self.image = pygame.image.load(f'./assets/{self.name}_True.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, 20)


class Vida(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/Borracha_True.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 30)


def draw_minimap(surface, cam, nave, p_certos, p_errados, obs_group):
    mw, mh = 160, 120
    mx = SCREEN_WIDTH - mw - 12
    my = SCREEN_HEIGHT - mh - 12
    mapa = pygame.Surface((mw, mh), pygame.SRCALPHA)
    mapa.fill((10, 10, 30, 180))
    pygame.draw.rect(mapa, (100, 100, 150), (0, 0, mw, mh), 1)
    sx = mw / WORLD_WIDTH
    sy = mh / WORLD_HEIGHT

    for obs in obs_group:
        pygame.draw.circle(mapa, (80, 80, 80),
                           (int(obs.rect.centerx * sx), int(obs.rect.centery * sy)), 2)
    for info in p_certos.values():
        for spr in info['grupo']:
            pygame.draw.circle(mapa, (0, 255, 100),
                               (int(spr.rect.centerx * sx), int(spr.rect.centery * sy)), 3)
    for info in p_errados.values():
        for spr in info['grupo']:
            pygame.draw.circle(mapa, (255, 60, 60),
                               (int(spr.rect.centerx * sx), int(spr.rect.centery * sy)), 3)

    pygame.draw.circle(mapa, (255, 255, 255),
                       (int(nave.rect.centerx * sx), int(nave.rect.centery * sy)), 3)
    vx = int(cam.x * sx)
    vy = int(cam.y * sy)
    vw = int(SCREEN_WIDTH * sx)
    vh = int(SCREEN_HEIGHT * sy)
    pygame.draw.rect(mapa, (255, 255, 255, 100), (vx, vy, vw, vh), 1)
    surface.blit(mapa, (mx, my))


def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = get_font(size)
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y))
    surface.blit(txt, rect)


def draw_planeta(surface, cx, cy, raio, ticks):
    """Desenha um planeta bonito com aneis"""
    ps = pygame.Surface((raio * 4, raio * 4), pygame.SRCALPHA)
    pc = raio * 2  # centro no surface

    # Sombra
    pygame.draw.circle(ps, (0, 0, 0, 50), (pc + 5, pc + 5), raio)

    # Corpo — gradiente radial
    for r in range(raio, 0, -1):
        t = r / raio
        cr = int(220 - 80 * t)
        cg = int(130 - 60 * t)
        cb = int(60 - 30 * t)
        pygame.draw.circle(ps, (cr, cg, cb), (pc, pc), r)

    # Faixas atmosfericas (mascara circular)
    faixas = pygame.Surface((raio * 4, raio * 4), pygame.SRCALPHA)
    cores_faixa = [(255, 180, 100, 25), (255, 200, 130, 20), (200, 140, 80, 30)]
    for i, cor in enumerate(cores_faixa):
        fy = pc - raio // 2 + i * (raio // 2)
        pygame.draw.rect(faixas, cor, (pc - raio, fy, raio * 2, raio // 4))

    # Aplicar mascara circular nas faixas
    mascara = pygame.Surface((raio * 4, raio * 4), pygame.SRCALPHA)
    pygame.draw.circle(mascara, (255, 255, 255, 255), (pc, pc), raio)
    faixas.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    ps.blit(faixas, (0, 0))

    # Brilho superior esquerdo
    for br in range(raio // 2, 0, -1):
        a = max(0, min(80, int(80 * (1 - br / (raio // 2)))))
        pygame.draw.circle(ps, (255, 250, 220, a),
                           (pc - raio // 3, pc - raio // 3), br)

    # Anel traseiro (atras do planeta - desenhar antes)
    anel_w = int(raio * 2.5)
    anel_h = int(raio * 0.35)
    anel_surf = pygame.Surface((raio * 4, raio * 4), pygame.SRCALPHA)

    # Anel externo
    anel_rect = pygame.Rect(pc - anel_w // 2, pc - anel_h // 2, anel_w, anel_h)
    pygame.draw.ellipse(anel_surf, (210, 190, 160, 50), anel_rect, 0)
    pygame.draw.ellipse(anel_surf, (230, 210, 180, 100), anel_rect, 2)

    # Anel interno
    anel_w2 = int(raio * 2)
    anel_h2 = int(raio * 0.22)
    anel_rect2 = pygame.Rect(pc - anel_w2 // 2, pc - anel_h2 // 2, anel_w2, anel_h2)
    pygame.draw.ellipse(anel_surf, (240, 220, 200, 70), anel_rect2, 2)

    # Combinar: anel + planeta
    final = pygame.Surface((raio * 4, raio * 4), pygame.SRCALPHA)
    final.blit(anel_surf, (0, 0))
    final.blit(ps, (0, 0))

    # Rotacao suave
    angulo = math.sin(ticks / 3000) * 2
    rotated = pygame.transform.rotate(final, angulo)
    rect = rotated.get_rect(center=(cx, cy))
    surface.blit(rotated, rect)


def draw_tela_vitoria(surface, palavra, nivel_idx, total_niveis, all_done, ticks):
    """Tela de vitoria"""
    # Fundo solido escuro
    surface.fill((12, 10, 35))

    # Estrelas decorativas
    random.seed(42)  # seed fixa pra nao piscar
    for i in range(80):
        sx = random.randint(0, SCREEN_WIDTH)
        sy = random.randint(0, SCREEN_HEIGHT)
        b = 120 + int(60 * math.sin(ticks / 400 + i * 0.7))
        pygame.draw.circle(surface, (b, b, int(b * 0.8)), (sx, sy), random.choice([1, 1, 2]))
    random.seed()  # restaurar seed

    # --- HIERARQUIA ---

    # 1. TITULO — maior, topo
    ty = 80 + int(math.sin(ticks / 400) * 4)
    font_big = get_font(56)
    # Sombra
    s = font_big.render("PARABENS!", True, (100, 50, 0))
    surface.blit(s, s.get_rect(center=(SCREEN_WIDTH // 2 + 2, ty + 2)))
    # Texto
    t = font_big.render("PARABENS!", True, (255, 210, 60))
    surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, ty)))

    # 2. PLANETA — centro visual
    draw_planeta(surface, SCREEN_WIDTH // 2, 230, 55, ticks)

    # 3. PALAVRA — abaixo do planeta, bem visivel
    palavra_y = 320
    font_palavra = get_font(18)
    pt = font_palavra.render(f'Palavra "{palavra}" completa!', True, (255, 230, 140))
    surface.blit(pt, pt.get_rect(center=(SCREEN_WIDTH // 2, palavra_y)))

    # 4. LETRAS — cards grandes e claros
    letra_size = 60
    gap = 10
    total_w = len(palavra) * (letra_size + gap) - gap
    bx = (SCREEN_WIDTH - total_w) // 2
    by = 350

    for i, letra in enumerate(palavra):
        lx = bx + i * (letra_size + gap)
        fy = by + int(math.sin(ticks / 300 + i * 0.9) * 3)

        # Card com borda brilhante
        pygame.draw.rect(surface, (50, 45, 30), (lx, fy, letra_size, letra_size), border_radius=10)
        pygame.draw.rect(surface, (180, 150, 80), (lx, fy, letra_size, letra_size), 2, border_radius=10)

        img = pygame.image.load(f'./assets/{letra}_True.png').convert_alpha()
        img = pygame.transform.scale(img, (letra_size - 8, letra_size - 8))
        surface.blit(img, (lx + 4, fy + 4))

    # 5. NIVEL — discreto
    draw_text(surface, f"Nivel {nivel_idx + 1} de {total_niveis}", 14,
              SCREEN_WIDTH // 2, by + letra_size + 25, (120, 120, 180))

    # 6. INSTRUCAO — rodape
    if all_done:
        draw_text(surface, "Todos os niveis completos!", 22,
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, (80, 255, 120))
        draw_text(surface, "ENTER jogar de novo   |   ESC sair", 15,
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40, (150, 150, 200))
    else:
        # Botao visual
        btn_w, btn_h = 280, 42
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        btn_y = SCREEN_HEIGHT - 65
        pulse = int(math.sin(ticks / 300) * 8)
        pygame.draw.rect(surface, (40, 40, 80), (btn_x, btn_y, btn_w, btn_h), border_radius=20)
        pygame.draw.rect(surface, (100 + pulse, 100 + pulse, 200 + pulse),
                         (btn_x, btn_y, btn_w, btn_h), 2, border_radius=20)
        draw_text(surface, "ENTER  proximo nivel", 16,
                  SCREEN_WIDTH // 2, btn_y + btn_h // 2, (200, 200, 255))


def draw_tela_derrota(surface, ticks):
    """Tela de derrota"""
    # Fundo escuro avermelhado
    surface.fill((25, 8, 12))

    # Estrelas vermelhas
    random.seed(99)
    for i in range(50):
        sx = random.randint(0, SCREEN_WIDTH)
        sy = random.randint(0, SCREEN_HEIGHT)
        b = 80 + int(30 * math.sin(ticks / 500 + i))
        pygame.draw.circle(surface, (b, int(b * 0.4), int(b * 0.3)), (sx, sy), 1)
    random.seed()

    # Titulo grande
    ty = 150 + int(math.sin(ticks / 500) * 3)
    font_big = get_font(50)
    s = font_big.render("Voce Perdeu!", True, (80, 10, 10))
    surface.blit(s, s.get_rect(center=(SCREEN_WIDTH // 2 + 2, ty + 2)))
    t = font_big.render("Voce Perdeu!", True, (255, 90, 80))
    surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, ty)))

    # Icone — circulo com X
    icone_y = 280
    pygame.draw.circle(surface, (50, 20, 20), (SCREEN_WIDTH // 2, icone_y), 45)
    pygame.draw.circle(surface, (120, 40, 40), (SCREEN_WIDTH // 2, icone_y), 45, 3)
    fx = get_font(40)
    xt = fx.render("X", True, (255, 70, 60))
    surface.blit(xt, xt.get_rect(center=(SCREEN_WIDTH // 2, icone_y)))

    # Mensagem motivacional
    draw_text(surface, "Nao desista! Tente novamente.", 20,
              SCREEN_WIDTH // 2, 365, (200, 160, 160))

    # Botao visual
    btn_w, btn_h = 320, 42
    btn_x = (SCREEN_WIDTH - btn_w) // 2
    btn_y = SCREEN_HEIGHT - 65
    pulse = int(math.sin(ticks / 300) * 6)
    pygame.draw.rect(surface, (50, 20, 25), (btn_x, btn_y, btn_w, btn_h), border_radius=20)
    pygame.draw.rect(surface, (150 + pulse, 60, 60),
                     (btn_x, btn_y, btn_w, btn_h), 2, border_radius=20)
    draw_text(surface, "ENTER tentar de novo   |   ESC sair", 14,
              SCREEN_WIDTH // 2, btn_y + btn_h // 2, (220, 160, 160))


def gerar_posicoes_seguras(quantidade, nave_pos, min_dist=300):
    """Gera posicoes aleatorias no mundo longe da nave e entre si"""
    posicoes = []
    margem = 200
    tentativas = 0
    while len(posicoes) < quantidade and tentativas < 5000:
        x = random.randint(margem, WORLD_WIDTH - margem)
        y = random.randint(margem, WORLD_HEIGHT - margem)
        dist_nave = math.sqrt((x - nave_pos[0])**2 + (y - nave_pos[1])**2)
        if dist_nave < min_dist:
            tentativas += 1
            continue
        ok = True
        for px, py in posicoes:
            if math.sqrt((x - px)**2 + (y - py)**2) < 150:
                ok = False
                break
        if ok:
            posicoes.append((x, y))
        tentativas += 1
    return posicoes


def create_level(nivel_idx):
    """Cria todos os objetos para um nivel especifico"""
    nivel = NIVEIS[nivel_idx]
    palavra = nivel['palavra']
    erradas = nivel['erradas']

    nave_start = (WORLD_WIDTH // 2, WORLD_HEIGHT // 2 + 200)
    nave = Nave(*nave_start)
    nave_group = pygame.sprite.GroupSingle(nave)

    # Gerar posicoes para tudo
    total_planetas = len(palavra) + len(erradas)
    total_obstaculos = 12 + nivel_idx * 2  # mais obstaculos por nivel
    todas_posicoes = gerar_posicoes_seguras(
        total_planetas + total_obstaculos, nave_start, min_dist=250
    )

    pos_planetas = todas_posicoes[:total_planetas]
    pos_obstaculos = todas_posicoes[total_planetas:]

    # Obstaculos
    obstaculos = []
    obstaculo_group = pygame.sprite.Group()
    imgs_obs = ['./assets/Asteroides.png', './assets/Ativo 7.png',
                './assets/Ativo 7 (1).png', './assets/Ativo 7 (2).png']

    for i, (x, y) in enumerate(pos_obstaculos):
        img = imgs_obs[i % len(imgs_obs)]
        grupo = pygame.sprite.Group()
        obs = Obstaculo(img, x, y)
        grupo.add(obs)
        obstaculo_group.add(obs)
        obstaculos.append(grupo)

    # Planetas corretos
    planetas_certos = {}
    for i, letra in enumerate(palavra):
        pos = pos_planetas[i]
        grupo = pygame.sprite.Group()
        planeta = PlanetaLetra(f'./assets/{letra}.png', *pos)
        grupo.add(planeta)
        cor = CORES_PLANETA.get(letra, 'Laranja')
        planetas_certos[f'{letra}_{i}'] = {
            'grupo': grupo, 'letra': letra, 'cor': cor
        }

    # Planetas errados
    planetas_errados = {}
    for i, letra in enumerate(erradas):
        pos = pos_planetas[len(palavra) + i]
        grupo = pygame.sprite.Group()
        planeta = PlanetaLetra(f'./assets/{letra}.png', *pos)
        grupo.add(planeta)
        cor = CORES_PLANETA.get(letra, 'Laranja')
        planetas_errados[f'{letra}_{i}'] = {
            'grupo': grupo, 'letra': letra, 'cor': cor
        }

    # HUD letras — centralizar na tela
    hud_letras = {}
    hud_group = pygame.sprite.Group()
    largura_letra = 80
    total_largura = len(palavra) * largura_letra
    inicio_x = (SCREEN_WIDTH - total_largura) // 2
    for i, letra in enumerate(palavra):
        chave = f'{letra}_{i}'
        hud = LetraHUD(letra, inicio_x + i * largura_letra)
        hud_letras[chave] = hud
        hud_group.add(hud)

    # Ordem de coleta (qual a proxima letra esperada)
    ordem = [f'{letra}_{i}' for i, letra in enumerate(palavra)]

    vidas_sprites = [Vida(50), Vida(90), Vida(130)]
    vidas_group = pygame.sprite.Group(vidas_sprites)

    explosao_group = pygame.sprite.Group()

    lifeUp = LifeUp(random.randint(150, WORLD_WIDTH - 150),
                     random.randint(150, WORLD_HEIGHT - 150))
    lifeUp_group = pygame.sprite.Group(lifeUp)

    return {
        'nave': nave, 'nave_group': nave_group,
        'obstaculos': obstaculos, 'obstaculo_group': obstaculo_group,
        'planetas_certos': planetas_certos, 'planetas_errados': planetas_errados,
        'hud_letras': hud_letras, 'hud_group': hud_group,
        'ordem': ordem, 'proximo_idx': 0,
        'vidas_sprites': vidas_sprites, 'vidas_group': vidas_group,
        'explosao_group': explosao_group,
        'lifeUp': lifeUp, 'lifeUp_group': lifeUp_group,
        'palavra': nivel['palavra'],
    }


# ==================== INICIALIZACAO ====================

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

BACKGROUND = pygame.image.load('./assets/background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (WORLD_WIDTH, WORLD_HEIGHT))

pygame.display.set_caption("Freirinho")
icon = pygame.image.load('./assets/icone.png')
pygame.display.set_icon(icon)

camera = Camera()
estrelas_fundo = EstrelasBackground()

# Estado do jogo
nivel_atual = 0
game = create_level(nivel_atual)
game_over = False
game_won = False
all_levels_done = False

# ==================== GAME LOOP ====================

while True:
    current_time = pygame.time.get_ticks()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    nivel_atual = 0
                    game = create_level(nivel_atual)
                    game_over = False
                    game_won = False
                    all_levels_done = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif game_won:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if all_levels_done:
                        nivel_atual = 0
                        all_levels_done = False
                    else:
                        nivel_atual += 1
                    game = create_level(nivel_atual)
                    game_won = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    nave = game['nave']
    nave_group = game['nave_group']
    obstaculos = game['obstaculos']
    obstaculo_group = game['obstaculo_group']
    planetas_certos = game['planetas_certos']
    planetas_errados = game['planetas_errados']
    hud_letras = game['hud_letras']
    hud_group = game['hud_group']
    vidas_sprites = game['vidas_sprites']
    vidas_group = game['vidas_group']
    explosao_group = game['explosao_group']
    lifeUp = game['lifeUp']
    lifeUp_group = game['lifeUp_group']

    game_active = not game_over and not game_won

    nave.update(obstaculos, game_active)
    camera.follow(nave.rect)

    # Fundo
    screen.fill((5, 5, 15))
    screen.blit(BACKGROUND, (-camera.x, -camera.y))
    estrelas_fundo.draw(screen, camera)

    if game_active:
        # Atualizar planetas (flutuacao)
        for info in planetas_certos.values():
            for spr in info['grupo']:
                spr.update(current_time)
        for info in planetas_errados.values():
            for spr in info['grupo']:
                spr.update(current_time)

        # Colisao com letras corretas (precisa pegar na ordem!)
        ordem = game['ordem']
        proximo_idx = game['proximo_idx']

        for chave, info in list(planetas_certos.items()):
            if pygame.sprite.spritecollideany(nave, info['grupo']):
                cx, cy = info['grupo'].sprites()[0].rect.center
                info['grupo'].empty()
                explosao_group.add(Explosao(info['cor'], cx, cy))

                if proximo_idx < len(ordem) and chave == ordem[proximo_idx]:
                    # Letra certa na ordem certa!
                    hud_letras[chave].ativar()
                    nave.score += 1
                    game['proximo_idx'] += 1
                else:
                    # Letra certa mas fora de ordem — perde vida e reaparece em outro lugar
                    nave.vida -= 1
                    nova_pos = gerar_posicoes_seguras(1, (nave.rect.centerx, nave.rect.centery), min_dist=400)
                    if nova_pos:
                        nx, ny = nova_pos[0]
                    else:
                        nx = random.randint(200, WORLD_WIDTH - 200)
                        ny = random.randint(200, WORLD_HEIGHT - 200)
                    novo_planeta = PlanetaLetra(f'./assets/{info["letra"]}.png', nx, ny)
                    info['grupo'].add(novo_planeta)

        # Colisao com letras erradas (sempre perde vida)
        for chave, info in list(planetas_errados.items()):
            if pygame.sprite.spritecollideany(nave, info['grupo']):
                cx, cy = info['grupo'].sprites()[0].rect.center
                info['grupo'].empty()
                nave.vida -= 1
                explosao_group.add(Explosao(info['cor'], cx, cy))

        # Colisao com lifeUp
        if lifeUp.is_on and pygame.sprite.spritecollideany(nave, lifeUp_group):
            if nave.vida < 3:
                nave.vida += 1
            lifeUp_group.empty()
            lifeUp = LifeUp(random.randint(150, WORLD_WIDTH - 150),
                            random.randint(150, WORLD_HEIGHT - 150))
            lifeUp_group.add(lifeUp)
            game['lifeUp'] = lifeUp
            game['lifeUp_group'] = lifeUp_group

        # Checar vitoria/derrota
        if nave.score >= len(game['palavra']):
            game_won = True
            if nivel_atual >= len(NIVEIS) - 1:
                all_levels_done = True
        if nave.vida <= 0:
            game_over = True

        # LifeUp timer
        if lifeUp.is_on:
            if current_time >= lifeUp.end_showing:
                lifeUp_group.empty()
                lifeUp = LifeUp(random.randint(150, WORLD_WIDTH - 150),
                                random.randint(150, WORLD_HEIGHT - 150))
                lifeUp_group.add(lifeUp)
                lifeUp.is_on = False
                lifeUp.start_showing = current_time + random.randint(2, 6) * 1000
                game['lifeUp'] = lifeUp
                game['lifeUp_group'] = lifeUp_group
        else:
            if current_time >= lifeUp.start_showing:
                lifeUp.is_on = True
                lifeUp.end_showing = current_time + random.randint(3, 7) * 1000

    # ==================== DESENHAR ====================

    for obs in obstaculo_group:
        screen.blit(obs.image, camera.apply(obs.rect))

    for info in planetas_certos.values():
        for spr in info['grupo']:
            screen.blit(spr.image, camera.apply(spr.rect))
    for info in planetas_errados.values():
        for spr in info['grupo']:
            screen.blit(spr.image, camera.apply(spr.rect))

    screen.blit(nave.image, camera.apply(nave.rect))

    explosao_group.update()
    for expl in explosao_group:
        screen.blit(expl.image, camera.apply(expl.rect))

    if lifeUp.is_on:
        for spr in lifeUp_group:
            screen.blit(spr.image, camera.apply(spr.rect))

    # ==================== HUD ====================

    vidas_group.empty()
    for i in range(nave.vida):
        vidas_group.add(vidas_sprites[i])
    vidas_group.draw(screen)

    hud_group.draw(screen)

    # Indicador da proxima letra (seta pulsante)
    if game_active:
        ordem = game['ordem']
        proximo_idx = game['proximo_idx']
        if proximo_idx < len(ordem):
            chave_prox = ordem[proximo_idx]
            if chave_prox in hud_letras:
                hud_spr = hud_letras[chave_prox]
                arrow_x = hud_spr.rect.centerx
                arrow_y = hud_spr.rect.top - 8 + int(math.sin(current_time / 200) * 4)
                # Seta triangular
                pygame.draw.polygon(screen, (255, 220, 50), [
                    (arrow_x, arrow_y),
                    (arrow_x - 8, arrow_y - 12),
                    (arrow_x + 8, arrow_y - 12),
                ])

    # Nivel indicator — pill badge
    nivel_txt = f"Nivel {nivel_atual + 1}/{len(NIVEIS)}"
    nf = get_font(14)
    nt = nf.render(nivel_txt, True, (220, 220, 255))
    nw = nt.get_width() + 20
    nh = nt.get_height() + 8
    nx = SCREEN_WIDTH - nw - 12
    ny = 10
    pygame.draw.rect(screen, (20, 20, 60, 180), (nx, ny, nw, nh), border_radius=12)
    pygame.draw.rect(screen, (80, 80, 160), (nx, ny, nw, nh), 1, border_radius=12)
    screen.blit(nt, (nx + 10, ny + 4))

    draw_minimap(screen, camera, nave, planetas_certos, planetas_errados, obstaculo_group)

    # Telas finais (desenhadas por codigo, cobrem tudo)
    if game_won:
        draw_tela_vitoria(screen, game['palavra'], nivel_atual, len(NIVEIS),
                          all_levels_done, current_time)

    if game_over:
        draw_tela_derrota(screen, current_time)

    pygame.display.update()
