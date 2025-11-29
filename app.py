import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 1. ساخت داده‌های نمونه
df = pd.DataFrame({
    "محصول": ["گوشی موبایل", "لپ‌تاپ", "هدفون", "ساعت هوشمند", "تبلت", 
               "گوشی موبایل", "لپ‌تاپ", "هدفون", "ساعت هوشمند", "تبلت"],
    "تعداد فروش": [120, 85, 200, 150, 90, 130, 95, 210, 160, 100],
    "شهر": ["تهران", "تهران", "تهران", "تهران", "تهران", 
            "اصفهان", "اصفهان", "اصفهان", "اصفهان", "اصفهان"],
    "درامد (میلیون)": [2400, 4250, 600, 750, 1800, 2600, 4750, 630, 800, 2000]
})

# 2. راه‌اندازی اپلیکیشن
app = dash.Dash(__name__, title="داشبورد فروش")

# *** خط بسیار مهم برای Render ***
server = app.server 

# 3. طراحی ظاهر (Layout)
app.layout = html.Div(style={'font-family': 'Tahoma, Arial', 'direction': 'rtl', 'padding': '20px'}, children=[
    
    html.H1("📊 داشبورد تحلیل فروش آنلاین", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div("این داشبورد جهت نمایش به کارفرما طراحی شده است.", 
             style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '30px'}),

    # انتخاب‌گر شهر
    html.Div([
        html.Label("انتخاب شهر:"),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in df['شهر'].unique()],
            value='تهران',
            clearable=False
        )
    ], style={'width': '30%', 'marginBottom': '20px'}),

    # نمودارها
    html.Div([
        dcc.Graph(id='sales-bar-graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='revenue-pie-chart', style={'display': 'inline-block', 'width': '48%'})
    ])
])

# 4. بخش تعاملی (Callback)
@app.callback(
    [Output('sales-bar-graph', 'figure'),
     Output('revenue-pie-chart', 'figure')],
    [Input('city-dropdown', 'value')]
)
def update_charts(selected_city):
    filtered_df = df[df['شهر'] == selected_city]
    
    # نمودار میله‌ای
    fig1 = px.bar(filtered_df, x='محصول', y='تعداد فروش', 
                  title=f"تعداد فروش در {selected_city}", text='تعداد فروش')
    fig1.update_traces(marker_color='#3498db')
    
    # نمودار دایره‌ای
    fig2 = px.pie(filtered_df, values='درامد (میلیون)', names='محصول', 
                  title=f"سهم درآمد در {selected_city}")
    
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
