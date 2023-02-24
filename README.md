# api_xml_response
Endpoint che accetta un oggetto di tipo file, e restituisce un oggetti di tipo file, se e solo se, l'estensione del file è .csv, altrimenti invierà un error code 500.
L'applicativo in se, permette di manipolare un file csv, e di scrivere le righe interessate nel file xml.
(
REQUIRMENTS FOR RUN APPLICATION:
1)pip install "fastapi[all]"
2)pip install python-multipart
3)pip install jinja2
//runserver
python -m uvicorn main:app --reload
