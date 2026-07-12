import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

model = joblib.load("../sales_prediction_model.pkl")
encoders = joblib.load("../label_encoders.pkl")

df = pd.read_excel("../Dataset/superstore_sales_cleaned.xlsx")

if st.checkbox("Show Dataset"):

    st.dataframe(df, use_container_width=True)

    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    st.subheader("Missing Values")
    st.dataframe(df.isnull().sum())
    st.write("Dataset Shape")
    st.write(df.shape)
    st.write("Summary Statistics")
    st.dataframe(df.describe())
    st.write("Missing Values")
    st.dataframe(df.isnull().sum())

st.markdown("""
<style>

/* Input boxes */
div[data-baseweb="select"] > div:hover{
    border:2px solid #4CAF50 !important;
    box-shadow:0 0 10px rgba(76,175,80,0.5);
    transition:0.3s;
    cursor: pointer !important;
}

/* Number input */
div[data-testid="stNumberInput"] input:hover{
    border:2px solid #4CAF50 !important;
    transition:0.3s;
    cursor: pointer !important;
}

/* Slider */
div[data-testid="stSlider"]:hover{
    transform:scale(1.02);
    transition:0.3s;
    cursor: pointer !important;
}

/* Button */
.stButton > button:hover{
    border-radius:10px;
    transition:0.3s;
    cursor: pointer !important;
}

.stButton > button:hover{
    background:linear-gradient(90deg,#4CAF50,#00C853);
    color:white;
    transform:translateY(-3px);
    box-shadow:0 10px 25px rgba(0,200,83,0.45);
    cursor: pointer !important;
}

/* Sidebar card */
section[data-testid="stSidebar"] div.stAlert:hover{
    transform:scale(1.02);
    transition:0.3s;
    cursor: pointer !important;
}

/* Selectbox shadow */
div[data-baseweb="select"]{
    transition:0.3s;
    cursor: pointer !important;
}

div[data-baseweb="select"]:hover{
    transform:translateY(-2px);
    cursor: pointer !important;
}

</style>
""", unsafe_allow_html=True)

st.title("Sales Prediction Dashboard")

st.sidebar.title("About")

metrics = joblib.load("../metrics.pkl")

st.sidebar.info(f"""
  Model : {metrics["Model"]}

  Dataset : Superstore Sales Dataset

  Target Variable : Sales

  Features : Customer, Product, Shipping and Order Details
  """)

st.markdown(f"""
### Project Description

This machine learning application predicts retail sales using the **best-performing regression model** selected automatically from multiple machine learning algorithms (Linear Regression, Decision Tree, Random Forest, Gradient Boosting, and XGBoost). The model was chosen based on its evaluation performance.

**Best Model:** {metrics["Model"]}

**Technologies Used:** Python • Streamlit • Scikit-learn • XGBoost • Pandas • Plotly
""")

ship_mode = st.selectbox(
    "Ship Mode",
    encoders["Ship Mode"].classes_
)

segment = st.selectbox(
    "Segment",
    encoders["Segment"].classes_
)

country = st.selectbox(
    "Country",
    encoders["Country"].classes_
)

city = st.selectbox(
    "City",
    encoders["City"].classes_
)

state = st.selectbox(
    "State",
    encoders["State"].classes_
)

postal = st.number_input("Postal Code",value=10001)

region = st.selectbox(
    "Region",
    encoders["Region"].classes_
)

category = st.selectbox(
    "Category",
    encoders["Category"].classes_
)

subcategory = st.selectbox(
    "Sub-Category",
    encoders["Sub-Category"].classes_
)

product = st.selectbox(
    "Product Name",
    encoders["Product Name"].classes_
)

quantity = st.slider("Quantity",1,20,2)

discount = st.slider("Discount",0.0,0.8,0.2)

year = st.selectbox("Order Year",[2014,2015,2016,2017])

month = st.slider("Order Month",1,12,6)

day = st.slider("Order Day",1,31,15)

shipping = st.slider("Shipping Days",0,15,4)

if st.button("Predict Sales"):

    data = pd.DataFrame({

        "Ship Mode":[encoders["Ship Mode"].transform([ship_mode])[0]],

        "Segment":[encoders["Segment"].transform([segment])[0]],

        "Country":[encoders["Country"].transform([country])[0]],

        "City":[encoders["City"].transform([city])[0]],

        "State":[encoders["State"].transform([state])[0]],

        "Postal Code":[postal],

        "Region":[encoders["Region"].transform([region])[0]],

        "Category":[encoders["Category"].transform([category])[0]],

        "Sub-Category":[encoders["Sub-Category"].transform([subcategory])[0]],

        "Product Name":[encoders["Product Name"].transform([product])[0]],

        "Quantity":[quantity],

        "Discount":[discount],

        "Order Year":[year],

        "Order Month":[month],

        "Order Day":[day],

        "Shipping Days":[shipping]

    })

    prediction = model.predict(data)[0]
    st.session_state.history.append({
    "Product": product,
    "Category": category,
    "Quantity": quantity,
    "Discount": discount,
    "Prediction": round(prediction, 2)
    })

    st.metric(
    label="Predicted Sales",
    value=f"${prediction:,.2f}"
    )

    if prediction < 200:
       st.warning("Low Expected Sales")
    elif prediction < 600:
       st.info("Moderate Expected Sales")
    else:
       st.success("High Expected Sales")

    st.session_state.setdefault("history", [])


    st.subheader("Prediction History")
    st.dataframe(pd.DataFrame(st.session_state.history))


    st.subheader("Prediction")
    st.metric(
    "Estimated Sales",
    f"${prediction:,.2f}",
    delta=None
    )

    history_df = pd.DataFrame(st.session_state.history)

    history_df["Prediction No"] = range(1, len(history_df)+1)

    fig = px.line(
    history_df.reset_index(),
    x="Prediction No",
    y="Prediction",
    markers=True,
    title="Prediction Trend"
)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("Clear History"):
      st.session_state.history = []

    if st.button("Reset Dashboard"):
      st.session_state.history=[]
      st.rerun()
    
    result = pd.DataFrame({

    "Ship Mode":[ship_mode],

    "Segment":[segment],

    "Country":[country],

    "City":[city],

    "State":[state],

    "Category":[category],

    "Sub-Category":[subcategory],

    "Product":[product],

    "Quantity":[quantity],

    "Discount":[discount],

    "Prediction":[prediction]

    })

    st.download_button(
        "Download Result",
        result.to_csv(index=False),
        file_name="Sales_Prediction_Result.csv"
    )

comparison = pd.read_csv("../model_comparison.csv")


st.subheader("Model Comparison")
st.dataframe(
    comparison.style.highlight_max(
        subset=["R2"],
        color="#90EE90"
    ).highlight_min(
        subset=["RMSE"],
        color="#90EE90"
    ).highlight_min(
        subset=["MAE"],
        color="#90EE90"
    ),
    use_container_width=True
)

st.markdown("---")

st.subheader("Model Information")

st.write(f"""
✔ Algorithm : {metrics["Model"]}

✔ Input Features : Customer, Product, Shipping and Order Information

✔ Output : Predicted Sales Amount
""")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Best Model", metrics["Model"])
col2.metric("R²", metrics["R2"])
col3.metric("MAE", metrics["MAE"])
col4.metric("RMSE", metrics["RMSE"])


metrics = joblib.load("../metrics.pkl")

if "history" not in st.session_state:
    st.session_state.history = []

importance = pd.read_csv("../feature_importance.csv")

st.subheader("Feature Importance")

fig = px.bar(
    importance,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Top Features Affecting Sales Prediction"
)

st.plotly_chart(fig,use_container_width=True)



st.markdown("---")
st.caption("Developed by Drishti Yadav\n")
st.caption("Machine Learning Sales Prediction Dashboard\n")
st.caption("Random Forest Regression | Streamlit | Python")
