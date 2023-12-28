import matplotlib.pyplot as plt
import calendar
import pandas as pd
import numpy as np

def categorize_sum(filename, month, is_visa):
    
    '''
    '''
    
    df = pd.read_csv(filename)
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
    
    def __init__(self, output_file, month, is_visa=True):
        
        df = pd.read_csv(output_file)
        self.attributes = set(df['Category'])
        self.filename = output_file
        self.month = month
        self.month_name = calendar.month_name[month]
        self.table = df
        self.is_visa = is_visa
                
    def visualize(self):

        df = pd.read_csv(self.filename)
        lk = df[df['Expenditure'] < 0].copy()
            
            
        lk['Expenditure'] = abs(lk['Expenditure'])
            
        plt.pie(lk['Expenditure'], labels=lk['Category'])
        plt.title(self.month_name)
        plt.show()
        
    def compare(self, other):
        ''''''
              
        common_attributes = list(self.attributes.intersection(other.attributes))
        Inter_transfer_string = 'Inter-Transfer'
        if Inter_transfer_string in common_attributes:
            common_attributes.remove(Inter_transfer_string)
        
        
        #category = []
        #for attribute in common_attributes:
        #    category.append(f'{self.month_name} {attribute}')
        #    category.append(f'{other.month_name} {attribute}')
       
        values_oct = []
        values_nov = []
        for attribute in common_attributes:
            ind1 = self.table.index[self.table['Category'] == attribute].item()
            ind2 = other.table.index[other.table['Category'] == attribute].item()
            
            values_oct.append(self.table.at[ind1, 'Expenditure'])
            values_nov.append(other.table.at[ind2, 'Expenditure']) 
        
        
        barwidth =0.25
        
        
        br1 = np.arange(len(values_nov))
        br2 = []
        for x in br1:
            br2.append(x+barwidth)
            
            
        
            
                       
        plt.bar(br1, values_oct, color='r', width=barwidth, label=self.month_name)
        plt.bar(br2, values_nov, color='b', width=barwidth, label=other.month_name)
        plt.ylabel = 'CAD$'
        plt.xticks([r+barwidth for r in range(len(values_nov))], common_attributes)
        plt.show()
            
         
            
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
def compare_one_att(file1, file2):
    # I would make bar charts
    # Bar charts would be made according to certain attribute which would be common between the two files.
    
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    file1_categories = set(df1['Category'])
    file2_categories = set(df2['Category'])
    
    common_attributes = (file1_categories.intersection(file2_categories))
    
    required_attribute = input(f'Options: {common_attributes}\n')
    
    ind1 = int(df1.index[df1['Category'] == required_attribute])
    ind2 = int(df2.index[df2['Category'] == required_attribute])
        
    categories = ['October', 'November']
    values = [df1.at[ind1, 'Expenditure'], df2.at[ind2, 'Expenditure']]
    print(values)
    
    plt.bar(categories, values)
    plt.show()
    
    
    
