import streamlit as st
from PIL import Image
import regex as re
#import numpy as np
#import pandas as pd
import torch
import spacy


# model loading
model = torch.load('bert_model_cpu_ep3_0.79e4_bat32.pth', map_location='cpu')
nlp = spacy.load('fr_core_news_md')

# Defining two vocabs
comparison_operator_vocab = {
    "égal": " = "                 ,  "moins": " < "                 , "plus d'une":" > 1 "         , "n'ont pas Android":" != " ,
    "plus de": " > "              ,  "plus": " > "                  , "avant": " < "               , "concernés par": " "       ,
    "après": " > "                ,  "atteint": " = "               , "inférieur": " < "           , "supérieure": " > "        ,
    "supérieur ou égal": " >= "   ,  "supérieure ou égale": " >= "  , "est": " = "                 , "n'ont pas": " != "        ,
    "en": " = "                   ,  "au moins": " < "              , "dehors": " != "             , "inférieure": " < "        ,
    "situées": " = "              ,  "ont":" = "                    , "supérieur":" > "            , "inscrits": " = "          ,
    "nommée": " = "               ,  "dessous de":" < "             , "ou après": " > "            , "de": " = "                ,
    "n'a pas": " != "             ,  "inférieur ou égal": "<= "     , "ne sont pas": " != "        , "ou plus":" > "            , 
    "d'au plus": " > "            ,  "d'au moins": " < "            , "pas": " != "                , "n'est pas": " != "        ,
    "n'ont pas": " != "           ,  "vers": " = "                  , "pas les": " != "            , "supérieure à": " > "      ,
    }

aggregate_function_vocab = {
    'total': 'COUNT'         ,  'totaux': 'COUNT'       ,  'maximale': 'MAX'        , 'maximales': 'MAX'     ,
    'minimal': 'MIN'         ,  'moyen,':'AVG'          ,  'plus élevé': 'MAX'      , 'plus bas': 'MIN'      ,
    'nombre total': 'COUNT'  ,  'maximaux': 'MAX'       ,  'totale': 'COUNT'        , 'totales': 'COUNT'     ,
    'tous': 'COUNT'          ,  'moyenne,': 'AVG'       ,  'maximales': 'MAX'       , 'Combien': 'COUNT'     ,
    'moins de': 'MIN'        ,  'plus élevés': 'MAX'    ,  'montants': 'COUNT'      , 'moyenne': 'AVG'       ,
    'minimale': 'MIN'        ,  'minimales': 'MIN'      ,  'minimale': 'MIN'        , 'Compter': 'COUNT'     ,
    'plus grands': 'MAX'     ,  'plus élevé': 'MAX'     ,  'maximum': 'max'         , 'plus petits': 'MIN'   ,
    'nombres' : 'COUNT'      ,  'moyen': 'AVG'          ,  'moyens' : 'AVG'         , 'minimum': ' MIN'      ,
    'plus haute': 'MAX'      ,  'combien': 'COUNT'      ,  'somme': 'SUM'           , 'moyenne': 'AVG'       ,
    'moyens': 'AVG'          ,  'minimum': 'MIN'        ,  'le nombre': 'COUNT'     , 'nombre moyen': 'AVG'  ,
    'moyennes': 'AVG'        ,  'maximum': 'MAX'        ,  'maximal': 'MAX'         , 'nombre': 'COUNT'      ,
    'moyennes': 'AVG'        ,  'somme moyenne': 'AVG'  ,  'les plus': 'MAX'        , 'maximale': 'MAX'      ,
    'minimales': 'MIN'       ,  'Comptez': 'COUNT'      ,  'nombre maximum': 'MAX'  , 'nombre': 'COUNT'     ,
    'max' : 'MAX'            , 'min' : 'MIN'            ,  'total' : 'SUM'          
    } 


def clean(s): 
  #######################################################
  # This function take a string str remove punctuations #
  #######################################################
  regex = r"[!\"#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~]"
  res = re.sub(regex, " ", s)
  return res.strip()

# Lemmatization
def extract_lemma(w):
    tok = nlp(w)
    return str(tok[-1].lemma_)

# Create a function to use the model to make predictions
def get_sql(prediction):
  cols_name = []
  table_name = ''
  aggregate_fct = []
  aggregate_fct_attr = []
  comparison_attr = ''
  comparison_word = ''
  comparison_operator = ''
  value = ''
  group_by_flag = ''

  for i in range(len(prediction)): 
      key_and_value = prediction[i]
      item = ' '.join(key_and_value.values())
      tok  = ' '.join(key_and_value.keys())

      # Check for a column name, table name, aggregate function
      # aggregate function attribute, comparison attribute

      if item == 'COLUMN_NAME': 
        cols_name.append(tok.split("'")[-1])
      elif item == 'TABLE_NAME':
        if not table_name:
            table_name = tok
        else:
          cols_name.append(table_name)
          table_name = tok
      elif item == 'AGGREGATE_FUNCTION':
        agregat = tok
        aggregate_fct.append(agregat)
        try:
            key_and_value = prediction[i+1]
            item_ag =' '.join(key_and_value.values())
            tok_ag  =' '.join(key_and_value.keys())
            if item_ag == 'AGGREGATE_FUNCTION': 
              agregat += tok_ag
              i += 1
              aggregate_fct.append(agregat)
        except :
            pass
            
      elif item == 'AGGREGATE_FUNCTION_ATTR':
        aggregate_fct_attr.append(tok) 
      elif item == 'COMPARISON_ATTR':     
        comparison_attr = tok.split("'")[-1]
      elif item == 'COMPARISON_OPERATOR':
            comparison_word += tok + ' '
      elif item == 'VALUE':
        value += tok + ' '
  value = value.strip()
  comparison_word = comparison_word.strip()
  # print("The cols name is : ", cols_name)
  # Lemmatization of columns name
  """for i in range(0, len(cols_name)):
    cols_name[i] = extract_lemma(cols_name[i])

  if comparison_attr:
    comparison_attr = extract_lemma(comparison_attr)"""

  # Table name, column names checking and extraction
  if table_name != 0:
    table_name = table_name.split("'")[-1]
    column = ''
    if len(cols_name) > 0:
      column += cols_name[0]
      for i in range(1, len(cols_name)):
            column += ', ' + cols_name[i]
      
  #  Aggregate function checking
    agg_fct = ''
    if len(aggregate_fct) == len(aggregate_fct_attr) > 0:  
      if aggregate_fct[0] in aggregate_function_vocab:
          agg_fct += aggregate_function_vocab[aggregate_fct[0]] + '('+aggregate_fct_attr[0] + ')'        
      for i in range(1, len(aggregate_fct)):
            if aggregate_fct[i] in aggregate_function_vocab:
              agg_fct += ' , ' + aggregate_function_vocab[aggregate_fct[i]] + '(' +aggregate_fct_attr[0] + ')'          
            else:
              agg_fct += ' , $' + aggregate_fct[i] + '$(' +aggregate_fct_attr[0] + ')'
  
    elif len(aggregate_fct) > 0 and len(aggregate_fct_attr) == 1:
      if aggregate_fct[0] in aggregate_function_vocab:
          agg_fct += aggregate_function_vocab[aggregate_fct[0]] + '('+aggregate_fct_attr[0] + ')'       
      for i in range(1, len(aggregate_fct)):
            if aggregate_fct[i] in aggregate_function_vocab:
              agg_fct += ' , ' + aggregate_function_vocab[aggregate_fct[i]] + '('+aggregate_fct_attr[0] + ')'
              
            else:
              agg_fct += ' , $' + aggregate_fct[i] + '$('+aggregate_fct_attr[0] + ')'
          
    elif len(aggregate_fct) > 0:
      if aggregate_fct[0] in aggregate_function_vocab:
          agg_fct += aggregate_function_vocab[aggregate_fct[0]] +'(*) '        
      for i in range(1, len(aggregate_fct)):
            if aggregate_fct[i] in aggregate_function_vocab:
              agg_fct += ' , ' + aggregate_function_vocab[aggregate_fct[i]] +'(*) '         
            else:
              agg_fct += ' , $' + aggregate_fct[i] +'$(*) '         

    if not table_name:
      table_name = "$table$"

    # Check if there is a conditional statement
    conditional_statement = ''
    if comparison_attr or comparison_operator or value:
      if value == '':
        value = '$value$'
      if not comparison_word:
          comparison_operator = '='    
      else:
          if comparison_word in comparison_operator_vocab: 
              comparison_operator = comparison_operator_vocab[comparison_word]
          else :
            comparison_operator = "$" + comparison_word + "$"           
      if not comparison_attr:
          comparison_attr = "$comparison attribute$"    

      conditional_statement = '\nWHERE' + ' ' + table_name + '.' + comparison_attr + ' ' + str(comparison_operator) + ' ' + str(value)
      
  # Check if we must use the group by statement
    group_by = ''
    if column !='' and agg_fct!='':
      group_by  +=' GROUP BY '
      for col in cols_name:
        group_by += col + ', '
    elif column == '' and agg_fct == '':
      column='* '

  # Generate the SQL Query
  sql_query = ""
  sp = " " 
  if not conditional_statement and not group_by:
    sp = ""
  sql_query += 'SELECT '+ column + agg_fct + '\nFROM ' + table_name + sp + conditional_statement + group_by + ';'
      
  return sql_query

# Create a main function
def main():
    img = Image.open('SQLogo.png')
    st.set_page_config(page_title='NLP Project', page_icon=img)
    # Create a title
    st.title('French Text to SQL Query Project')

    # Get input features from the user
    # le titre et la specialité des départements ?
    s = st.text_input('Give a sentence')

    # Create a predict button
    btn = st.button('Generate SQL Query')
    if btn:
        # Make predictions using the model
        s = clean(s)
        prediction, model_output = model.predict([s])
        print(prediction)
        sql_query = get_sql(prediction[0])
        #sql_query = 'le titre et la specialité des départements ?'
        #st.success(f'Prediction: {preds[0]}')
        st.markdown(f'<p style="font-family:Courier; color:White; font-size: 20px;">{sql_query}</p>', unsafe_allow_html=True)
if __name__ == '__main__':
    main()