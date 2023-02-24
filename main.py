import logging
import os
import shutil
import re
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from starlette.responses import FileResponse
app = FastAPI()


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("helloword.html", {"request": request})


@app.get('/ciao')
async def ciao():
    return {"message": "ciao"}


@app.post("/")
async def uploadFile( request: Request, filetoupload: str = Form(...)):
    fn = filetoupload
    return templates.TemplateResponse('helloword.html', context={'request': request, 'fn':fn})
    #return f'{filetoupload}'

@app.post('/upload')
async def uploadF(filetoUpload : UploadFile = File(...)):


    with open(f'{filetoUpload.filename}', 'wb') as f:
        shutil.copyfileobj(filetoUpload.file, f)


    os.getcwd()
    punti_e_virgola = ';;;;;;;;;\n'
    if filetoUpload.filename[-4:] == '.csv':
        string_interessed_file_name = filetoUpload.filename.replace(filetoUpload.filename[-4:], '')
        f = open(filetoUpload.filename, 'r+', encoding='utf-8-sig')
        header = f.readline()
        cont = f.readlines()
        f.close()
        valori_puliti = []
        for i in cont:
            if i == punti_e_virgola:
                del i
            else:
                valori_puliti.append(i)

        valori_puliti_2 = []
        for i in valori_puliti:
            nl = i.replace('\xa0', '')
            nl1 = nl.replace('\n', '')
            nl2 = nl1.replace(';', ',')
            valori_puliti_2.append(nl2)



        prima_linea = header.split(';')

        valori_puliti_3 = []
        for v in valori_puliti_2:
            new_el = v.split(',')
            valori_puliti_3.append(new_el)

        file_name = string_interessed_file_name + '.xml'
        # apro il file e sceivo intestazione, con cod utente e distr
        z = open(file_name, "w")
        z.write(
            '<?xml version="1.0" encoding = "UTF-8"?>\n<Prestazione xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  ' +
            prima_linea[1] + "=" "'" + valori_puliti_3[0][0] + "' " + prima_linea[0] + "=" + "'" + valori_puliti_3[0][
                1] + "'" + ">")
        second_line = z.write('\n<IdentificativiRichiesta>')
        third_line = z.write('\n<' + prima_linea[2] + '>' + valori_puliti_3[0][2] + '/<' + prima_linea[2] + '>')
        foruth_line = z.write('\n<' + prima_linea[3] + '>' + valori_puliti_3[0][3] + '/<' + prima_linea[3] + '>')
        fifth_line = z.write('\n</IdentificativiRichiesta>')
        z.close()
        # scrivo tutti i dati pdr
        for h in valori_puliti_3:
            l = open(file_name, "a")
            sixth_line = l.write('\n<DatiPdr>')
            l.write('\n<' + prima_linea[4] + '>' + h[4] + '/<' + prima_linea[4] + '>')
            l.write('\n<' + prima_linea[5] + '>' + h[5] + '/<' + prima_linea[5] + '>')
            l.write('\n<' + prima_linea[7] + '>' + h[7] + '/<' + prima_linea[7] + '>')
            l.write('\n<' + prima_linea[8] + '>' + h[8] + '/<' + prima_linea[8] + '>')
            l.write('\n</DatiPdr>')
            l.close()
        # chiudo il tag di apertura ed il file è pronto
        b = open(file_name, "a")
        b.write('\n</Prestazione>')
        b.close()

        folder_path = 'C:\\Users\\User\\PycharmProjects\\api'
        file_location = f'{folder_path}{os.sep}{file_name}'
        return FileResponse(file_location, media_type='application/xml', filename=str(file_name))


    else:
        raise HTTPException(status_code=500, detail='Extension file not valid!')





    #prima_lina = filetoUpload.file.read()


