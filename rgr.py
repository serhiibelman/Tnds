import numpy as np
import xlrd

from matrix import sum_products


class Tnds:
    """
    Get T, t, n, D, S from xls file
    """
    def __init__(self, filename='rgr.xls', check=False):
        if check:
            self.start, self.end = 13, 19
        else:
            self.start, self.end = 1, 13
        self.wb = xlrd.open_workbook(filename)
        self.sheet = self.wb.sheet_by_name('Sheet1')
        self.T = self.get_col(0)
        self.t = self.get_col(1)
        self.n = self.get_col(2)
        self.D = self.get_col(3)
        self.S = self.get_col(4)
        self.PX = self.get_col(5)
        self.Py = self.get_col(6)
        self.Pz = self.get_col(7)

    def get_col(self, col_n):
        """
        Get column in excel sheet
        """
        return self.sheet.col_values(
                col_n, start_rowx=self.start, end_rowx=self.end
            )
    
    def permutations(self):
        """
        Find all permutations for Tnds atributes
        """
        T, t, n, D, S = self.T, self.t, self.n, self.D, self.S
        return [
            T, t, n, D, S,
            [T, t], [T, n], [T, D], [T, S],
            [t, n], [t, D], [t, S],
            [n, D], [n, S], [D, S],
            [T, t, n], [T, t, D], [T, t, S],
            [T, n, D], [T, n, S], [T, D, S],
            [t, n, D], [t, n, S], [t, D, S],
            [T, t, n, D], [T, t, n, S], [T, n, D, S],
            [t, n, D, S], [T, t, D, S], [T, t, n, D, S]
        ]
        
            


class P_equation:
    """
    Dynamic create lineir equation for Px, Py and Pz
    like: a0 + a1*x1 = Px -> a0 + a1*x1 + a2*x2 = Px
    :n: number of unknown arguments for equation
    """
    def __init__(self, N=1, P=None):
        self.N = N
        self.P = P or []

    def __setattr__(self, name, value):
        dc = self.__dict__.keys()
        if name not in dc and name != 'P':
            if 'N' in dc:
                self.__dict__['N'] += 1
        super().__setattr__(name, value)
    
    @property
    def equation_args(self):
        """
        grab all atributes for the instance and create an 
        equation args list
        This list contains names of ... and their values
        """
        equation_list = []
        for key, val in self.__dict__.items():
            if key != 'P':
                equation_list.append((key, val))
        # equation_list.append(('P', self.P))
        return equation_list
    
    def _create_matrix(self):
        """
        create matrix from existing atributes
        :return: lists M, V
        """
        eq = list(map(lambda x: x[1], self.equation_args))
        M = []
        V = []
        for k in range(self.N):
            M.append([])
            if k == 0:
                V.append(sum_products(self.P))
            else:
                V.append(sum_products(self.P, eq[k]))
            for i in range(len(eq)):
                if k == 0:
                    if i == 0:
                        M[k].append(eq[i])
                    else:
                        M[k].append(sum_products(eq[i]))
                else:
                    if i == 0:
                        M[k].append(sum_products(eq[k]))
                    else:
                        M[k].append(sum_products(eq[k], eq[i]))
        # print('M:', M)
        # print('V:', V)
        assert len(M) == self.N
        assert len(M[0]) == self.N
        return M, V
    
    def solve_equation(self):
        """
        Solve matrix
        Length of the returned list shoold be self.N
        :return: list of unknown arguments [a0, a1, a2, ... an]
        """
        M, V = self._create_matrix()
        # solve it
        args_list = np.linalg.pinv(M).dot(V)
        assert len(args_list) == self.N
        return args_list
    
    def delta(self):
        Pxx = self.solve_equation()
        delta = sum([(p1-p2)**2 for p1, p2 in zip(Pxx, self.P)])/sum([p**2 for p in Pxx])
        return delta**0.5
    
    def __str__(self):
        eq_str = ' + '.join(list(map(lambda x: x[0], self.equation_args)))
        return f'{eq_str} = P'


def find_min_delta(permutations):
    """
    Find men delta for all permutations
    """
    return


if __name__ == '__main__':
    tnds = Tnds()
    check = Tnds(check=True)
    Px = tnds.PX
    p = P_equation(P=Px)
    p.T = tnds.T
    p.t = tnds.t
    p.__setattr__('D', tnds.D)
    p.__setattr__('S', tnds.S)
    p.__setattr__('DS', [tnds.D, tnds.S])
    # dd = sum_products(p.DS, p.T)
    # print('DD:', dd)
    p._create_matrix()
    print(p.delta()) 
    print(p)
