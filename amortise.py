from collections import OrderedDict


def amortise(loan):
    structure = loan[0]
    drawdowns = loan[1]

    # print(drawdowns)

    prev_date = structure.start_date
    beg_balance = drawdowns.iloc[0][0]
    principal = beg_balance

    for row in structure.itertuples():
        curr_date = row[0].date()
        p = row[1]
        principal_rate = row[2]
        margin_rate = structure.margin_rate
        interest_rate = row[3]
        d = curr_date - prev_date
        for row in drawdowns.itertuples():
            principal_increase = row[1]
            dd_date = row[2]
            if (dd_date == structure.start_date):
                if (p + structure.principal_offset) % \
                        structure.principal_period == 0:
                    ppmt = round(principal * principal_rate, 2)
                    if ppmt > beg_balance:
                        ppmt = beg_balance
                else:
                    ppmt = 0
            elif prev_date < dd_date and dd_date < curr_date:
                beg_balance += principal_increase
                principal += principal_increase
                end_balance = beg_balance
                yield OrderedDict([('Period', 0),
                                   ('Date', dd_date),
                                   ('Begin Balance', beg_balance),
                                   ('Principal', 0),
                                   ('Interest', 0),
                                   ('End Balance', end_balance)])
        # print(date)
        # print(d.days)
        if ((p + structure.interest_offset) % structure.interest_period) \
                == 0:
            mpmt = round(beg_balance * margin_rate *
                         d.days / structure.days_in_year, 2)
            ipmt = round(beg_balance * interest_rate *
                         d.days / structure.days_in_year, 2)
            # print(date, mpmt, ipmt)
        else:
            mpmt = 0
            ipmt = 0

        # print(mpmt, ipmt)
        end_balance = beg_balance - ppmt
        prev_date = curr_date

        yield OrderedDict([('Period', p),
                           ('Date', curr_date),
                           ('Begin Balance', beg_balance),
                           ('Principal', ppmt),
                           ('Interest', ipmt + mpmt),
                           ('End Balance', end_balance)])

        beg_balance = end_balance
