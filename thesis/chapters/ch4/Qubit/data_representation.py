from database import Database


class LatexData():

    def __init__(self,table_name):

        settings = {'table name':table_name
                    }
        self.db = Database(settings,'simlab_db','db.cs.usask.ca','simlabuser1','simlab_01')

    def generate_table(self,n,orderby,column_names,minimum=True,desc=True):

        data = self.db.get_n_best_values(n,sort_by,minimum)
        print data
        column_str = ''
        column_names = ''
        for c in column_names:
            column_str += 'c|'
            column_names += c+'&'
        column_names = column_names[:-1]
        print r"\begin{tabular}{|%s}"%column_str
        print r"\hline"
        print r"%s\\"%column_names
        print r"\hline"
        print r"\end{tabular}"

if __name__ == '__main__':

    lb = LatexData('t_4qubit')
    lb.generate_table(3,'T',['Dueration time \Theta','Fidelity'],False)

