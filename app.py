import streamlit as st
import pandas as pd
import altair as alt

df_products = pd.read_csv('products.csv')
df_bodovani = pd.read_csv('bodovani_ridici.csv')
df_selected = df_bodovani[(df_bodovani['uzemi_typ'] == 'kraj') & (df_bodovani['pohlavi_txt'] == 'celkem')]
df_selected = df_selected[['uzemi_txt', 'pocet_bodovanych_ridicu', 'celkovy_pocet_ridicu']]


st.title('Dashboard')
st.write("Toto bude jednoduchý text!")

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
    )

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