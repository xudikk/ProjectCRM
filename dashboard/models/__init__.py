class PositionChoice:
    STATUS_CHOICES = ((1, 'Faol emas'),
                      (2, 'Faol'),
                      (3, 'Mavjud emas'),
                      (4, 'Yangi qo`shilmoqchi')
                      )

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.STATUS_CHOICES:
            if i == index:
                result = name
        return result


class MemberChoice:
    STATUS_CHOICES = ((1, 'Faol emas'),
                      (2, 'Faol'),
                      (3, 'Mavjud emas'),
                      (4, 'Yangi qo`shilmoqchi')
                      )

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.STATUS_CHOICES:
            if i == index:
                result = name
        return result


class PaymentType:
    CHOICES = ((1, 'Naqd'), (2, 'Terminal'), (3, 'Pul o`tkazish'), (4, 'Online'))

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result


class StudentChoice:
    STATUS_CHOICES = ((1, 'Faol emas'),
                      (2, 'Faol'),
                      (3, 'Mavjud emas'),
                      (4, 'Yangi qo`shilmoqchi')
                      )

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.STATUS_CHOICES:
            if i == index:
                result = name
        return result


class PaymentChoice:
    STATUS_CHOICES = ((1, 'To`lanmagan'),
                      (2, 'Qisman to`langan'),
                      (3, 'To`langan')
                      )

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.STATUS_CHOICES:
            if i == index:
                result = name
        return result


class PeriodType:
    CHOICES = ((1, 'Har 1 oy'), (2, 'Oyning 1 kuni'),)

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result


class StudentPayment:
    STATUS_CHOICES = ((1, "yo'q"),
                      (2, 'qisman'),
                      (3, "To'liq")
                      )

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.STATUS_CHOICES:
            if i == index:
                result = name
        return result
