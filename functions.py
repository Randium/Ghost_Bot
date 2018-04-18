def import_file(file,old_table):
    bestand = open_file(file,'r')
    
    table = old_table
    
    for line in bestand:
        table.append(line.split(','))
    
    return table
