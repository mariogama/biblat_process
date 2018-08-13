from biblat_process.marc2dict import Marc2Dict
from biblat_schema.models import Document, Revista, Fasciculo

marcprocess = Marc2Dict()
for reg_marc in marcprocess.get_dict():
    print(reg_marc)