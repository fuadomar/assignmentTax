taxrate_male = [[0, 250000], [10, 400000], [15, 500000], [20, 600000], [25, 3000000],
                [30, "On remaining amount"]]  # [[%rate][Onamount]]
taxrate_female = [[0, 300000], [10, 400000], [15, 500000], [20, 600000], [25, 3000000],
                  [30, "On remaining amount"]]


class Output:

    def __init__(self, person):
        self.name = person.name
        self.gender = person.gender
        self.pf = person.pf
        self.total_income = person.total_income
        self.bonus = person.fest_bonus

        self.emp_id = person.emp_id
        self.department = person.department
        self.designation = person.designation
        self.joining_date = person.joining_date
        self.income_year = person.income_year
        self.assessment_year = person.assessment_year

        self.investment_made = person.investment_made
        self.tax_deducted_by_nascenia = person.tax_deducted_by_nascenia

        self.transport = 30000
        self.basic = self.magic(self.total_income, self.bonus, self.transport, self.pf)
        self.house_rent = min(300000, int(self.basic / 2))
        self.medical = min(120000, int(self.basic * .1))
        # round handle
        self.basic += self.total_income - (
                self.basic + self.house_rent + self.transport + self.medical + self.bonus + self.pf)

        self.individual_tax_reliability_list = self.calculateIndividualTaxLiability()
        self.total_individual_tax_liability = sum(row[3] for row in self.individual_tax_reliability_list)
        self.investment_allowed = int(round(self.get_total_taxable_income() * .25))
        self.net_tax_payable= self.total_individual_tax_liability-self.get_tax_rebate_due_to_investment()
        self.total_tax_to_be_deducted_by_nascenia=self.net_tax_payable
        self.advance_tax=min(0,self.total_tax_to_be_deducted_by_nascenia-self.tax_deducted_by_nascenia)

        self.chalan=person.chalan

    def magic(self, total, bonus, transport, pf):

        def calculateTotal(b):
            return pf + bonus + transport + min(300000, int(b / 2)) + min(120000, int(b * .1)) + b

        low = 0
        high = total
        mid = int((low + high) / 2)
        cnt = 1
        while low < high and cnt < 100:

            tmpTotal = calculateTotal(mid)
            if tmpTotal < total:
                low = mid
            elif tmpTotal > total:
                high = mid

            prev_mid = mid
            mid = int((low + high) / 2)

            if prev_mid == mid:
                break
        return mid

    def calculateIndividualTaxLiability(self):
        totalTaxableIncome = self.get_total_taxable_income()
        ans = []
        taxrate = None
        if self.gender == "M":
            taxrate = taxrate_male
        else:
            taxrate = taxrate_female

        for row in taxrate:

            rate = row[0]
            if rate == 30:
                amount = totalTaxableIncome
            else:
                amount = row[1]
            taxableIncome = min(amount, totalTaxableIncome)
            individualTaxLiability = int(round(taxableIncome * (rate / 100.0)))
            ans.append([rate, row[1], taxableIncome, individualTaxLiability, totalTaxableIncome - taxableIncome])

            totalTaxableIncome -= min(amount, totalTaxableIncome)

        return ans

    def get_total_less_exempted(self):
        return self.house_rent + self.transport + self.medical

    def get_total_taxable_income(self):
        return self.total_income - self.get_total_less_exempted()

    def get_tax_rebate_due_to_investment(self):
        mn = min(self.investment_allowed, self.investment_made)
        if mn <= 250000:
            return int(round(mn * .15))
        else:
            return int(round(((mn - 250000) * .12) + (250000 * .15)))
