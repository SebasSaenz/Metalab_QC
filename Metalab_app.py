import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import os
import sidetable
import base64

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:file/txt;base64,{bin_str}" download="{bin_file}"><input type="button" value="Download"></a>'
    return href

#upload file
st.title("Summary of Metalab output v.01")
st.markdown("#### Author: **Johan Sebastián Saenz**")
st.markdown("#### Twitter: @SaenzJohanS")

#Read file with pandas
uploaded_file = st.file_uploader("Choose a file", type=['txt'])
if uploaded_file is not None:
    df = pd.read_table(uploaded_file)
    st.write(df.head(10))

    #make a summary table
    st.markdown("## Summary table")
    table = df[["MS/MS Identified", "MS/MS Identified [%]", "Peptide Sequences Identified"]].describe()
    table.to_csv("table.csv")
    st.write(table)
    st.markdown(get_binary_file_downloader_html('table.csv', 'Picture'), unsafe_allow_html=True)

    #make a violinplot
    st.markdown("## Violin plot")
    boxplot_variable = st.selectbox('Select a variable', options=['MS/MS Identified', 'MS/MS Identified [%]',
                                                                  'Peptide Sequences Identified'])

    boxplot_fig = fig, ax1 = plt.subplots()
    ax1.violinplot(df[boxplot_variable])
    ax1.set_title(boxplot_variable)
    plt.savefig('violinplot.png')
    st.pyplot()
    st.markdown(get_binary_file_downloader_html('violinplot.png', 'Picture'), unsafe_allow_html=True)

    #make a histogram
    st.markdown("## Histogram plot")
    histo_variable = st.selectbox('Select a variable for histogram', options=['MS/MS Identified', 'MS/MS Identified [%]',
                                                                              'Peptide Sequences Identified'])
    hist_fig = fig, ax1 = plt.subplots()
    ax1.hist(df[histo_variable])
    ax1.set_title(histo_variable)
    plt.savefig('histogram.png')
    st.pyplot()
    st.markdown(get_binary_file_downloader_html('histogram.png', 'Picture'), unsafe_allow_html=True)