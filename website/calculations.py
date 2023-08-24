import heapq

class Total_balance():
    def __init__(self, members, group):
        self.balances = []
        self.paybacks = []
        for member in members:
            self.balances.append([member.id, 0])

        for e in group.expenses:
            next(m for m in self.balances if m[0] == e.paid_by)[1] += e.amount
            for d in e.debtors:
                next(mem for mem in self.balances if mem[0] == d.group_user_id)[1] -= d.debt_amount

        for p in group.paybacks:
            next(m for m in self.balances if m[0] == p.payer)[1] += p.amount
            next(m for m in self.balances if m[0] == p.reciver)[1] -= p.amount

    def get_balance(self):
        return self.balances

    def simplify_debts(self):
        credit = []
        debit = []

        for person in self.balances:
            if person[1] > 0:
                credit.append((-person[1], person[0]))
            if person[1] < 0:
                debit.append((person[1], person[0]))

        heapq.heapify(credit)
        heapq.heapify(debit)
        answer = []

        while credit and debit:
            credit_value, credit_name = heapq.heappop(credit)
            debit_value, debit_name = heapq.heappop(debit)

            if credit_value < debit_value:
                amount_left = credit_value - debit_value
                answer.append((debit_name, credit_name, -1 * debit_value))
                heapq.heappush(credit, (amount_left, credit_name))

            elif debit_value < credit_value:
                amount_left = debit_value - credit_value
                answer.append((debit_name, credit_name, -1 * credit_value))
                heapq.heappush(debit, (amount_left, debit_name))

            else:
                answer.append((debit_name, credit_name, -1 * credit_value))

        return answer