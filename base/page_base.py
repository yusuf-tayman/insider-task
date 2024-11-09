from base.base_functions import Base


class PageBase(Base):
    def __init__(self, driver, explicit_wait=50):
        super().__init__(driver, explicit_wait)
        self.driver = driver
