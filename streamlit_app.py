# Import python packages
import streamlit as st


from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    f"""Choose the fruits you want!!
    """)



name_on_order = st.text_input("Name on the Smootie")
st.write("Name on the Smootie", name_on_order)
cnx=st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)



ingredients = st.multiselect(
    "Choose Upto 5 ingrediants"
    ,my_dataframe,max_selections=5)
if ingredients:
    
    ingrediants_string=''
    for fruit in ingredients:
        ingrediants_string+=fruit+' '
    st.write(ingrediants_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingrediants_string + """','""" + name_on_order + """')"""
    time_to_insert=st.button('Submit Button')
    if time_to_insert:

    #st.write(my_insert_stmt)
    #if ingrediants_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
