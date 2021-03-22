import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64


# upload file
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:file/txt;base64,{bin_str}" download="{bin_file}"><input type="button" value="Download"></a>'
    return href

# Set wide layout
st.set_page_config(layout="wide")

# Set side bar
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt'])
type_figure = st.sidebar.selectbox('Select type of figure', ["Individual samples", "Summary"])
st.sidebar.markdown("#### Author: **Johan Sebastián Sáenz**")
st.sidebar.markdown("#### Twitter: @SaenzJohanS")



# Read file with pandas and filter last row
st.title("MetaLab Quality control output v.01")
if uploaded_file is not None:
    st.write("\n 10 first rows of your summary file")
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

    # make plots
    if type_figure == "Summary":
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
        ax1.axvline(df[histo_variable].mean(), color='k', linestyle='dashed', linewidth=1)
        min_ylim, max_ylim = plt.ylim()
        ax1.text(df[histo_variable].mean() * 1, max_ylim * 0.9, 'Mean: {:.2f}'.format(df[histo_variable].mean()))
        ax1.set_ylabel("Number of samples")
        plt.savefig('histogram.png')
        col2.pyplot(fig)
        col2.markdown(get_binary_file_downloader_html('histogram.png', 'Picture'), unsafe_allow_html=True)
    else:
        col1.markdown("## Bar plot")
        barplot_variable = col1.selectbox('Select a variable', options=['MS/MS Identified', 'MS/MS Identified [%]',
                                                                      'Peptide Sequences Identified'])
        barplot_fig = fig, ax1 = plt.subplots()
        ax1.bar("Raw file", barplot_variable, data=df)
        ax1.set_xlabel("Samples")
        ax1.set_ylabel(barplot_variable)
        plt.xticks(rotation=90)
        plt.savefig('barplot.png')
        col1.pyplot(fig)
        col1.markdown(get_binary_file_downloader_html('barplot.png', 'Picture'), unsafe_allow_html=True)

        col2.markdown("## Scatter plot")
        scatter_variable = col2.selectbox('Select a variable for histogram',
                                        options=['MS/MS Identified', 'MS/MS Identified [%]',
                                                 'Peptide Sequences Identified'])
        hist_fig = fig, ax1 = plt.subplots()
        ax1.scatter("Raw file", scatter_variable, data=df)
        ax1.set_xlabel("Samples")
        ax1.set_ylabel(scatter_variable)
        plt.xticks(rotation=90)
        plt.savefig('Scatter.png')
        col2.pyplot(fig)
        col2.markdown(get_binary_file_downloader_html('Scatter.png', 'Picture'), unsafe_allow_html=True)




    st.markdown(
        "You can find the code in the [GitHub](https://www.github.com/SebasSaenz/Metalab_QC)")