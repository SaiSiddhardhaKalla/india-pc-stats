from ast import Pass
from logging import PlaceHolder
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table
from requests import options

pc_df = pd.read_excel('PC wise.xlsx',sheet_name='Master')
bar_df = pd.read_excel('PC wise.xlsx',sheet_name='seats_won')
pie_df = pd.read_excel('PC wise.xlsx',sheet_name='VoteShare')
geo_df = gpd.read_file('india_pc_2019.geojson')

state_lis = list(pc_df['State_Name'].unique())
state_lis = sorted(state_lis)
state_lis.insert(0, "All")
pc_lis = list(pc_df['PC'].unique())
pc_lis = sorted(pc_lis)
dfx = pc_df.copy()
party_cmap = {'AAP':'#0066A4', 'AGP':'#99CCFF',
                'AIFB':'#D70000', 'AIMIM':'#136B4B',
                'AINRC':'#FFC000', 'AITC':'#20C646',
                'BJD':'#006400', 'BJP':'#FF9933',
                'BSP':'#22409A', 'CPI':'#FF0000',
                'CPI(M)':'#FF1D15', 'DMDK':'#FFEA19',
                'DMK':'#DD1100', 'HSPDP':'#0000FF',
                'INC':'#19AAED', 'INLD':'#336600',
                'IPFT':'#008000', 'IUML':'#228B22',
                'JCC':'#FFC0DB', 'JD(S)':'#138808',
                'JKNPP':'#000180', 'JKPDP':'#058532',
                'JMM':'#215B30', 'LJP':'#0093DD',
                'MNF':'#2E5694', 'MNS':'#5F2301',
                'NCP':'#00B2B2', 'NDPP':'#ED1B24',
                'NPF':'#990066', 'NPP':'#DB7093',
                'PDA':'#FF0000', 'PMK':'#FFFF00',
                'PPA':'#008000', 'RJD':'#008000',
                'RLD':'#006400', 'RLTP':'#DBE934',
                'RSP':'#FF4A4A', 'SAD':'#0F204A',
                'SDF':'#FFFC06', 'SKM':'#ED1E26',
                'SP':'#FF2222', 'SHS':'#F26F21',
                'TDP':'#FCEE23', 'TRS':'#FF0274',
                'UDP':'#CEF2E0', 'UPPL':'#F3ED13',
                'Others':'#696969',
                'YSRCP':'#1569C7','ST':'#228B22','SC':'#00008B','GEN':'#f4c2c2'}

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Parlimentary Election Summary", style={'text-align':'center','fontweight':'bold'})
    ],className='Header'),
    html.Div(style={'background-image': 'url("/assets/rose-bl.svg")'},className='bground'),
    html.Div([
        html.Label("Select State", style={'colour': '#000000',
                                             'fontsize' : '16px','fontWeight':'bold'}),
        dcc.Dropdown(id="state",
                options=[{"label" : i, "value" : i} for i in state_lis],
                placeholder="Select State",
                multi=False,
                searchable=True,
                value= 'All',
                clearable=False,
                style={'width': '100%', 'verticalAlign': 'middle',
                       'color':'black'}
                )],className='Dropdown1'),
        html.Div([
        html.Label("Select Parlimentary Constituency", 
                   style={'color':'#000000','text-align':'centre',
                          'fontSize':'16px','fontWeight':'bold'}),
        dcc.Dropdown(id="PC",
                     options=[],
                     placeholder="None",
                     multi = False,
                     searchable=True,
                     value='None',
                     clearable=True,
                     style={'width': '100%', 'verticalAlign': 'middle',
                            'color':'black'})
        ],className="Dropdown2"),
        html.Div([
        html.Label("Select Map", 
                   style={'color':'#000000','text-align':'centre',
                          'fontSize':'16px','fontWeight':'bold'}),
        dcc.Dropdown(id="map_type",
                              options=[{"label":"Winner Party", "value":"Party"},
                                             {"label":"Constituency Type", "value":"Constituency_Type"},
                                             {"label":"Education", "value":"MyNeta education"},
                                             {"label":"Runner Party", "value":"Party_x"}
                                             ],
                     value="Party",
                     multi = False,
                     searchable=True,
                     clearable=False,
                     style={'width': '100%', 'verticalAlign': 'middle',
                            'color':'black'})
        ],className="Dropdown3"),
        html.Div([
        html.Label("Select Year", 
                   style={'color':'#000000','text-align':'centre',
                          'fontSize':'16px','fontWeight':'bold'}),
        dcc.Dropdown(id="year",
                              options=[{"label":2019, "value":2019},
                                             {"label":2014, "value":2014},
                                             {"label":2009, "value":2009},
                                             ],
                     placeholder="Select Map",
                     multi = False,
                    #  searchable=True,
                     value=2019,
                     clearable=False,
                     style={'width': '100%', 'verticalAlign': 'middle',
                            'color':'black'})
        ],className="Dropdown4"),
        html.Div([
        dcc.Graph(id='map', figure={},style={
                                             "height": "85vh",
                                            })],className='map'),
        html.Div([
            dcc.Graph(id='bar')
            ],className='bar'),
        html.Div([
            dcc.Graph(id='pie')
            ],className='pie'),
        html.Div([
            html.Label('Parlimentary Election Stats', style={'fontSize' : '16px','fontWeight':'bold'}),
            dash_table.DataTable(id="pc_sta", style_cell={'text-align':'left',
                                                'height':'auto',
                                                'fontSize': 13,
                                                'maxWidth': '35%',
                                                'font-family': 'Ariel'
                                                },
                                    style_header={'fontWeight':'bold',
                                                            'color': '#000000',
                                                            'backgroundColor':'#63bbe3'},
                                    style_data={'fontWeight':'bold',
                                                        'whiteSpace': 'normal',
                                                        'height': 'auto',
                                                        'backgroundColor': 'transparent' 
                                                        },
                                    style_cell_conditional=[
                                        {'if': {'column_id':'Year'}, 'width' : '25%'},
                                        {'if': {'column_id':'Turnout'}, 'width' : '25%'},
                                        {'if': {'column_id':'Electors'}, 'width' : '25%'},
                                        {'if':{'column_id':'Valid Votes'},'width':'25%'}
                                        ], 
                                    style_as_list_view=True)],className='pc_ta'),
        html.Div(children=[
            html.Label('Parlimentary Election', style={'fontSize' : '16px','fontWeight':'bold'}),
            dash_table.DataTable(id="pc_stats", style_cell={'text-align':'left',
                                                'height':'auto',
                                                'fontSize': 13,
                                                'maxWidth': '35%',
                                                'font-family': 'Ariel'
                                                },
                                    style_header={'fontWeight':'bold',
                                                            'color': '#000000',
                                                            'backgroundColor':'#63bbe3'},
                                    style_data={'fontWeight':'bold',
                                                        'whiteSpace': 'normal',
                                                        'height': 'auto',
                                                        'backgroundColor': 'transparent' 
                                                        },
                                    style_cell_conditional=[
                                        {'if': {'column_id':'Candidate'}, 'width' : '20%'},
                                        {'if': {'column_id':'Position'}, 'width' : '13%'},
                                        {'if': {'column_id':'Party'}, 'width' : '13%'},
                                        {'if': {'column_id':'Votes'}, 'width' : '13%'},
                                        {'if': {'column_id':'Vote Share'}, 'width' : '15%'},
                                        {'if': {'column_id':'Margin'}, 'width' : '13%'},
                                        {'if':{'column_id':'Contested'},'width':'13%'}
                                        ], 
                                    style_as_list_view=True)],className='pc_tab'),
],className='pc')

@app.callback(
    [Output('PC','options'),
     Output('PC','value')],
    [Input('state','value')]
)
def update_pc(state):
    df=pc_df[pc_df['State_Name']==state]
    k =  df['PC'].unique()
    return[{'label':i,'value':i}for i in df['PC'].sort_values().unique()],k[-1]

@app.callback(
    Output('map','figure'),
    [
    Input('year','value'),
     Input('map_type','value'),
     Input('state','value'),
    Input('PC','value')
     ]
)
def update_map(yer,type, stat,pc):
    df1=dfx[dfx['Year']==yer]  
    if type=='Party_x':
        df8=df1[df1['Position']==2]
        df8=df8[df8['month']==4]
        if stat == 'All':
                fig4 = px.choropleth_mapbox(
                    data_frame=df8,
                    geojson=geo_df,
                    featureidkey='properties.pc',
                    locations='PC',
                    color='Party',
                    color_discrete_map=party_cmap,
                    center = {'lon':82.8496, 'lat':22.6944},
                    mapbox_style='carto-positron',
                    zoom=3.95,
                    # title='Party',
                    # hover_name='PC',
                    # title='State values',
                    hover_name='State_Name',
                    custom_data=[df8['Candidate'],df8['Party'],df8['Valid Votes'],df8['State_Name'],df8['PC_Name']]
                    )
                hovertemp='<i>State Name :</i> %{customdata[3]}<br>'
                hovertemp+='<i>Constituency Name :</i> %{customdata[4]}<br>'
                hovertemp+='<i>Candidate :</i> %{customdata[0]}<br>'
                hovertemp+='<i>Party :</i> %{customdata[1]}<br>'
                hovertemp+='<i>Valid Votes :</i> %{customdata[2]}<br>'
                fig4.update_traces(hovertemplate=hovertemp)
                fig4.update_layout(
                            margin=dict(l=10, r=10, t=50, b=10),
                            paper_bgcolor='rgba(0,0,0,0)',
                            title={
                                    'text': "India",
                                    'y':0.975,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},
                            title_font_family='Arial',
                            font_family='Arial',
                            dragmode='pan'
                        )
                return fig4
        else:
            sta = df8[df8['State_Name']==stat]
            cent = geo_df[geo_df['st_name']==stat]
            cen = cent.centroid
            lon = cen.apply(lambda p: p.x)
            lat = cen.apply(lambda p: p.y)           
            if pc == 'None':
                fig5 = px.choropleth_mapbox(
                        data_frame = sta,
                        geojson = cent,
                        featureidkey='properties.pc', # from geojson
                        locations = 'PC', # from df
                        center = {'lon':lon.iloc[0], 'lat':lat.iloc[0]},
                        mapbox_style='carto-positron',
                        zoom=5.25,
                        color='Party',
                        color_discrete_map=party_cmap,
                        # range_color=[650,1300],
                        # color_continuous_scale=px.colors.sequential.deep,
                        # title='State values',
                        hover_name='State_Name',
                        custom_data=[sta['Candidate'],sta['Party'],sta['Votes'],sta['PC_Name']]
                    )
                hovertemp='<i>Constituency Name :</i> %{customdata[3]}<br>'
                hovertemp+='<i>Candidate :</i> %{customdata[0]}<br>'
                hovertemp+='<i>Party :</i> %{customdata[1]}<br>'
                hovertemp+='<i>Votes :</i> %{customdata[2]}<br>'
                fig5.update_traces(hovertemplate=hovertemp)
                fig5.update_layout(
                            margin=dict(l=10, r=10, t=50, b=10),
                            paper_bgcolor='rgba(0,0,0,0)',
                            title={
                                    'text': "State Value",
                                    'y':0.975,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},
                            title_font_family='Arial',
                            font_family='Arial',
                            dragmode='pan'
                        )
                return fig5
            else:
                sta_df = sta[sta['PC']==pc]
                cent = geo_df[geo_df['pc']==pc]
                cen = cent.centroid
                lon = cen.apply(lambda p: p.x)
                lat = cen.apply(lambda p: p.y)
                fig6 = px.choropleth_mapbox(
                        data_frame = sta_df,
                        geojson = cent,
                        featureidkey='properties.pc', # from geojson
                        locations = 'PC', # from df
                        center = {'lon':lon.iloc[0], 'lat':lat.iloc[0]},
                        mapbox_style='carto-positron',
                        zoom=6.25,
                        color='Party',
                        color_discrete_map=party_cmap,
                        # range_color=[650,1300],
                        # color_continuous_scale=px.colors.sequential.deep,
                        # title='State values',
                        hover_name='State_Name',
                        custom_data=[sta_df['Candidate'],sta_df['Party'],sta_df['Votes'],sta_df['PC_Name']]
                    )
                hovertemp='<i>Constituency Name :</i> %{customdata[3]}<br>'
                hovertemp+='<i>Candidate :</i> %{customdata[0]}<br>'
                hovertemp+='<i>Party :</i> %{customdata[1]}<br>'
                hovertemp+='<i>Votes :</i> %{customdata[2]}<br>'
                fig6.update_traces(hovertemplate=hovertemp)
                fig6.update_layout(
                            margin=dict(l=10, r=10, t=50, b=10),
                            paper_bgcolor='rgba(0,0,0,0)',
                            title={
                                    'text': "Parlimentary Constituency",
                                    'y':0.975,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},
                            title_font_family='Arial',
                            font_family='Arial',
                            dragmode='pan'
                        )
                return fig6
    else:
        df9=df1[df1['Position']==1]
        df9=df9[df9['month']==4]
        if stat == 'All':
                fig1 = px.choropleth_mapbox(
                    data_frame=df9,
                    geojson=geo_df,
                    featureidkey='properties.pc',
                    locations='PC',
                    color=type,
                    color_discrete_map=party_cmap,
                    center = {'lon':82.8496, 'lat':22.6944},
                    mapbox_style='carto-positron',
                    zoom=3.95,
                    # title='Party',
                    # hover_name='PC',
                    # title='State values',
                    hover_name='State_Name',
                    custom_data=[df9['Candidate'],df9['Party'],df9['Votes'],df9['State_Name'],df9['PC_Name']]
                    )
                hovertemp='<i>State Name :</i> %{customdata[3]}<br>'
                hovertemp+='<i>Constituency Name :</i> %{customdata[4]}<br>'
                hovertemp+='<i>Candidate :</i> %{customdata[0]}<br>'
                hovertemp+='<i>Party :</i> %{customdata[1]}<br>'
                hovertemp+='<i>Votes :</i> %{customdata[2]}<br>'
                fig1.update_traces(hovertemplate=hovertemp)
                fig1.update_layout(
                            margin=dict(l=10, r=10, t=50, b=10),
                            paper_bgcolor='rgba(0,0,0,0)',
                            title={
                                    'text': "India",
                                    'y':0.975,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},
                            title_font_family='Arial',
                            font_family='Arial',
                            dragmode='pan'
                        )
                return fig1
        else:   
            sta = df9[df9['State_Name']==stat]
            cent = geo_df[geo_df['st_name']==stat]
            cen = cent.centroid
            lon = cen.apply(lambda p: p.x)
            lat = cen.apply(lambda p: p.y)  
            if pc == 'None':  
                # sta = df9[df9['State_Name']==stat]
                # cent = geo_df[geo_df['st_name']==stat]
                # cen = cent.centroid
                # lon = cen.apply(lambda p: p.x)
                # lat = cen.apply(lambda p: p.y)            
                fig2 = px.choropleth_mapbox(
                        data_frame = sta,
                        geojson = cent,
                        featureidkey='properties.pc', # from geojson
                        locations = 'PC', # from df
                        center = {'lon':lon.iloc[0], 'lat':lat.iloc[0]},
                        mapbox_style='carto-positron',
                        zoom=5.25,
                        color=type,
                        color_discrete_map=party_cmap,
                        # range_color=[650,1300],
                        # color_continuous_scale=px.colors.sequential.deep,
                        # title='State values',
                        hover_name='State_Name',
                        custom_data=[sta['Candidate'],sta['Party'],sta['Votes'],sta['PC_Name']]
                    )
                hovertemp='<i>Constituency Name :</i> %{customdata[3]}<br>'
                hovertemp+='<i>Candidate :</i> %{customdata[0]}<br>'
                hovertemp+='<i>Party :</i> %{customdata[1]}<br>'
                hovertemp+='<i>Votes :</i> %{customdata[2]}<br>'
                fig2.update_traces(hovertemplate=hovertemp)
                fig2.update_layout(
                            margin=dict(l=10, r=10, t=50, b=10),
                            paper_bgcolor='rgba(0,0,0,0)',
                            title={
                                    'text': "State Values",
                                    'y':0.975,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},
                            title_font_family='Arial',
                            font_family='Arial',
                            dragmode='pan'
                        )
                return fig2
            else:
                # sta = df9[df9['State_Name']==stat]
                sta_df = sta[sta['PC']==pc]
                cent = geo_df[geo_df['pc']==pc]
                cen = cent.centroid
                lon = cen.apply(lambda p: p.x)
                lat = cen.apply(lambda p: p.y)
                fig3 = px.choropleth_mapbox(
                        data_frame = sta_df,
                        geojson = cent,
                        featureidkey='properties.pc', # from geojson
                        locations = 'PC', # from df
                        center = {'lon':lon.iloc[0], 'lat':lat.iloc[0]},
                        mapbox_style='carto-positron',
                        zoom=6.25,
                        color=type,
                        color_discrete_map=party_cmap,
                        # range_color=[650,1300],
                        # color_continuous_scale=px.colors.sequential.deep,
                        # title='State values',
                        hover_name='State_Name',
                        custom_data=[sta_df['Candidate'],sta_df['Party'],sta_df['Votes'],sta_df['PC_Name']]
                    )
                hovertemp='<i>Constituency Name :</i> %{customdata[3]}<br>'
                hovertemp+='<i>Candidate :</i> %{customdata[0]}<br>'
                hovertemp+='<i>Party :</i> %{customdata[1]}<br>'
                hovertemp+='<i>Votes :</i> %{customdata[2]}<br>'
                fig3.update_traces(hovertemplate=hovertemp)
                fig3.update_layout(
                            margin=dict(l=10, r=10, t=50, b=10),
                            paper_bgcolor='rgba(0,0,0,0)',
                            title={
                                    'text': "Parlimentary Constituency",
                                    'y':0.975,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},
                            title_font_family='Arial',
                            font_family='Arial',
                            dragmode='pan'
                        )
                return fig3            

@app.callback(
    Output('bar','figure'),
    [Input('year','value'),
    Input('state', 'value')
    ]
)
def update_bar(yers,states):
    dfy = pc_df.copy()
    df2=dfy[dfy['Year']==yers]
    df2=df2[df2['Position']==1]
    df2=df2[df2['month']==4]
    df3=df2[['Party','Constituency_No','State_Name']]
    df3.rename(columns = {'Constituency_No':'Seats Won'}, inplace = True)
    df4=df3.groupby(['Party']).count()
    df4=df4.reset_index()
    df4.rename(columns = {'Constituency_No':'Seats Won'}, inplace = True)
    df5=bar_df[bar_df['Year']==yers]
    if states == 'All':
        barchart1=px.bar(
            data_frame=df5,
            x='Party',
            y='Seats Won',
            color='Party',
            color_discrete_map=party_cmap,
            # text='Constituency_No',            
            opacity=0.8,
            orientation='v',
            barmode='relative',
            # width=400
            )
        barchart1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return (barchart1)
    else:
        df6=df3[df3['State_Name']==states]
        df7=df6.groupby(['Party']).count()
        df7=df7.reset_index()
        df7=df7.sort_values(by='Seats Won',ascending=False)
        barchart2=px.bar(
            data_frame=df7,
            x='Party',
            y='Seats Won',
            color='Party',
            color_discrete_map=party_cmap,
            # text='Constituency_No',            
            opacity=0.8,
            orientation='v',
            barmode='relative',
            # width=400
            )
        barchart2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return (barchart2)

@app.callback(
    Output('pie','figure'),
    [Input('year','value'),
    Input('state', 'value'),
    Input('PC','value')
    ]
)
def update_pie(yers,states,pcc):
    dfz = pie_df.copy()
    df2=dfz[dfz['Year']==yers]
    if states == 'All':
        pie1=px.pie(
            data_frame=df2,
            values='Votes', 
            names='Party',
            color='Party',
            color_discrete_map=party_cmap,       
            opacity=0.8,
            )
        pie1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
        )
        return (pie1)
    else:
            df6=dfx[dfx['State_Name']==states]
            df6=df6[df6['Year']==yers]   
            if pcc == 'None':    
                df7=df6.groupby(['State_Name','Party','Votes']).sum().reset_index()
                df7 = df7[['State_Name','Party','Votes']]
                df7 = df7.groupby('Party').sum().reset_index()
                df7 = df7.sort_values(by='Votes',ascending=False)
                df7 = df7.head(4)
                pie2=px.pie(
                    data_frame=df7,
                    values='Votes', 
                    names='Party',
                    color='Party',
                    color_discrete_map=party_cmap,       
                    opacity=0.8,
                    )
                pie2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                    )
                return (pie2)
            else:
                df8=df6[df6['PC']==pcc]
                df8 = df8.sort_values(by='Votes',ascending=False)
                df8 = df8.head(4)
                pie3=px.pie(
                    data_frame=df8,
                    values='Votes', 
                    names='Party',
                    color='Party',
                    color_discrete_map=party_cmap,       
                    opacity=0.8,
                    )
                pie3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                    )
                return (pie3)

@app.callback(
    [
    Output('pc_sta','data'),
    Output('pc_sta', 'columns'),  
    ],
    [Input('PC','value')]
)
def update_table(cons):
    #dtable for PC stats
    df_pc_stas = pc_df.copy()
    df_pc_stas = df_pc_stas[df_pc_stas['PC']==cons]
    df_pc_stas = df_pc_stas.drop_duplicates(subset=['Year'])
    df_pc_stas = df_pc_stas[["Year","Turnout Percentage","Electors","Valid Votes"]]
    df_pc_stas = df_pc_stas.sort_values(by='Year',ascending=False)
    columns_pc_sta = [{'name':col,'id':col} for col in df_pc_stas.columns]
    data_pc_sta = df_pc_stas.to_dict(orient='records')

    return data_pc_sta,columns_pc_sta

@app.callback(
    [Output('pc_stats','data'),
    Output('pc_stats','columns')],
    [Input('PC','value'),
    Input('year','value')]
)
def update_table(cons,years):
    #dtable for pc cans
    df_pc_sts = pc_df.copy()
    df_pc_sts=df_pc_sts[df_pc_sts['PC']==cons]
    df_pc_sts=df_pc_sts[df_pc_sts['Year']==years]
    pos=[1,2,3]
    df_pc_sts=df_pc_sts[df_pc_sts['Position'].isin(pos)]
    df_pc_sts= df_pc_sts.sort_values(by='Position',ascending=True)
    df_pc_sts.rename(columns = {'Vote Share Percentage':'Vote Share'}, inplace = True)
    df_pc_sts= df_pc_sts[["Candidate",'Position','Party',"Votes",'Vote Share', 'Margin','Contested']]
    columns_pc_sts = [{'name':coll,'id':coll} for coll in df_pc_sts.columns]
    data_pc_sts = df_pc_sts.to_dict(orient='records')

    return data_pc_sts,columns_pc_sts

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)