import time
# from pep_parse.settings import BASE_DIR

BASE_DIR = 'results/'


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_pep = dict()
        self.filename = (
            f'''{BASE_DIR}/status_summary_{
            time.strftime("%Y-%m-%d %H-%M")
            }.csv'''
        )
        self.file = open(self.filename, 'w')

    def close_spider(self, spider):

        total = 0
        with open(self.filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status in self.status_pep:
                total += int(self.status_pep[status])
                f.write(f'{status},{self.status_pep[status]}\n')
            f.write(f'Total,{total}\n')

    def process_item(self, item, spider):
        if item['status'] in self.status_pep:
            self.status_pep[item['status']] += 1
        else:
            self.status_pep[item['status']] = 1
        return item
