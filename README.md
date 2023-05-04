O projeto tem como propósito treinar programação com a linguagem python. Nisso, foi efetuado todos os tratamentos e análises através de um dataset disponibilizado no kaggle e implantado para uma pagina web através da biblioteca Streamlit. (link : https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data)

# 1. Problema de negocio: 

A Zomato é uma multinacional indiana focada na área de delivery e catálogo de dados, na qual presta serviço para os restaurantes cadastrados, entregadores e pessoas. 

Através de seu negócio, é possivel realizar pedidos de refeição em qualquer restaurante cadastrado, tendo a opção de escolher diversos tipos de culinária e receber sua comida no conforto de sua casa.

A empresa disponibilizou poucos dados, porém fornece estes diante ao mundo todo, o que indica que o estudo tem como foco a questão macroecônomica e as descobertas de possiveis oportuninidades para melhorar a receita da empresa, que serão visualmente disponiniblizadas através de KPIs e enviadas em um navegador web.

# 2. Premissas do negócio:
## -  Geral

	1. Quantos restaurantes únicos estão registrados? 

	2. Quantos países únicos estão registrados? 

	3. Quantas cidades únicas estão registradas?

	4. Qual o total de avaliações feitas? 

	5. Qual o total de tipos de culinária registrados?

## - Pais

	1. Qual o nome do país que possui mais cidades registradas? 

	2. Qual o nome do país que possui mais restaurantes registrados?

	3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados? 

	4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos? 

	5. Qual o nome do país que possui a maior quantidade de avaliações feitas? 

	6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega? 

	7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas? 

	8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?

	9. Qual o nome do país que possui, na média, a maior nota média registrada?  

	10. Qual o nome do país que possui, na média, a menor nota média registrada?

	11. Qual a média de preço de um prato para dois por país?



## - Cidade 
	1. Qual o nome da cidade que possui mais restaurantes registrados? 

	2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4? 

	3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?

	4. Qual o nome da cidade que possui o maior valor médio de um prato para dois? 

	5. Qual o nome da cidade que possui a maior quantidade de tipos de 
	culinária distintas? 

	6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas? 

	7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas? 

	8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

## - Restaurantes
	1. Qual o nome do restaurante que possui a maior quantidade de avaliações? 

	2. Qual o nome do restaurante com a maior nota média? 

	3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas? 

	4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?

	5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação? 

	6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas? 




# 3. Estratégia de solução 

## -  Análise Pais
	1. Custo médio por pais
	
	2. Quantidade de delivery
	
	3. Quantidade tipos de culinária 

## - Análise Cidade
	1. Restaurantes 
	2. Quantidade de culinária 
	3. Métrica de avaliação e serviço

## - Análise Restaurantes 
	1. Principais restaurantees 
	2. Principais Culinárias
	3. Restaurantes por pais



# Top 3 Insights
	1.Existe uma correlação entre a quantidade de culinária com a quantidade de mais entregas
	2.Os restaurantes com avalição > 4: Estão localizados em metrópoles ou capitais e possuem grande quantidade de avaliações. Já para as poucas quantidades de avaliações, percebe-se que é uma cidade pequena.
	3. Mesmo a Indian food sendo o principal pedido, os principais fast food americano é que são responsaveis por essa demanda, se aperfeiçoando as culinárias locais.


