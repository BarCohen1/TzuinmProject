class Result:

    def __init__(self, bagrout, sechem, accepted, opt_bagrout=None):
        self.avg_bagrut_score = bagrout
        self.opt_bargout = opt_bagrout
        self.sechem_score = sechem
        self.accepted_profs = accepted

    def __str__(self):
        str = ''
        str += 'AVG Bagrut score is: ' + self.avg_bagrut_score
        if self.sechem_score:
            str += ', Sechem score is: ' + self.sechem_score
        if self.opt_bargout:
            str += 'Optimal AVG bagrut score is:' + self.opt_bargout
        str += ', list of accepted majors is: '
        # str += self.accepted_profs
        return str