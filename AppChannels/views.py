import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

import sqlite3
from sqlite3 import Error

DB_PATH_KOLIBRI = '/home/franklin/.kolibri/db.sqlite3'

def index(request):
    list_data = getData()
    length = len(list_data)
    context = { 'list_data':list_data,'length':length }
    return render(request,'list_channels.html',context)

def exportCSV(request):
    response = HttpResponse(content_type='text/csv')
    response["Content-Disposition"] = 'attachment; filename="file.csv"'
    list_data = getData()

    writer = csv.writer(response)
    writer.writerow(['Canal', 'Recurso', 'Tipo Recurso', 'Peso (bytes)'])
    for row in list_data:
        writer.writerow([row["channel_name"] , row["title"], row["kind"], row["file_size"]])
    return response

def getData():
    conn = None
    list_data = []
    try:
        sql = ""
        sql = sql + "SELECT "
        sql = sql + "    cn.channel_id, "
        sql = sql + "    cmd.name as channel_name,"
        sql = sql + "    cn.title, "
        sql = sql + "    cn.kind, "
        sql = sql + "    (  "
        sql = sql + "        SELECT sum(clf.file_size) "
        sql = sql + "        FROM content_file cf  "
        sql = sql + "            INNER JOIN content_localfile clf  "
        sql = sql + "            ON(clf.id = cf.local_file_id)  "
        sql = sql + "        WHERE cf.contentnode_id = cn.id AND clf.available = 1 "
        sql = sql + "    ) as file_size "
        sql = sql + "FROM  "
        sql = sql + "content_contentnode cn INNER JOIN content_channelmetadata cmd ON(cmd.id = cn.channel_id)   "
        sql = sql + "WHERE cn.level <> 0 and cn.kind <> 'topic' and cn.available = 1  ORDER BY cn.channel_id,cn.id "

        conn = sqlite3.connect(DB_PATH_KOLIBRI,uri=True)
        result = conn.execute(sql)        
        for row in result:
            list_data.append({ "channel_id": row[0],"channel_name": row[1],"title": row[2],"kind": row[3],"file_size": row[4] })
        return list_data
    except Error as e:
        print(e)
        list_data = []
    finally:
        if conn:
            conn.close()
        return list_data