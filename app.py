import streamlit as st
import pandas as pd
from googletrans import Translator
from pandas import ExcelWriter
import os
import base64

translate = Translator()


@st.cache
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

@st.cache
def en_xx(text,target_language):
	out = translate.translate(text=text,dest=target_language)
	return out.text

languages = ('en_IN','hi_IN','mr_IN','tl_IN','ta_IN','gu_IN','bn_IN')

def  process_csv(uploaded_file):
	# Can be usd wherever a "file-like" object is accepted:
	df = pd.read_csv(uploaded_file)
	for column in df.columns:
		df[column] = df[column].apply(lambda x : en_xx(x,'hi'))	
	st.write(df)
	st.markdown(get_binary_file_downloader_html('csv_output.csv', 'Translated CSV FILE'), unsafe_allow_html=True)

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
			

# Add a selectbox to the sidebar:
lang = st.selectbox(
    'Select Language (Comming soon) [ Not working , By default HINDI working]',
    languages
)

uploaded_file = st.file_uploader("Upload a CSV or Excel file (.csv or .xlsx)")
if uploaded_file is not None:
	ex = str(uploaded_file.name).split('.')[1]
	if ex=='csv':
		process_csv(uploaded_file)
	elif ex=='xlsx':
		process_xl(uploaded_file)
	else:
		st.write("File Not Supported \n File supported are: CSV and Excel")
	
