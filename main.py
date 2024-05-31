import streamlit as st
import pandas as pd

# Initialize the data
metrics = ["Contract Miles", "Drivers", "Tractors", "Trips", "Units", "WPL Miles"]
regions = ["East", "Midwest", "West", "TMX"]

# Streamlit App
st.set_page_config(page_title='LEER Monthly Data Entry Portal')
st.title('LEER Monthly Data Entry Portal')

# Select year and month
years = [str(year) for year in range(2020, 2026)]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_map = {month: f'{i+1:02d}' for i, month in enumerate(months)}

leer_logo_url = "leer.png"
st.sidebar.image(leer_logo_url, width =100)

selected_year = st.sidebar.selectbox('Select Year', years)
selected_month = st.sidebar.selectbox('Select Month', months)
selected_month_number = month_map[selected_month]
period = f"{selected_year}{selected_month_number}"


# Initialize or load data
csv_path = 'data.csv'

def load_data():
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Period', 'Metric', 'Region', 'Value'])

df = load_data()

# Filter data based on the selected month and year
filtered_data = df[df['Period'] == int(period)]

if filtered_data.empty:
    # Create a DataFrame for new data entry
    pivot_data = pd.DataFrame(index=metrics, columns=regions, data=None)
else:
    # Pivot existing data
    pivot_data = filtered_data.pivot(index='Metric', columns='Region', values='Value').reindex(index=metrics, columns=regions).fillna(0)

st.write(f"Enter data for {selected_month} {selected_year}")

# Use st.data_editor to create a table-like input form
edited_data = st.data_editor(pivot_data.reset_index(), use_container_width=True)

def validate_data(df):
    if df.isnull().values.any(): #or not df.applymap(lambda x: isinstance(x, (int, float))).values.all():
        return False
    return True

if st.button('Submit'):
    if not validate_data(edited_data):
        st.error("Please fill all cells with numeric values.")
    else:
        # Add the "Metric" column to the edited_data DataFrame
        edited_data['Metric'] = metrics
        
        # Transform the pivoted data back to the original long format
        melted_data = pd.melt(edited_data, id_vars=['Metric'], value_vars=regions, var_name='Region', value_name='Value')
        melted_data['Period'] = int(period)
        
        # Remove existing entries for the selected period
        df = df[df['Period'] != int(period)]
        
        # Append the edited data
        df = pd.concat([df, melted_data], ignore_index=True)
        
        # Save the updated DataFrame to the CSV file
        df.to_csv(csv_path, index=False)
        
        st.success(f"Data for {selected_month} {selected_year} has been updated.")
        st.rerun()  # Rerun to refresh the data


# Show updated DataFrame with a larger container width
st.write("Updated Data:")
st.dataframe(df, use_container_width=True)

st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("    ")
st.sidebar.markdown("---")
jb_logo_url = "JB_Poindexter_Logo.jpg"
st.sidebar.image(jb_logo_url, use_column_width=True)
