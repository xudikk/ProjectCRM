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
    STATUS_CHOICES = ((1, 'Chiqib ketgan'),
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
