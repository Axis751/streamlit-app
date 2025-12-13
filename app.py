import streamlit as st
import pandas as pd
import altair as alt

df_products = pd.read_csv('products.csv')
df_bodovani = pd.read_csv('bodovani_ridici.csv')
df_selected = df_bodovani[(df_bodovani['uzemi_typ'] == 'kraj') & (df_bodovani['pohlavi_txt'] == 'celkem')]
df_selected = df_selected[['uzemi_txt', 'pocet_bodovanych_ridicu', 'celkovy_pocet_ridicu']]

st.title('Dashboard')
st.write("Toto bude jednoduchý text!")


# ---
st.scatter_chart(df_selected,
      x='celkovy_pocet_ridicu',
      y='pocet_bodovanych_ridicu',
      x_label='Celkový počet řidičů',
      color='uzemi_txt')
# ---


_bodovani, _products = st.tabs(['Bodování řidičů', 'Produkty'])

with _bodovani:
    _1, _2 = st.columns(2)
    chart = alt.Chart(df_selected).mark_circle(size=120).encode(
        x=alt.X('celkovy_pocet_ridicu', title='Celkový počet řidičů'),
        y=alt.Y('pocet_bodovanych_ridicu', title='Počet bodovaných řidičů'),
        tooltip=[
            alt.Tooltip('celkovy_pocet_ridicu', title='Celkový počet řidičů'),
            alt.Tooltip('pocet_bodovanych_ridicu', title='Počet bodovaných řidičů'),
            alt.Tooltip('uzemi_txt', title='Kraj')]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    st.dataframe(df_selected,
                 hide_index=True,
                 height=300,
                 column_config=
                 {
                     'uzemi_txt': 'Kraj',
                     'celkovy_pocet_ridicu': 'Celkový počet řidičů',
                     'pocet_bodovanych_ridicu': 'Počet bodovaných řidičů'
                 })

with _products:
    st.bar_chart(df_products,
                 x='product_name',
                 y='price',
                 x_label='Název produktu',
                 y_label='Cena [Kč]')

    st.dataframe(df_products[['product_name', 'price']],
                 hide_index=True,
                 column_config=
                 {
                     'price': 'Cena [Kč]',
                     'product_name': 'Název produktu'
                 }
                 )

# _data, _graph, _desc = st.tabs(['Ukázka dat', 'Grafické zobrazení', 'Poznámky'])
# with _data:
#     st.dataframe(df_products.head(), hide_index=True)
# with _graph:
#     st.line_chart(df_products['price'].head(10))
# with _desc:
#     st.write("Toto bude popis!")
#
#
#
#
# _1, _2, _3 = st.columns(3)
# with _1:
#     st.success('Tohle je jasný úspěch!')
# with _2:
#     st.warning('Toto je varování!')
# with _3:
#     st.error('Takhle ukazuju chyby!')
#
# _1, _2 = st.columns(2)
# with _1:
#     st.info('Toto bude informační kousek!')
# with _2:
#     st.code("print('Ahoj')", language='python')
#
# st.code("""for i in range(10):
#     print(i)""", language='python')
#
#
# st.dataframe(df_products, hide_index=True)
# if "counter" not in st.session_state:
#     st.session_state.counter = 0
#
# st.session_state.counter += 1
#
# text = st.text_input("Enter some text")
#
# st.header(f"This page has run {st.session_state.counter} times and text is \"{text}\".")
# st.button("Run it again")