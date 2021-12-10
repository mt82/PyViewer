import sys
import io
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
import pandas as pd

"""
Folium in PyQt5
"""
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # coordinate = (37.8199286, -122.4782551)
        # m = folium.Map(
        # 	tiles='Stamen Terrain',
        # 	zoom_start=13,
        # 	location=coordinate
        # )

        m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)

        coord = pd.DataFrame({
        'lon':[-58, 2, 145, 30.32, -4.03, -73.57, 36.82, -38.5],
        'lat':[-34, 49, -38, 59.93, 5.33, 45.52, -1.29, -12.97],
        'name':['Buenos Aires', 'Paris', 'melbourne', 'St Petersbourg', 'Abidjan', 'Montreal', 'Nairobi', 'Salvador'],
        'value':[10, 12, 40, 70, 23, 43, 100, 43]
        }, dtype=str)

        # add marker one by one on the map
        for i in range(0,len(coord)):
            folium.Marker(
                location=[coord.iloc[i]['lat'], coord.iloc[i]['lon']],
                popup=coord.iloc[i]['name'],
            ).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')