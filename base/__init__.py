class StatusChoice:
    NOT_ACTIVE = 1
    ACTIVE = 2
    DELETED = 3
    NO_STUDENT = 4

    CHOICES = ((NOT_ACTIVE, 'Faol emas'),
               (ACTIVE, 'Faol'),
               (DELETED, 'Mavjud emas'),
               (NO_STUDENT, 'Yangi qo`shilmoqchi')
               )

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result


class GenderChoice:
    MALE = True
    FEMALE = False
    CHOICES = ((MALE, 'Erkak'), (FEMALE, 'Ayol'))

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result
