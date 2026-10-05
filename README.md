# Quitina

RPG de acción oscuro para navegador. Criaturas insecto en un reino subterráneo podrido, con niveles, equipamiento, refinado y metamorfosis. Pensado para publicarse en portales de juegos web (CrazyGames, Poki) y monetizar con publicidad.

## Cómo jugar

Abre `index.html` en el navegador. No necesita instalación ni servidor. La carpeta `assets/` tiene el arte conceptual de la portada y el atlas de sprites de la Mantis. Las hojas originales están en `hojas/`; para regenerar el atlas: `python3 tools/armar_sprites.py` (necesita Pillow, NumPy y SciPy).

- **Teclado y mouse:** WASD para moverte, clic o J para atacar, 1 · 2 · 3 habilidades, Q poción, I bolsa, C poderes, H caza automática, M mapa grande, B volver a la madriguera, Esc pausa.
- **Celular:** arrastra en la mitad izquierda para moverte y usa los botones de la derecha.

## Instalarlo como app en el celular

El juego es una app web instalable (PWA): tiene manifiesto, íconos y funciona sin conexión una vez abierto. Para instalarlo tiene que estar publicado en una dirección HTTPS (por ejemplo GitHub Pages). Desde Chrome en Android: abrir la dirección, menú ⋮ → **Instalar app** (o *Agregar a pantalla principal*). Se abre a pantalla completa y apaisado, sin barra del navegador. Si se juega desde el navegador, al entrar al mundo pide pantalla completa y gira a apaisado cuando el teléfono lo permite.

## Contenido de la versión 0.13

| Sistema | Estado |
|---|---|
| Sprites | La Mantis usa sprites animados del arte conceptual: quieto (4), caminar (8), tajada frontal (golpe simple y Embestida), tajada hacia arriba (Furia), tajada giratoria (Torbellino), golpe recibido y muerte. Una dirección espejada. Los sets se marcan con un brillo del color del set; el retrato de la madriguera sigue mostrando cada pieza. En la pausa se puede volver al dibujo clásico. |
| Personaje | Nombre propio al crear la criatura, placa con nombre y barras de vida y energía sobre la cabeza, y círculo de selección bajo los pies. La Mantis es una guerrera humanoide (hombreras, brazales con hebillas, cinturón, bolso y capa en la forma adulta) basada en el arte conceptual. |
| Razas | Mantis (guerrera) y Polilla (hechicera) jugables. Escarabajo y Avispa anunciadas. La Mantis tiene Torbellino, Embestida y Furia (+70% de daño por 4 s). El golpe simple hace 70% del daño base. |
| Metamorfosis | 3 etapas por raza (nivel 6 y 12). En la etapa adulta se elige una de dos ramas. |
| Región I: Raíces podridas | Mapa abierto de 4800 × 3600 con santuario de entrada y 5 zonas por nivel recomendado (1–4 a 13–16). Las criaturas reaparecen a los 9–14 s, las élites al minuto y el jefe (Ciempiés de Hueso) cada 5 minutos. Las zonas descubiertas habilitan el viaje directo. |
| Atributos | 4 puntos por nivel para Fuerza, Caparazón, Agilidad y Esencia. Reparto automático con receta por raza y reinicio pagando oro. |
| Habilidades | Rango 1 a 5, con 1 punto cada 3 niveles. La habilidad 2 se desbloquea en nivel 3 y la 3 en nivel 6. Los rangos 3 y 5 cambian el funcionamiento (radio, aturdimiento, duración, robo de vida). |
| Santuarios | 5 santuarios de ámbar (entrada y borde de cada zona): curan, alejan a las criaturas y tienen a Brugo, el artesano: flecha y nombre siempre visibles; se toca o cliquea (si estás lejos, el personaje camina hasta él) o tecla E. Su panel pausa el juego y ofrece Artesano, Equipo, Forja, Depósito y Mercader. |
| Artesano | Funde las 3 piezas más débiles de un set + oro + ámbar en una pieza nueva de ese set (arma, casco, coraza, patas o amuleto), un nivel por encima de la mejor, con la rareza más alta y 25% de chance de subirla. |
| Depósito | Baúl de 60 lugares compartido entre santuarios y madriguera. |
| Caza automática | Estilo MU Helper (tecla H): caza alrededor del punto de activación, usa habilidades, recoge botín según filtros y toma pociones. Se configura en la pausa. |
| Calidad de imagen | Resolución nativa de la pantalla (hasta 3×) y sprites a 300 px. Modo automático que baja la resolución si no llega a ~45 cuadros por segundo; también máxima y ahorro de batería desde el menú. Zoom más cercano en celulares. |
| Interfaz | Íconos en lugar de texto: caza automática (flechas en círculo; activa se pone verde azulado y gira, sin cartel en pantalla) y menú (tres líneas, pausa el juego). Los puntos sin repartir se avisan solo con el número sobre la bolsa. El cartel de zona ya no se encima con la barra del jefe. |
| Celular apaisado | App instalable a pantalla completa y apaisada. HUD compacto: bolsa en la fila de íconos de arriba, minimapa más chico, botones de ataque un poco menores y márgenes para la cámara/muesca. Si se juega vertical aparece un aviso para girar el teléfono (se puede descartar). |
| Comparación rápida | En las miniaturas del inventario, flecha verde si el objeto es de mejor nivel que lo equipado en ese casillero (nivel, luego rareza, luego refinado) y roja si es peor. Los atributos los decide el jugador con el detalle comparativo. |
| Bolsa en juego | Cajón que se despliega desde una pestaña con ícono en el borde derecho (o con la tecla I / Tab), con aviso de puntos sin repartir: oro, pociones, materiales, equipo, inventario completo y botín reciente. Permite equipar y tirar objetos sin salir del mapa. Parado en un santuario, un botón vende todos los objetos comunes. El oro del botín reciente se agrupa en una sola línea. |
| Muerte | Revivir con anuncio sin penalidad, o reaparecer en el santuario perdiendo 10% del nivel en experiencia. |
| Equipo | 6 slots (arma, casco, coraza, patas, amuleto, alas) y 5 rarezas: Común, Raro, Épico, Legendario y Mítico. |
| Sets | 5 sets (Quitina, Ámbar, Hierro negro, Viuda negra, Ciempiés de Hueso) que se ven sobre el personaje. 3 piezas dan un bono propio; 5 piezas reducen el enfriamiento de habilidades (10% a 25%). El set del Ciempiés solo cae del jefe. |
| Forja | Refinado de +0 a +6 con ámbar (sin riesgo) y de +6 a +9 con icor (puede fallar). Brillo a partir de +4 y +7. |
| Fusión | 3 objetos de la misma rareza se funden en uno de rareza superior, hasta Mítico. |
| Botín | Nombre y nivel del objeto en el suelo, con color por rareza. Tabla de probabilidades en el objeto `DROP` y visible en el Mercader. |
| Minimapa | Enemigos, élites, jefe, botín y portal. Tecla M para ocultarlo. |
| Gráficos | Sprites sombreados, suelo y obstáculos detallados, iluminación a resolución completa. |
| Mercader | Pociones, ámbar e icor. Venta de objetos. |
| Guardado | `localStorage` del navegador. |

## Integración con portales

En el código hay un objeto `PortalSDK` con funciones vacías (`gameplayStart`, `gameplayStop`, `commercialBreak`, `rewardedBreak`, `load`, `save`). Para publicar se reemplazan por las llamadas del SDK del portal:

- Anuncio recompensado: revivir al morir.
- Corte publicitario: entre niveles y al volver a la madriguera.
- Guardado: módulo de datos de CrazyGames en lugar de `localStorage`.

## Próximos pasos

- Regiones II a V: Pantano negro, Cripta bajo el cementerio, Colmena abandonada, Nido de la Reina Madre.
- Razas Escarabajo y Avispa.
- Alas de nivel 2 y 3.
- Integración real del SDK y pruebas de rendimiento en celulares.
