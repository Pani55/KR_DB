class Company:

    def __init__(self, employer_id, accredited, name, description,
                 url, vacancies_url, area):
        self.employer_id = employer_id
        self.accredited = accredited
        self.name = name
        self.description = description
        self.url = url
        self.vacancies_url = vacancies_url
        self.area = area

    @classmethod
    def cost_to_companies_obj_list(cls, companies):
        """
        Классовый метод для создания экзэмпляров класса и укладки их в список.

        """
        companies_list = []
        for company in companies:
            employer_id = company['id']
            accredited = company['accredited_it_employer']
            name = company['name']
            description = company['description']
            url = company['alternate_url']
            vacancies_url = company['vacancies_url']
            area = company['area']['name']

            company_obj = cls(employer_id, accredited, name, description,
                              url, vacancies_url, area)

            companies_list.append(company_obj)

        return companies_list

    def to_list(self):
        return [self.employer_id, self.accredited, self.name, self.description, self.url,
                self.vacancies_url, self.area]
