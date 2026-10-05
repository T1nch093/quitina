# Quitina

RPG de acción oscuro para navegador. Criaturas insecto en un reino subterráneo podrido, con niveles, equipamiento, refinado y metamorfosis. Pensado para publicarse en portales de juegos web (CrazyGames, Poki) y monetizar con publicidad.

## Cómo jugar

Abre `index.html` en el navegador. No necesita instalación ni servidor.

- **Teclado y mouse:** WASD para moverte, clic o J para atacar, 1 · 2 · 3 habilidades, Q poción, I bolsa, C poderes, H caza automática, M mapa grande, B volver a la madriguera, Esc pausa.
- **Celular:** arrastra en la mitad izquierda para moverte y usa los botones de la derecha.

## Contenido de la versión 0.4

| Sistema | Estado |
|---|---|
| Razas | Mantis (guerrera) y Polilla (hechicera) jugables. Escarabajo y Avispa anunciadas. La Mantis tiene Torbellino, Embestida y Furia (+70% de daño por 4 s). El golpe simple hace 70% del daño base. |
| Metamorfosis | 3 etapas por raza (nivel 6 y 12). En la etapa adulta se elige una de dos ramas. |
| Región I: Raíces podridas | Mapa abierto de 4800 × 3600 con santuario de entrada y 5 zonas por nivel recomendado (1–4 a 13–16). Las criaturas reaparecen a los 9–14 s, las élites al minuto y el jefe (Ciempiés de Hueso) cada 5 minutos. Las zonas descubiertas habilitan el viaje directo. |
| Atributos | 4 puntos por nivel para Fuerza, Caparazón, Agilidad y Esencia. Reparto automático con receta por raza y reinicio pagando oro. |
| Habilidades | Rango 1 a 5, con 1 punto cada 3 niveles. La habilidad 2 se desbloquea en nivel 3 y la 3 en nivel 6. Los rangos 3 y 5 cambian el funcionamiento (radio, aturdimiento, duración, robo de vida). |
| Caza automática | Estilo MU Helper (tecla H): caza alrededor del punto de activación, usa habilidades, recoge botín según filtros y toma pociones. Se configura en la pausa. |
| Bolsa en juego | Tecla I o Tab: oro, pociones, materiales, equipo, inventario completo y botín reciente. Permite equipar y tirar objetos sin salir del mapa. |
| Muerte | Revivir con anuncio sin penalidad, o reaparecer en el santuario perdiendo 10% del nivel en experiencia. |
| Equipo | 6 slots (arma, casco, coraza, patas, amuleto, alas) y 5 rarezas: Común, Raro, Épico, Legendario y Mítico. |
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
