import os
import streamlit as st
import pandas as pd
x = []
from src.db_ops import show_data, edit_data, delete_data

def insert_parameter(cursor,db):
    if 'flag' not in st.session_state:
        st.session_state.flag = 1
    

    global x
    st.sidebar.header('add or delete column')
    task = st.sidebar.selectbox('--------',
                                    ('Add column', 
                                     'Delete column'))

    if(task == "Add column"):
        # Streamlit Form
        st.title('Add Column to Database')

        # Form to get new column details
        new_column_name = st.text_input('Enter the new column name:')
        new_column_type = st.text_input('Enter the data type for the new column (e.g.,longtext, TEXT, INTEGER, double, VARCHAR(n)):')
        # x.append(new_column_name)
        # for i, element in enumerate(x, start=1):
        #     st.write(f" {element}")

        if st.button('Add Column'):
            # x = (new_column_name)
            x.append(new_column_name)
            for i, element in enumerate(x, start=1):
                st.write(f" {element}")
            
            
            # Use the ALTER TABLE statement to add the new column
            alter_query = f'''ALTER TABLE expense ADD COLUMN {new_column_name} {new_column_type}'''
                            ##AFTER document"
            # ALTER TABLE student_information ADD COLUMN new_column_name longtext;

            try:
                cursor.execute(alter_query)
                db.commit()
                st.success(f"Column '{new_column_name}' added successfully.")
                st.balloons()
            except:
                st.error("Error adding column")
                st.error()
    if(task == "Delete column"):
        st.title('Delete Column to Database')
        st.header('button for columns')
        cursor.execute('''SHOW COLUMNS FROM expense FROM ExpenseDB''')
        
        columns = [column[0] for column in cursor.fetchall()]
        
        if st.button('show Columns'):
            try:
                st.title('Columns for Table: expense')
                for column in columns:
                    st.write(column)
                    #st.success(f"Column '{new_column_name}' added successfully.")
                    st.balloons()
            except:
                st.error("Error adding column")

        # Streamlit Form
        st.title('Delete Column from Database')

        # Form to get the column name to be deleted
        column_to_delete = st.text_input('Enter the column name to be deleted:')

        if st.button('Delete Column'):
            # Use the ALTER TABLE statement to delete the column
            alter_query = f"ALTER TABLE expense DROP COLUMN {column_to_delete};"

            try:
                cursor.execute(alter_query)
                db.commit()
                st.success(f"Column '{column_to_delete}' deleted successfully.")
            except:
                st.error("Error deleting column: ")


def save_expense(cursor, db):
    if 'flag' not in st.session_state:
        st.session_state.flag = 1
    global x
    st.header('💸 Expense Entry')
    
    with st.form(key='expense_submit_form', clear_on_submit=False):
        expense_category = ['Shopping', 'Snacks', 'Mobile Recharge', 
                            'Online Course', 'Subscription']

        expense_date = st.date_input('Expense Date*')
        category = st.selectbox('Expense Category*', expense_category)
        amount = st.text_input('Amount*')
        notes = st.text_area('Notes')
        if len(x) > 0:
            for i, element in enumerate(x, start=1):
                st.text_input(f" {element}")
                # st.form_submit_button("input")
        #     st.form_submit_button(label='sunbk')
        # x = st.text_area(f'{x}')
        # st.form_submit_button(label='sunbk')
        document_upload = st.file_uploader('Upload Document', 
                                           type=['txt','pdf', 
                                                 'jpg', 'png', 'jpeg'], 
                                            accept_multiple_files=True)
        # expense_reason = st.text_area('Expemse_reason')
        # Streamlit Form
        
        if st.form_submit_button(label='Submit'):
            if not(expense_date and category and amount):
                st.write('Please fill all the * fields')
            else:
                st.session_state.flag = 1
                # st.success('Data Submitted Successfully')


    if st.session_state.flag:
        # st.write(final_parameter_calculation)

        with st.form(key='final', clear_on_submit=True):
             # st.write(final_parameter_calculation)

            if st.form_submit_button('Are you Sure?'):
                # st.write(final_parameter_calculation)
                st.session_state.flag = 0
                # insert data into expense table
                
                # st.write(document_upload.read())
                # st.write(document_upload.name)
                # st.write(document_upload.getvalue())
                # file = open(document_upload.read(),'rb')
                all_documents = []
                for file in document_upload:
                    st.write(file.name)
                    # st.write(file.getvalue())
                    # st.write(file.read())
                    if file is not None:
                        # Get the file name and extract the extension
                        file_name = file.name
                        # st.write(file_name)
                        file_extension = os.path.splitext(file_name)[1]
                        dir_name = "./documents/expenses"
                        if not os.path.isdir(dir_name):
                            os.makedirs(dir_name)

                        file_url = dir_name + '/' + file_name
                        # file_url = dir_name + file_name
                        all_documents.append(file_url)

                        # Save the file in its original format
                        with open(file_url, "wb") as f:
                            f.write(file.read())
                        st.success("File has been successfully saved.")
                        # for i, element in enumerate(x, start=1):
                            # st.text_input(f" {element}")


                query = '''Insert into expense (expense_date, category, amount, 
                                                notes, documents) 
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                values = (expense_date, category, amount, notes, str(all_documents))
                # st.write(query, values)
                cursor.execute(query, values)
                db.commit()
                st.success("Expense Record Inserted Successfully!")
                st.balloons()

            else:
                st.write("Click above button If you are Sure")
    else:
        st.warning("Please fill up above form")

    df = pd.read_sql('''SELECT id, expense_date, category, 
                        amount, notes, documents FROM expense''', con=db)
    
    # st.dataframe(df)

    # select the columns you want the users to see
    columns = ['id',
               'expense_date',
                'category',
                'amount',
                'notes']   
    # st.dataframe(df)
    show_data(df, columns)
    edit_data(cursor, db, df, columns, 'Edit Expenses', 'expense')
    delete_data(cursor, db, df, columns, 'Delete Expenses', 'expense')


