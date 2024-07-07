import numpy as np 
import pandas as pd
import plotly.express as px
import warnings

import plotly.graph_objects as go 
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

def clear_html_file(file_path):
    with open(file_path, 'w') as file:
        file.write(f'<head><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"></head><h1><b>  Automated Dashboard Reports    </h1></b>')
    return

def calculateTableValues(org_name,response_time_In_min, total_amounts):
    org_name_final=[]
    response_time_In_min_final=[]
    total_amounts_final=[]

    org_name_final.append(org_name)
    response_time_In_min_final.append(response_time_In_min)
    total_amounts_final.append(total_amounts)

    return [org_name_final, response_time_In_min_final, total_amounts_final]


def addfigures(interactive_plot, fig):
    # Read the existing HTML file
    with open(interactive_plot, 'r', encoding='utf-8') as f:
        existing_html = f.read()

    # Create the HTML code for the figures
    figures_html = []
    for i in range(len(fig)):
        figures_html.append(fig[i].to_html(
            full_html=False, include_plotlyjs="cdn"))

    # Create the div containers for each figure
    figures_divs = ''.join(
        [f'<div style="flex: 1;">{html}</div>' for html in figures_html])

    # Combine the figures divs with the existing HTML content
    updated_html = f'''{existing_html}\n<div style="display: flex;">{figures_divs}</div>
                        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                        <link rel="stylesheet" href="https://cdn.plot.ly/plotly-latest.min.css">'''

    # Write the updated HTML content back to the file
    with open(interactive_plot, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    return



def table11(org_name,response_time_In_min, total_amounts):
    with open(interactive_plot, 'a', encoding='utf-8') as file:
        file.write('''<html>
        <head>
            <style>
                table {
                    border-collapse: collapse;
                    width: 40%;
                }

                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                .table-heading {
                    border: none;
                }
                .blue-bg {
                    color: blue; /* Add white text color for better visibility */
                }
            </style>
            </head>
            <body>
            <table class='table table-striped table-hover'>
                <tr>
                    <th colspan='20' class='table-heading'><center><h1>Response Time & Invoice Analysis Table</h1></center></th>
                </tr>
                <tr>
                    <th><center>Serial Number</center></th>
                    <th><center>Organisation </center></th>
                    <th><center>Response Time(Min) </center></th>
                    <th><center>Total Invoice Amount</center></th>
           </tr>''')
        table_values1 = calculateTableValues(org_name,response_time_In_min, total_amounts)
        org_name_final = table_values1[0]
        response_time_In_min_final = table_values1[1]
        total_amounts_final = table_values1[2]
        

        
        for index in range(1):
            for j in range(len(org_name_final[index])):
                if j == 0:
                    row_span = len(org_name_final[index])
                    file.write(f'''
                        <tr>
                            <td><center> {j+1}</center></td>
                            <td><center>{org_name_final[index][j]}</center></td>
                            <td><center>{response_time_In_min_final[index][j]}</center></td>
                            <td><center>{total_amounts_final[index][j]}</center></td>
                            
                            
                        </tr>''')
                else:
                    file.write(f'''
                        <tr>
                            <td><center> {j+1}</center></td>
                            <td><center>{org_name_final[index][j]}</center></td>
                            <td><center>{response_time_In_min_final[index][j]}</center></td>
                            <td><center>{total_amounts_final[index][j]}</center></td>
                        </tr>''')
    with open(interactive_plot, 'a') as file:
        file.write('''
                </table>''')
    return 





def plot_bar_chart(fig, x, y, title, x_label, y_label):
    fig.add_trace(go.Bar(x=x, y=y))
    
    fig.update_layout(
        title={
            'text': title,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=500,
        width=700
    )


def plot_grouped_bar_chart(df, x, y, color, title, x_label, y_label, height=800, width=1200, bargroupgap=0.0):
    grouped_data = df.groupby([x, color]).size().reset_index(name=y)
    fig = px.bar(grouped_data, x=x, y=y, color=color, barmode='group',
                 title=title, labels={y: y_label, x: x_label})
    
    fig.update_layout(
        height=height,
        width=width,
        bargroupgap=bargroupgap
    )
    
    return fig





def plot_pie_chart(fig, df, names_column, title, height=500, width=500):
    """
    Plots a pie chart using the given DataFrame and fig object.
    
    Parameters:
    - fig: Plotly figure object.
    - df: DataFrame containing the data to plot.
    - names_column: Column name for the pie chart categories.
    - title: Title of the plot.
    - height: Height of the plot (default: 500).
    - width: Width of the plot (default: 500).
    """
    fig.update_traces(px.pie(df, names=names_column, title=title).data[0])
    
    # Adjust the height and width of the plot
    fig.update_layout(height=height, width=width)








def analysis_script(sheets_dict, interactive_plot):


  master_df = sheets_dict['Master Sheet']

  fig6=plot_grouped_bar_chart(
    df=master_df,
    x='Organisation Name ',
    y='Count',
    color='Type of Ambulance',
    title='Type of Ambulance by Organisation',
    x_label='Organisation',
    y_label='Number of Ambulances',
    height=700,
    width=1100
  )
  # fig6.show()

  fig4 = px.pie(master_df, names="Covid/ Non Covid", title="Covid vs. Non-Covid Cases")
  fig4.update_layout(height=600, width=600)
  # fig4.show()

  fig5 = px.bar(master_df, x="Ambulance Status", title="Ambulance Status")
  fig5.update_layout(height=500, width=600)
  # fig5.show()



  org_name =[]
  response_time_In_min =[]
  total_amounts = []

  df_hsbc = sheets_dict['HSBC']

  total_amounts.append(df_hsbc['Total Amount'].sum())
  df_hsbc['Response Time (Min)'] = pd.to_numeric(df_hsbc['Response Time (Min)'], errors='coerce')
  df_hsbc = df_hsbc.dropna(subset=['Response Time (Min)'])

  org_name.append('HSBC')
  response_time_In_min.append(round(df_hsbc['Response Time (Min)'].mean(),2))


  df_dhl = sheets_dict['DHL']
  total_amounts.append(df_dhl['Total Amount'].sum())
  df_dhl['Response Time (Min)'] = pd.to_numeric(df_dhl['Response Time (Min)'], errors='coerce')
  df_dhl = df_dhl.dropna(subset=['Response Time (Min)'])
  org_name.append('DHL')
  response_time_In_min.append(df_dhl['Response Time (Min)'].mean())
  




  # Praj Industries


  df_praj = sheets_dict['Praj Industries']
  total_amounts.append(df_praj['Total Amount'].sum())
  df_praj['Response Time (Min)'] = pd.to_numeric(df_praj['Response Time (Min)'], errors='coerce')
  df_praj = df_praj.dropna(subset=['Response Time (Min)'])

  org_name.append('Praj Industries')
  response_time_In_min.append(df_praj['Response Time (Min)'].mean())
  



  # SEIIRIS

  df_seiiris = sheets_dict['SEIIRIS']
  total_amounts.append(df_seiiris['Total Amount'].sum())
  
  df_seiiris['Response Time (Min)'] = pd.to_numeric(df_seiiris['Response Time (Min)'], errors='coerce')
  df_seiiris = df_seiiris.dropna(subset=['Response Time (Min)'])

  org_name.append('SEIIRIS')
  response_time_In_min.append(df_seiiris['Response Time (Min)'].mean())
  

  
  #Khopoli

  df_khopoli = sheets_dict['Khopoli']
  total_amounts.append(df_khopoli['Total Amount'].sum())
  df_khopoli['Response Time (Min)'] = pd.to_numeric(df_khopoli['Response Time (Min)'], errors='coerce')
  df_khopoli = df_khopoli.dropna(subset=['Response Time (Min)'])


  org_name.append('Khopoli')
  response_time_In_min.append(df_khopoli['Response Time (Min)'].mean())

  #NPCI


  df_npci = sheets_dict['NPCI']
  total_amounts.append(df_npci['Total Amount'].sum())
  df_npci['Response Time (Min)'] = pd.to_numeric(df_npci['Response Time (Min)'], errors='coerce')
  df_npci = df_npci.dropna(subset=['Response Time (Min)'])


  org_name.append('NPCI')
  response_time_In_min.append(df_npci['Response Time (Min)'].mean())

  #Artemis

  df_artemis = sheets_dict['Artemis']
  total_amounts.append(df_artemis['Total Amount'].sum())
  df_artemis['Response Time (Min)'] = pd.to_numeric(df_artemis['Response Time (Min)'], errors='coerce')
  df_artemis = df_artemis.dropna(subset=['Response Time (Min)'])


  org_name.append('Artemis')
  response_time_In_min.append(df_artemis['Response Time (Min)'].mean())



  #Zyla Health

  df_zyla_health = sheets_dict['Zyla Health']
  total_amounts.append(df_zyla_health['Invoice Amount'].sum())
  df_zyla_health['Response Time (In Mins.)'] = pd.to_numeric(df_zyla_health['Response Time (In Mins.)'], errors='coerce')
  df_zyla_health = df_zyla_health.dropna(subset=['Response Time (In Mins.)'])


  org_name.append('Zyla Health')
  response_time_In_min.append(df_zyla_health['Response Time (In Mins.)'].mean())
  #Rakuten

  df_zyla_rakuten = sheets_dict['Rakuten']
  total_amounts.append(df_zyla_rakuten['Invoice Amount'].sum())
  df_zyla_rakuten['Response Time (In Mins.)'] = pd.to_numeric(df_zyla_rakuten['Response Time (In Mins.)'], errors='coerce')
  df_zyla_rakuten = df_zyla_rakuten.dropna(subset=['Response Time (In Mins.)'])

  org_name.append('Rakuten')
  response_time_In_min.append(df_zyla_rakuten['Response Time (In Mins.)'].mean())


  print(f'org_name : {org_name} ')

  print(f'response_time_In_min : {response_time_In_min}')

  print(f'Total Amounts : {total_amounts}')

  fig1 = go.Figure()

  plot_bar_chart(fig1, org_name, response_time_In_min, f'Response Time (Min) vs Organisation ', f'Organisation Name',f'Response_Time(Min)')
  # fig1.show()

  fig2 = go.Figure()

  plot_bar_chart(fig2, org_name, total_amounts, f'Invoice Amount vs Organisation ', f'Organisation Name',f'Invoice Amount')
  # fig2.show()
  print('\033[91m                    Creating HTML file        \x1b[0m\n')


  figures =[]
  temp1=[]
  temp2 =[]
  temp3=[]
  temp4 =[]
  # temp5=[]

  temp1.append(fig1)
  temp1.append(fig2)
  temp2.append(fig4)
  temp3.append(fig5)
  temp4.append(fig6)

  figures.append(temp1)
  figures.append(temp2)
  figures.append(temp3)
  figures.append(temp4)





  clear_html_file(interactive_plot)
  for i in range(len(figures)):
      if (i == 0):
          with open(interactive_plot, 'a') as file:
              file.write('''<h1><center>Organisation Performance: Response Time & Invoice Analysis </center></h1>''')
          addfigures(interactive_plot, figures[i])
          table11(org_name,response_time_In_min, total_amounts)
      elif (i == 1):
          with open(interactive_plot, 'a') as file:
              file.write(
                  '''<br><br><br><br><h1><center> Covid-19 vs Non-Covid Case Distribution </center></h1>''')
          addfigures(interactive_plot, figures[i])
      elif (i == 2):
          with open(interactive_plot, 'a') as file:
              file.write(
                  '''<br><br><br><br><h1><center> Ambulance Status Overview </center></h1>''')
          addfigures(interactive_plot, figures[i])
      elif (i == 3):
          with open(interactive_plot, 'a') as file:
              file.write('''<h1><center> Distribution of Ambulance Types Across Organizations  </center></h1>''')
          addfigures(interactive_plot, figures[i])
  #     elif (i == 4):
  #         with open(interactive_plot, 'a') as file:
  #             file.write('''<br><br><br><br><h1><center> Comparing Energy Vs Time </center></h1>''')
  #         addfigures(interactive_plot, figures[i])
  #     elif (i == 5):
  #         with open(interactive_plot, 'a') as file:
  #             file.write(
  #                 '''<br><br><br><br><h1><center> Current-Voltage-Power-Temprature Vs Time </center></h1>''')
  #         addfigures(interactive_plot, figures[i])
  #     elif (i == 6):
  #         with open(interactive_plot, 'a') as file:
  #             file.write(
  #                 '''<br><br><br><br><h1><center> Comparison </center></h1>''')
  #         addfigures(interactive_plot, figures[i])
  #     else:
  #         print('Error')
  # table2_return_value = table2(area, no_of_raw_data_files, df, interactive_plot,df1)
  
  print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\033[94m                            Done :)\x1b[0m\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
  # EditableHTML(interactive_plot)
  return 






excel_file = '/Users/chamanlal/Desktop/Projects/Corporates MIS Report.xlsx'
interactive_plot ='generated_report.html'

sheets_dict = pd.read_excel(excel_file, sheet_name=None)
df_master_sheet = sheets_dict['Master Sheet']

analysis_script(sheets_dict, interactive_plot)



# df_HSBC = sheets_dict['HSBC']
# df_HSBC['Response Time (Min)'] = pd.to_numeric(df_HSBC['Response Time (Min)'], errors='coerce')
# df_HSBC = df_HSBC.dropna(subset=['Response Time (Min)'])
# response_time_org_HSBC = df_HSBC.groupby('Organisation Name')['Response Time (Min)'].mean().reset_index()
# fig = px.bar(response_time_org_HSBC, x='Organisation Name', y='Response Time (Min)', title='Average Response Time by Organisation')
# fig.write_html(output_file)




