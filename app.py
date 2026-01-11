import streamlit as st
import pandas as pd
import altair as alt

df_bodovani = pd.read_csv('bodovani_ridici.csv')
df_products = pd.read_csv('products.csv')
df_filmy = pd.read_csv('filmy.csv')


df_selected = df_bodovani[(df_bodovani['uzemi_typ'] == 'kraj') & (df_bodovani['pohlavi_txt'] == 'celkem')]
df_selected = df_selected[['uzemi_txt', 'pocet_bodovanych_ridicu', 'celkovy_pocet_ridicu']]
df_filmy = df_filmy[['no', 'title', 'rating_avg', 'rating_total', 'year']]
df_top5_hodnoceni = df_filmy.nlargest(5, 'rating_avg')


# kódu, který jsi posílal dříve, načítáš df_filmy, ale tabulku df_filmy_year (agregovaný počet filmů) musíš
# v kódu vypočítat.
# Tímto vytvoříš tabulku, kterou st.bar_chart hledá

# 1. Řádek: Seskupení a výpočet
# Tento řádek dělá tři věci najednou (tzv. chaining)
# df_filmy_year = df_filmy.groupby('year')   .size().   reset_index(name='pocet_filmu')

# .groupby('year'): Vezme tvou hlavní tabulku a rozdělí ji do "balíčků" podle roku vydání. Všechny filmy z roku 1994
# dá na jednu hromadu, filmy z roku 1995 na druhou atd.
# .size(): Spočítá, kolik řádků (filmů) je v každém balíčku. Výsledkem je série, kde indexem je rok a hodnotou počet.
# .reset_index(name='pocet_filmu'): Toto je klíčový krok. Převede výsledek zpět na tabulku (DataFrame).
# Původní index (rok) se stane normálním sloupcem a nově vypočítaný sloupec s počty se pojmenuje 'pocet_filmu'

# 2. Řádek: Přejmenování sloupce
# df_filmy_year = df_filmy_year.rename(columns={'year': 'rok'})
# Tento příkaz vezme sloupec s názvem 'year' a přejmenuje ho na 'rok'.
# Důvodem je pravděpodobně to, že ve svém grafu (st.bar_chart) voláš osu x='rok'. Pokud bys tento řádek
# vynechal, Python by vyhodil chybu, protože by v tabulce hledal "rok", ale našel by jen "year".


df_filmy_year = df_filmy.groupby('year').size().reset_index(name='pocet_filmu')
df_filmy_year = df_filmy_year.rename(columns={'year': 'rok'})


st.title('Dashboard')
st.write("Analyzovaná data:")

_1, _2, _3 = st.columns(3)
with _1:
    st.success('Bodování řidičů')
with _2:
    st.warning('Prodeje e-shopu')
with _3:
    st.error('Top filmy')


st.info('Zobrazení v grafu:')


_bodovani, _products, _filmy = st.tabs(['Bodování řidičů', 'Prodeje e-shopu', 'Top filmy'])


# Bodování
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

# Produkty
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
                 })

# Filmy
with _filmy:
    # st.write(df_filmy.head(5))
    st.header("Statistiky filmové databáze")

    st.dataframe(df_top5_hodnoceni,
             hide_index=True,
             column_config={
                 'no': 'Pořadí',
                 'title': 'Název TOP 5 filmů',
                 'rating_avg': 'Průměrné hodnocení',
                 'rating_total': 'Počet hlasů', # Opravil jsem popisek, ať není stejný jako u hodnocení
                 'year': 'Rok'
             })

    st.bar_chart(df_filmy_year,
                 x='rok',
                 y='pocet_filmu',
                 x_label='Rok vydání',
                 y_label='Počet filmů'
                 )

    st.dataframe(df_filmy,
                 hide_index=True,
                 height=300,
                 column_config=
                 {
                     'no': 'Pořadí',
                     'title': 'Všechny hodnocené filmy',
                     'rating_avg': 'Celkové hodnocení',
                     'rating_total': 'Celkové hodnocení',
                     'year': 'Rok'

                 })

# no,title,rating_avg,rating_total,year
# rok, pocet_filmu, filmy_year.csv




