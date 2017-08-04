from database import Database


class LatexData():

    def __init__(self,table_name):

        settings = {'table name':table_name
                    }
        self.db = Database(settings,'simlab_db','simlabuser1','db.cs.usask.ca','simlab_01')

    def generate_table(self,n,orderby,columns,asc='asc'):

        data = self.db.get_n_best_value(orderby,n,asc)
        column_str = ''
        column_names = ''
        for c in columns:
            column_str += 'c|'
            column_names += c+' & '
        column_names = column_names[:-2]
        print r"\begin{tabular}{|%s}"%column_str
        print r"\hline"
        print r"%s\\ \hline"%column_names
        for d in data:
            data_row = ''
            for c in range(len(columns)):
                data_row += str(d[c])+' & '
            data_row = data_row[:-2]

            print r"%s \\ \hline"%data_row
        print r"\end{tabular}"

if __name__ == '__main__':

    lb = LatexData('t_4qubit')
    lb.generate_table(3,'T',['Duration time \Theta','Fidelity'])

