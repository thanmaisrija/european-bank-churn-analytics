import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="European Bank Churn Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1F3864; }
    .metric-label { font-size: 0.85rem; color: #666; margin-top: 4px; }
    .metric-red .metric-value { color: #C55A11; }
    .section-header {
        background: linear-gradient(135deg, #1F3864, #2E75B6);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        margin: 16px 0 10px 0;
    }
    .sidebar .sidebar-content { background: #1F3864; }
    h1 { color: #1F3864; }
    h2 { color: #2E75B6; }
</style>
""", unsafe_allow_html=True)

# ── Load & Prepare Data ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("European_Bank.xlsx")
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0,30,45,60,200],
                            labels=['<30','30-45','46-60','60+'])
    df['CreditBand'] = pd.cut(df['CreditScore'], bins=[0,579,719,850],
                              labels=['Low','Medium','High'])
    df['TenureGroup'] = pd.cut(df['Tenure'], bins=[-1,2,6,10],
                               labels=['New','Mid-term','Long-term'])
    df['BalanceSegment'] = pd.cut(df['Balance'], bins=[-1,0,50000,250900],
                                  labels=['Zero-balance','Low-balance','High-balance'])
    df['AgeGroup'] = df['AgeGroup'].astype(str)
    df['CreditBand'] = df['CreditBand'].astype(str)
    df['TenureGroup'] = df['TenureGroup'].astype(str)
    df['BalanceSegment'] = df['BalanceSegment'].astype(str)
    return df

df = load_data()
overall_churn = df['Exited'].mean()
hv_threshold = df[df['Balance']>0]['Balance'].quantile(0.75)
hv = df[df['Balance'] >= hv_threshold]

COLORS = {
    'primary': '#1F3864',
    'secondary': '#2E75B6',
    'accent': '#C55A11',
    'green': '#70AD47',
    'red': '#FF4B4B',
    'light': '#DEEAF1'
}
PALETTE = ['#1F3864','#2E75B6','#70AD47','#C55A11','#FFC000','#9E3B7B']

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/bank-building.png", width=60)
st.sidebar.title("🏦 Churn Analytics")
st.sidebar.markdown("**European Banking Dashboard**")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "📊 Overview",
    "🌍 Geography Analysis",
    "👥 Demographics",
    "💰 High-Value Customers",
    "🔍 Segment Explorer"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")
geo_filter = st.sidebar.multiselect("Geography", ['France','Germany','Spain'],
                                     default=['France','Germany','Spain'])
gender_filter = st.sidebar.multiselect("Gender", ['Male','Female'],
                                        default=['Male','Female'])

dff = df[df['Geography'].isin(geo_filter) & df['Gender'].isin(gender_filter)]

# ── Helper ───────────────────────────────────────────────────────────────────
def churn_by(col, data=None):
    d = data if data is not None else dff
    g = d.groupby(col)['Exited'].agg(['sum','count']).reset_index()
    g.columns = [col,'Churned','Total']
    g['Retained'] = g['Total'] - g['Churned']
    g['Churn Rate'] = g['Churned'] / g['Total']
    g['Churn Rate %'] = (g['Churn Rate']*100).round(1)
    return g

def kpi_card(label, value, suffix="", red=False):
    color = "#C55A11" if red else "#1F3864"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{color}">{value}{suffix}</div>
        <div class="metric-label">{label}</div>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Overview":
    st.title("Customer Segmentation & Churn Pattern Analytics")
    st.markdown("**European Banking | 10,000 Customers | France • Spain • Germany**")
    st.markdown("---")

    # KPI Row
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi_card("Total Customers", f"{len(dff):,}")
    with c2: kpi_card("Total Churned", f"{dff['Exited'].sum():,}", red=True)
    with c3: kpi_card("Overall Churn Rate", f"{dff['Exited'].mean()*100:.1f}", "%", red=True)
    with c4: kpi_card("Active Members", f"{dff['IsActiveMember'].sum():,}")
    with c5: kpi_card("Avg Balance", f"€{dff['Balance'].mean():,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Churn Distribution</div>', unsafe_allow_html=True)
        pie_data = pd.DataFrame({'Status':['Retained','Churned'],
                                  'Count':[dff['Exited'].eq(0).sum(), dff['Exited'].sum()]})
        fig = px.pie(pie_data, values='Count', names='Status',
                     color_discrete_sequence=['#2E75B6','#C55A11'],
                     hole=0.45)
        fig.update_traces(textposition='outside', textinfo='percent+label',
                          textfont_size=13)
        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10),
                          height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Churn Rate by Geography</div>', unsafe_allow_html=True)
        geo = churn_by('Geography')
        fig2 = px.bar(geo, x='Geography', y='Churn Rate %',
                      color='Churn Rate %',
                      color_continuous_scale=['#70AD47','#FFC000','#C55A11'],
                      text='Churn Rate %')
        fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig2.update_layout(coloraxis_showscale=False, height=300,
                           yaxis_title="Churn Rate (%)",
                           margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">Churn by Age Group</div>', unsafe_allow_html=True)
        age_order = ['<30','30-45','46-60','60+']
        age_g = churn_by('AgeGroup')
        age_g['AgeGroup'] = pd.Categorical(age_g['AgeGroup'], categories=age_order, ordered=True)
        age_g = age_g.sort_values('AgeGroup')
        fig3 = px.bar(age_g, x='AgeGroup', y='Churn Rate %',
                      color='Churn Rate %',
                      color_continuous_scale=['#70AD47','#FFC000','#C55A11'],
                      text='Churn Rate %')
        fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig3.update_layout(coloraxis_showscale=False, height=300,
                           yaxis_title="Churn Rate (%)",
                           margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Churn by Gender</div>', unsafe_allow_html=True)
        gen = churn_by('Gender')
        fig4 = px.bar(gen, x='Gender', y='Churn Rate %',
                      color='Gender',
                      color_discrete_sequence=['#2E75B6','#C55A11'],
                      text='Churn Rate %')
        fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig4.update_layout(showlegend=False, height=300,
                           yaxis_title="Churn Rate (%)",
                           margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 2: GEOGRAPHY
# ════════════════════════════════════════════════════════════════════════════
elif page == "🌍 Geography Analysis":
    st.title("🌍 Geography Analysis")
    st.markdown("Regional churn patterns across France, Spain, and Germany")
    st.markdown("---")

    geo = churn_by('Geography')
    c1,c2,c3 = st.columns(3)
    for col, (_, row) in zip([c1,c2,c3], geo.iterrows()):
        with col:
            kpi_card(f"{row['Geography']} Churn Rate",
                     f"{row['Churn Rate']*100:.1f}", "%",
                     red=row['Churn Rate'] > overall_churn)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Churned vs Retained by Geography</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Retained', x=geo['Geography'], y=geo['Retained'],
                             marker_color='#2E75B6'))
        fig.add_trace(go.Bar(name='Churned', x=geo['Geography'], y=geo['Churned'],
                             marker_color='#C55A11'))
        fig.update_layout(barmode='stack', height=320,
                          margin=dict(t=10,b=10,l=10,r=10),
                          legend=dict(orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Geography × Age Churn Heatmap</div>', unsafe_allow_html=True)
        age_order = ['<30','30-45','46-60','60+']
        pivot = dff.groupby(['Geography','AgeGroup'])['Exited'].mean().reset_index()
        pivot_wide = pivot.pivot(index='Geography', columns='AgeGroup', values='Exited')
        pivot_wide = pivot_wide.reindex(columns=[c for c in age_order if c in pivot_wide.columns])
        pivot_wide = pivot_wide.fillna(0)
        fig2 = px.imshow(pivot_wide,
                         color_continuous_scale=['#DEEAF1','#FFC000','#C55A11'],
                         aspect='auto', text_auto='.1%')
        fig2.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">Geography + Gender Churn Breakdown</div>', unsafe_allow_html=True)
    geo_gen = dff.groupby(['Geography','Gender'])['Exited'].mean().reset_index()
    geo_gen['Churn Rate %'] = (geo_gen['Exited']*100).round(1)
    fig3 = px.bar(geo_gen, x='Geography', y='Churn Rate %', color='Gender',
                  barmode='group', text='Churn Rate %',
                  color_discrete_sequence=['#2E75B6','#C55A11'])
    fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig3.update_layout(height=340, margin=dict(t=10,b=10,l=10,r=10),
                       yaxis_title="Churn Rate (%)")
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 3: DEMOGRAPHICS
# ════════════════════════════════════════════════════════════════════════════
elif page == "👥 Demographics":
    st.title("👥 Demographic Analysis")
    st.markdown("Age, gender, credit score, tenure, and engagement patterns")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Churn by Credit Score Band</div>', unsafe_allow_html=True)
        cr = churn_by('CreditBand')
        cr['CreditBand'] = pd.Categorical(cr['CreditBand'], ['Low','Medium','High'], ordered=True)
        cr = cr.sort_values('CreditBand')
        fig = px.bar(cr, x='CreditBand', y='Churn Rate %', text='Churn Rate %',
                     color='Churn Rate %',
                     color_continuous_scale=['#70AD47','#FFC000','#C55A11'])
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(coloraxis_showscale=False, height=300,
                          margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Churn by Tenure Group</div>', unsafe_allow_html=True)
        ten = churn_by('TenureGroup')
        ten['TenureGroup'] = pd.Categorical(ten['TenureGroup'],
                             ['New','Mid-term','Long-term'], ordered=True)
        ten = ten.sort_values('TenureGroup')
        fig2 = px.bar(ten, x='TenureGroup', y='Churn Rate %', text='Churn Rate %',
                      color='TenureGroup',
                      color_discrete_sequence=['#C55A11','#FFC000','#2E75B6'])
        fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig2.update_layout(showlegend=False, height=300,
                           margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">Active vs Inactive Member Churn</div>', unsafe_allow_html=True)
        dff2 = dff.copy()
        dff2['Member Status'] = dff2['IsActiveMember'].map({1:'Active',0:'Inactive'})
        eng = churn_by('Member Status', dff2)
        fig3 = px.bar(eng, x='Member Status', y='Churn Rate %', text='Churn Rate %',
                      color='Member Status',
                      color_discrete_sequence=['#2E75B6','#C55A11'])
        fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig3.update_layout(showlegend=False, height=300,
                           margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Age Distribution — Churned vs Retained</div>', unsafe_allow_html=True)
        fig4 = px.histogram(dff, x='Age', color='Exited',
                            color_discrete_map={0:'#2E75B6',1:'#C55A11'},
                            nbins=30, barmode='overlay', opacity=0.7,
                            labels={'Exited':'Status'},
                            category_orders={'Exited':[0,1]})
        fig4.for_each_trace(lambda t: t.update(name='Retained' if t.name=='0' else 'Churned'))
        fig4.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                           legend=dict(orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Financial Profile: Churned vs Retained Customers</div>', unsafe_allow_html=True)
    comp = dff.groupby('Exited').agg(
        Avg_Balance=('Balance','mean'),
        Avg_Salary=('EstimatedSalary','mean'),
        Avg_CreditScore=('CreditScore','mean'),
        Avg_Age=('Age','mean'),
        Count=('Exited','count')
    ).reset_index()
    comp['Status'] = comp['Exited'].map({0:'Retained',1:'Churned'})
    st.dataframe(comp[['Status','Count','Avg_Balance','Avg_Salary',
                        'Avg_CreditScore','Avg_Age']].style.format({
        'Avg_Balance':'€{:,.0f}',
        'Avg_Salary':'€{:,.0f}',
        'Avg_CreditScore':'{:.0f}',
        'Avg_Age':'{:.1f}'
    }), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 4: HIGH-VALUE CUSTOMERS
# ════════════════════════════════════════════════════════════════════════════
elif page == "💰 High-Value Customers":
    st.title("💰 High-Value Customer Churn Analysis")
    st.markdown("Premium customers (top 25% balance) — churn risk and revenue exposure")
    st.markdown("---")

    hv_f = dff[dff['Balance'] >= hv_threshold]
    hv_churn = hv_f['Exited'].mean()
    revenue_at_risk = hv_f[hv_f['Exited']==1]['Balance'].sum()

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi_card("HV Customers", f"{len(hv_f):,}")
    with c2: kpi_card("HV Churn Rate", f"{hv_churn*100:.1f}", "%", red=True)
    with c3: kpi_card("HV Churned", f"{hv_f['Exited'].sum():,}", red=True)
    with c4: kpi_card("Revenue at Risk", f"€{revenue_at_risk/1e6:.1f}M", red=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">HV Churn by Geography</div>', unsafe_allow_html=True)
        hv_geo = churn_by('Geography', hv_f)
        fig = px.bar(hv_geo, x='Geography', y='Churn Rate %', text='Churn Rate %',
                     color='Geography',
                     color_discrete_sequence=['#1F3864','#2E75B6','#C55A11'])
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(showlegend=False, height=320,
                          margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Balance Distribution — Churned vs Retained</div>', unsafe_allow_html=True)
        fig2 = px.box(dff[dff['Balance']>0], x='Exited', y='Balance',
                      color='Exited',
                      color_discrete_map={0:'#2E75B6',1:'#C55A11'},
                      labels={'Exited':'0=Retained, 1=Churned'})
        fig2.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">Revenue at Risk by Geography (High-Value Churners)</div>', unsafe_allow_html=True)
    risk = hv_f[hv_f['Exited']==1].groupby('Geography')['Balance'].sum().reset_index()
    risk.columns = ['Geography','Revenue at Risk']
    fig3 = px.bar(risk, x='Geography', y='Revenue at Risk',
                  color='Geography', text='Revenue at Risk',
                  color_discrete_sequence=['#1F3864','#C55A11','#2E75B6'])
    fig3.update_traces(texttemplate='€%{text:,.0f}', textposition='outside')
    fig3.update_layout(showlegend=False, height=320,
                       margin=dict(t=10,b=10,l=10,r=10),
                       yaxis_title="Balance (€)")
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 5: SEGMENT EXPLORER
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Segment Explorer":
    st.title("🔍 Interactive Segment Explorer")
    st.markdown("Drill down into any combination of customer attributes")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        seg_x = st.selectbox("Primary Dimension", ['Geography','AgeGroup','Gender',
                                                    'CreditBand','TenureGroup','BalanceSegment'])
    with c2:
        seg_color = st.selectbox("Color By", ['Gender','Geography','AgeGroup',
                                              'CreditBand','TenureGroup','BalanceSegment'])
    with c3:
        chart_type = st.selectbox("Chart Type", ['Grouped Bar','Stacked Bar','Line'])

    seg = dff.groupby([seg_x, seg_color])['Exited'].mean().reset_index()
    seg['Churn Rate %'] = (seg['Exited']*100).round(1)

    if chart_type == 'Grouped Bar':
        fig = px.bar(seg, x=seg_x, y='Churn Rate %', color=seg_color,
                     barmode='group', text='Churn Rate %',
                     color_discrete_sequence=PALETTE)
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    elif chart_type == 'Stacked Bar':
        fig = px.bar(seg, x=seg_x, y='Churn Rate %', color=seg_color,
                     barmode='stack', color_discrete_sequence=PALETTE)
    else:
        fig = px.line(seg, x=seg_x, y='Churn Rate %', color=seg_color,
                      markers=True, color_discrete_sequence=PALETTE)

    fig.update_layout(height=420, margin=dict(t=10,b=10,l=10,r=10),
                      yaxis_title="Churn Rate (%)",
                      legend=dict(orientation='h', yanchor='bottom', y=1.02))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Raw Segment Data</div>', unsafe_allow_html=True)
    seg_table = dff.groupby([seg_x, seg_color])['Exited'].agg(['sum','count','mean']).reset_index()
    seg_table.columns = [seg_x, seg_color, 'Churned','Total','Churn Rate']
    seg_table['Churn Rate'] = (seg_table['Churn Rate']*100).round(1).astype(str) + '%'
    st.dataframe(seg_table, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888; font-size:0.8rem;'>"
    "Customer Segmentation & Churn Pattern Analytics in European Banking | "
    "Unified Mentor Internship Project | Data Science</p>",
    unsafe_allow_html=True
)

