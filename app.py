from flask import Flask, render_template, request
import plotly.express as px
import manish
import numpy as np
import pandas as pd

app = Flask(__name__)
df = manish.load_data("csv_files")   
@app.route("/")
def home():
    return render_template(
        "index.html",
        locations=sorted(df["location"].dropna().unique()) if "location" in df.columns else [],
        industries=sorted(df["industry"].dropna().unique()) if "industry" in df.columns else [],
        ratings=sorted(df["company_rating"].dropna().unique()) if "company_rating" in df.columns else [],
        types=sorted(df["type"].dropna().unique()) if "type" in df.columns else []
    )
@app.route("/submit", methods=["POST"])
def submit():
    
    location = request.form.get("location")
    industry = request.form.get("industry")
    rating = request.form.get("rating")
    comp_type = request.form.get("type")
    output = request.form.get("output")

    filtered_df = df.copy()
    
    if location: 
        filtered_df = filtered_df[filtered_df["location"] == location]

    if industry: 
        filtered_df = filtered_df[filtered_df["industry"] == industry]

    if rating: 
        filtered_df = filtered_df[filtered_df["company_rating"] >= float(rating)]

    if comp_type: 
        filtered_df = filtered_df[filtered_df["type"] == comp_type]

    if output == "table":
        table_html = filtered_df.to_html(
            classes="table table-striped table-bordered table-hover align-middle",
            index=False,
            border=0,
            justify="center",
            escape=False
        )
        return render_template(
            "table.html",
            table=table_html,
            titles=filtered_df.columns.values
        )

    else:
        fig1 = px.scatter(filtered_df, x="company_rating", y="company_name",
                          title="Rating vs Company Name")

        fig2 = px.bar(filtered_df, x="company_name", y="company_rating", 
                      title="Distribution of Company Ratings")
        fig2.update_layout(xaxis_tickangle=45)

        fig3 = px.bar(filtered_df, x="company_name", y="years_old",
                      title="Distribution of Company Age")
        fig3.update_layout(xaxis_tickangle=45)

        fig4 = px.pie(filtered_df, names="company_name", 
                      title="Company Rating Distribution")
        fig5 = px.scatter(filtered_df, x="company_rating", y="years_old",
                          title="company age vs Company rating")
        fig6 = px.bar(filtered_df, x="size", y="company_rating",
                      title="company rating by size")
        fig6.update_layout(xaxis_tickangle=45)


        return render_template(
            "charts.html",
            chart1=fig1.to_html(full_html=True),
            chart2=fig2.to_html(full_html=True),
            chart3=fig3.to_html(full_html=False),
            chart4=fig4.to_html(full_html=False),
            chart5=fig5.to_html(full_html=False),
            chart6=fig6.to_html(full_html=False)
        )

if __name__ == "__main__":
    app.run(debug=True, port=5002)
