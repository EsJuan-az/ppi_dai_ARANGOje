import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, box
import osmnx as ox
import pandas as pd
import numpy as np
from scipy import stats
from sqlmodel import Session, select
from io import BytesIO
import base64
from ..models import Order, User, OrderProduct, Product
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

class DataHelper:
    @staticmethod
    def calculate_distance(point1, point2):
        """Calcula la distancia euclidiana entre dos puntos.

        Args:
            point1 (Point): El primer punto.
            point2 (Point): El segundo punto.

        Returns:
            float: La distancia entre los dos puntos.
        """
        return point1.distance(point2)

    @staticmethod
    def tsp(start_point, other_points):
        """Encuentra la ruta más corta que pasa por todos los puntos, comenzando por el punto inicial.

        Args:
            start_point (Point): El punto de inicio.
            other_points (list of Point): Una lista de otros puntos a visitar.

        Returns:
            list of Point: La ruta más corta como una lista de puntos.
        """
        # Crear un GeoDataFrame para los puntos
        points = [start_point] + other_points
        gdf = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")
        
        # Crear un grafo completo
        G = nx.complete_graph(len(points))
        
        # Asignar pesos a las aristas basados en la distancia entre los puntos
        for i, j in G.edges():
            G[i][j]['weight'] = DataHelper.calculate_distance(points[i], points[j])
        
        # Encontrar el ciclo Hamiltoniano de peso mínimo
        tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)
        
        # Convertir los índices de vuelta a puntos
        route = [points[i] for i in tsp_path]
        
        return route
    
    @staticmethod
    def plot_route(route):
        """Dibuja la ruta más corta en un mapa.

        Args:
            route (list of Point): La ruta más corta como una lista de puntos.
        """
        # Crear un GeoDataFrame para la ruta
        gdf = gpd.GeoDataFrame(geometry=route, crs="EPSG:4326")
        
        # Crear una LineString para representar la ruta
        line = LineString(route)
        line_gdf = gpd.GeoDataFrame(geometry=[line], crs="EPSG:4326")
        
        # Determinar los límites del mapa
        minx, miny, maxx, maxy = gdf.total_bounds
        bbox = box(minx, miny, maxx, maxy)
        
        # Ampliar los límites del mapa para incluir algo de margen
        margin = 0.01
        bbox = box(minx - margin, miny - margin, maxx + margin, maxy + margin)
        
        # Descargar los datos de calles de OpenStreetMap para el área de interés
        streets = ox.graph_from_bbox(north=bbox.bounds[3], south=bbox.bounds[1], east=bbox.bounds[2], west=bbox.bounds[0], network_type='drive', simplify=True)
        streets_gdf = ox.graph_to_gdfs(streets, nodes=False)
        
        # Configuración del gráfico
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        
        # Dibujar las calles
        streets_gdf.plot(ax=ax, color='lightgrey', linewidth=0.5, alpha=0.7)
        
        # Dibujar los puntos
        gdf.plot(ax=ax, color='blue', markersize=50, label='Órdenes')
        gdf.iloc[[0]].plot(ax=ax, color='red', markersize=100, label='Tú')  # Primer punto en rojo
        
        # Dibujar la ruta
        line_gdf.plot(ax=ax, color='blue')
        
        # Añadir leyenda
        plt.legend()
        
        # Ajustar los límites del gráfico para que coincidan con el área de interés
        ax.set_xlim(bbox.bounds[0], bbox.bounds[2])
        ax.set_ylim(bbox.bounds[1], bbox.bounds[3])
        
        # Mostrar el gráfico
        return fig, ax

    @staticmethod
    async def analyze_data(session: AsyncSession, business_id: int) -> dict:
        """Analiza los datos de la base de datos para una empresa específica.

        Args:
            session (AsyncSession): Sesión de base de datos asíncrona SQLModel.
            business_id (int): ID de la empresa a analizar.

        Returns:
            dict: Un diccionario con los resultados del análisis y las imágenes en data URLs.
        """
        results = {}

        # Obtener todos los datos necesarios filtrados por business_id
        orders = (await session.exec(select(Order).where(Order.business_id == business_id))).all()
        products = (await session.exec(select(Product).where(Product.business_id == business_id))).all()
        order_products = (await session.exec(select(OrderProduct).join(OrderProduct.order).where(Order.business_id == business_id))).all()
        users = (await session.exec(select(User).join(Order, User.id == Order.customer_id).where(Order.business_id == business_id))).all()

        # Crear DataFrames de pandas
        orders_df = pd.DataFrame([order.dict() for order in orders])
        products_df = pd.DataFrame([product.dict() for product in products])
        order_products_df = pd.DataFrame([order_product.dict() for order_product in order_products])
        users_df = pd.DataFrame([user.dict() for user in users])

        # Reemplazar NaN y valores infinitos en DataFrames
        orders_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        products_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        order_products_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        users_df.replace([np.inf, -np.inf], np.nan, inplace=True)

        orders_df.fillna(0, inplace=True)
        products_df.fillna(0, inplace=True)
        order_products_df.fillna(0, inplace=True)
        users_df.fillna(0, inplace=True)

        # Análisis de productos más vendidos
        product_sales = order_products_df.groupby('product_id')['amount'].sum().reset_index()
        product_sales = product_sales.merge(products_df[['id', 'name', 'price']], left_on='product_id', right_on='id')
        product_sales['total_revenue'] = product_sales['amount'] * product_sales['price']
        product_sales = product_sales[['name', 'amount', 'total_revenue']].sort_values(by='amount', ascending=False)

        # Análisis de total ganado
        order_products_df = order_products_df.merge(products_df[['id', 'price']], left_on='product_id', right_on='id')
        order_products_df['total_price'] = order_products_df['amount'] * order_products_df['price']
        total_earned = order_products_df['total_price'].sum()

        # Agregar resultados al diccionario
        results['total_earned'] = float(total_earned)  # Asegurar que sea un float válido
        results['top_selling_products'] = product_sales.to_dict(orient='records')

        # Cantidad de órdenes hechas
        results['total_orders'] = len(orders)

        async def create_bar_chart(data):
            """Crea un gráfico de barras y lo convierte a data URL.

            Args:
                data (pd.DataFrame): DataFrame con los datos para el gráfico.

            Returns:
                str: Data URL de la imagen del gráfico.
            """
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(data['name'], data['amount'])
            ax.set_title('Productos más vendidos')
            ax.set_xlabel('Producto')
            ax.set_ylabel('Cantidad Vendida')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_data = buffer.getvalue()
            data_url = base64.b64encode(image_data).decode('utf-8')
            plt.close(fig)
            return data_url

        async def create_histogram(data):
            """Crea un histograma y lo convierte a data URL.

            Args:
                data (pd.DataFrame): DataFrame con los datos para el histograma.

            Returns:
                str: Data URL de la imagen del histograma.
            """
            data = data[data['price'] >= 0]  # Omitir valores menores a cero
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data['price'], bins=20, edgecolor='k')
            ax.set_title('Distribución de Precios de Productos')
            ax.set_xlabel('Precio')
            ax.set_ylabel('Frecuencia')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_data = buffer.getvalue()
            data_url = base64.b64encode(image_data).decode('utf-8')
            plt.close(fig)
            return data_url

        async def create_scatter_plot(data):
            """Crea un gráfico de dispersión y lo convierte a data URL.

            Args:
                data (pd.DataFrame): DataFrame con los datos para el gráfico.

            Returns:
                str: Data URL de la imagen del gráfico.
            """
            # Realizar la regresión lineal
            slope, intercept, r_value, p_value, std_err = stats.linregress(data['price'], data['amount'])

            # Crear el gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(data['price'], data['amount'], label='Datos')

            # Añadir la línea de regresión
            line = slope * data['price'] + intercept
            ax.plot(data['price'], line, color='red', label=f'Tendencia')

            # Añadir títulos y etiquetas
            ax.set_title('Precio vs Cantidad Vendida')
            ax.set_xlabel('Precio')
            ax.set_ylabel('Cantidad Vendida')
            ax.legend()

            # Guardar la imagen en un buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_data = buffer.getvalue()
            data_url = base64.b64encode(image_data).decode('utf-8')
            plt.close(fig)

            return data_url

        async def create_geospatial_plot(data):
            """Crea un gráfico geoespacial de las órdenes y lo convierte a data URL.

            Args:
                data (pd.DataFrame): DataFrame con los datos para el gráfico.

            Returns:
                str: Data URL de la imagen del gráfico.
            """
            # Convertir el DataFrame a un GeoDataFrame
            gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.lon, data.lat))
            
            # Cargar el mapa del mundo
            world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
            
            # Crear el gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            world.plot(ax=ax, color='lightgrey')

            # Añadir los puntos de las órdenes
            gdf.plot(ax=ax, color='blue', markersize=5)

            # Ajustar el área de visualización con padding
            minx, miny, maxx, maxy = gdf.total_bounds
            padding = 0.05  # Ajuste de padding, 5% del tamaño actual de la visualización
            ax.set_xlim(minx - (maxx - minx) * padding, maxx + (maxx - minx) * padding)
            ax.set_ylim(miny - (maxy - miny) * padding, maxy + (maxy - miny) * padding)

            # Añadir el título
            ax.set_title('Ubicación de las Órdenes')

            # Guardar la imagen en un buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_data = buffer.getvalue()
            data_url = base64.b64encode(image_data).decode('utf-8')
            plt.close(fig)
            
            return data_url

        # Ejecutar la creación de gráficos en paralelo
        bar_chart_url, histogram_url, scatter_plot_url, geospatial_plot_url = await asyncio.gather(
            create_bar_chart(product_sales),
            create_histogram(products_df),
            create_scatter_plot(order_products_df),
            create_geospatial_plot(orders_df)
        )

        results['top_selling_products_chart'] = f'data:image/png;base64,{bar_chart_url}'
        results['price_distribution_chart'] = f'data:image/png;base64,{histogram_url}'
        results['price_quantity_scatter'] = f'data:image/png;base64,{scatter_plot_url}'
        results['orders_geospatial_chart'] = f'data:image/png;base64,{geospatial_plot_url}'

        # Análisis de correlación entre precio y cantidad vendida
        merged_df = order_products_df.merge(products_df, left_on='product_id', right_on='id')
        merged_df = merged_df.replace([np.inf, -np.inf], np.nan).dropna(subset=['price_x', 'amount'])

        # Convertir las columnas a los tipos de datos correctos
        merged_df['price_x'] = merged_df['price_x'].astype('float64')
        merged_df['amount'] = merged_df['amount'].astype('int')

        # Solo calcular la correlación si hay datos suficientes y no contienen NaN
        correlation, p_value = None, None
        if len(merged_df) > 1 and not merged_df[['price_x', 'amount']].isnull().values.any():
            correlation, p_value = stats.pearsonr(merged_df['price_x'], merged_df['amount'])
        correlation = None if np.isnan(correlation) else correlation
        p_value = None if np.isnan(p_value) else p_value

        results['price_quantity_correlation'] = {
            'correlation': correlation,
            'p_value': p_value
        }

        return results

