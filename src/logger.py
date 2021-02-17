import xlsxwriter

class Logger:

    def __init__(self, filepath, name):
        self.wb = xlsxwriter.Workbook(filepath)
        self.new_sheet(name)
        self.pr_succ = 1


    def new_sheet(self, name):
        self.ws = self.wb.add_worksheet(name)
        self.row = 0
        self.col = 0

    def log_t(self, real_t, estimate_t):
        sum = 0
        for a in range(len(real_t)):
            for s1 in range(len(real_t[a])):
                for s2 in range(len(real_t[a][s1])):
                    sum += abs(real_t[a][s1][s2] - estimate_t[a][s1][s2])

        self.ws.write_number(self.row, self.col, sum)
        self.ws.write_number(self.row + 1, self.col, self.pr_succ)
        self.col += 1

    def log_t_complete(self, real_t, estimate_t):
        ws2 = self.wb.add_worksheet("t_" + str(self.col))
        col = 0
        row = 0
        breadt = len(real_t[0][0])
        for a in range(len(real_t)):
            for s1 in range(len(real_t[a])):
                for s2 in range(len(real_t[a][s1])):
                    ws2.write_number(row, col, real_t[a][s1][s2])
                    ws2.write_number(row, col  + breadt + 2, estimate_t[a][s1][s2])
                    col += 1
                row += 1
                col = 0
            row += 1


    def log_pr_succ(self, pr_succ):
        self.pr_succ = pr_succ*10 #*10 for nice visual

    def __del__(self):
        self.wb.close()


