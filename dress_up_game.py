import pygame

pygame.init()
pygame.mixer.music.load("musica_jogo.mpeg")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

SCREEN_WIDTH = 1480
SCREEN_HEIGHT = 820
FPS = 60
CHAR_WIDTH = 64
CHAR_HEIGHT = 64
CHAR_SCALE = 8

tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dress Up")
clock = pygame.time.Clock()

# fontes
fonte = pygame.font.SysFont("arial", 50, True)
pequena = pygame.font.SysFont("arial", 35, True)


def load_scaled(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (CHAR_WIDTH * CHAR_SCALE, CHAR_HEIGHT * CHAR_SCALE))


def carregar_imagem(nome_arquivo, tamanho):
    imagem = pygame.image.load(nome_arquivo)
    return pygame.transform.scale(imagem, tamanho)

imagem_inicio = carregar_imagem("inicio_pixel.jpeg", (SCREEN_WIDTH, SCREEN_HEIGHT))
imagem_principal = carregar_imagem("definitivo_fundo.jpeg", (SCREEN_WIDTH, SCREEN_HEIGHT))
imagem_terceira = carregar_imagem("definitivo_fundo2.jpeg", (SCREEN_WIDTH, SCREEN_HEIGHT))

# botões
botao_play = pygame.Rect(510, 490, 460, 90)

botao_avancar_img = carregar_imagem("avancar_image.png", (155, 80))
botao_voltar_img = carregar_imagem("voltar_image.png", (155, 80))

pos_botao_avancar = (1300, 30)
ret_botao_avancar = pygame.Rect(pos_botao_avancar, botao_avancar_img.get_size())

pos_botao_voltar = (1300, 30)
ret_botao_voltar = pygame.Rect(pos_botao_voltar, botao_voltar_img.get_size())

# assets por gênero
def load_assets(genero):
    vazio = pygame.Surface((CHAR_WIDTH * CHAR_SCALE, CHAR_HEIGHT * CHAR_SCALE), pygame.SRCALPHA)
    return {
        "cabelo": [load_scaled(f"{'masc' if genero == 'm' else 'fem'}{i+1}.png") for i in range(3)],
        "rosto": [load_scaled(f"rosto{genero}{i+1}.png") for i in range(3)] + [vazio],
        "roupa": [load_scaled(f"roupa{genero}{i+1}.png") for i in range(3)],
        "calca": [load_scaled(f"calca{genero}{i+1}.png") for i in range(3)],
        "saia": [load_scaled(f"saia{i+1}.png") for i in range(3)],
    }

# personagem variáveis
current_gender = "m"
modo_vestido = False
current_cabelo = 0
current_rosto = 0
current_roupa = 0
current_calca = 0
current_saia = 0
assets = load_assets(current_gender)
char_img = load_scaled("pixil-frame-0.png")
char_x = SCREEN_WIDTH // 2 - (CHAR_WIDTH * CHAR_SCALE) // 2
char_y = SCREEN_HEIGHT // 2 - (CHAR_HEIGHT * CHAR_SCALE) // 2


centro_x = SCREEN_WIDTH // 2
centro_y = SCREEN_HEIGHT // 2
setas = {
    "cabelo_esq": pygame.Rect(centro_x - 270, centro_y - 200, 40, 40),
    "cabelo_dir": pygame.Rect(centro_x + 230, centro_y - 200, 40, 40),
    "rosto_esq": pygame.Rect(centro_x - 270, centro_y - 100, 40, 40),
    "rosto_dir": pygame.Rect(centro_x + 230, centro_y - 100, 40, 40),
    "roupa_esq": pygame.Rect(centro_x - 270, centro_y + 0, 40, 40),
    "roupa_dir": pygame.Rect(centro_x + 230, centro_y + 0, 40, 40),
    "calca_esq": pygame.Rect(centro_x - 270, centro_y + 140, 40, 40),
    "calca_dir": pygame.Rect(centro_x + 230, centro_y + 140, 40, 40),
    "saia_dir": pygame.Rect(centro_x + 230, centro_y + 75, 40, 40)
}


tela_atual = "inicio"
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if tela_atual == "inicio" and botao_play.collidepoint(event.pos):
                tela_atual = "personalizacao"

            elif tela_atual == "personalizacao":
                if ret_botao_avancar.collidepoint(event.pos):
                    tela_atual = "final"

                for nome, rect in setas.items():
                    if rect.collidepoint(event.pos):
                        if nome == "cabelo_esq":
                            current_cabelo = (current_cabelo - 1) % 3
                        elif nome == "cabelo_dir":
                            current_cabelo = (current_cabelo + 1) % 3
                        elif nome == "rosto_esq":
                            current_rosto = (current_rosto - 1) % 4
                        elif nome == "rosto_dir":
                            current_rosto = (current_rosto + 1) % 4
                        elif nome == "roupa_esq":
                            current_roupa = (current_roupa - 1) % 3
                        elif nome == "roupa_dir":
                            current_roupa = (current_roupa + 1) % 3
                        elif nome == "calca_esq":
                            current_calca = (current_calca - 1) % 3
                        elif nome == "calca_dir":
                            current_calca = (current_calca + 1) % 3
                        elif nome == "saia_dir" and current_gender == "f" and modo_vestido:
                            current_saia = (current_saia + 1) % 3

            elif tela_atual == "final":
                if ret_botao_voltar.collidepoint(event.pos):
                    tela_atual = "personalizacao"

        if event.type == pygame.KEYDOWN:
            if tela_atual == "personalizacao":
                if event.key == pygame.K_g:
                    current_gender = "f" if current_gender == "m" else "m"
                    assets = load_assets(current_gender)
                    modo_vestido = False
                if event.key == pygame.K_5 and current_gender == "f":
                    modo_vestido = not modo_vestido

    
    if tela_atual == "inicio":
        tela.blit(imagem_inicio, (0, 0))

    elif tela_atual == "personalizacao":
        tela.blit(imagem_principal, (0, 0))
        tela.blit(char_img, (char_x, char_y))
        if modo_vestido and current_gender == "f":
            tela.blit(assets["saia"][current_saia], (char_x, char_y))
        else:
            tela.blit(assets["calca"][current_calca], (char_x, char_y))
            tela.blit(assets["roupa"][current_roupa], (char_x, char_y))
        tela.blit(assets["rosto"][current_rosto], (char_x, char_y))
        tela.blit(assets["cabelo"][current_cabelo], (char_x, char_y))

        tela.blit(botao_avancar_img, pos_botao_avancar)

        for nome, rect in setas.items():
            if modo_vestido and current_gender == "f" and (nome.startswith("roupa") or nome.startswith("calca")):
                continue
            if "saia" in nome and not (modo_vestido and current_gender == "f"):
                continue
            pygame.draw.rect(tela, (255, 255, 255), rect, 2)
            seta = "<" if "esq" in nome else ">"
            texto = pequena.render(seta, True, (255, 255, 255))
            tela.blit(texto, (rect.x + 10, rect.y))

    elif tela_atual == "final":
        tela.blit(imagem_terceira, (0, 0))
        tela.blit(botao_voltar_img, pos_botao_voltar)

        tela.blit(char_img, (char_x, char_y))
        if modo_vestido and current_gender == "f":
            tela.blit(assets["saia"][current_saia], (char_x, char_y))
        else:
            tela.blit(assets["calca"][current_calca], (char_x, char_y))
            tela.blit(assets["roupa"][current_roupa], (char_x, char_y))
        tela.blit(assets["rosto"][current_rosto], (char_x, char_y))
        tela.blit(assets["cabelo"][current_cabelo], (char_x, char_y))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()