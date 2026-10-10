from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__, template_folder='../frontend/templates')

# Yahan apni CSV file ka exact naam likhein (e.g., 'Garba_Event_Dataset.csv' ya jo bhi aapne rakha hai)
DATASET_PATH = 'Garba_Event_Dataset - Copy.csv'

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # CSV file read karna
    df = pd.read_csv(DATASET_PATH)

    # Agar user naya pass submit kare (Form Input)
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        contact_number = request.form['contact_number']
        pass_type = request.form['pass_type']
        event_date = request.form['event_date']
        price_inr = int(request.form['price_inr'])
        payment_status = request.form['payment_status']
        check_in_status = request.form['check_in_status']

        # Auto-generate Pass ID
        new_id_num = len(df) + 101
        pass_id = f"GRB-2026-{new_id_num}"

        # Naya row dataframe me add karna
        new_row = {
            'Pass_ID': pass_id,
            'Guest_Name': guest_name,
            'Contact_Number': int(contact_number),
            'Pass_Type': pass_type,
            'Event_Date': event_date,
            'Price_INR': price_inr,
            'Payment_Status': payment_status,
            'Check_In_Status': check_in_status
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # CSV file me save karna
        df.to_csv(DATASET_PATH, index=False)
        return redirect(url_for('dashboard'))

    # Dashboard Metrics Calculations
    total_passes = int(df['Pass_ID'].count())
    total_revenue = int(df['Price_INR'].sum())
    paid_count = int(df[df['Payment_Status'] == 'Paid']['Pass_ID'].count())
    checked_in_count = int(df[df['Check_In_Status'] == 'Checked In']['Pass_ID'].count())
    
    # Visualizations / Chart Data
    pass_type_counts = df['Pass_Type'].value_counts().to_dict()
    payment_status_counts = df['Payment_Status'].value_counts().to_dict()
    revenue_by_date = df.groupby('Event_Date')['Price_INR'].sum().to_dict()
    
    return render_template('index.html', 
                           total_passes=total_passes,
                           total_revenue=total_revenue,
                           paid_count=paid_count,
                           checked_in_count=checked_in_count,
                           pass_type_counts=pass_type_counts,
                           payment_status_counts=payment_status_counts,
                           revenue_by_date=revenue_by_date,
                           passes=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)