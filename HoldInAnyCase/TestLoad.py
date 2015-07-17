__author__ = 'jeong-yonghan'

data_num = "0_Anno"
file = open("../Data/" + data_num + ".txt",'r').read()
List_Anno = file.split("\n")
List_Anno = [int(x) for x in List_Anno]
print List_Anno
