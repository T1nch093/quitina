# Quitina

RPG de acción oscuro para navegador. Criaturas insecto en un reino subterráneo podrido, con niveles, equipamiento, refinado y metamorfosis. Pensado para publicarse en portales de juegos web (CrazyGames, Poki) y monetizar con publicidad.

## Cómo jugar

Abre `index.html` en el navegador. No necesita instalación ni servidor.

- **Teclado y mouse:** WASD para moverte, clic o J para atacar, 1 · 2 · 3 habilidades, Q poción, Esc pausa.
- **Celular:** arrastra en la mitad izquierda para moverte y usa los botones de la derecha.

## Contenido de la versión 0.1

| Sistema | Estado |
|---|---|
| Razas | Mantis (guerrera) y Polilla (hechicera) jugables. Escarabajo y Avispa anunciadas. |
| Metamorfosis | 3 etapas por raza (nivel 6 y 12). En la etapa adulta se elige una de dos ramas. |
| Región I: Raíces podridas | 5 niveles, élites, jefe final (Ciempiés de Hueso) y 3 estrellas por nivel. |
| Equipo | 6 slots (arma, casco, coraza, patas, amuleto, alas) y 4 rarezas. |
| Forja | Refinado de +0 a +6 con ámbar (sin riesgo) y de +6 a +9 con icor (puede fallar). Brillo a partir de +4 y +7. |
| Fusión | 3 objetos de la misma rareza se funden en uno de rareza superior. |
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
