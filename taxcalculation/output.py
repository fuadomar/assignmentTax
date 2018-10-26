taxrate_male = [[0,250000],[10,400000],[15,500000],[20,600000],[25,600000],[30,3000000]]  # [[%rate][Onamount]]
taxrate_female = [[0,300000],[10,400000],[15,500000],[20,600000],[25,600000],[30,3000000]]


class Output:

    def __init__(self, person):
        self.name = person.name
        self.gender = person.gender
        self.pf = person.pf
        self.total_income = person.total_income
        self.bonus = person.fest_bonus
        self.transport = 30000
        self.basic = self.magic(self.total_income, self.bonus, self.transport, self.pf)
        self.house_rent = min(300000, int(self.basic / 2))
        self.medical = min(120000, int(self.basic * .1))
        # round handle
        self.basic += self.total_income - (
                self.basic + self.house_rent + self.transport + self.medical + self.bonus + self.pf)

        self.individual_tax_reliability_list=self.calculateIndividualTaxLiability()
        self.total_individual_tax_liability_list=sum(row[3] for row in self.individual_tax_reliability_list)

    def magic(self, total, bonus, transport, pf):
        print(bonus)

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
            t = []
            rate = row[0]
            t.append(rate)
            amount = row[1]
            t.append(amount)
            taxableIncome = min(amount, totalTaxableIncome)
            t.append(taxableIncome)
            individualTaxLiability = int(taxableIncome * (rate/100.0))
            t.append(individualTaxLiability)
            t.append(totalTaxableIncome-taxableIncome)
            totalTaxableIncome -= min(amount, totalTaxableIncome)
            ans.append(t)
        print(ans)
        return ans

    def get_total_less_exempted(self):
        return self.house_rent + self.transport + self.medical

    def get_total_taxable_income(self):
        return self.basic + self.bonus + self.pf
