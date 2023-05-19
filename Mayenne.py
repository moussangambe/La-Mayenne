#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
get_ipython().system('jupyter nbconvert --to script Mayenne.ipynb')
# Lire les fichier Excel
df2019 = pd.read_excel('/Users/moussangambe/Desktop/Mayenne/Donées/data.gouv-cd53-2019.xlsx',header =0)
df2020 = pd.read_excel('/Users/moussangambe/Desktop/Mayenne/Donées/data.gouv-cd53-2020.xlsx',header =0)
df2021 = pd.read_excel('/Users/moussangambe/Desktop/Mayenne/Donées/data.gouv-cd53-2021.xlsx',header =0)
df2022 = pd.read_excel('/Users/moussangambe/Desktop/Mayenne/Donées/donnees-essentielles-de-subvention (1).xlsx',header =0)


# In[ ]:





# In[2]:


df2022


# In[ ]:





# In[ ]:





# In[3]:


# Calculer le pourcentage de NA dans chaque colonne
df2022.isna().mean() * 100




# In[4]:


df2021.isna().mean() * 100


# In[5]:


df2020.isna().mean() * 100


# In[6]:


df2019.isna().mean() * 100


# #### Les valeurs manquantes
# Nous remarquons la plus part des valeurs manquantes concernent:
# datesPeriodeVersement
# dateDeuxiemeVersement
# dateSoldeVersement

# #### Nettoyage de la base de données 2022

# In[7]:


# Supprimer les doublons
df2022.drop_duplicates(inplace=True)

# Supprimer les colonnes inutiles
df2022.drop(['nomAttribuant','idAttribuant','dateConvention','nature','conditionsVersement.1','datePremierVersement','dateDeuxiemeVersement','dateSoldeVersement',
'notificationUE','pourcentageSubvention'], axis=1, inplace=True)

# Supprimer les lignes contenant des valeurs manquantes
df2022 = df2022.dropna()

# Convertir la colonne 'date' en type 'datetime'
df2022['referenceDecision'] = pd.to_datetime(df2022['referenceDecision'])

# Extraire l'année et le mois de chaque date et les stocker dans une nouvelle colonne 'annee_mois'
df2022['annee_mois'] = df2022['referenceDecision'].dt.strftime('%Y-%m')
    



# In[8]:


df2022


# #### Nettoyage de la base de données 2021

# In[9]:


# Supprimer les doublons
df2021.drop_duplicates(inplace=True)
df2021 = df2021.rename(columns={'nombeneficiaire': 'nomBénéficiaire'})
# Supprimer les colonnes inutiles
df2021.drop(['nomAttribuant','idAttribuant','dateConvention','nature','datePremierVersement','datedeuxiemeVersement','dateVersementSolde',
'notificationUE','PourcentageSubvention'], axis=1, inplace=True)

# Supprimer les lignes contenant des valeurs manquantes
df2021 = df2021.dropna()

# Convertir la colonne 'date' en type 'datetime'
df2021['referenceDecision'] = pd.to_datetime(df2021['referenceDecision'])

# Extraire l'année et le mois de chaque date et les stocker dans une nouvelle colonne 'annee_mois'
df2021['annee_mois'] = df2021['referenceDecision'].dt.strftime('%Y-%m')


# In[10]:


df2021


# #### Nettoyage de la base de données 2020

# In[11]:


# Supprimer les doublons
df2020.drop_duplicates(inplace=True)
df2020 = df2020.rename(columns={'nombeneficiaire': 'nomBénéficiaire'})
# Supprimer les colonnes inutiles
df2020.drop(['nomAttribuant','idAttribuant','dateConvention','nature','datePremierVersement','datedeuxiemeVersement','dateVersementSolde',
'notificationUE','PourcentageSubvention'], axis=1, inplace=True)
# supprimer la ligne qui contient "740000/AN"
df2020 = df2020.drop(df2020.loc[df2020['montant']=='740000/AN'].index)
# convertir la colonne 'montant' en type float
df2020['montant'] = pd.to_numeric(df2020['montant'])
# Supprimer les lignes contenant des valeurs manquantes
df2020 = df2020.dropna()

# Convertir la colonne 'date' en type 'datetime'
df2020['referenceDecision'] = pd.to_datetime(df2020['referenceDecision'])

# Extraire l'année et le mois de chaque date et les stocker dans une nouvelle colonne 'annee_mois'
df2020['annee_mois'] = df2020['referenceDecision'].dt.strftime('%Y-%m')


# In[12]:


df2020


# #### Nettoyage de la base de données 2019

# In[13]:


# Supprimer les doublons
df2019.drop_duplicates(inplace=True)
df2019 = df2019.rename(columns={'nombeneficiaire': 'nomBénéficiaire'})
# Supprimer les colonnes inutiles
df2019.drop(['nomAttribuant','idAttribuant','dateConvention','nature','datePremierVersement','datedeuxiemeVersement','dateVersementSolde',
'notificationUE','PourcentageSubvention'], axis=1, inplace=True)

# Supprimer les lignes contenant des valeurs manquantes
df2019 = df2019.dropna()

# Convertir la colonne 'date' en type 'datetime'
df2019['referenceDecision'] = pd.to_datetime(df2019['referenceDecision'])
# Extraire l'année et le mois de chaque date et les stocker dans une nouvelle colonne 'annee_mois'
df2019['annee_mois'] = df2019['referenceDecision'].dt.strftime('%Y-%m')


# In[ ]:





# In[14]:


df2022


# In[15]:


import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html,dash_table
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output

# Agréger le montant total de subvention par année
df_agg1 = df2022.groupby(df2022['annee_mois'])['montant'].sum().reset_index()
df_agg2 = df2021.groupby(df2021['annee_mois'])['montant'].sum().reset_index()
df_agg3 = df2020.groupby(df2020['annee_mois'])['montant'].sum().reset_index()
df_agg4 = df2019.groupby(df2019['annee_mois'])['montant'].sum().reset_index()

# Agréger les montants de subvention par bénéficiaire
df_aggSub1 = df2022.groupby('nomBénéficiaire').sum().reset_index()
df_aggSub2 = df2021.groupby('nomBénéficiaire').sum().reset_index()
df_aggSub3 = df2020.groupby('nomBénéficiaire').sum().reset_index()
df_aggSub4 = df2019.groupby('nomBénéficiaire').sum().reset_index()

# Création du dictionnaire contenant les dataframes
dataframes1 = {
    'df_aggSub1': df_aggSub1,
    'df_aggSub2': df_aggSub2,
    'df_aggSub3': df_aggSub3,
    'df_aggSub4': df_aggSub4
}
# création du graphiques 1


# création du graphiques 1
graph1 = dcc.Graph(
    id='graph1',
    figure={
        'data': [
            go.Scatter(
                x=df_agg1['annee_mois'],
                y=df_agg1['montant'],
                mode='lines+markers',
                name = '2022'
            ),
            go.Scatter(
                x=df_agg2['annee_mois'],
                y=df_agg2['montant'],
                mode='lines+markers',
                name = '2021'
            ),
            go.Scatter(
                x=df_agg3['annee_mois'],
                y=df_agg3['montant'],
                mode='lines+markers',
                name = '2020'
            ),
            go.Scatter(
                x=df_agg4['annee_mois'],
                y=df_agg4['montant'],
                mode='lines+markers',
                name = '2019'
            )
        ],
        'layout': go.Layout(
            title='Comparaison des montants de subventions entre les années',
            xaxis={'title': 'Années'},
            yaxis={'title': 'Le montant de subvention en euros'}
        )
    }
)

# Création du graphique 2

# Création du dataframe agrégé
dfagg2022 = df2022.agg({'montant': 'sum'})
dfagg2021 = df2021.agg({'montant': 'sum'})
dfagg2020 = df2020.agg({'montant': 'sum'})
dfagg2019 = df2019.agg({'montant': 'sum'})
Yaxis=[dfagg2019['montant'],dfagg2020['montant'],dfagg2021['montant'],dfagg2022['montant']]
# Création du graphique
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Liste de couleurs
fig = px.histogram( x=['2019','2020','2021','2022'], y=Yaxis,title='Montants totaux pour chaque année',
                   color_discrete_sequence=['#1f77b4'], template='plotly_white')

# Personnalisation de l'histogramme

fig.update_traces(marker=dict(color=colors,line=dict(color=colors, width=1.5)),text=Yaxis)

fig.update_layout(
    xaxis=dict(title='Années', tickmode='linear', dtick=1),
    yaxis=dict(title='Montant total en euros', gridcolor='#f0f0f0'),
    bargap=0.1,
    margin=dict(l=40, r=40, t=40, b=40),
    plot_bgcolor='#ffffff'
)
graph2 = dcc.Graph(id='graph2', figure=fig)

# création du graphiques 3

# Création du graphique initial
fig = px.bar(df_aggSub1, x='nomBénéficiaire', y='montant', title='Montants de subventions accordées aux associations en 2022',
            color_discrete_sequence=['#1f77b4'], template='plotly_white')
graph3 = dcc.Graph(id='graph3', figure=fig)

# création de la mise en page
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# Création du Dropdown
dropdown1 = dcc.Dropdown(
        id='dropdown1',
        options=[
            {'label': 'Montants de subventions accordées aux associations en 2022', 'value': 'df_aggSub1'},
            {'label': 'Montants de subventions accordées aux associations en 2021', 'value': 'df_aggSub2'},
            {'label': 'Montants de subventions accordées aux associations en 2020', 'value': 'df_aggSub3'},
            {'label': 'Montants de subventions accordées aux associations en 2019', 'value': 'df_aggSub4'}
        ],
        value='df_aggSub1'
    )
# Callback pour mettre à jour le graphique
@app.callback(
    Output('graph3', 'figure'),
    Input('dropdown1','value')
)
def update_graph3(value):
    df = dataframes1[value]
    fig = px.bar(df, x='nomBénéficiaire', y='montant')

    # Ajouter le nom de l'axe des abscisses (axe x)
    fig.update_xaxes(title_text="Bénéficiaire")

    # Ajouter le nom de l'axe des ordonnées (axe y)
    fig.update_yaxes(title_text="Montant en euros")

    # Ajouter la légende
    fig.update_layout(
        legend=dict(
            title="Légende",
            title_font=dict(size=14),
            font=dict(size=12)
        )
    )

    # Ajouter le titre
    fig.update_layout(
        title={
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=16)
        }
    )

    return fig






# Creation du tableau

# Création du dictionnaire contenant les dataframes
dataframes2 = {
    'df_agg2022': df2022,
    'df_agg2021': df2021,
    'df_agg2020': df2020,
    'df_agg2019': df2019
}

dropdown2 = dcc.RadioItems(
         id='annees',
        options=[
            {'label': '2022', 'value': 'df_agg2022'},
            {'label': '2021', 'value': 'df_agg2021'},
            {'label': '2020', 'value': 'df_agg2020'},
            {'label': '2019', 'value': 'df_agg2019'}
        ],
        value='df_agg2022',inline=True
    )

# Création du tableau
table_columns = [
    {'name': 'Bénéficiaire', 'id': 'nomBénéficiaire'},
    {'name': 'Mois', 'id': 'annee_mois'},
    {'name': 'Montant', 'id': 'montant'},
    {'name': 'Objet de la subvention', 'id': 'objet'}
]
table = dash_table.DataTable(
    id='table',
    columns=table_columns,
    data=[]
)

dropdown3 = dcc.Dropdown(
        id='beneficiaire',
        options=[],
        multi=True
    )

@app.callback(
    Output('beneficiaire', 'options'),
    Input('annees', 'value')
    
)
def update_beneficiaires(dataframe_name):
    beneficiaires = dataframes2[dataframe_name]['nomBénéficiaire'].unique()
    options = [{'label': beneficiaire, 'value': beneficiaire} for beneficiaire in beneficiaires]
    return options


@app.callback(
    Output('table', 'data'),
    Input('beneficiaire', 'value'),
    Input('annees', 'value')
)
def update_table(beneficiaires, dataframe_name):
    df = dataframes2[dataframe_name]
    df_filtered = df[df['nomBénéficiaire'].isin(beneficiaires)]
    group_df = df_filtered.groupby(['annee_mois', 'nomBénéficiaire', 'objet'], as_index=False).sum()
    total_df = df_filtered.groupby('nomBénéficiaire', as_index=False).sum()
    total_df['annee_mois'] = 'Total'
    total_df['objet'] = 'Total'
    return group_df.append(total_df, ignore_index=True).to_dict('records')

# ajout d'un logo et d'un texte
logo1 = html.Div(
    children=[
    html.Img(src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5Tx5qu9iJNEte1mOE70YdfocZ1o7ahHJ67C0aHv_I09kPwvmvcBG2CViWNvQ&s', style={'height': '70px'})
    ]
)

logo2 = html.Div(
    children=[
    html.Img(src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyS_biJwfe4rK9ImWtDEuYFG73nu6Py2RigCQh-OuKHmX6rKQn8JGQN8lvgw&s', style={'height': '40px','align':'right'})
    ]
)

titre = html.Div(
    html.H1(children='Tableau de Bord de l\'attribution des subventions du Conseil départemental de la Mayenne', style={'margin': 'auto', 'textAlign': 'center'})
)


titre1 = html.Div(
    html.H6(children='Montants de subventions accordées aux associations en années', style={'margin': 'auto', 'textAlign': 'center'})
)
titre2 = html.Div(
    html.H6(children='Tableau des montants de subventions par mois, bénéficiaire et objet', style={'margin': 'auto', 'textAlign': 'center'})
)
text= html.Div(
    html.H5(children='©2023ngambmoussa', style={'margin': 'auto'})
)
def make_break(num_breaks):
    br_list = [html.Br()] * num_breaks
    return br_list


# In[ ]:





# In[ ]:


app.layout = html.Div([
    html.Div([
        dbc.Row([
        dbc.Col(logo1, width=2.5),
        dbc.Col(titre, width=15),
            *make_break(3),
    ], className='header'),
        dbc.Row([
        dbc.Col(graph1, width=6),
        dbc.Col(graph2, width=6)
    ], className='row'),
       *make_break(3),
       dbc.Row([
        dbc.Col([titre1,*make_break(1),dropdown1,graph3], md=6),
        dbc.Col([titre2,*make_break(1),dropdown2,dropdown3,table], md=6)
    ], className='row'),
        *make_break(3),
        dbc.Row([
            dbc.Col([logo2,text])
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)


# In[ ]:




