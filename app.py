import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
import investpy as inv

#vamos separar os modulos para ficar organizado definindo funcoes com o def

def home():
	col1, col2, col3 = st.columns(3)
	with col2:
		st.image('grafico_logo.png')
		st.markdown('---')
		st.title('App Financeiro')
		st.markdown('---')



# ---------------------- mudando para outrao opcao do menu
def panorama():
	st.title('Panorama do Mercado')
	st.markdown(date.today().strftime('%d/%m/%Y'))
	
	st.subheader('Mercados pelo Mundo')
	
	dict_tickers = {'Bovespa':'^BVSP','S&P500':'^GSPC','NASDAQ':'^IXIC','DAX':'^GDAXI', 'FTSE 100': '^FTSE','Cruid Oil': 'CL=F','Gold': 'GC=F','BITCOIN': 'BTC-USD','ETHEREUM': 'ETH-USD'}


	df_info = pd.DataFrame({'Ativo': dict_tickers.keys(),'Ticker': dict_tickers.values()}) # O DF C/ A COLUNA ATIVO RECEBENDO O DICIONARIO E A TICKER RECEB O VALUES
	df_info['Ult. Valor'] = ''                                         #AQUI ESTAMOS APENAS CRIANDO 2 COLUNAS VAZIAS PARA POPULAR
	df_info['%'] =''
	count = 0                                                           #criamos um contador para cada interacao do loop a seguir
	with st.spinner('Baixando cotações...'):                            #criamos um spiner para carregar as cotacoes                                                 
		for ticker in dict_tickers.values():                          #para cada ticker dentro do df dicttickers pegando os valores
			cotacoes = yf.download(ticker, period ='5d')['Adj Close']
			variacao = ((cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
			df_info['Ult. Valor'][count] = round(cotacoes.iloc[-1],2)
			df_info['%'][count] = round(variacao,2)
			count +=1
			#st.write(df_info) #aqui colocamos a exibicao do dfinfo para ver quando rodar se dava certo a funcao for. podemos apagar
	
	col1,col2, col3 = st.columns(3)

	with col1:
		st.metric(df_info['Ativo'][0], value = df_info['Ult. Valor'][0], delta = str(df_info['%'][0])+' %')
		st.metric(df_info['Ativo'][1], value = df_info['Ult. Valor'][1], delta = str(df_info['%'][1])+' %')
		st.metric(df_info['Ativo'][2], value = df_info['Ult. Valor'][2], delta = str(df_info['%'][2])+' %')

	with col2:
		st.metric(df_info['Ativo'][3], value = df_info['Ult. Valor'][3], delta = str(df_info['%'][3])+' %')
		st.metric(df_info['Ativo'][4], value = df_info['Ult. Valor'][4], delta = str(df_info['%'][4])+' %')
		st.metric(df_info['Ativo'][5], value = df_info['Ult. Valor'][5], delta = str(df_info['%'][5])+' %')

	with col3:
		st.metric(df_info['Ativo'][6], value = df_info['Ult. Valor'][6], delta = str(df_info['%'][6])+' %')
		st.metric(df_info['Ativo'][7], value = df_info['Ult. Valor'][7], delta = str(df_info['%'][7])+' %')
		st.metric(df_info['Ativo'][8], value = df_info['Ult. Valor'][8], delta = str(df_info['%'][8])+' %')

	st.markdown('---')
	st.header('Comportamento durante o dia')

	lista_indices = ['IBOV', 'S&P500', 'NASDAQ']
	indice = st.selectbox('Selecione o Índice', lista_indices)

	if indice =='IBOV':
		indice_diario = yf.download('^BVSP', period = '1d', interval = '5m')
	if indice =='S&P500':
		indice_diario = yf.download('^GSPC', period = '1d', interval = '5m')
	if indice =='NASDAQ':
		indice_diario = yf.download('^IXIC', period = '1d', interval = '5m')

	import plotly.graph_objects as go

	fig = go.Figure(data = [go.Candlestick(x=indice_diario.index, open = indice_diario['Open'], high = indice_diario['High'], low=indice_diario['Low'], close= indice_diario['Close'])])
	fig.update_layout(title = indice, xaxis_rangeslider_visible = False)
	st.plotly_chart(fig)
		
	lista_acoes = ['PETR4.SA', 'VALE3.SA', 'EQTL3.SA', 'CSNA3.SA']
	acao = st.selectbox('Selecione a Ação', lista_acoes)
	hist_acao = yf.download(acao, period = '1d', interval = '5m')

	fig = go.Figure(data = [go.Candlestick(x=hist_acao.index, open = hist_acao['Open'], high = hist_acao['High'], low=hist_acao['Low'], close= hist_acao['Close'])])
	fig.update_layout(title = acao, xaxis_rangeslider_visible = False)
	st.plotly_chart(fig)


# ---------------------- mudando para outrao opcao do menu

def mapa_mensal():
	st.title('Análise Retornos Mensais')
	
	with st.expander('Escolha', expanded = True):
		opcao = st.radio('Selecione', ['Indices', 'Ações'])
	
	if opcao == 'Indices':
		with st.form(key='form_indice'):
			ticker = st.selectbox('Indice', ['Bovespa', 'Financials','Basic Materials'])
			analisar = st.form_submit_button('Analisar')
	else:
		with st.form(key = 'form_acoes'):
			ticker = st.selectbox('Ações', ['PETR4', 'EQTL3', 'VALE3'])
			analisar = st.form_submit_button('Analisar')
	
	if analisar:
		data_inicial = '1999-12-01'
		data_final   = '2022-12-31'
		
		if opcao == 'Indices':
			retornos = yf.download('^BVSP', start = data_inicial, end = data_final, interval ='1mo')['Close'].pct_change()
		else:
			retornos = yf.download(str(ticker)+'.SA', start = data_inicial, end = data_final, interval ='1mo')['Close'].pct_change()
	
		retornos.index = pd.to_datetime(retornos.index)
		#st.write(retornos)	aqui colocamos para saber se esta rodando certo, depois pode tirar

		#vamos separar e agrupar os anos e meses
		retorno_mensal = retornos.groupby([retornos.index.year.rename('Year'), retornos.index.month.rename('Month')]).mean()
		#st.write(retorno_mensal) aqui colocamos para saber se esta rodando certo, depois pode tirar

		#criando a tabela de matriz de retornos
		tabela_retornos = pd.DataFrame(retorno_mensal)
		tabela_retornos = pd.pivot_table(tabela_retornos, values = 'Close', index = 'Year', columns = 'Month')
		tabela_retornos.columns = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
		#st.write(tabela_retornos) aqui colocamos para saber se esta rodando certo, depois pode tirar

		#criacao do heatmap
		fig, ax = plt.subplots(figsize = (12,10)) #cria 2 figuras
		cmap = sns.color_palette('RdYlGn', 50) # define as cores 
		sns.heatmap(tabela_retornos, cmap = cmap, annot = True, fmt = '.2%', center = 0, vmax = 0.02, vmin = -0.02, cbar = False, linewidths=1, xticklabels = True, yticklabels = True, ax = ax)
		ax.set_title(ticker, fontsize = 18)
		ax.set_yticklabels(ax.get_yticklabels(), rotation = 0, verticalalignment = 'center', fontsize = '12')
		ax.set_xticklabels(ax.get_xticklabels(), fontsize = '12')
		ax.xaxis.tick_top() #colocar o x axis em cima
		plt.ylabel('')
		st.pyplot(fig)


		stats = pd.DataFrame(tabela_retornos.mean() , columns = ['media'])
		stats['mediana']   = tabela_retornos.median()
		stats['maior']     = tabela_retornos.max()
		stats['menor']     = tabela_retornos.min()
		stats['positivos'] = tabela_retornos.gt(0).sum() / tabela_retornos.count()#conte os valores maior que 0 com a .gt e some p/ saber quantas vezes ficou positivo
		stats['negativos'] = tabela_retornos.le(0).sum() / tabela_retornos.count()#contagem de qtde de numeros menor q zeros
		#st.write(stats) a gente coloca esse comando so para ver coo ficou a tabela, depois pode tirar


		stats_a = stats[['media', 'mediana', 'maior', 'menor']]
		stats_a = stats_a.transpose() # vai inverter coluna com linha

		#criacao do heatmap
		fig, ax = plt.subplots(figsize = (12,2.5)) #cria 2 figuras
		sns.heatmap(stats_a, cmap = cmap, annot = True, fmt = '.2%', center = 0, vmax = 0.02, vmin = -0.02, cbar = False, linewidths=1, xticklabels = True, yticklabels = True, ax = ax)
		#ax.set_title(ticker, fontsize = 18)
		ax.set_yticklabels(ax.get_yticklabels(), rotation = 0, verticalalignment = 'center', fontsize = '12')
		ax.set_xticklabels(ax.get_xticklabels(), fontsize = '12')
		#ax.xaxis.tick_top() #colocar o x axis em cima
		#plt.ylabel('')
		st.pyplot(fig)
	

		stats_b = stats[['positivos', 'negativos']]
		stats_b = stats_b.transpose() # vai inverter coluna com linha

		#criacao do heatmap
		fig, ax = plt.subplots(figsize = (12,1.5)) #cria 2 figuras
		sns.heatmap(stats_b, annot = True, fmt = '.2%', center = 0, vmax = 0.02, vmin = -0.02, cbar = False, linewidths=1, xticklabels = True, yticklabels = True, ax = ax)
		#ax.set_title(ticker, fontsize = 18)
		ax.set_yticklabels(ax.get_yticklabels(), rotation = 0, verticalalignment = 'center', fontsize = '12')
		ax.set_xticklabels(ax.get_xticklabels(), fontsize = '12')
		#ax.xaxis.tick_top() #colocar o x axis em cima
		#plt.ylabel('')
		st.pyplot(fig)




# ---------------------- mudando para outrao opcao do menu
def fundamentos():
	import fundamentus as fd
	st.title('Informações sobre Fundamentos')

	#importar toda a lista de tickers que tem na api da fundamentus
	lista_tickers = fd.list_papel_all()
	#st.write(lista_tickers) aqui, colocamos para exibir a lista para saber se esta rodando ok , depois pode tirar
	
	comparar = st.checkbox('Comparar 2 ativos')
	col1, col2 = st.columns(2) #fizemos uma estrutura de 2 colunas para exibicao no app
	with col1:
		with st.expander('Ativo 1', expanded = True):
			papel1 = st.selectbox('Selecione o Papel', lista_tickers)
			info_papel1 = fd.get_detalhes_papel(papel1) #funcao da fundamentus para pegar todas as inform do papel selecionado

			#st.write(info_papel1) #aqui, usamos o infopapel para saber as colunas que podemos exibir, depois construimos acima separado o que queremos analisar
			st.write('**Empresa:**'            ,       info_papel1      ['Empresa'][0])  #** é negrito e o indice 0 é p/ pegar o valor que esta na variavel
			st.write('**Setor:**'              ,       info_papel1      ['Setor'][0]) 
			st.write('**Subsetor:**'           ,       info_papel1      ['Subsetor'][0])
			st.markdown('---')
			try:
				st.write('**Valor de mercado:**'   , f"R$ {float(info_papel1['Valor_de_mercado'][0]):,.2f}")
			except:
				st.write('**Valor de mercado:**', 'Sem informação')
			try:
				st.write('**Patrimônio Líquido:**' , f"R$ {float(info_papel1['Patrim_Liq' ][0]):,.2f}")
			except:
				st.write('**Patrimônio Líquido:**' , 'Sem informação')
			try:
				st.write('**Receita Líquida 12m:**', f"R$ {float(info_papel1['Receita_Liquida_12m'][0]):,.2f}")
			except:
				st.write('**Receita Líquida 12m:**', 'Sem informação')
			try:
				st.write('**Dívida Bruta:**'       , f"R$ {float(info_papel1['Div_Bruta'  ][0]):,.2f}")
			except:
				st.write('**Dívida Bruta:**'       , 'Sem informação')
			try:
				st.write('**Dívida Líquida:**'     , f"R$ {float(info_papel1['Div_Liquida'][0]):,.2f}")
			except:
				st.write('**Dívida Líquida:**'     , 'Sem informação')
			try:
				st.write('**Lucro Líquido 12m:**'  , f"R$ {float(info_papel1['Lucro_Liquido_12m'][0]):,.2f}")
			except:
				st.write('**Lucro Líquido 12m:**'  , 'Sem informação')
			try:
				st.write('**P/L:**'                , f"R$ {float(info_papel1['PL'         ][0]):,.2f}")
			except:
				st.write('**P/L:**'                , 'Sem informação')
			try:
				st.write('**Dividend Yield:**'     , f"   {info_papel1      ['Div_Yield'  ][0]}")
			except:
				st.write('**Dividend Yield:**'     , 'Sem informação')


	if comparar:
		with col2:
			with st.expander('Ativo 2', expanded = True):
				papel2 = st.selectbox('Selecione o 2º Papel', lista_tickers)
				info_papel2 = fd.get_detalhes_papel(papel2)                 #funcao da fundamentus para pegar todas as inform do papel selecionado
				st.write('**Empresa:**'            ,       info_papel2      ['Empresa'][0])  
				st.write('**Setor:**'              ,       info_papel2      ['Setor'][0]) 
				st.write('**Subsetor:**'           ,       info_papel2      ['Subsetor'][0]) 
				st.markdown('---')
				try:
					st.write('**Valor de Mercado:**'   , f"R$ {float(info_papel2['Valor_de_mercado'][0]):,.2f}") 
				except:
					st.write('**Valor de Mercado:**'   , 'Sem informação') 
				try:
					st.write('**Patrimônio Líquido:**' , f"R$ {float(info_papel2['Patrim_Liq' ][0]):,.2f}")
				except:
					st.write('**Patrimônio Líquido:**' , 'Sem informação')
				try:
					st.write('**Receita Líquida 12m:**', f"R$ {float(info_papel2['Receita_Liquida_12m'][0]):,.2f}")
				except:
					st.write('**Receita Líquida 12m:**', 'Sem informação')
				try:
					st.write('**Dívida Bruta:**'       , f"R$ {float(info_papel2['Div_Bruta'  ][0]):,.2f}")
				except:
					st.write('**Dívida Bruta:**'       , 'Sem informação')
				try:
					st.write('**Dívida Líquida:**'     , f"R$ {float(info_papel2['Div_Liquida'][0]):,.2f}")
				except:
					st.write('**Dívida Líquida:**'     , 'Sem informação')
				try:
					st.write('**Lucro Líquido 12m:**'  , f"R$ {float(info_papel2['Lucro_Liquido_12m'][0]):,.2f}")
				except:
					st.write('**Lucro Líquido 12m:**'  , 'Sem informação')
				try:
					st.write('**P/L:**'                , f"R$ {float(info_papel2['PL'         ][0]):,.2f}")
				except:
					st.write('**P/L:**'                , 'Sem informação')
				try:
					st.write('**Dividend Yield:**'     , f"   {info_papel2      ['Div_Yield'  ][0]}")
				except:
					st.write('**Dividend Yield:**'     , 'Sem informação')
					
	

#a funcao main: a principal funcao que vai carregar a sidebar e chamar o menu
def main():
	st.sidebar.image('grafico_logo.png', width = 200)
	st.sidebar.title('App Financeiro')
	st.sidebar.markdown('---')
	lista_menu = ['Home', 'Panorama do Mercado', 'Rentabilidades Mensais', 'Fundamentos']
	escolha = st.sidebar.radio('Escolha a opção:', lista_menu)

	if escolha == 'Home':
		home()
	if escolha == 'Panorama do Mercado':
		panorama()
	if escolha == 'Rentabilidades Mensais':
		mapa_mensal()
	if escolha == 'Fundamentos':
		fundamentos()

main()




