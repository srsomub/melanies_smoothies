# Import python packages
import streamlit as st 
from snowflake.snowpark.functions import col 
import requests
import pandas as pd



cnx = st.connection("snowflake")
session = cnx.session()


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your **Custom Smoothie!**
    """
)
  

# Text box to insert name
name = st.text_input("Name on Smoothie", "") 

if name:
    st.write("Name on Smoothie will be: ",name)



# load data from your database
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Convert snowflake dataframe to Pandas dataframe so that we can use loc function and search for values of search_on in API using FRUIT_NAME
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df) # display 
st.stop()

# multiselect return list object
ingredients_list = st.multiselect(
            "Choose Five ingredients:",
             my_dataframe,
             max_selections=5    
            ) 


# Display list as string;
if ingredients_list:
    ingredients_string=''
    for i in ingredients_list:
        ingredients_string+= i + ' '

        st.subheader(i+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+i) # return JSON response by sending API request
        ftv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True) # convert JSON to dataframe and display it.

 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,"NAME_ON_ORDER")
            values ('""" + ingredients_string +"""', '"""+ name + """')""" 

    # Write to our database 
    insert_button = st.button("Submit Order")
    if insert_button:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon") # return JSON response
# st.text(fruityvice_response.json())




