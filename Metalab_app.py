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

# Set wide layout
st.set_page_config(layout="wide")

# upload file
st.title("Summary of Metalab output v.01")
st.markdown("#### Author: **Johan Sebastián Saenz**")
st.markdown("#### Twitter: @SaenzJohanS")

# Read file with pandas
uploaded_file = st.file_uploader("Choose a file", type=['txt'])
if uploaded_file is not None:
    df = pd.read_table(uploaded_file)
    df = df[df['Raw file'] != 'Total']
    st.write(df.head(10))

    # make a summary table
    st.markdown("## Summary table")
    table = df[["MS/MS Identified", "MS/MS Identified [%]", "Peptide Sequences Identified"]].describe()
    table.to_csv("table.csv")
    st.write(table)
    st.markdown(get_binary_file_downloader_html('table.csv', 'Picture'), unsafe_allow_html=True)

    st.beta_columns((3,2))
    col1, col2 = st.beta_columns(2)

    # make a violinplot
    col1.markdown("## Violin plot")
    boxplot_variable = col1.selectbox('Select a variable', options=['MS/MS Identified', 'MS/MS Identified [%]',
                                                                  'Peptide Sequences Identified'])
    boxplot_fig = fig, ax1 = plt.subplots()
    ax1.violinplot(df[boxplot_variable])
    ax1.set_xlabel(" ")
    ax1.set_ylabel(boxplot_variable)
    plt.savefig('violinplot.png')
    col1.pyplot(fig)
    col1.markdown(get_binary_file_downloader_html('violinplot.png', 'Picture'), unsafe_allow_html=True)

    # make a histogram
    col2.markdown("## Histogram plot")
    histo_variable = col2.selectbox('Select a variable for histogram',
                                  options=['MS/MS Identified', 'MS/MS Identified [%]',
                                           'Peptide Sequences Identified'])
    hist_fig = fig, ax1 = plt.subplots()
    ax1.hist(df[histo_variable])
    ax1.set_xlabel(histo_variable)
    ax1.set_ylabel("Number of samples")
    plt.savefig('histogram.png')
    col2.pyplot(fig)
    col2.markdown(get_binary_file_downloader_html('histogram.png', 'Picture'), unsafe_allow_html=True)

    st.markdown(
        "You can find the code in the [GitHub](https://www.github.com/SebasSaenz/Metalab_QC)")