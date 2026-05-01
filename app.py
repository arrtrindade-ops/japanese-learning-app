import random

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Kana", layout="wide")


def cargar_datos():
    return pd.read_csv("data/kana.csv").fillna("")


def cargar_pronunciacion():
    return pd.read_csv("data/kana_pronunciation_examples.csv").fillna("")


df = cargar_datos()
df_pronunciacion = cargar_pronunciacion()

st.title("Kana（仮名［かな］）: hiragana（平仮名［ひらがな］） y katakana（片仮名［カタカナ］）")

capas_es = {
    "base": "Base",
    "dakuten": "Dakuten",
    "handakuten": "Handakuten",
    "yoon": "Combinaciones yōon",
    "special": "Signos especiales",
}

filas_es = {
    "vocal": "Vocales",
    "k": "Fila K",
    "s": "Fila S",
    "t": "Fila T",
    "n": "Fila N",
    "h": "Fila H",
    "m": "Fila M",
    "y": "Fila Y",
    "r": "Fila R",
    "w": "Fila W",
    "g": "Fila G",
    "z": "Fila Z",
    "d": "Fila D",
    "b": "Fila B",
    "p": "Fila P",
    "j": "Fila J",
    "special": "Signos especiales",
}

orden_vocales = {"a": 0, "i": 1, "u": 2, "e": 3, "o": 4, "": 99}

# --- Filtros dependientes ---
col1, col2, col3 = st.columns(3)

with col1:
    capas_disponibles = sorted(df["layer"].unique().tolist())
    opciones_capa = ["Todas"] + [capas_es.get(c, c) for c in capas_disponibles]
    capa_visible = st.selectbox("Capa", opciones_capa)

capa_real = "Todas" if capa_visible == "Todas" else {v: k for k, v in capas_es.items()}[capa_visible]

df_capa = df.copy()
if capa_real != "Todas":
    df_capa = df_capa[df_capa["layer"] == capa_real]

with col2:
    filas_disponibles = (
        df_capa[["row", "orden"]]
        .drop_duplicates()
        .sort_values("orden")["row"]
        .tolist()
    )
    opciones_fila = ["Todas"] + [filas_es.get(f, f) for f in filas_disponibles]
    fila_visible = st.selectbox("Fila", opciones_fila)

fila_real = "Todas" if fila_visible == "Todas" else {v: k for k, v in filas_es.items()}[fila_visible]

df_filtrado = df_capa.copy()
if fila_real != "Todas":
    df_filtrado = df_filtrado[df_filtrado["row"] == fila_real]

with col3:
    escritura = st.selectbox("Escritura", ["Ambas", "Hiragana", "Katakana"])

df_filtrado = df_filtrado.copy()
df_filtrado["orden_vocal"] = df_filtrado["vowel"].map(orden_vocales).fillna(99)
df_filtrado = df_filtrado.sort_values(by=["orden", "orden_vocal", "sound"])

# --- Tabla principal ---
st.subheader("Tabla de caracteres")

if escritura == "Hiragana":
    tabla = df_filtrado[["sound", "hiragana", "category_es", "notes_es"]].rename(
        columns={
            "sound": "sonido",
            "category_es": "categoría",
            "notes_es": "nota",
        }
    )
elif escritura == "Katakana":
    tabla = df_filtrado[["sound", "katakana", "category_es", "notes_es"]].rename(
        columns={
            "sound": "sonido",
            "category_es": "categoría",
            "notes_es": "nota",
        }
    )
else:
    tabla = df_filtrado[
        ["sound", "hiragana", "katakana", "category_es", "notes_es"]
    ].rename(
        columns={
            "sound": "sonido",
            "category_es": "categoría",
            "notes_es": "nota",
        }
    )

st.dataframe(tabla, use_container_width=True, hide_index=True)
st.caption(f"{len(tabla)} elementos")

# --- Vista en matriz ---
st.subheader("Tabla kana（仮名表［かなひょう］）")

df_matriz = df_filtrado[df_filtrado["vowel"] != ""].copy()

if escritura == "Katakana":
    columna_valor = "katakana"
else:
    columna_valor = "hiragana"

matriz = df_matriz.pivot_table(
    index="row",
    columns="vowel",
    values=columna_valor,
    aggfunc="first",
)

if matriz.empty:
    st.info("Este elemento no se representa en la matriz porque no pertenece a una fila vocálica.")
else:
    columnas_presentes = [v for v in ["a", "i", "u", "e", "o"] if v in matriz.columns]
    matriz = matriz[columnas_presentes]

    filas_ordenadas = (
        df_matriz[["row", "orden"]]
        .drop_duplicates()
        .sort_values("orden")["row"]
        .tolist()
    )
    filas_presentes = [f for f in filas_ordenadas if f in matriz.index]
    matriz = matriz.loc[filas_presentes]

    matriz = matriz.fillna("")
    matriz = matriz.rename(index=filas_es)
    matriz.index.name = "fila"
    matriz.columns.name = "vocal"

    st.dataframe(matriz, use_container_width=True)

# --- Pronunciación ---
st.subheader("Pronunciación — 発音［はつおん］: casos especiales")

orden_tipo = {
    "vocal larga": 0,
    "tsu pequeña": 1,
    "nasal final": 2,
}

df_pronunciacion = df_pronunciacion.copy()
df_pronunciacion["orden_tipo"] = df_pronunciacion["tipo"].map(orden_tipo).fillna(99)
df_pronunciacion = df_pronunciacion.sort_values(
    by=["orden_tipo", "subtipo", "ejemplo_jp"]
)

columnas_pronunciacion = [
    "subtipo",
    "estructura",
    "ejemplo_jp",
    "lectura",
    "hatsuon",
    "significado_es",
]

nombres_columnas = {
    "subtipo": "subtipo",
    "estructura": "estructura",
    "ejemplo_jp": "ejemplo",
    "lectura": "lectura",
    "hatsuon": "pronunciación",
    "significado_es": "significado",
}

for tipo in ["vocal larga", "tsu pequeña", "nasal final"]:
    bloque = df_pronunciacion[df_pronunciacion["tipo"] == tipo].copy()

    if len(bloque) > 0:
        st.markdown(f"### {tipo.capitalize()}")

        tabla_bloque = bloque[columnas_pronunciacion].rename(
            columns=nombres_columnas
        )

        st.dataframe(
            tabla_bloque,
            use_container_width=True,
            hide_index=True
        )

# --- Modo de práctica ---
st.markdown("## Modo de práctica (練習［れんしゅう］)")

modo_practica = st.selectbox(
    "Tipo de ejercicio",
    ["Caracteres", "Pronunciación"]
)

if modo_practica == "Caracteres":

    tipo_quiz = st.selectbox(
        "Tipo de práctica",
        [
            "Hiragana → sonido",
            "Katakana → sonido",
            "Sonido → hiragana",
            "Sonido → katakana",
        ],
    )

    quiz_data = df_filtrado.copy()

    if len(quiz_data) >= 4:

        def generar_pregunta_caracteres():
            item = quiz_data.sample(1).iloc[0].to_dict()

            if tipo_quiz == "Hiragana → sonido":
                pregunta = item["hiragana"]
                correcta = item["sound"]
                opciones = quiz_data["sound"].unique().tolist()

            elif tipo_quiz == "Katakana → sonido":
                pregunta = item["katakana"]
                correcta = item["sound"]
                opciones = quiz_data["sound"].unique().tolist()

            elif tipo_quiz == "Sonido → hiragana":
                pregunta = item["sound"]
                correcta = item["hiragana"]
                opciones = quiz_data["hiragana"].unique().tolist()

            else:
                pregunta = item["sound"]
                correcta = item["katakana"]
                opciones = quiz_data["katakana"].unique().tolist()

            incorrectas = [o for o in opciones if o != correcta]
            distractores = random.sample(incorrectas, 3)

            opciones_finales = distractores + [correcta]
            random.shuffle(opciones_finales)

            return pregunta, correcta, opciones_finales

        if (
            "pregunta_caracteres" not in st.session_state
            or st.session_state.get("tipo_quiz_caracteres") != tipo_quiz
        ):
            p, c, o = generar_pregunta_caracteres()
            st.session_state["pregunta_caracteres"] = p
            st.session_state["correcta_caracteres"] = c
            st.session_state["opciones_caracteres"] = o
            st.session_state["tipo_quiz_caracteres"] = tipo_quiz

        if st.button("Nueva pregunta", key="nueva_pregunta_caracteres"):
            p, c, o = generar_pregunta_caracteres()
            st.session_state["pregunta_caracteres"] = p
            st.session_state["correcta_caracteres"] = c
            st.session_state["opciones_caracteres"] = o

        st.markdown("### Ejercicio")
        st.write("Pregunta:")
        st.markdown(f"# {st.session_state['pregunta_caracteres']}")

        respuesta_usuario = st.radio(
            "Elige una opción:",
            st.session_state["opciones_caracteres"],
            key="respuesta_caracteres",
        )

        if st.button("Comprobar respuesta", key="comprobar_caracteres"):
            st.markdown("### Resultado")
            if respuesta_usuario == st.session_state["correcta_caracteres"]:
                st.success("¡Correcto!")
            else:
                st.error(
                    f"Incorrecto. La respuesta correcta es: "
                    f"{st.session_state['correcta_caracteres']}"
                )

    else:
        st.info("Necesitas al menos 4 elementos con los filtros actuales para usar este quiz.")

else:

    st.markdown("### Pronunciación")

    modo_pronunciacion = st.selectbox(
        "Modo de pronunciación",
        [
            "Nivel 1: vocal larga",
            "Nivel 2: vocal larga + tsu pequeña",
            "Nivel 3: vocal larga + tsu pequeña + nasal final",
            "Libre: elegir tipo"
        ]
    )

    if modo_pronunciacion == "Nivel 1: vocal larga":
        tipos_seleccionados = ["vocal larga"]

    elif modo_pronunciacion == "Nivel 2: vocal larga + tsu pequeña":
        tipos_seleccionados = ["vocal larga", "tsu pequeña"]

    elif modo_pronunciacion == "Nivel 3: vocal larga + tsu pequeña + nasal final":
        tipos_seleccionados = ["vocal larga", "tsu pequeña", "nasal final"]

    else:
        tipo_libre = st.selectbox(
            "Tipo de pronunciación",
            ["vocal larga", "tsu pequeña", "nasal final"]
        )
        tipos_seleccionados = [tipo_libre]

    quiz_pronunciacion = df_pronunciacion[
        df_pronunciacion["tipo"].isin(tipos_seleccionados)
    ].copy()

    if len(quiz_pronunciacion) > 0:

        def generar_pregunta_pronunciacion():
            item = quiz_pronunciacion.sample(1).iloc[0].to_dict()

            opciones = [
                item["opcion_a_es"],
                item["opcion_b_es"],
                item["opcion_c_es"],
                item["opcion_d_es"],
            ]

            random.shuffle(opciones)

            return item, opciones

        if (
            "item_pronunciacion" not in st.session_state
            or st.session_state.get("modo_pronunciacion_actual") != modo_pronunciacion
        ):
            item, opciones = generar_pregunta_pronunciacion()
            st.session_state["item_pronunciacion"] = item
            st.session_state["opciones_pronunciacion"] = opciones
            st.session_state["modo_pronunciacion_actual"] = modo_pronunciacion

        if st.button("Nueva pregunta", key="nueva_pregunta_pronunciacion"):
            item, opciones = generar_pregunta_pronunciacion()
            st.session_state["item_pronunciacion"] = item
            st.session_state["opciones_pronunciacion"] = opciones

        item = st.session_state["item_pronunciacion"]

        st.markdown("### Ejercicio")
        st.caption(f"Tipo: {item['tipo']} — {item['subtipo']}")

        st.markdown(f"# {item['ejemplo_jp']}")
        st.write(f"Lectura: {item['lectura']}")
        st.write(f"Significado: {item['significado_es']}")

        respuesta = st.radio(
            item["pregunta_es"],
            st.session_state["opciones_pronunciacion"],
            key="respuesta_pronunciacion",
        )

        if st.button("Comprobar respuesta", key="comprobar_pronunciacion"):
            st.markdown("### Resultado")
            if respuesta == item["respuesta_correcta_es"]:
                st.success("¡Correcto!")
                st.info(f"Explicación: {item['hatsuon']}")
            else:
                st.error("Incorrecto.")
                st.warning(
                    f"Este caso pertenece a: {item['tipo']} — {item['subtipo']}."
                )
                st.info(
                    f"Respuesta correcta: {item['respuesta_correcta_es']}. "
                    f"Explicación: {item['hatsuon']}"
                )

    else:
        st.info("No hay ejemplos disponibles para este modo.")