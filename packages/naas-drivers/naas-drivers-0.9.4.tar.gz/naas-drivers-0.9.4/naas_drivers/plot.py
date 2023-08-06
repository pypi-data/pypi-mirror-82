import plotly.graph_objects as go
import pandas as pd
import requests
import datetime as dt
import os


class Plot:
    """ Plot generator lib"""

    __css_base = ".modebar {display: none;} \n.modebar-container {display: none;} "

    def export(self, chart, filename, css=None):
        """ create html export and add css to it"""
        html_filename = f"{filename.split('.')[0]}.html"
        html_exist = os.path.exists(html_filename)
        chart.write_html(html_filename)
        html_map = None
        if css is None:
            css = self.__css_base
        else:
            css = css + self.__css_base
        with open(html_filename) as f:
            html_map = f.read()
            result = html_map.replace(
                "</head>", f'<style id="naas_css">{css}</style></head>'
            )
        with open(html_filename, "w") as f:
            f.write(result)
            f.close()
        if filename.endswith(".png"):
            html_text = result
            json = {
                "output": "screenshot",
                "html": html_text,
                "emulateScreenMedia": True,
                "ignoreHttpsErrors": True,
                "scrollPage": False,
                "screenshot": {"type": "png", "selector": ".cartesianlayer"},
            }
            req = requests.post(
                url=f"{os.environ.get('SCREENSHOT_API', 'http://naas-screenshot:9000')}/api/render",
                json=json,
            )
            req.raise_for_status()
            open(filename, "wb").write(req.content)
            if not html_exist:
                os.remove(html_filename)
        elif not filename.endswith(".png") and not filename.endswith(".html"):
            print("Not supported for now")
            os.remove(html_filename)
            return
        print("Save as", filename)

    def stock(
        self,
        stock_companies,
        date_from=-30,
        date_to="today",
        interval="1d",
        kind="candlestick",
        moving_average=False,
        filter=False,
        filter_title="Stock",
    ):
        """ generate financial_chart """
        if isinstance(stock_companies, str):
            stock_companies = [stock_companies]
        if isinstance(date_from, int) and date_from < 0:
            date_from = dt.datetime.today() + dt.timedelta(days=date_from)
        else:
            raise ValueError(f"date_from ({date_from}) cannot be positive")
        if isinstance(date_to, int) and date_to > 0:
            date_to = dt.datetime.today() + dt.timedelta(days=date_to)
        if isinstance(date_to, str) and date_to == "today":
            date_to = dt.datetime.today()
        else:
            raise ValueError(f"date_to ({date_to}) cannot be negative")
        stocks = []
        data = []
        period1 = date_from.strftime("%s")
        period2 = date_to.strftime("%s")
        buttons = []
        buttons.append(
            dict(
                args=[{"visible": [True for x in stock_companies]}],
                label="All",
                method="restyle",
            )
        )
        for company in stock_companies:
            url = (
                f"https://query1.finance.yahoo.com/v7/finance/download/"
                f"{company}?period1={period1}&period2={period2}&interval={interval}&events=history"
            )
            print("getting data for", company, url)
            stock = pd.read_csv(url)
            stock["Company"] = company
            stocks.append(stock)
            visibility = [x == company for x in stock_companies]
            if moving_average:
                stock["MA20"] = stock.Close.rolling(20).mean()
                stock["MA50"] = stock.Close.rolling(50).mean()
                data.append(
                    go.Scatter(
                        x=stock["Date"],
                        y=stock.MA20,
                        line=dict(color="green", width=1),
                        name="20 MA",
                    )
                )
                data.append(
                    go.Scatter(
                        x=stock["Date"],
                        y=stock.MA50,
                        line=dict(color="red", width=1),
                        name="50 MA",
                    )
                )
            if kind == "candlestick":
                data.append(
                    go.Candlestick(
                        name=company,
                        x=stock["Date"],
                        open=stock["Open"],
                        high=stock["High"],
                        low=stock["Low"],
                        close=stock["Close"],
                    )
                )

            elif kind == "linechart":
                data.append(
                    go.Scatter(
                        x=stock["Date"], y=stock["Open"], mode="lines", name="Open"
                    )
                )
                data.append(
                    go.Scatter(
                        x=stock["Date"], y=stock["Close"], mode="lines", name="Close"
                    )
                )
            else:
                print("Not supported for now")
                return
            buttons.append(
                dict(
                    args=[{"visible": visibility}],
                    label=company,
                    visible=True,
                    method="restyle",
                )
            )
        print("generating plot")
        updatemenus = list(
            [
                dict(
                    active=0,
                    buttons=list(buttons),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top",
                ),
            ]
        )
        layout = None
        if filter:
            layout = dict(
                dragmode="pan",
                xaxis_rangeslider_visible=False,
                showlegend=False,
                updatemenus=updatemenus,
            )
        else:
            layout = dict(
                dragmode="pan",
                xaxis_rangeslider_visible=False,
                showlegend=False,
                updatemenus=[],
            )
        fig = go.Figure(data=list(data), layout=layout)
        if filter:
            fig.update_layout(
                template="plotly_white",
                margin=dict(t=0, b=0, l=0, r=0),
                annotations=[
                    dict(
                        text=filter_title,
                        x=0,
                        xref="paper",
                        y=1.16,
                        yref="paper",
                        align="left",
                        showarrow=False,
                    )
                ],
            )
        return fig

    def table(self, header_values, cells_values, header_color="rgb(136,233,175)"):
        """ generate table html """

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(header_values),
                        fill_color=header_color,
                        line_color="white",
                        align="center",
                        font=dict(family="Helvetica", color="white", size=14),
                    ),
                    cells=dict(
                        values=cells_values,
                        fill_color="white",
                        line_color="lightgray",
                        align="left",
                        font=dict(family="Helvetica", size=12),
                    ),
                )
            ]
        )

        fig.update_layout(margin=dict(l=10, r=10, t=0, b=0))

        return fig
