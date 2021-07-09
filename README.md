
# Bulk csv-excel G Translator using Streamlit

A stream app for translation for single sentence and for bulk sentences in csv or excel sheets using google-trans library in Python.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all libraries from requirements.txt

```bash
pip install -r requirements.txt
```

## Run the Streamlit app by
To run on local system you will need only app.py
```
streamlit run app.py
```

# Deploy on Heroku
Four files needed for Heroku deployment
## app.py
```python
#import libraries
import streamlit as st
import pandas as pd
from googletrans import Translator , LANGUAGES
from pandas import ExcelWriter
import os
import base64

# translator object
translate = Translator()

# download file function
@st.cache
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

# translator function
@st.cache
def en_xx(text,target_language):
	out = translate.translate(text=text,dest=target_language)
	return out.text
# translate values all columns of csv and return the file
def  process_csv(uploaded_file):
	# Can be usd wherever a "file-like" object is accepted:
	df = pd.read_csv(uploaded_file)
	for column in df.columns:
		df[column] = df[column].apply(lambda x : en_xx(x,'hi'))
	df.to_csv('csv_output.csv')	
	st.write(df)
	st.markdown(get_binary_file_downloader_html('csv_output.csv', 'Translated CSV FILE'), unsafe_allow_html=True)

# translate values in all columns of all sheets one by one and return the file
def process_xl(uploaded_file):
	# Can be usd wherever a "file-like" object is accepted:
	file = pd.ExcelFile(uploaded_file)
	sheets = file.sheet_names
	with ExcelWriter('excel_output.xlsx') as writer:
		for sheet in sheets:
			df = pd.read_excel(uploaded_file,sheet_name=sheet)
			for column in df.columns:
				df[column] = df[column].apply(lambda x : en_xx(x,'hi'))	
				df.to_excel(writer,sheet_name=sheet)
			st.write(df)
		writer.save()
		st.markdown(get_binary_file_downloader_html('excel_output.xlsx', ' Translated Excel FILE'), unsafe_allow_html=True)
			
# Add a selectbox to select Target Language:
lang = st.selectbox(
    'Select Language',
    list(LANGUAGES.values())
)
if lang!='':
	lang = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(lang)]

# text box for single input translation
en_sen = st.text_input('Enter the English sentence here:') 
if en_sen!='':
	st.write(en_xx(en_sen,lang))

# upload a file to process ( files allowed csv and excel)
uploaded_file = st.file_uploader("Upload a CSV or Excel file (.csv or .xlsx)")
if uploaded_file is not None:
	ex = str(uploaded_file.name).split('.')[1]
	if ex=='csv':
		process_csv(uploaded_file)
	elif ex=='xlsx':
		process_xl(uploaded_file)
	else:
		st.write("File Not Supported \n File supported are: CSV and Excel")
```
## Prockfile
```
web: sh setup.sh && streamlit run app.py
```
## setup.sh
```
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"Your.mail@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```
## Requirements text file
requirements.txt file is available in this repo.

## Sample app link
[BW-translator](https://gt-en.herokuapp.com/) 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
