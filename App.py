import calendar
from datetime import datetime

from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import streamlit as st

import database as db

#---------------- Settings -----------------------

incomes = ["sallery", "investments", "tax returns" "other income"]
expences = ["food", "rent/morgage", "utilities", "car", "other expences", "savings"]    
curency = "usd"
page_title = "Income and Expences Tracker"
page_icon = ":money_with_wings:"
layout = "centered"
#--------------------------------------------------

st.set_page_config(page_icon=page_icon, page_title=page_title, layout=layout)
st.title(page_title + " " + page_icon)

#-- DROP DOWN VALUES FOR SELECTING THE PERIOD --------------
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

# --- DATABASE INTERFACE ---
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#---------NAVAGATION MENU-------------
selected = option_menu(
    menu_title=None,
    options=["Data entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"],
    orientation="horizontal",
)

#----IMPUT & SAVE METHODS
if selected == "Data entry":
    st.header(f"Data entry in {curency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("select month: ", months, key="month")
        col2.selectbox("select year: ", years, key="year")


        "-----"
        with st.expander("income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step= 10, key=income)
        with st.expander("expences"):
            for expence in expences:
                st.number_input(f"{expence}:", min_value=0, format="%i", step= 10, key=expence)
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter a comment here ___")
        
        "----"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expences = {expence: st.session_state[expence] for expence in expences}
            db.insert_period(period, incomes, expences, comment)
            st.success("Data Saved!")

# ----- PLOT PERIODS ----
if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"):
        period = st.selectbox("select period", [get_all_periods()])
        submitted = st.form_submit_button("plot period")
        if submitted:
            #TODO get data from database
            period_data = db.get_period(period)
            comment = period_data.get("comment")
            expences = period_data.get("expenses")
            incomes = period_data.get("incomes")


            #Create Metrics
            total_income = sum(incomes.values())
            total_expences = sum(expences.values())
            remaining_budget = total_income - total_expences
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income:", f"{total_income} {curency}")
            col2.metric("Total Expences:", f"{total_expences} {curency}")
            col3.metric("Remaining Budget:", f"{remaining_budget} {curency}")
            st.text(f"Comment: {comment}")

            #creat sankey chart
            label = list(incomes.keys()) + ["Total Income"] + list(expences.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expences)
            target = [len(incomes)] * len(incomes) + [label.index(expences) for expence in expences]
            value = list(incomes.values()) + list(expences.values())

            #data to dic, dic to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)

            #plot it
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r =0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)


