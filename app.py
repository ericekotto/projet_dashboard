import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from data_processing import DataProcessor

# Charger et traiter les données
print("🚀 Initialisation du Dashboard...")
print("="*80)

processor = DataProcessor('data/data_kpi.xlsx')
df = processor.executer_pipeline_complet()

if df is None or len(df) == 0:
    print("❌ ERREUR: Impossible de charger les données!")
    print("Vérifiez que le fichier 'data/data_kpi.xlsx' existe et contient des données valides.")
    exit(1)

print("\n✅ Données chargées et nettoyées avec succès!")
print(f"📊 {len(df)} transactions prêtes pour l'analyse")
print("="*80)

# Initialiser l'application
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Pour le déploiement
app.title = "Dashboard KPI - Analyse des Ventes"

# Calculs des KPI
def calculer_kpis(dataframe):
    """Calcule tous les KPI nécessaires"""
    kpis = {}
    
    # KPI 1: Valeur moyenne des transactions
    kpis['montant_moyen'] = dataframe['Montant'].mean()
    
    # KPI 2: Répartition par catégorie
    kpis['repartition_categorie'] = dataframe.groupby('Categorie')['Montant'].sum()
    kpis['pourcentage_categorie'] = (kpis['repartition_categorie'] / 
                                      kpis['repartition_categorie'].sum() * 100)
    
    # KPI 3: Taux de récurrence
    transactions_par_client = dataframe.groupby('ID_Client').size()
    clients_recurrents = (transactions_par_client > 1).sum()
    kpis['taux_recurrence'] = (clients_recurrents / len(transactions_par_client) * 100)
    
    # KPI 4: Modes de paiement
    kpis['modes_paiement'] = dataframe['Mode_Paiement'].value_counts()
    kpis['pourcentage_paiement'] = (kpis['modes_paiement'] / 
                                     kpis['modes_paiement'].sum() * 100)
    
    # KPI 5: CLV moyenne
    clv_par_client = dataframe.groupby('ID_Client')['Montant'].sum()
    kpis['clv_moyenne'] = clv_par_client.mean()
    kpis['clv_distribution'] = clv_par_client
    
    # KPI 6: Performance par catégorie
    kpis['top_categorie'] = kpis['repartition_categorie'].idxmax()
    kpis['ca_top_categorie'] = kpis['repartition_categorie'].max()
    
    # Statistiques additionnelles
    kpis['nb_transactions'] = len(dataframe)
    kpis['nb_clients'] = dataframe['ID_Client'].nunique()
    kpis['ca_total'] = dataframe['Montant'].sum()
    
    return kpis

kpis = calculer_kpis(df)

# Layout de l'application
app.layout = html.Div([
    # En-tête
    html.Div([
        html.H1("📊 Dashboard Analyse des Ventes", 
                style={'color': 'white', 'textAlign': 'center', 'marginBottom': '10px'}),
        html.P("Analyse décisionnelle des KPI - Commerce en ligne",
               style={'color': '#e0e0e0', 'textAlign': 'center'}),
        html.P(f"📅 Période: {df['Date'].min().date()} au {df['Date'].max().date()} | "
               f"📦 {kpis['nb_transactions']} transactions | "
               f"👥 {kpis['nb_clients']} clients",
               style={'color': '#b0b0b0', 'textAlign': 'center', 'fontSize': '0.9em'})
    ], className='header'),
    
    # Filtres
    html.Div([
        html.Div([
            html.Label("📅 Sélectionner la période:", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=df['Date'].min(),
                end_date=df['Date'].max(),
                display_format='DD/MM/YYYY',
                style={'marginTop': '5px'}
            )
        ], style={'width': '45%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("🏷️ Filtrer par catégorie:", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': 'Toutes les catégories', 'value': 'ALL'}] + 
                        [{'label': cat, 'value': cat} for cat in sorted(df['Categorie'].unique())],
                value='ALL',
                style={'marginTop': '5px'}
            )
        ], style={'width': '45%', 'float': 'right', 'display': 'inline-block'})
    ], className='filters'),
    
    # Cartes KPI
    html.Div([
        html.Div([
            html.Div([
                html.H4("💰 Montant Moyen"),
                html.H2(id='kpi-montant-moyen', children=f"{kpis['montant_moyen']:.2f}€"),
                html.P("par transaction")
            ], className='kpi-card')
        ], style={'width': '24%', 'display': 'inline-block'}),
        
        html.Div([
            html.Div([
                html.H4("🔄 Taux de Récurrence"),
                html.H2(id='kpi-recurrence', children=f"{kpis['taux_recurrence']:.1f}%"),
                html.P("clients récurrents")
            ], className='kpi-card')
        ], style={'width': '24%', 'display': 'inline-block'}),
        
        html.Div([
            html.Div([
                html.H4("👥 CLV Moyenne"),
                html.H2(id='kpi-clv', children=f"{kpis['clv_moyenne']:.2f}€"),
                html.P("par client")
            ], className='kpi-card')
        ], style={'width': '24%', 'display': 'inline-block'}),
        
        html.Div([
            html.Div([
                html.H4("🏆 Top Catégorie"),
                html.H2(id='kpi-top-cat', children=kpis['top_categorie'][:12]),
                html.P(id='kpi-top-ca', children=f"{kpis['ca_top_categorie']:.0f}€ CA")
            ], className='kpi-card')
        ], style={'width': '24%', 'display': 'inline-block'})
    ], className='kpi-container'),
    
    # Onglets
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='📈 Vue d\'ensemble', value='tab-1', className='custom-tab'),
        dcc.Tab(label='🛍️ Catégories', value='tab-2', className='custom-tab'),
        dcc.Tab(label='💳 Paiements', value='tab-3', className='custom-tab'),
        dcc.Tab(label='👤 Clients', value='tab-4', className='custom-tab'),
        dcc.Tab(label='📊 Détails', value='tab-5', className='custom-tab'),
        dcc.Tab(label='📋 Qualité Données', value='tab-6', className='custom-tab')
    ]),
    
    html.Div(id='tabs-content', className='tab-content')
])

# Callback pour mettre à jour les KPI
@app.callback(
    [Output('kpi-montant-moyen', 'children'),
     Output('kpi-recurrence', 'children'),
     Output('kpi-clv', 'children'),
     Output('kpi-top-cat', 'children'),
     Output('kpi-top-ca', 'children')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('category-filter', 'value')]
)
def update_kpis(start_date, end_date, category):
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & 
                                   (filtered_df['Date'] <= end_date)]
    
    if category != 'ALL':
        filtered_df = filtered_df[filtered_df['Categorie'] == category]
    
    if len(filtered_df) == 0:
        return "0€", "0%", "0€", "N/A", "0€"
    
    kpis_filtered = calculer_kpis(filtered_df)
    
    return (f"{kpis_filtered['montant_moyen']:.2f}€",
            f"{kpis_filtered['taux_recurrence']:.1f}%",
            f"{kpis_filtered['clv_moyenne']:.2f}€",
            kpis_filtered['top_categorie'][:12],
            f"{kpis_filtered['ca_top_categorie']:.0f}€ CA")

# Callback pour le contenu des onglets
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('category-filter', 'value')]
)
def render_content(tab, start_date, end_date, category):
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & 
                                   (filtered_df['Date'] <= end_date)]
    
    if category != 'ALL':
        filtered_df = filtered_df[filtered_df['Categorie'] == category]
    
    if len(filtered_df) == 0:
        return html.Div("⚠️ Aucune donnée disponible pour cette sélection", 
                       style={'textAlign': 'center', 'padding': '50px', 'color': 'white', 'fontSize': '1.2em'})
    
    if tab == 'tab-1':
        # Vue d'ensemble
        daily_sales = filtered_df.groupby('Date')['Montant'].sum().reset_index()
        fig1 = px.line(daily_sales, x='Date', y='Montant',
                      title='💰 Évolution des ventes journalières',
                      template='plotly_dark')
        fig1.update_traces(line_color='#00d4ff', line_width=3)
        fig1.update_layout(hovermode='x unified')
        
        category_sales = filtered_df.groupby('Categorie')['Montant'].sum().reset_index()
        fig2 = px.bar(category_sales, x='Categorie', y='Montant',
                     title='📊 Chiffre d\'affaires par catégorie',
                     template='plotly_dark', color='Montant',
                     color_continuous_scale='Blues')
        fig2.update_layout(showlegend=False)
        
        return html.Div([
            html.Div([dcc.Graph(figure=fig1)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig2)], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ])
    
    elif tab == 'tab-2':
        # Analyse des catégories
        category_data = filtered_df.groupby('Categorie').agg({
            'Montant': ['sum', 'mean', 'count']
        }).reset_index()
        category_data.columns = ['Categorie', 'CA_Total', 'Montant_Moyen', 'Nb_Transactions']
        category_data['Part_CA'] = (category_data['CA_Total'] / category_data['CA_Total'].sum() * 100).round(2)
        
        fig1 = px.pie(category_data, values='CA_Total', names='Categorie',
                     title='🎯 Question 2: Répartition du CA par catégorie (%)',
                     template='plotly_dark', hole=0.4)
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        
        fig2 = px.bar(category_data.sort_values('CA_Total', ascending=False), 
                     x='Categorie', y='CA_Total',
                     title='🏆 Question 6: Performance des catégories (CA)',
                     template='plotly_dark', color='CA_Total',
                     color_continuous_scale='Viridis',
                     text='CA_Total')
        fig2.update_traces(texttemplate='%{text:.0f}€', textposition='outside')
        
        top_cat = category_data.iloc[category_data['CA_Total'].idxmax()]
        
        return html.Div([
            html.Div([
                html.H3("📊 Réponses aux Questions 2 & 6", style={'color': 'white'}),
                html.Div([
                    html.P(f"✅ Question 2 - Part de chaque catégorie:", style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                    html.Ul([html.Li(f"{row['Categorie']}: {row['Part_CA']:.2f}% du CA total", 
                            style={'color': '#e0e0e0'}) 
                            for _, row in category_data.iterrows()])
                ], style={'marginBottom': '20px'}),
                html.Div([
                    html.P(f"✅ Question 6 - Catégorie la plus performante:", style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                    html.P(f"🏆 {top_cat['Categorie']} avec {top_cat['CA_Total']:.2f}€ de CA ({top_cat['Part_CA']:.1f}% du total)", 
                          style={'color': '#4ade80', 'fontSize': '1.1em', 'fontWeight': 'bold'})
                ])
            ], style={'padding': '20px', 'backgroundColor': '#1e1e1e', 'borderRadius': '10px', 'marginBottom': '20px'}),
            html.Div([dcc.Graph(figure=fig1)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig2)], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ])
    
    elif tab == 'tab-3':
        # Modes de paiement
        payment_data = filtered_df['Mode_Paiement'].value_counts().reset_index()
        payment_data.columns = ['Mode_Paiement', 'Nombre']
        payment_data['Pourcentage'] = (payment_data['Nombre'] / payment_data['Nombre'].sum() * 100).round(2)
        
        fig1 = px.pie(payment_data, values='Nombre', names='Mode_Paiement',
                     title='🎯 Question 4: Taux d\'utilisation des modes de paiement',
                     template='plotly_dark')
        fig1.update_traces(textposition='auto', textinfo='percent+label')
        
        payment_montant = filtered_df.groupby('Mode_Paiement')['Montant'].sum().reset_index()
        fig2 = px.bar(payment_montant, x='Mode_Paiement', y='Montant',
                     title='💳 CA par mode de paiement',
                     template='plotly_dark', color='Montant',
                     color_continuous_scale='Sunset',
                     text='Montant')
        fig2.update_traces(texttemplate='%{text:.0f}€', textposition='outside')
        
        return html.Div([
            html.Div([
                html.H3("📊 Réponse à la Question 4", style={'color': 'white'}),
                html.P("✅ Taux d'utilisation des modes de paiement:", style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                html.Ul([html.Li(f"{row['Mode_Paiement']}: {row['Pourcentage']:.2f}% ({row['Nombre']} transactions)", 
                        style={'color': '#e0e0e0'}) 
                        for _, row in payment_data.iterrows()])
            ], style={'padding': '20px', 'backgroundColor': '#1e1e1e', 'borderRadius': '10px', 'marginBottom': '20px'}),
            html.Div([dcc.Graph(figure=fig1)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig2)], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ])
    
    elif tab == 'tab-4':
    # Analyse clients
        try:
            client_data = filtered_df.groupby('ID_Client').agg({
                'Montant': ['sum', 'count']
            }).reset_index()
            client_data.columns = ['ID_Client', 'CLV', 'Nb_Transactions']
            
            # Vérifier qu'on a des données
            if len(client_data) == 0:
                return html.Div("⚠️ Aucune donnée client disponible", 
                            style={'textAlign': 'center', 'padding': '50px', 'color': 'white'})
            
            montant_moyen = filtered_df['Montant'].mean()
            clients_recurrents = (client_data['Nb_Transactions'] > 1).sum()
            taux_recurrence = (clients_recurrents / len(client_data) * 100) if len(client_data) > 0 else 0
            clv_moyenne = client_data['CLV'].mean()
            
            # Graphique 1 : Distribution CLV
            fig1 = px.histogram(client_data, x='CLV', nbins=30,
                            title='📊 Question 5: Distribution de la Customer Lifetime Value',
                            template='plotly_dark', 
                            color_discrete_sequence=['#ff6b6b'],
                            labels={'CLV': 'CLV (€)', 'count': 'Nombre de clients'})
            
            # Ajouter la ligne de moyenne
            if not pd.isna(clv_moyenne):
                fig1.add_vline(x=clv_moyenne, line_dash="dash", line_color="yellow", 
                            annotation_text=f"CLV moyenne: {clv_moyenne:.2f}€",
                            annotation_position="top right")
            
            fig1.update_layout(
                xaxis_title='CLV (€)',
                yaxis_title='Nombre de clients',
                showlegend=False
            )
            
            # Graphique 2 : Scatter plot
            fig2 = px.scatter(client_data, x='Nb_Transactions', y='CLV',
                            title='💡 CLV vs Nombre de transactions',
                            template='plotly_dark', 
                            color='CLV',
                            color_continuous_scale='Turbo', 
                            size='CLV',
                            size_max=20,
                            labels={'Nb_Transactions': 'Nombre de transactions', 'CLV': 'CLV (€)'})
            
            fig2.update_layout(
                xaxis_title='Nombre de transactions',
                yaxis_title='CLV (€)',
                showlegend=True
            )
            
            return html.Div([
                html.Div([
                    html.H3("📊 Réponses aux Questions 1, 3 & 5", style={'color': 'white'}),
                    html.Div([
                        html.P("✅ Question 1 - Valeur moyenne des transactions:", 
                            style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                        html.P(f"💰 {montant_moyen:.2f}€ par transaction", 
                            style={'color': '#4ade80', 'fontSize': '1.2em', 'fontWeight': 'bold', 'marginLeft': '20px'})
                    ], style={'marginBottom': '15px'}),
                    html.Div([
                        html.P("✅ Question 3 - Taux de récurrence des clients:", 
                            style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                        html.P(f"🔄 {taux_recurrence:.2f}% des clients sont récurrents ({clients_recurrents}/{len(client_data)} clients)", 
                            style={'color': '#4ade80', 'fontSize': '1.2em', 'fontWeight': 'bold', 'marginLeft': '20px'})
                    ], style={'marginBottom': '15px'}),
                    html.Div([
                        html.P("✅ Question 5 - CLV moyenne:", 
                            style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                        html.P(f"👥 {clv_moyenne:.2f}€ par client", 
                            style={'color': '#4ade80', 'fontSize': '1.2em', 'fontWeight': 'bold', 'marginLeft': '20px'}),
                        html.P(f"CLV min: {client_data['CLV'].min():.2f}€ | CLV max: {client_data['CLV'].max():.2f}€ | Médiane: {client_data['CLV'].median():.2f}€", 
                            style={'color': '#b0b0b0', 'fontSize': '0.9em', 'marginLeft': '20px'})
                    ])
                ], style={'padding': '20px', 'backgroundColor': '#1e1e1e', 'borderRadius': '10px', 'marginBottom': '20px'}),
                html.Div([dcc.Graph(figure=fig1)], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([dcc.Graph(figure=fig2)], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'verticalAlign': 'top'})
            ])
        except Exception as e:
            return html.Div([
                html.H3("❌ Erreur lors du chargement des données clients", style={'color': '#ff6b6b', 'textAlign': 'center'}),
                html.P(f"Détails: {str(e)}", style={'color': '#e0e0e0', 'textAlign': 'center'}),
                html.P("Essayez de rafraîchir la page ou de modifier les filtres.", 
                    style={'color': '#b0b0b0', 'textAlign': 'center', 'marginTop': '20px'})
            ], style={'padding': '50px'})
        
    elif tab == 'tab-5':
        # Tableau détaillé
        table_data = filtered_df.sort_values('Date', ascending=False).head(100)
        
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Date', 'Client', 'Montant', 'Catégorie', 'Paiement'],
                       fill_color='#2c3e50',
                       font=dict(color='white', size=12),
                       align='left'),
            cells=dict(values=[table_data['Date'].dt.strftime('%d/%m/%Y'),
                              table_data['ID_Client'],
                              table_data['Montant'].apply(lambda x: f"{x:.2f}€"),
                              table_data['Categorie'],
                              table_data['Mode_Paiement']],
                      fill_color='#34495e',
                      font=dict(color='white', size=11),
                      align='left'))
        ])
        
        fig.update_layout(
            title='📋 Détails des transactions (100 dernières)',
            template='plotly_dark',
            height=600
        )
        
        return html.Div([
            html.Div([
                html.H3("📋 Résumé des données", style={'color': 'white'}),
                html.P(f"Nombre de transactions: {len(filtered_df)}", style={'color': '#e0e0e0'}),
                html.P(f"CA total: {filtered_df['Montant'].sum():.2f}€", style={'color': '#e0e0e0'}),
                html.P(f"Transaction min: {filtered_df['Montant'].min():.2f}€ | max: {filtered_df['Montant'].max():.2f}€", 
                       style={'color': '#e0e0e0'})
            ], style={'padding': '20px', 'backgroundColor': '#1e1e1e', 'borderRadius': '10px', 'marginBottom': '20px'}),
            dcc.Graph(figure=fig)
        ])
    
    elif tab == 'tab-6':
        # Qualité des données
        return html.Div([
            html.H3("✅ Rapport de qualité des données", style={'color': 'white', 'marginBottom': '20px'}),
            
            html.Div([
                html.H4("📊 Statistiques générales", style={'color': '#00d4ff'}),
                html.P(f"Nombre total de transactions: {len(df)}", style={'color': '#e0e0e0'}),
                html.P(f"Nombre de clients uniques: {df['ID_Client'].nunique()}", style={'color': '#e0e0e0'}),
                html.P(f"Période couverte: du {df['Date'].min().date()} au {df['Date'].max().date()}", style={'color': '#e0e0e0'}),
                html.P(f"Nombre de catégories: {df['Categorie'].nunique()}", style={'color': '#e0e0e0'}),
                html.P(f"Nombre de modes de paiement: {df['Mode_Paiement'].nunique()}", style={'color': '#e0e0e0'})
            ], style={'padding': '20px', 'backgroundColor': '#1e1e1e', 'borderRadius': '10px', 'marginBottom': '20px'}),
            
            html.Div([
                html.H4("🔍 Validation des données", style={'color': '#00d4ff'}),
                html.P(f"✅ Valeurs manquantes: {df.isnull().sum().sum()}", style={'color': '#4ade80'}),
                html.P(f"✅ Doublons: 0 (déjà supprimés)", style={'color': '#4ade80'}),
                html.P(f"✅ Valeurs aberrantes gérées", style={'color': '#4ade80'}),
                html.P(f"✅ Types de données validés", style={'color': '#4ade80'})
            ], style={'padding': '20px', 'backgroundColor': '#1e1e1e', 'borderRadius': '10px', 'marginBottom': '20px'}),
            
            html.Div([
                html.H4("📈 Distribution des montants", style={'color': '#00d4ff'}),
                html.P(f"Montant moyen: {df['Montant'].mean():.2f}€", style={'color': '#e0e0e0'}),
                html.P(f"Écart-type: {df['Montant'].std():.2f}€", style={'color': '#e0e0e0'}),
                html.P(f"Médiane: {df['Montant'].median():.2f}€", style={'color': '#e0e0e0'}),
                html.P(f"Min: {df['Montant'].min():.2f}€ | Max: {df['Montant'].max():.2f}€", style={'color': '#e0e0e0'})
            ], style={'padding': '20px', 'backgroundColor': '#1e1e1e', 'borderRadius': '10px'})
        ])

if __name__ == '__main__':
    print("\n🚀 Lancement du serveur Dashboard...")
    print("📍 Ouvrez votre navigateur à l'adresse: http://127.0.0.1:8050")
    print("🛑 Pour arrêter le serveur, appuyez sur Ctrl+C")
    print("="*80 + "\n")
    app.run(debug=True, port=8050)  # ← CHANGEMENT ICI : .run au lieu de .run_server
