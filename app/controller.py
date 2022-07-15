from datetime import datetime
from googletrans import Translator

def tanggal(input):
    def bulan(month):
        if month == 'Berbaris':
            month = 'Maret'
            return month
        elif month == 'Mungkin':
            month = 'Mei'
            return month
        else:
            return month

    str_tanggal = datetime.strptime(input, '%Y-%m-%d')
    str_hari = str_tanggal.strftime('%A')
    str_bulan = str_tanggal.strftime('%B')
    trans_hari = Translator().translate(str_hari, src='en', dest='id')
    trans_bulan = Translator().translate(str_bulan, src='en', dest='id')
    result = str_tanggal.strftime('{}, %d {} %Y'.format(trans_hari.text, bulan(trans_bulan.text)))
    
    return result

