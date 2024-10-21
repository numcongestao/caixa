import streamlit as st
import pandas as pd
import plotly.express as px

# Função para ler os dados do arquivo Excel
@st.cache_data
def load_excel(file):
    xls = pd.ExcelFile(file)
    sheets = xls.sheet_names
    data = {sheet: xls.parse(sheet) for sheet in sheets}
    return data, sheets

# Função para processar os dados e agregar por semana/dia
def process_data(df):
    # Garantir que a coluna 'Data' seja do tipo datetime
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Adicionar coluna para semana
    df['Semana'] = df['Data'].dt.isocalendar().week
    
    # Agregar dados por dia
    daily_data = df.groupby('Data').agg({'Receita': 'sum', 'Despesa': 'sum'}).reset_index()
    
    # Agregar dados por semana
    weekly_data = df.groupby('Semana').agg({'Receita': 'sum', 'Despesa': 'sum'}).reset_index()
    
    return daily_data, weekly_data

# Função para gerar gráfico
def plot_graph(df, title, x_column):
    fig = px.line(df, x=x_column, y=['Receita', 'Despesa'], title=title, markers=True)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)

# Função principal para o Streamlit
def main():
    st.title("Análise de Receita e Despesa")
    
    # Upload do arquivo Excel
    uploaded_file = st.file_uploader("Faça o upload da planilha Excel", type=["xlsx"])
    
    if uploaded_file:
        data, sheets = load_excel(uploaded_file)
        
        # Selecione o mês (sheet) a ser visualizado
        selected_sheets = st.multiselect("Escolha os meses (sheets) para visualizar", sheets)
        
        if selected_sheets:
            for sheet in selected_sheets:
                st.subheader(f"Análise do mês: {sheet}")
                
                # Carregar os dados do sheet selecionado
                df = data[sheet]
                
                # Processar os dados para agregar por dia e semana
                daily_data, weekly_data = process_data(df)
                
                # Exibir gráficos de receita e despesa por dia
                plot_graph(daily_data, f"Receita e Despesa Diária - {sheet}", 'Data')
                
                # Exibir gráficos de receita e despesa por semana
                weekly_data['Semana'] = 'Semana ' + weekly_data['Semana'].astype(str)
                plot_graph(weekly_data, f"Receita e Despesa Semanal - {sheet}", 'Semana')
                
                # Exibir os dados em formato de tabela
                st.write(f"Dados Diários - {sheet}")
                st.dataframe(daily_data)
                
                st.write(f"Dados Semanais - {sheet}")
                st.dataframe(weekly_data)
        else:
            st.warning("Por favor, selecione ao menos um mês para visualizar.")
        
if __name__ == "__main__":
    main()

