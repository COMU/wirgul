#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wirgul.settings'

UNITS_PATH = "/home/oguz/wirgul/sql/birimler.sql"

from wirgul.web.models import Faculty

class Units:

    def __init__(self):
        pass

    def read_csv(self, file_name):

        f = file(file_name)
        return f.readlines()

    def traverse_csv(self):

        lines = self.read_csv(UNITS_PATH)
        faculty_dict = dict()
        department_dict = dict()
        for line in lines:
            if line.startswith("--"):
                continue
            start = line.find("(")
            end = line.find(")")
            content = line[start+1:end].split(",")
            faculty_id_raw = content[1].strip()
            faculty_id = int(faculty_id_raw.replace("'",""))

            unit_raw = content[4].strip()
            unit = unit_raw.replace("'","")

            faculty_status_id = content[2].strip()
            faculty_status = int(faculty_status_id.replace("'",""))

            if faculty_status == 0:
                faculty_dict[faculty_id] = unit.decode("utf-8").encode("utf-8")
                department_dict[faculty_id] = [unit.decode("utf-8").encode("utf-8")]

            else:
                if department_dict.has_key(faculty_id):
                    department_dict[faculty_id].append(unit.decode("utf-8").encode("utf-8"))
                else:
                    department_dict[faculty_id] = [unit.decode("utf-8").encode("utf-8")]

        return faculty_dict, department_dict


    def strip_units(self):
        faculties = Faculty.objects.all()
        for faculty in faculties:
            name = faculty.name.strip()
            faculty.name = name
            faculty.save()

            for department in faculty.department_set.all():
                name = department.name.strip()
                department.name = name
                department.save()

    def update_units(self):
        faculty_dict, department_dict = self.traverse_csv()

        for key, value in faculty_dict.items():
            try:
                faculty = Faculty.objects.get(name=value)
                departments = faculty.department_set.all()
                department_li = map(lambda x: x.name.encode("utf-8"), departments)
                for department in department_dict[key]:
                    if department in department_li:
                        continue
                    else:
                        faculty.department_set.create(name=department)

            except:
                faculty = Faculty.objects.create(name=value.decode("utf-8"))
                try:
                    departments = department_dict[key]
                    for department in departments:
                        faculty.department_set.create(name=department)
                except Exception, ex:
                    print ex



if __name__ == "__main__":
    units = Units()
    units.strip_units()
    units.update_units()





