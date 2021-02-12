import streamlit as st
import altair as alt
from vega_datasets import data

def draw_map():
    map_source = alt.topo_feature(data.world_110m.url, 'countries')
    world_map = alt.Chart(map_source).mark_geoshape(
        fill='#666666',
        stroke='white'
    ).properties(
        width=700,
        height=300
    ).project(
        'equirectangular'  # options: ['equirectangular', 'mercator', 'orthographic', 'gnomonic']
    )
    st.write(world_map)