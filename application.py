from flask import Flask, render_template, request
import pandas as pd
import datetime

df=pd.read_csv('C:\\Users\\Gordon\\Downloads\\year-worth-of-preds.csv')
# df['Date']=pd.to_datetime(df['ds']).dt.date
# df['Time']=pd.to_datetime(df['ds']).dt.time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  # estimation
def predict():
    index_list = df['Date'].unique()

    chosen_option = None

    if request.method == 'POST':
        default_value = 'None Selected'
        chosen_option = request.form.get(
            key='select_Ride',
            default=default_value,
        )
    # filtering data based on 'chosen option
    df2=df[df['Date'] ==chosen_option]

    df3 = df2.groupby(['Hour', 'ride']).agg({'yhat': ['mean']})
    df3 = df3.reset_index()
    df3.columns = ['Hour', 'Ride', 'Wait']
    df3['Rank'] = df3.groupby('Ride')['Hour'].rank(ascending=True)

    df4 = df3[df3['Rank'] < 4]
    df4 = df4.sort_values(by=['Ride', 'Rank', 'Hour'], ascending=True)

    return render_template(
        template_name_or_list='index.html',
        index_list=index_list,
        # prediction=prediction,
        chosen_option=chosen_option,
        tables=[df4.to_html(classes='data')],
        titles=['Time','Ride','Estimate Wait Time','Priority']#df4.columns.values
    )



if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(debug=True)