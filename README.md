# Quitina

RPG de acción oscuro para navegador. Criaturas insecto en un reino subterráneo podrido, con niveles, equipamiento, refinado y metamorfosis. Pensado para publicarse en portales de juegos web (CrazyGames, Poki) y monetizar con publicidad.

## Cómo jugar

Abre `index.html` en el navegador. No necesita instalación ni servidor. La carpeta `assets/` tiene el arte conceptual de la portada y el atlas de sprites de la Mantis. Las hojas originales están en `hojas/`; para regenerar el atlas: `python3 tools/armar_sprites.py` (necesita Pillow, NumPy y SciPy).

- **Teclado y mouse:** WASD para moverte, clic o J para atacar, 1 · 2 · 3 habilidades, Q poción, I bolsa, C poderes, H caza automática, M mapa grande, B volver a la madriguera, Esc pausa.
- **Celular:** arrastra en la mitad izquierda para moverte y usa los botones de la derecha.

## Instalarlo como app en el celular

El juego es una app web instalable (PWA): tiene manifiesto, íconos y funciona sin conexión una vez abierto. Para instalarlo tiene que estar publicado en una dirección HTTPS (por ejemplo GitHub Pages). Desde Chrome en Android: abrir la dirección, menú ⋮ → **Instalar app** (o *Agregar a pantalla principal*). Se abre a pantalla completa y apaisado, sin barra del navegador. Si se juega desde el navegador, al entrar al mundo pide pantalla completa y gira a apaisado cuando el teléfono lo permite.

## Contenido de la versión 0.24

| Sistema | Estado |
|---|---|
| Sprites | La Mantis usa sprites animados del arte conceptual: quieto (4), caminar (8), tajada frontal (golpe simple y Embestida), tajada hacia arriba (Furia), tajada giratoria (Torbellino), golpe recibido y muerte. Una dirección espejada. Los sets se marcan con un brillo del color del set; el retrato de la madriguera sigue mostrando cada pieza. En la pausa se puede volver al dibujo clásico. |
| Personaje | Nombre propio al crear la criatura, placa con nombre y barras de vida y energía sobre la cabeza, y círculo de selección bajo los pies. La Mantis es una guerrera humanoide (hombreras, brazales con hebillas, cinturón, bolso y capa en la forma adulta) basada en el arte conceptual. |
| Razas | Mantis (guerrera) y Polilla (hechicera) jugables. Escarabajo y Avispa anunciadas. La Mantis tiene Torbellino, Embestida y Furia (+70% de daño por 4 s). El golpe simple hace 70% del daño base. |
| Metamorfosis | 3 etapas por raza (nivel 6 y 12). En la etapa adulta se elige una de dos ramas. |
| Región I: Raíces podridas | Mapa abierto de 4800 × 3600 con santuario de entrada y 5 zonas por nivel recomendado (1–4 a 13–16). Las criaturas reaparecen a los 9–14 s, las élites al minuto y el jefe (Ciempiés de Hueso) cada 5 minutos. Las zonas descubiertas habilitan el viaje directo. |
| Atributos | 4 puntos por nivel para Fuerza, Caparazón, Agilidad y Esencia. Reparto automático con receta por raza y reinicio pagando oro. |
| Habilidades | Rango 1 a 5, con 1 punto cada 3 niveles. La habilidad 2 se desbloquea en nivel 3 y la 3 en nivel 6. En los rangos 3 y 5 cada habilidad **cambia de forma** y ataca distinto. Mantis: Torbellino → Torbellino doble (atrae y gira dos veces) → Tornado de guadañas (6 cuchillas en abanico); Embestida → Embestida de sombra (el corte estalla) → Triple embestida (encadena 2 más); Furia → Furia sangrienta (cada golpe lanza un tajo) → Furia del depredador (rugido que empuja y aturde). Polilla: Polvo maldito → Nube maldita → Plaga (la maldición salta); Fuego frío → Doble estallido → Invierno (8 esquirlas); Enjambre → Nube de esporas → Esporas explosivas. Los botones muestran II o III según la forma. |
| Santuarios | 5 santuarios de ámbar (entrada y borde de cada zona): curan, alejan a las criaturas y tienen a Brugo, el artesano: flecha y nombre siempre visibles; se toca o cliquea (si estás lejos, el personaje camina hasta él) o tecla E. Su panel se abre como cajón lateral (igual que la bolsa, el mapa queda a la vista y en pausa; tocar el mapa lo cierra) con Mesa, Depósito y Mercader. |
| Brugo + bolsa | En apaisado (o pantallas de 600 px o más) Brugo se abre a la izquierda y la bolsa a la derecha, como en el MU. Tocar un objeto de la bolsa hace la acción de la pestaña abierta: Mesa → lo pone o saca de la mesa; Depósito → lo guarda; Mercader → muestra el detalle con Vender. En vertical, Brugo sigue abriéndose solo con sus propias listas. |
| Mesa de Brugo | Se colocan objetos en la mesa (3 lugares) tocándolos en la bolsa o en lo equipado, y Brugo hace lo que corresponda con un botón: **1 objeto** → refinar +1 (con probabilidad, riesgo y protección por anuncio); **3 piezas del mismo set** → pieza nueva del set elegida (arma, casco, coraza, patas o amuleto) un nivel más arriba, con 25% de subir rareza; **3 de la misma rareza** → un objeto de rareza superior. Si sirven las dos recetas se elige cuál. Muestra el resultado esperado, costos y probabilidad antes de confirmar. También es la pestaña Mesa de la madriguera. |
| Depósito | Baúl de 60 lugares compartido entre santuarios y madriguera. |
| Caza automática | Estilo MU Helper (tecla H): caza alrededor del punto de activación, usa habilidades, recoge botín según filtros y toma pociones. Con la bolsa llena o sin pociones va sola al santuario más cercano, vende comunes y raros peores que lo equipado, compra hasta 10 pociones, guarda en el depósito lo más débil si sigue llena y vuelve al punto de caza. Se configura en la pausa. |
| Objetos excelentes | Estilo MU: cualquier objeto puede salir **Excelente** (nombre y borde verdes, +15% de atributos base) con 1 o 2 opciones especiales: golpe excelente (daño ×1,6), vida al matar, energía al matar, +oro de criaturas, −daño recibido o +velocidad de ataque. Probabilidad: 2,5% en criaturas, 10% en élites, 30% en jefes. Aviso en pantalla cuando cae uno. La caza automática siempre los recoge; no se funden ni se venden en lote. |
| Suerte | 12% de los objetos raros o mejores traen Suerte: +5% de crítico y +20% de probabilidad al refinar. |
| Refinado | Hasta +12. De +0 a +6 con ámbar y sin riesgo; de +6 en adelante con icor (desde +9 cuesta 2) y probabilidad 70/60/50/45/35/25%. Si falla entre +6 y +8 baja un nivel; **desde +9, si falla vuelve a +0**. Se puede proteger un intento viendo un anuncio. |
| Foso de la Colmena | Evento por horario (estilo Devil Square): abre cada 15 minutos durante 3, desde nivel 6, una vez por apertura. Se entra desde el panel de Brugo. 5 oleadas en 4 minutos; recompensa por oleada y, al ganar, objeto excelente garantizado, icor, ámbar, oro y 25% de un nivel de experiencia. Aviso en pantalla cuando está abierto. Si caes, reaparecer te saca del foso; revivir con anuncio te deja seguir. |
| Renacer | Estilo reset del MU: desde nivel 30, en la madriguera (pestaña Poderes), vuelves a nivel 1 conservando equipo, metamorfosis y habilidades. Cada renacer da 25 puntos de atributo permanentes y +4% de vida y daño; cuesta 3.000 oro por renacer acumulado. El nombre muestra ✦ y la cantidad. |

| Calidad de imagen | Resolución nativa de la pantalla (hasta 3×) y sprites a 300 px. Modo automático que baja la resolución si no llega a ~45 cuadros por segundo; también máxima y ahorro de batería desde el menú. Zoom más cercano en celulares. |
| Interfaz | Íconos en lugar de texto: caza automática (flechas en círculo; activa se pone verde azulado y gira, sin cartel en pantalla) y menú (tres líneas, pausa el juego). Los puntos sin repartir se avisan solo con el número sobre la bolsa. El cartel de zona ya no se encima con la barra del jefe. |
| Subir de nivel: la muda | El insecto rompe su caparazón: cámara lenta, capullo de ámbar con grietas de luz que estalla en esquirlas, onda que empuja y aturde a los enemigos cercanos, columna de luz, título grande «Nivel N» con lo ganado y la piel vieja (exuvia) queda en el suelo unos segundos. Sonido propio. |
| Bitácora (inicio) | Lista de criaturas creadas a la izquierda y ficha de la elegida a la derecha (retrato, nivel, tipo, color, vida, daño, oro, zona más profunda) con Descender, Madriguera y Borrar (confirmación doble). Vacía, invita a crear la primera. |
| Crear criatura | Linaje, **tipo** (Mantis: Segadora, Acechadora, Coracera; Polilla: Bruja, Ceniza, Capullo; +3 al atributo principal y receta de reparto propia), **color del caparazón** (Musgo, Ámbar, Ceniza, Sangre, Noche) y nombre. |
| Mapas del reino | Ícono de mapa (tecla V): viajar con oro a los 5 santuarios y 5 zonas. Se puede ir desde 3 niveles por debajo del recomendado; si estás por debajo, aparece «(nivel sugerido N)» en rojo. Regiones II–V anunciadas. |
| Set completo +10 | Dos destellos dorados giran alrededor del cuerpo dejando estela. El arma +10 suma lenguas violetas que giran sobre las guadañas. En el menú hay un botón de prueba para equipar el set Ciempiés +10. |
| Íconos pintados | Hojas generadas con IA (fondo magenta, 3×2) en `hojas/iconos-*.jpg`; `python3 tools/armar_iconos.py` arma `assets/iconos.webp`. Sets con íconos: Ciempiés de Hueso y Hierro negro, más alas, ámbar, icor, poción y oro (también en el suelo y en los contadores). Los sets sin hoja usan el ícono dibujado. |
| Equipo montado | El sprite de la Mantis se separa por color y altura en guadañas, cabeza, torso y patas; cada pieza equipada repinta su zona con la paleta del set (Hierro negro acero, Ámbar dorado, Viuda negra rojo oscuro, Ciempiés hueso). Las alas se ven detrás y el amuleto brilla en el pecho. También en la bitácora y la madriguera. Quitina es el aspecto natural. |
| Armas +10 | Fuego violeta solo sobre las guadañas (estilo Lineage): llamas y rayos que salen del filo, tajos violetas; +12 más intenso. Desde +4 el filo brilla con el color del refinado. En la bolsa el casillero arde en violeta. |
| Vender | Con Brugo (Mercader): vender comunes, vender todos los peores (▼) o tocar un objeto para venderlo; en la ventana doble también desde la bolsa. Cerca de un santuario el detalle de la bolsa ofrece Vender. La caza automática ahora vende todo lo peor que lo equipado (no excelentes ni con suerte). |
| Tamaño de la interfaz | En el menú: 80% a 130% (100% por defecto). Escala bolsa, Brugo, botones táctiles, íconos de arriba y HUD dibujado. Botones táctiles al tamaño recomendado (ataque 76 px, habilidades 52 px, poción 44 px). |
| Estilo de ventanas | Inspirado en MU Online: ventanas de metal oscuro con doble borde y remaches, barra de título roja con ✕, equipo alrededor de la silueta (alas, casco y amuleto arriba; arma, coraza y patas; resumen de set al costado), inventario como cuadrícula apretada con brillo por rareza y el oro abajo. La bolsa es una ventana angosta (como el inventario del MU, cerca de un cuarto del ancho en apaisado) con ventana de detalle compacta al costado. |
| Celular apaisado | App instalable a pantalla completa y apaisada. HUD compacto: bolsa en la fila de íconos de arriba, minimapa más chico, botones de ataque un poco menores y márgenes para la cámara/muesca. Si se juega vertical aparece un aviso para girar el teléfono (se puede descartar). Vida, energía, nivel y experiencia en barras arriba a la izquierda (el joystick ya no tapa la vida). Portada, creación de criatura y madriguera compactas en apaisado; las pantallas ya no se cortan arriba. |
| Comparación rápida | En las miniaturas del inventario, flecha verde si el objeto es de mejor nivel que lo equipado en ese casillero (nivel, luego rareza, luego refinado) y roja si es peor. Los atributos los decide el jugador con el detalle comparativo. |
| Bolsa en juego | Cajón que se despliega desde una pestaña con ícono en el borde derecho (o con la tecla I / Tab), con aviso de puntos sin repartir: oro, pociones, materiales, equipo, inventario completo y botín reciente. Más angosta, con casilleros chicos; al tocar un objeto se abre una ventana con sus atributos, la comparación y Equipar / Tirar (al costado de la bolsa en apaisado, abajo en vertical), sin tener que bajar. Los puntos sin repartir se marcan con flechas verdes: en el ícono de la bolsa, la pestaña Poderes, los botones +1 y Mejorar y el botón de la habilidad que se puede mejorar. Parado en un santuario, un botón vende todos los objetos comunes. El oro del botín reciente se agrupa en una sola línea. |
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
