import xml.etree.ElementTree as etree
import re
import sys

__author__ = 'Ramon Costi Fernandes <ramon.fernandes@acad.pucrs.br>'

SVG_namespace = "http://www.w3.org/2000/svg"
SVG_fname = ''
OUTPUT_fname = 'output.txt'
coordinates_list = []
output_list = []


#Instrucoes de uso.
def usage():
    print("Como executar:\n")
    print("{} <{}>".format(sys.argv[0], "SVG input file"))
    print("ou")
    print("{} <{}> <{}>".format(sys.argv[0], "SVG input file", "OUTPUT file"))
    sys.exit(1)


# Remove as coordenadas duplicadas do arquivo SVG de entrada.
def remove_duplicates(coord_list):
    global coordinates_list
    temp_list = []
    for item in coord_list:
        if item not in temp_list:
            temp_list.append(item)
    coordinates_list = temp_list


#Enumera os pontos.
def enumerate_coordinates():
    count = 1
    for item in coordinates_list:
        coord = re.split(",", item)
        output_list.append("{} {} {}\n".format(count, coord[0], coord[1]))
        count += 1


#Gera o arquivo de saida.
def write_output_file():
    file = open(OUTPUT_fname, "w+")
    for item in output_list:
        file.write("".join(str(s) for s in item) + "\n")
    file.close()


#Processa o arquivo XML de entrada.
def parse_xml():
    global coordinates_list
    tree = etree.parse(SVG_fname)
    root = tree.getroot()
    coordinates = root.find('.//{%s}path' % SVG_namespace).get("d")
    coordinates_list = re.findall("[0-9]+\.[0-9]+,[0-9]+\.[0-9]+", coordinates)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    elif len(sys.argv) < 3:
        print("Gravando resultados no arquivo de saida \"{}\"\n".format(OUTPUT_fname))
    elif len(sys.argv) == 3:
        OUTPUT_fname = sys.argv[2]
        print("Gravando resultados no arquivo de saida \"{}\"\n".format(OUTPUT_fname))
    else:
        usage()

    SVG_fname = sys.argv[1]
    parse_xml()
    remove_duplicates(coordinates_list)
    enumerate_coordinates()
    write_output_file()