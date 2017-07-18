from flask import Flask, render_template
import json
import numpy as np
import pandas as pd
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
    LabelSet,
    Range1d
)
from bokeh.embed import components
from bokeh.plotting import figure


app = Flask(__name__)

@app.route("/")
def bar():

    with open('country.json', 'r') as bar_file:
        data = pd.read_json("country.json")

    country_rates = [x for x in data['percentage'] ]
    country_rates.pop(50)

    country_names = [x for x in data['country'] if x != ""]

    country_cdn = [x for x in data['cdn']]
    country_cdn.pop(50)

    country_p2p = [x for x in data['p2p']]
    country_p2p.pop(50)

    source = ColumnDataSource(data=dict(
        CDN=country_cdn,
        P2P=country_p2p,
        name=country_names,
        rate=country_rates,
    ))

    TOOLS = "pan,wheel_zoom,reset,hover,save"
    p = figure(title='CDN vs P2P',tools=TOOLS,
               x_range=Range1d(min(country_p2p), max(country_p2p)))

    p.scatter(x='CDN', y='P2P', size=8, source=source)

    p.yaxis[0].axis_label = 'CDN'
    p.xaxis[0].axis_label = 'P2P'

    #labels = LabelSet(x='P2P', y='CDN', text='name', level='glyph', x_offset=5, y_offset=5, source=source, render_mode='canvas')




    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Country", "@name"),
        ("CDN", "$CDN"),
        ("P2P", "$P2P"),
        ("Percentage", "$rate"),



    ]

    plot_script, plot_div = components(p)

    return render_template('mainBo.html', script=plot_script, div=plot_div)

if __name__ == "__main__":
    #app.run()
    #app.debug = True
    app.run(host='0.0.0.0', port=5000, debug = True)