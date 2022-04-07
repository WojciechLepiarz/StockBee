import numpy as np
import glob
import pandas as pd
from bokeh.plotting import figure, show, gridplot
from bokeh.models import HoverTool
from math import pi
from bokeh.io import output_notebook

def plot_candlestick(inputDf: pd.DataFrame, dateStart: str = "19000101", ma1Period: int = 0, ma2Period: int = 0, 
                     stochPeriod: int = 10) -> None:
    df = inputDf.copy()
    w = 12*60*60*1000 # half day in ms
    if ma1Period > 0:
        df['MA_'+str(ma1Period)] = df["<CLOSE>"].rolling(ma1Period).mean()
    if ma2Period > 0:
        df['MA_'+str(ma2Period)] = df["<CLOSE>"].rolling(ma2Period).mean()
    
    df = df.loc[df.index >= dateStart]
    inc = df["<CLOSE>"] > df["<OPEN>"]
    dec = df["<OPEN>"] > df["<CLOSE>"]
    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,save"

    df["%K"] = (100 
                * (df["<CLOSE>"] - df["<CLOSE>"].rolling(stochPeriod).min()) 
                / (df["<CLOSE>"].rolling(stochPeriod).max() - df["<CLOSE>"].rolling(stochPeriod).min()))
    df["%D"] = df["%K"].rolling(3).mean()
    df["%D-slow"] = df["%D"].rolling(2).mean()
    
    pp = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = df["<TICKER>"].values[0])
    ppv = figure(x_axis_type="datetime", x_range=pp.x_range, tools=TOOLS, 
                 plot_width=1000, plot_height=200, title="VOLUME")
    ppstoch = figure(x_axis_type="datetime", x_range=pp.x_range, tools=TOOLS, 
                     plot_width=1000, plot_height=200, title="STOCH")
    
    pp.xaxis.major_label_orientation = pi/4
    pp.xaxis.ticker.desired_num_ticks = 60
    pp.yaxis.ticker.desired_num_ticks = 20
    pp.grid.grid_line_alpha=0.3
    
    ppv.xaxis.major_label_orientation = pi/4
    ppv.xaxis.ticker.desired_num_ticks = 60
    ppv.yaxis.ticker.desired_num_ticks = 5
    ppv.grid.grid_line_alpha=0.3
    
    ppstoch.xaxis.major_label_orientation = pi/4
    ppstoch.xaxis.ticker.desired_num_ticks = 60
    ppstoch.yaxis.ticker.desired_num_ticks = 5
    ppstoch.grid.grid_line_alpha=0.3

    pp.segment(df.index, df["<HIGH>"], df.index, df["<LOW>"], color="black")
    pp.vbar(df.index[inc], w, df["<OPEN>"][inc], df["<CLOSE>"][inc], fill_color="#D5E1DD", line_color="black")
    pp.vbar(df.index[dec], w, df["<OPEN>"][dec], df["<CLOSE>"][dec], fill_color="#F2583E", line_color="black")
    pp.add_tools(HoverTool(tooltips=[( 'price',  '$y')]))
    if ma1Period > 0:
        pp.line(df.index, df['MA_'+str(ma1Period)], color="blue")
    if ma2Period > 0:
        pp.line(df.index, df['MA_'+str(ma2Period)], color="red")
    ppv.vbar(df.index, w, 0, df["<VOL>"], fill_color="#F2583E", line_color="black")
    
    ppstoch.line(df.index, df['%D'], color="red")
    ppstoch.line(df.index, df['%D-slow'], color="green")
    
    gg = gridplot([[pp], [ppv], [ppstoch]])
    
    show(gg)  # open a browser

def plot_change_range(inputDataframe: pd.DataFrame, dateStart: str) -> pd.DataFrame:
    df = inputDataframe.copy()
    w = 12*60*60*1000 # half day in ms
    df = df.loc[df.index >= dateStart]
    df["Change"] = (df["<CLOSE>"] / df["<CLOSE>"].shift(1)) * 100 - 100
    df["Range"] = (df["<HIGH>"] - df["<LOW>"]) / df["<CLOSE>"] * 100 
    inc = df["Change"] >= 0
    dec = df["Change"] < 0
    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,save"

    pp = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, plot_height=400, 
                title = df["<TICKER>"].values[0] + " Close change vs. t-1 [%]")
    ppv = figure(x_axis_type="datetime", x_range=pp.x_range, tools=TOOLS, plot_width=1000, 
                 plot_height=200, title="VOLUME")
    ppx = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, plot_height=300, 
                 title = df["<TICKER>"].values[0] + " (Low-High range) / Close [%]")
    pp.xaxis.major_label_orientation = pi/4
    pp.xaxis.ticker.desired_num_ticks = 60
    pp.yaxis.ticker.desired_num_ticks = 5
    pp.grid.grid_line_alpha=0.3
    
    ppv.xaxis.major_label_orientation = pi/4
    ppv.xaxis.ticker.desired_num_ticks = 60
    ppv.yaxis.ticker.desired_num_ticks = 5
    ppv.grid.grid_line_alpha=0.3
    
    ppx.xaxis.major_label_orientation = pi/4
    ppx.xaxis.ticker.desired_num_ticks = 60
    ppx.yaxis.ticker.desired_num_ticks = 5
    ppx.grid.grid_line_alpha=0.3

    pp.vbar(df.index[inc], w, 0, df["Change"][inc], fill_color="#D5E1DD", line_color="black")
    pp.vbar(df.index[dec], w, 0, df["Change"][dec], fill_color="#F2583E", line_color="black")
    pp.add_tools(HoverTool(tooltips=[( 'Change [%]',  '$y')]))
    
    ppx.vbar(df.index, w, 0, df["Range"], fill_color="#D5E1DD", line_color="black")
    ppx.add_tools(HoverTool(tooltips=[( 'Range [%]',  '$y')]))
  
    ppv.vbar(df.index, w, 0, df["<VOL>"], fill_color="#F2583E", line_color="black")
    
    gg = gridplot([[pp], [ppv], [ppx]])
    show(gg)  # open a browser
    return df
