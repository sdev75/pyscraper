

class ScraperConfigBase:
    def __init__(self):
        self.data = {}
        self.options = []
        self.exp_options = {}
        self.service_args = []

    def __new__(cls, *args, **kwargs):
        if cls is ScraperConfigBase:
            raise TypeError('base class may not be instantiated')
        return object.__new__(cls, *args, **kwargs)

    def set(self, k, v):
        self.data[k] = v

    def get(self, k, default=False):
        return self.data.get(k, default)

    def add_option(self, v):
        self.options.append(v)

    def add_exp_option(self, k, v):
        self.exp_options[k] = v

    def add_service_args(self, list):
        for item in list:
            if item[1] is not None:
                val = f'--{item[0]}={item[1]}'
            else:
                val = f'--{item[0]}'

            self.service_args.append(val)
       

