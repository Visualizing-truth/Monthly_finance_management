import matplotlib.pyplot as plt
import calendar
import pandas as pd
import numpy as np

def categorize_sum(filename, month, is_visa):
    '''
        (str, int, bool)-> pandas<dataframe>
        Takes a cumulative bank statement csv filename, required month (as integer) and
        whether the analysis is to be done overall(except credit card expenses) or whether
        we want analyse credit card spending.
        It then asks for input from user for each single expense in the bank statement.
        The user input is used to categorize the expenses and then sum the expenses
        according to that categorization.
        PS this is more suited to my account and how I spend my money (however could be tweaked),
        since I use my credit card for most small scale expenses.
    '''
    df = pd.read_csv(filename)
    
    # Defining global variables related to
    VISA_COL = 'Visa'
    EXPENSE_DESC = 'Category'
    AMOUNT = 'Expenditure'
        
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
        
    dk = df[df['Transaction Date'].dt.month == month].copy()
    
    if not is_visa:
        lk = dk[dk['Account Type'] != VISA_COL].copy()
    else:
        lk = dk[dk['Account Type'] == VISA_COL].copy()
            
    # Categorizing
    categories = [input(row.to_string() + '\n') for index, row in lk.iterrows()]
        
    # Making a new category column
    lk[EXPENSE_DESC] = categories
    unique_categories = set(categories)
        
    # Summing for each category
    Sum_category = [lk.loc[lk[EXPENSE_DESC] == category, 'CAD$'].sum() for category in unique_categories]
    dict1 = {EXPENSE_DESC: list(unique_categories), AMOUNT: Sum_category}
        
    # Creating a new table
    category_table = pd.DataFrame(dict1)
    month_name = calendar.month_name[month]
    
    # Creating an output file
    if is_visa:
        category_table.to_csv(filename[:-4] + '_Visa' +'_'+ month_name, index=False)
    else:
        category_table.to_csv(filename[:-4] + '_Overall_'+ month_name, index=False)
    
    return category_table

class Expense:
    '''
        This class can only be used after one has run the categorize_sum() function
        for their balance sheet.
        ATTRIBUTES:
        1. attributes (set)
        2. filename (str)
        3. month (int)
        4. month_name (str)
        5. table (pandas<dataframe>)
        6. is_visa (bool)
    '''
    
    def __init__(self, output_file, month, is_visa=True):
        
        '''
            Takes as input an output_file (which would be generally acquired
            after running the categorize_sum function on required balance sheet),
            required month integer and if the output file is for credit card expenses
            or not.
            Convention: True if credit expenses, False if otherwise.
            Assigns the input for the initializer to the required attributes.
        '''
        df = pd.read_csv(output_file)
        self.attributes = set(df['Category'])
        self.filename = output_file
        self.month = month
        self.month_name = calendar.month_name[month]
        self.table = df
        self.is_visa = is_visa
                
    def visualize(self):
        ''' 
            () -> NoneType
            Helps visualize individual expense using a pie chart
        '''

        df = pd.read_csv(self.filename)
        lk = df[df['Expenditure'] < 0].copy()
            
            
        lk['Expenditure'] = abs(lk['Expenditure'])
            
        plt.pie(lk['Expenditure'], labels=lk['Category'])
        plt.title(self.month_name)
        plt.show()
        
    def compare(self, other):
        '''
            (Expense_obj)-> NoneType
            Helps visualize the comparison in spending and income for two different
            months using a bar chart.
        '''
              
        common_attributes = list(self.attributes.intersection(other.attributes))
        Inter_transfer_string = 'Inter-Transfer'
        if Inter_transfer_string in common_attributes:
            common_attributes.remove(Inter_transfer_string)
       
        values_oct = []
        values_nov = []
        for attribute in common_attributes:
            ind1 = self.table.index[self.table['Category'] == attribute].item()
            ind2 = other.table.index[other.table['Category'] == attribute].item()
            
            values_oct.append(self.table.at[ind1, 'Expenditure'])
            values_nov.append(other.table.at[ind2, 'Expenditure']) 
              
        barwidth =0.25
    
        br1 = np.arange(len(values_nov))
        br2 = [x+barwidth for x in br1]
              
        plt.bar(br1, values_oct, color='r', width=barwidth, label=self.month_name)
        plt.bar(br2, values_nov, color='b', width=barwidth, label=other.month_name)
        plt.ylabel = 'CAD$'
        plt.xticks([r+barwidth for r in range(len(values_nov))], common_attributes)
        plt.legend()
        plt.show()
        
    def surplus(self):
        '''
            This should only work for when is_visa is False.
        '''
        if not(self.is_visa):
            ind1 = self.table.index[self.table['Category']== 'Expense'].item()
            ind2 = self.table.index[self.table['Category']== 'Income'].item()
            
      
            exp = round(self.table.at[ind1, 'Expenditure'])
            income = round(self.table.at[ind2, 'Expenditure'])
            
            surplus = round(exp + income)
            
            print(f'Expense: {exp}\nIncome: {income}\nSurplus: {surplus}')
        else:
            raise AssertionError('Cannot calculate surplus for visa.')
    