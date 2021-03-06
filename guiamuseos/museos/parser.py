from .models import Museo
from django.views.decorators.csrf import csrf_exempt
import sys

#StackOverflow: https://stackoverflow.com/questions/2373532/django-parse-xml-with-template
#try:
import xml.etree.ElementTree as ET
#except ImportError:
#    import xml.etree.ElementTree as ET

@csrf_exempt
def parserXML(file):
    tree = ET.parse(file)
    contenidos = tree.getroot()
    dat_id = "No proporcionado"
    nom = "No proporcionado"
    desc_ent = "No proporcionado"
    horas = "No proporcionado"
    equip = "No proporcionado"
    trans = "No proporcionado"
    desc = "No proporcionado"
    acc = "No proporcionado"
    cont_url = "No proporcionado"
    localiz = "No proporcionado"
    dat_cont = "No proporcionado"
    dat_tipo = "No proporcionado"
    for contenido in contenidos.findall('contenido'):
        for atributos in contenido.findall('atributos'):
            for atributo in atributos.findall('atributo'):
                if atributo.get ('nombre') == ("ID-ENTIDAD"):
                    dat_id = atributo.text;
                if atributo.get ('nombre') == ("NOMBRE"):
                    nom = atributo.text;
                if atributo.get ('nombre') == ("DESCRIPCION-ENTIDAD"):
                    desc_ent = atributo.text;
                if atributo.get ('nombre') == ("HORARIO"):
                    horas = atributo.text;
                if atributo.get ('nombre') == ("EQUIPAMIENTO"):
                    equip = atributo.text;
                if atributo.get ('nombre') == ("TRANSPORTE"):
                    trans = atributo.text;
                if atributo.get ('nombre') == ("DESCRIPCION"):
                    desc = atributo.text;
                if atributo.get ('nombre') == ("ACCESIBILIDAD"):
                    acc = atributo.text;
                if atributo.get ('nombre') == ("CONTENT-URL"):
                    cont_url = atributo.text;
                if atributo.get ('nombre') == ("LOCALIZACION"):
                    for atributo_sub in atributo.findall('atributo'):
                        if atributo_sub.get ('nombre') == ("NOMBRE-VIA"):
                            localiz = atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("CLASE-VIAL"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("TIPO-NUM"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("NUM"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("LOCALIDAD"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("PROVINCIA"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("CODIGO-POSTAL"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("BARRIO"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("DISTRITO"):
                            dat_distrito = atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("COORDENADA-X"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("COORDENADA-Y"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("LATITUD"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                        if atributo_sub.get ('nombre') == ("LONGITUD"):
                            localiz += ", ";
                            localiz += atributo_sub.text;
                if atributo.get ('nombre') == ("DATOSCONTACTOS"):
                    for atributo_sub in atributo.findall('atributo'):
                        if atributo_sub.get ('nombre') == ("TELEFONO"):
                            dat_telefono = atributo_sub.text
                        if atributo_sub.get ('nombre') == ("FAX"):
                            dat_fax = atributo_sub.text
                        if atributo_sub.get ('nombre') == ("EMAIL"):
                            dat_email = atributo_sub.text
                if atributo.get ('nombre') == ("TIPO"):
                    dat_tipo = atributo.text;
                    continue

        museo = Museo ( identidad = dat_id, nombre = nom, descripcion_entidad = desc_ent, horario  = horas,
                        equipamiento = equip, transporte = trans, descripcion = desc, accesibilidad = acc,
                        url = cont_url, localizacion = localiz, telefono = dat_telefono, fax = dat_fax,
                        email = dat_email, tipo = dat_tipo, distrito=dat_distrito)
        museo.save()