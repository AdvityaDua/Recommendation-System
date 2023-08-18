import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix


def recommend(location, data, book_table, online_order, rating, reviews, cost, type):
    data = data[data['location'] == location]
    data = data.drop(['location'], axis=1)
    data = data.drop_duplicates(subset=['name'], keep='first')
    data1 = data.copy()
    data[['res1', 'res2']] = data['rest_type'].str.split(',', expand=True)
    data['res1'] = data['res1'].astype('category')
    data = data.drop(['name', 'dish_liked', 'cuisines', 'rest_type', 'res2', 'type'], axis=1)
    data = data.replace(['Yes', 'No'], [1, 0])
    data['approx_cost'] = data['approx_cost'].str.replace(',', '')
    model = NearestNeighbors(n_neighbors=5)
    data['res1'] = data['res1'].cat.codes
    model.fit(data.loc[:, :])
    if book_table == 'Yes':
        book_table = 1
    else:
        book_table = 0

    if online_order == 'Yes':
        online_order = 1
    else:
        online_order = 0
    li = ['Bakery', 'Bar', 'Beverage Shop', 'Cafe', 'Casual Dining', 'Delivery', 'Dessert Parlor', 'Pub', 'Lounge', 'Mess', 'Quick Bites', 'Sweet Shop', 'Takeaway']
    type = li.index(type)
    a = model.kneighbors([[book_table, online_order, rating, reviews, cost, type]])
    new_df = pd.DataFrame()
    for i in a[1]:
        new_df = pd.DataFrame(data1.iloc[i, :])
    return new_df

