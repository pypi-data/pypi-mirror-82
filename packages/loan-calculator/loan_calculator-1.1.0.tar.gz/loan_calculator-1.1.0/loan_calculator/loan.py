from datetime import timedelta

from loan_calculator.schedule import (
    ProgressivePriceSchedule,
    RegressivePriceSchedule,
    ConstantAmortizationSchedule,
)


class Loan(object):
    """Loan.

    Attributes
    ----------
    principal : float, required
        The loan's principal.
    annual_interest_rate : float, required
        The loan's annual interest rate.
    start_date : date, required
        The loan's reference date. This date is usually the one when the
        borrower signed the loan's contract.
    return_dates : list, required
        List of date objects with the expected return dates. These dates
        are usually contractually agreed.
    year_size : int, optional
        The reference year size for converting from annual to daily
        interest rates. (default 365)
    grace_period : int, optional
        The number of days for which the principal is not affected by the
        capitalization process. (default 0)
    amortization_schedule_type : str, optional
        A discriminator string indicating the amortization schedule to be
        adopted. The available schedules are progressive_price_schedule,
        regressive_price_schedule, constant_amortization_schedule.
        (default progressive_price_schedule).
    """

    def __init__(
        self,
        principal,
        annual_interest_rate,
        start_date,
        return_dates,
        year_size=365,
        grace_period=0,
        amortization_schedule_type='progressive_price_schedule'
    ):
        """Initialize loan."""

        self.principal = principal

        self.annual_interest_rate = annual_interest_rate

        self.daily_interest_rate = (
            (1 + annual_interest_rate) ** (1.0 / year_size) - 1
        )

        self.start_date = start_date
        self.capitalization_start_date = (
            start_date + timedelta(grace_period)
        )

        self.return_dates = return_dates

        self.year_size = year_size
        self.grace_period = grace_period

        self.amortization_schedule_type = amortization_schedule_type

        if amortization_schedule_type == 'progressive_price_schedule':
            self.amortization_schedule_cls = ProgressivePriceSchedule

        elif amortization_schedule_type == 'regressive_price_schedule':
            self.amortization_schedule_cls = RegressivePriceSchedule

        elif amortization_schedule_type == 'constant_amortization_schedule':
            self.amortization_schedule_cls = ConstantAmortizationSchedule

        else:
            raise TypeError('Unknown amortization schedule type.')

        if any(
            self.capitalization_start_date >= r_date
            for r_date in self.return_dates
        ):
            raise ValueError('Grace period can not exceed loan start.')

        self.amortization_schedule = self.amortization_schedule_cls(
            principal,
            self.daily_interest_rate,
            [
                (r_date - self.capitalization_start_date).days
                for r_date in return_dates
            ]
        )

    @property
    def amortization_function(self):

        def f_(principal, daily_interest_rate, return_days):

            return self.amortization_schedule_cls(
                principal, daily_interest_rate, return_days
            ).amortizations

        return f_

    @property
    def return_days(self):
        return self.amortization_schedule.return_days  # pragma: no cover

    @property
    def balance(self):
        return self.amortization_schedule.balance  # pragma: no cover

    @property
    def due_payments(self):
        return self.amortization_schedule.due_payments  # pragma: no cover

    @property
    def interest_payments(self):
        return self.amortization_schedule.interest_payments  # pragma: no cover

    @property
    def amortizations(self):
        return self.amortization_schedule.amortizations  # pragma: no cover

    @property
    def total_amortization(self):
        return (
            self.amortization_schedule.total_amortization   # pragma: no cover
        )

    @property
    def total_interest(self):
        return self.amortization_schedule.total_interest  # pragma: no cover

    @property
    def total_paid(self):
        return self.amortization_schedule.total_paid  # pragma: no cover
