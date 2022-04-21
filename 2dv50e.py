# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import umap
import streamlit as st
import plotly.express as px
from sklearn import preprocessing

# Page layout
st.set_page_config(page_title='Visually-Assisted Performance Evaluation of Metamodels in Stacking Ensemble Learning',layout='wide')

# Sidebar - Collects user input features into dataframe
st.sidebar.header('Upload your model probabilities data')
uploaded_probabilities = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"], key=0)
# st.sidebar.header('Upload your target data')
# uploaded_target = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"], key=1)
st.sidebar.header('Upload your model data')
uploaded_model = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"], key=2)


# Sidebar - Specify parameter settings
st.sidebar.header('Set Parameters for UMAP')
parameter_umap_n_neighbors = st.sidebar.number_input('Number of neighbors (n_neighbors)', 5)
parameter_umap_metric = st.sidebar.selectbox('Metric', ('euclidean', 'manhattan', 'chebyshev', 'minkowski'))
parameter_umap_min_dist = st.sidebar.number_input('Minimal distance', 0.1)
st.sidebar.write('---')

st.subheader('Dataset')
st.write('The dataset consists of the model probabilities for each model in the ensemble and the target variable.')

algos = {1:'K-Nearest Neighbor', 2:'Support Vector Machine', 3:'Gaussian Naive Bayes', 4:'Multilayer Perceptron', 5:'Logistic Regression',
        6:'Linear Discriminant Analysis', 7:'Quadratic Discriminant Analysis', 8:'Random Forest', 9:'Extra Trees', 10:'Adaptive Boosting',
        11:'Gradient Boosting'}


# Function to plot the UMAP plot
def create_UMAP_chart(df_probabilities, algo_nr):
    # Create UMAP
    umap_model = umap.UMAP(n_neighbors=parameter_umap_n_neighbors, metric=parameter_umap_metric, min_dist=parameter_umap_min_dist)
    umap_embedding = umap_model.fit_transform(df_probabilities)
    #convert umap_embedding to dataframe
    df_umap = pd.DataFrame(umap_embedding, columns=['UMAP_1', 'UMAP_2'])
    # Add model name
    df_umap['algorithm_nr'] = algo_nr
    #match algo_nr with algos keys
    df_umap['algorithm_name'] = df_umap['algorithm_nr'].map(algos)
    # add overall performance data to umap
    df_umap['performance'] = df_model['overall_performance']
    # re-scale df.performance in scale from 0 to 1 and save as new column for better visualization
    df_umap['performance_scaled'] = preprocessing.MinMaxScaler().fit_transform(df_umap['performance'].values.reshape(-1,1))
    # Plot UMAP with algorithm as a color 
    fig = px.scatter(df_umap, x='UMAP_1', y='UMAP_2', color='algorithm_name',
            hover_name='algorithm_name', hover_data=['performance'])
    fig.update_layout(title_text='UMAP Plot')
    # change legend name to algorithm
    fig.update_layout(legend_title_text='Algorithm')
    # change size of points to 10, reduce opacity and change marker border color, based on performance
    fig.update_traces(marker=dict(size=10, opacity=0.75, line=dict(width=2, color=df_umap['performance_scaled'])), 
    selector=dict(mode='markers'))
    st.plotly_chart(fig)



if uploaded_probabilities is not None and uploaded_model is not None:
    df_probabilities = pd.read_csv(uploaded_probabilities)
    df_model = pd.read_csv(uploaded_model)
    algo_nr = df_model.algorithm_id
    # Check if the number of rows in the probabilities dataframe is equal to the number of columns in the models dataframe
    if len(df_probabilities) == len(algo_nr):
        create_UMAP_chart(df_probabilities, algo_nr)
    else:
        st.write('The number of columns in the probabilities dataframe is not equal to the number of rows in the target dataframe.')
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        path = r'D:\github\2dv50e\Data\1. Heart Disease'
        df_probabilities = pd.read_csv(path + r'\topModelsProbabilities.csv')
        df_target = pd.read_csv(path + r'\target.csv')
        df_model = pd.read_csv(path + r'\topModels.csv')
        algo_nr = df_model.algorithm_id
        create_UMAP_chart(df_probabilities, algo_nr)





